#!/usr/bin/env python3

import os
import sys
import argparse
from collections import Counter, defaultdict
import re

DN_OU_RE = re.compile(r"OU=([^,]+)", re.IGNORECASE)


def parse_args():
    parser = argparse.ArgumentParser(description="Contar usuarios en Active Directory por OU")
    parser.add_argument('--server', '-s', help='Host o IP del servidor LDAP (ej: ad.example.com).',
                        default=os.environ.get('LDAP_SERVER'))
    parser.add_argument('--user', '-u', help='Usuario para bind. Puede ser DOMAIN\\user o user@example.com.',
                        default=os.environ.get('LDAP_USER'))
    parser.add_argument('--password', '-p', help='Password para bind.',
                        default=os.environ.get('LDAP_PASSWORD'))
    parser.add_argument('--base-dn', '-b', help='Base DN para la búsqueda (ej: DC=example,DC=com).',
                        default=os.environ.get('BASE_DN'))
    parser.add_argument('--port', type=int, default=os.environ.get('LDAP_PORT', None),
                        help='Puerto LDAP. Por defecto 389 (no-ssl) o 636 (ssl).')
    parser.add_argument('--use-ssl', action='store_true', default=(os.environ.get('LDAP_USE_SSL') in ['1', 'true', 'True']),
                        help='Usar LDAPS (puerto 636). También puede configurarse via LDAP_USE_SSL=1')
    parser.add_argument('--page-size', type=int, default=500, help='Tamaño de página para búsquedas paginadas.')
    parser.add_argument('--show-sample-dn', action='store_true', help='Mostrar algunos DN de ejemplo (debug).')
    parser.add_argument('--csv', dest='csv_path', help='Ruta del archivo CSV de salida. Si se especifica, guardará los recuentos en CSV.',
                        default=os.environ.get('OUTPUT_CSV'))
    return parser.parse_args()


def extract_ou_parts(dn):
    # Extrae la lista de OU en orden (desde el primer OU encontrado hasta el último antes de DCs)
    # Ej: CN=Juan,OU=Ventas,OU=Latam,DC=example,DC=com -> ['Ventas', 'Latam']
    return DN_OU_RE.findall(dn) if dn else []


def count_users_by_ou(entries, immediate=True):
    # entries: iterable de distinguishedName strings
    counter = Counter()
    for dn in entries:
        ou_parts = extract_ou_parts(dn)
        if not ou_parts:
            counter['<no-ou>'] += 1
        else:
            if immediate:
                # OU padre inmediato (la primera OU en el DN después del CN)
                counter[ou_parts[0]] += 1
            else:
                # Ruta OU completa (concatenación de OUs, separadas por /)
                counter['/'.join(ou_parts)] += 1
    return counter


def pretty_print_counts(title, counter, top_n=None):
    print(f"\n{title}")
    print("-" * len(title))
    total = sum(counter.values())
    if total == 0:
        print("No se encontraron usuarios.")
        return
    items = counter.most_common(top_n)
    for name, cnt in items:
        pct = cnt * 100.0 / total
        print(f"{name:40} {cnt:6d} ({pct:5.1f}%)")
    print(f"\nTotal usuarios: {total}\n")


def write_counts_to_csv(path, count_immediate, count_fullpath):
    import csv

    # Escribe dos secciones en el CSV: primero OU inmediata, luego una línea vacía y ruta completa
    try:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['type', 'ou', 'count'])
            for ou, cnt in count_immediate.most_common():
                writer.writerow(['immediate', ou, cnt])
            # separador
            writer.writerow([])
            for ou, cnt in count_fullpath.most_common():
                writer.writerow(['fullpath', ou, cnt])
        print(f"Resultados guardados en CSV: {path}")
    except Exception as exc:
        print(f"Error al escribir CSV {path}: {exc}")


def main():
    args = parse_args()
    # Validaciones mínimas
    if not args.server or not args.user or not args.password or not args.base_dn:
        print("Faltan parámetros. Usa --help para más información o configura las variables de entorno LDAP_SERVER, LDAP_USER, LDAP_PASSWORD y BASE_DN.")
        sys.exit(2)

    # Import ldap3 lazily to keep module import lightweight for static checks
    try:
        from ldap3 import Server, Connection, ALL, SUBTREE
    except Exception as exc:
        print("Error al importar ldap3. Instala la dependencia: pip install ldap3")
        print(str(exc))
        sys.exit(1)

    # Determinar puerto por defecto si no se pasó
    port = args.port
    if not port:
        port = 636 if args.use_ssl else 389

    server = Server(args.server, port=port, use_ssl=args.use_ssl, get_info=ALL)

    print(f"Conectando a {args.server}:{port} (ssl={args.use_ssl}) como {args.user} ...")
    try:
        conn = Connection(server, user=args.user, password=args.password, auto_bind=True)
    except Exception as exc:
        print("Error al conectar o autenticar contra el servidor LDAP:")
        print(str(exc))
        sys.exit(1)

    # Filtro para usuarios en Active Directory
    search_filter = '(&(objectCategory=person)(objectClass=user))'

    # Usamos paged search para evitar límites
    try:
        # entries will be a generator of dicts (ldap3 paged search returns dicts per entry)
        entries = []
        for entry in conn.extend.standard.paged_search(search_base=args.base_dn,
                                                       search_filter=search_filter,
                                                       search_scope=SUBTREE,
                                                       attributes=['distinguishedName'],
                                                       paged_size=args.page_size,
                                                       generator=True):
            # Cada resultado viene como un dict. Filtramos los controles y contadores de paginación
            if 'attributes' not in entry:
                continue
            attrs = entry['attributes']
            dn = entry.get('dn') or attrs.get('distinguishedName')
            if not dn:
                # en algunos backends la DN aparece en 'dn' y no en atributos.
                continue
            entries.append(dn)
            # debug sample
            if args.show_sample_dn and len(entries) <= 5:
                print(f"Ejemplo DN: {dn}")
    except Exception as exc:
        print("Error durante la búsqueda LDAP:")
        print(str(exc))
        conn.unbind()
        sys.exit(1)

    conn.unbind()

    # Contar por OU inmediata y por ruta OU completa
    count_immediate = count_users_by_ou(entries, immediate=True)
    count_fullpath = count_users_by_ou(entries, immediate=False)

    pretty_print_counts('Usuarios por OU inmediata (OU padre)', count_immediate)
    pretty_print_counts('Usuarios por ruta OU completa', count_fullpath)

    # Guardar en CSV si se solicito
    if args.csv_path:
        write_counts_to_csv(args.csv_path, count_immediate, count_fullpath)


if __name__ == '__main__':
    main()
