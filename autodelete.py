#!/usr/bin/env python3
"""
autodelete.py
Elimina carpetas de fechas antiguas dentro de subcarpetas de camaras,
conservando solo los ultimos DAYS_TO_KEEP dias.

Estructura esperada:
  BASE_DIR/
    camera1/
      2025-01-01/
      2025-01-02/
      ...
    camera2/
      ...

Uso:
  python autodelete.py            # elimina realmente
  python autodelete.py --dry-run  # solo muestra lo que se borraria
"""

import os
import sys
import shutil
from datetime import datetime, timedelta

# ─── CONFIGURACION ────────────────────────────────────────────────────────────
BASE_DIR = "/ruta/a/tus/camaras"   # <-- cambia esto a tu directorio real
DAYS_TO_KEEP = 20                  # cuantos dias recientes conservar
DATE_FORMAT = "%Y-%m-%d"           # formato de las carpetas de fecha
# ──────────────────────────────────────────────────────────────────────────────

def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("[MODO SIMULACION] No se eliminara nada.\n")

    if not os.path.isdir(BASE_DIR):
        print(f"Error: el directorio base no existe: {BASE_DIR}")
        sys.exit(1)

    cutoff_date = datetime.now().date() - timedelta(days=DAYS_TO_KEEP)
    print(f"Fecha de corte: {cutoff_date}  (se eliminan carpetas anteriores a esta fecha)")
    print(f"Directorio base: {BASE_DIR}\n")

    total_deleted = 0
    total_size = 0

    # Recorrer subcarpetas (camera1, camera2, ...)
    camera_dirs = sorted([
        d for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d))
    ])

    if not camera_dirs:
        print("No se encontraron subcarpetas en el directorio base.")
        sys.exit(0)

    for camera in camera_dirs:
        camera_path = os.path.join(BASE_DIR, camera)
        date_dirs = sorted(os.listdir(camera_path))

        to_delete = []
        to_keep = []

        for entry in date_dirs:
            entry_path = os.path.join(camera_path, entry)
            if not os.path.isdir(entry_path):
                continue
            try:
                folder_date = datetime.strptime(entry, DATE_FORMAT).date()
            except ValueError:
                # No es una carpeta de fecha, ignorar
                continue

            if folder_date < cutoff_date:
                to_delete.append((entry, entry_path, folder_date))
            else:
                to_keep.append(entry)

        print(f"  [{camera}]  conservar: {len(to_keep)} carpetas | eliminar: {len(to_delete)} carpetas")

        for name, path, date in to_delete:
            folder_size = get_dir_size(path)
            total_size += folder_size
            total_deleted += 1
            size_str = format_size(folder_size)
            if dry_run:
                print(f"    [DRY-RUN] Eliminaria: {name}  ({size_str})")
            else:
                try:
                    shutil.rmtree(path)
                    print(f"    Eliminado: {name}  ({size_str})")
                except Exception as e:
                    print(f"    ERROR al eliminar {name}: {e}")

    print()
    action = "Se eliminarian" if dry_run else "Se eliminaron"
    print(f"{action} {total_deleted} carpetas  (~{format_size(total_size)} liberados)")


def get_dir_size(path):
    """Calcula el tamano total de un directorio en bytes."""
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except OSError:
                    pass
    except OSError:
        pass
    return total


def format_size(size_bytes):
    """Formatea bytes a una cadena legible."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


if __name__ == "__main__":
    main()
