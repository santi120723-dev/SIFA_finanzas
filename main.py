from src.ingestion.extract import (
    load_libro_mayor,
    load_movimientos_inventario,
    load_ordenes_fabricacion
)

from src.preprocess.normalizer import normalize_libro_mayor

from src.logger import logger


# =========================
# EJECUCIÓN PIPELINE
# =========================

def main():

    logger.info("Iniciando pipeline ETL...")

    # 1. INGESTA
    libro_mayor = load_libro_mayor()
    inventario = load_movimientos_inventario()
    ordenes = load_ordenes_fabricacion()

    # 2. TRANSFORMACIÓN (STAGING)
    libro_mayor = normalize_libro_mayor(libro_mayor)

    # 3. VALIDACIÓN
    required = ["fecha", "cuenta", "debe", "haber"]

    missing = [c for c in required if c not in libro_mayor.columns]

    if missing:
        raise ValueError(f"Faltan columnas: {missing}")

    logger.info("Pipeline ejecutado exitosamente")


if __name__ == "__main__":
    main()