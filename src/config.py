from pathlib import Path

# =========================
# BASE DEL PROYECTO
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# CAPAS DE DATOS
# =========================

DATA_RAW = BASE_DIR / "data" / "raw"

DATA_STAGING = BASE_DIR / "data" / "staging"

DATA_CLEAN = BASE_DIR / "data" / "clean"

# =========================
# ARCHIVOS FUENTE
# =========================

LIBRO_MAYOR = (
    DATA_RAW / "libro_mayor_2025.xlsx"
)

MOVIMIENTOS_INVENTARIO = (
    DATA_RAW / "movimientos_inventario_2025.xlsx"
)

ORDENES_FABRICACION = (
    DATA_RAW / "ordenes_fabricacion_2025.xlsx"
)