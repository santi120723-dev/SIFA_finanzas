from src.ingestion.extract import (
    load_libro_mayor,
    load_movimientos_inventario,
    load_ordenes_fabricacion
)

# =========================
# EJECUCIÓN PIPELINE
# =========================

from src.logger import logger

def main():

    libro_mayor = (
        load_libro_mayor()
    )

    inventario = (
        load_movimientos_inventario()
    )

    ordenes = (
        load_ordenes_fabricacion()
    )

    print("\nPipeline ejecutado")


if __name__ == "__main__":

    main()