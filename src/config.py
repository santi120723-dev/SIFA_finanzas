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
# CALIDAD Y GOBIERNO
# =========================

DATA_QUALITY = (
    BASE_DIR / "data" / "quality"
)

THIRD_PARTY_MAPPING = (
    DATA_QUALITY / "third_party_mapping.parquet"
)

THIRD_PARTY_REVIEW = (
    DATA_QUALITY / "third_party_review.parquet"
)

# =========================
# DIMENSIONES
# =========================

DIM_TERCEROS = (
    DATA_SILVER
    / "dimensions"
    / "dim_terceros.parquet"
)

# =========================
# TERCEROS
# =========================

TERCEROS_MASTER = (
    DATA_BRONZE / "terceros_2025.xlsx"
)

# =========================
# DATASETS ANONIMIZADOS
# =========================

ANONYMIZED_ACCOUNTING = (
    DATA_SILVER
    / "accounting"
    / "libro_mayor_2025_anon.parquet"
)

# =========================
# ARCHIVOS FUENTE
# =========================

LIBRO_MAYOR = (
    DATA_BRONZE
    / "accounting"
    / "libro_mayor_2025.xlsx"
)

MOVIMIENTOS_INVENTARIO = (
    DATA_BRONZE
    / "inventory"
    / "movimientos_inventario_2025.xlsx"
)

ORDENES_FABRICACION = (
    DATA_BRONZE
    / "manufacturing"
    / "ordenes_fabricacion_2025.xlsx"
)