import glob
import re
from collections import defaultdict, Counter

# Patrón de archivo de log
log_files = glob.glob("pihole.log.2024-12-*")

# Diccionario para almacenar los contadores por tipo de query
query_counts = defaultdict(Counter)

# Expresión regular para capturar tipo de query y dominio/dirección
query_pattern = re.compile(r"query\[(\w+)] ([^\s]+)")

for log_file in log_files:
    with open(log_file, 'r') as file:
        for line in file:
            match = query_pattern.search(line)
            if match:
                query_type = match.group(1)  # Tipo de query (A, PTR, etc.)
                query_target = match.group(2)  # Dominio o dirección
                query_counts[query_type][query_target] += 1

# Generar el top 100 por tipo de query
for query_type, counter in query_counts.items():
    print(f"\nTop 100 queries for type [{query_type}]:")
    for target, count in counter.most_common(100):
        print(f"{target}: {count}")
