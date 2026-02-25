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
import logging
from datetime import datetime, timedelta

# ─── CONFIGURACION ────────────────────────────────────────────────────────────
BASE_DIR = "/ruta/a/tus/camaras"   # <-- cambia esto a tu directorio real
DAYS_TO_KEEP = 20                  # cuantos dias recientes conservar
DATE_FORMAT = "%Y-%m-%d"           # formato de las carpetas de fecha
LOG_FILE = "/var/log/autodelete.log"  # fichero de log (ajusta la ruta si es necesario)
# ──────────────────────────────────────────────────────────────────────────────

def setup_logger():
    logger = logging.getLogger("autodelete")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    # Fichero de log
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    # Consola
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger

def main():
    dry_run = "--dry-run" in sys.argv
    log = setup_logger()

    log.info("=" * 60)
    log.info(f"Inicio de ejecucion  |  modo: {'SIMULACION (dry-run)' if dry_run else 'REAL'}")
    log.info(f"Directorio base: {BASE_DIR}")
    log.info(f"Dias a conservar: {DAYS_TO_KEEP}")

    if not os.path.isdir(BASE_DIR):
        log.error(f"El directorio base no existe: {BASE_DIR}")
        sys.exit(1)

    cutoff_date = datetime.now().date() - timedelta(days=DAYS_TO_KEEP)
    log.info(f"Fecha de corte: {cutoff_date}  (se eliminan carpetas anteriores a esta fecha)")

    total_deleted = 0
    total_errors = 0
    total_size = 0

    # Recorrer subcarpetas (camera1, camera2, ...)
    camera_dirs = sorted([
        d for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d))
    ])

    if not camera_dirs:
        log.warning("No se encontraron subcarpetas en el directorio base.")
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
                continue

            if folder_date < cutoff_date:
                to_delete.append((entry, entry_path, folder_date))
            else:
                to_keep.append(entry)

        log.info(f"[{camera}]  conservar: {len(to_keep)} | a eliminar: {len(to_delete)}")

        for name, path, date in to_delete:
            folder_size = get_dir_size(path)
            size_str = format_size(folder_size)
            if dry_run:
                log.info(f"  [DRY-RUN] Eliminaria: {camera}/{name}  ({size_str})")
                total_size += folder_size
                total_deleted += 1
            else:
                try:
                    shutil.rmtree(path)
                    log.info(f"  Eliminado: {camera}/{name}  ({size_str})")
                    total_size += folder_size
                    total_deleted += 1
                except Exception as e:
                    log.error(f"  ERROR al eliminar {camera}/{name}: {e}")
                    total_errors += 1

    action = "Se eliminarian" if dry_run else "Se eliminaron"
    log.info(f"{action} {total_deleted} carpetas  |  espacio liberado: ~{format_size(total_size)}  |  errores: {total_errors}")
    log.info("Fin de ejecucion")
    log.info("=" * 60)


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
    
'''
Compatibility python 2.7

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
autodelete.py
Compatible con Python 2.7
"""

import os
import sys
import shutil
import logging
from datetime import datetime, timedelta

# ─── CONFIGURACION ────────────────────────────────────────────────────────────
BASE_DIR = "/ruta/a/tus/camaras"   # <-- cambia esto a tu directorio real
DAYS_TO_KEEP = 20
DATE_FORMAT = "%Y-%m-%d"
LOG_FILE = "/var/log/autodelete.log"
# ──────────────────────────────────────────────────────────────────────────────

def setup_logger():
    logger = logging.getLogger("autodelete")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Fichero de log
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Consola
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger


def main():
    dry_run = "--dry-run" in sys.argv
    log = setup_logger()

    log.info("=" * 60)
    mode = "SIMULACION (dry-run)" if dry_run else "REAL"
    log.info("Inicio de ejecucion  |  modo: {0}".format(mode))
    log.info("Directorio base: {0}".format(BASE_DIR))
    log.info("Dias a conservar: {0}".format(DAYS_TO_KEEP))

    if not os.path.isdir(BASE_DIR):
        log.error("El directorio base no existe: {0}".format(BASE_DIR))
        sys.exit(1)

    cutoff_date = datetime.now().date() - timedelta(days=DAYS_TO_KEEP)
    log.info("Fecha de corte: {0}  (se eliminan carpetas anteriores a esta fecha)".format(cutoff_date))

    total_deleted = 0
    total_errors = 0
    total_size = 0

    camera_dirs = sorted([
        d for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d))
    ])

    if not camera_dirs:
        log.warning("No se encontraron subcarpetas en el directorio base.")
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
                continue

            if folder_date < cutoff_date:
                to_delete.append((entry, entry_path, folder_date))
            else:
                to_keep.append(entry)

        log.info("[{0}]  conservar: {1} | a eliminar: {2}".format(
            camera, len(to_keep), len(to_delete)
        ))

        for name, path, date in to_delete:
            folder_size = get_dir_size(path)
            size_str = format_size(folder_size)

            if dry_run:
                log.info("  [DRY-RUN] Eliminaria: {0}/{1}  ({2})".format(
                    camera, name, size_str
                ))
                total_size += folder_size
                total_deleted += 1
            else:
                try:
                    shutil.rmtree(path)
                    log.info("  Eliminado: {0}/{1}  ({2})".format(
                        camera, name, size_str
                    ))
                    total_size += folder_size
                    total_deleted += 1
                except Exception as e:
                    log.error("  ERROR al eliminar {0}/{1}: {2}".format(
                        camera, name, str(e)
                    ))
                    total_errors += 1

    action = "Se eliminarian" if dry_run else "Se eliminaron"

    log.info("{0} {1} carpetas  |  espacio liberado: ~{2}  |  errores: {3}".format(
        action, total_deleted, format_size(total_size), total_errors
    ))

    log.info("Fin de ejecucion")
    log.info("=" * 60)


def get_dir_size(path):
    """Calcula el tamaño total de un directorio en bytes."""
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
            return "{0:.1f} {1}".format(size_bytes, unit)
        size_bytes = float(size_bytes) / 1024
    return "{0:.1f} PB".format(size_bytes)


if __name__ == "__main__":
    main()

'''
