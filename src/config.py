from pathlib import Path

# =========================
# BASE DEL PROYECTO
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# CAPAS DE DATOS
# =========================

DATA_BRONZE = BASE_DIR / "data" / "bronze"

DATA_SILVER = BASE_DIR / "data" / "silver"

DATA_GOLD = BASE_DIR / "data" / "gold"

# =========================
# ARCHIVOS FUENTE
# =========================

LIBRO_MAYOR = (
    DATA_BRONZE / "accounting" / "libro_mayor_2025.xlsx"
)

MOVIMIENTOS_INVENTARIO = (
    DATA_BRONZE / "inventory" / "movimientos_inventario_2025.xlsx"
)

ORDENES_FABRICACION = (
    DATA_BRONZE / "manufacturing" / "ordenes_fabricacion_2025.xlsx"
)