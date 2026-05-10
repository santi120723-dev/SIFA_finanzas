from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_RAW = BASE_DIR / "data_raw"
DATA_CLEAN = BASE_DIR / "data_clean"

LIBRO_MAYOR = DATA_RAW / "libro_mayor_2025.xlsx"
MOVIMIENTOS_INVENTARIO = DATA_RAW / "movimientos_inventario_2025.xlsx"
ORDENES_FABRICACION = DATA_RAW / "ordenes_fabricacion_2025.xlsx"