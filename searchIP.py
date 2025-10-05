import json
from ipaddress import ip_network, ip_address

# Definir los rangos de CIDR a filtrar
allowed_cidrs = [
    "152.206.0.0/15",
    "169.158.0.0/16",
    "181.225.224.0/19",
    "190.6.64.0/20",
    "190.6.80.0/20",
    "190.15.144.0/20",
    "190.92.112.0/20",
    "190.107.0.0/20",
    "196.1.112.0/24",
    "196.1.135.0/24",
    "196.3.152.0/24",
    "200.0.16.0/24",
    "200.0.24.0/22",
    "200.5.12.0/22",
    "200.13.144.0/21",
    "200.14.48.0/21",
    "200.55.128.0/19",
    "200.55.160.0/20",
    "200.55.176.0/20",
    "201.220.192.0/20",
    "201.220.208.0/20"
]

# IP a excluir
#excluded_ip = "200.14.52.67"

# Rango a excluir
excluded_range = ip_network("200.14.52.64/28")

# Convertir los CIDRs a objetos ip_network
allowed_networks = [ip_network(cidr) for cidr in allowed_cidrs]

# Función para verificar si una IP pertenece a uno de los CIDRs permitidos
def is_ip_allowed(ip):
    ip_obj = ip_address(ip)
    # Verificar que no esté en el rango excluido y que pertenezca a los rangos permitidos
    return ip_obj not in excluded_range and any(ip_obj in network for network in allowed_networks)

# Archivo de logs de entrada
log_file_path = "default.log.2024-12-15"

# Archivo de salida
output_file_path = "resultIPs.log"

# Leer y procesar los logs
with open(log_file_path, "r", encoding="utf-8", errors="ignore") as log_file, \
     open(output_file_path, "w", encoding="utf-8") as output_file:
    for line in log_file:
        try:
            if "src_ip" in line and "suricata" in line:
                line_split = line.split(": ", 1)  # Dividir solo en el primer ':' para evitar errores
                if len(line_split) > 1:
                    potential_json = line_split[1].strip()
                    try:
                        log_data = json.loads(potential_json)  # Intentar cargar como JSON
                        if "src_ip" in log_data:
                            src_ip = log_data["src_ip"]
                            if is_ip_allowed(src_ip) and not log_data["dest_port"] == 443 and not log_data["dest_port"] == 80 and not log_data["dest_port"] == 53:
                                output_line = f"Allowed src_ip: {src_ip} | Full Log: {line.strip()}\n"
                                output_file.write(output_line)
                    except json.JSONDecodeError:
                        # No es un JSON válido, continuar con la siguiente línea
                        continue
        except Exception as e:
            # Manejo de errores genérico
            continue


