import pandas as pd
from src.logger import logger

def validate_debe_haber(
    df: pd.DataFrame,
    tolerance: float = 1.0
) -> bool:
    """
    Valida que la diferencia entre sumatoria
    de 'debe' y 'haber' sea ≤ tolerancia.
    """

    try:

        debe_sum = df['debe'].sum()
        haber_sum = df['haber'].sum()

    except KeyError as e:

        raise ValueError(
            f"Faltan columnas requeridas: {e}"
        ) from e

    diferencia = abs(
        debe_sum - haber_sum
    )

    logger.info(
        f"Validate Debe/Haber: "
        f"Debe={debe_sum:.2f}, "
        f"Haber={haber_sum:.2f}, "
        f"Diff={diferencia:.2f}"
    )

    if diferencia > tolerance:

        raise ValueError(
            f"❌ Error de validación contable: "
            f"Debe={debe_sum:.2f} vs "
            f"Haber={haber_sum:.2f} "
            f"(diferencia={diferencia:.2f} "
            f"> tolerancia={tolerance})"
        )

    logger.info(
        "✅ Validación de Debe/Haber pasada correctamente."
    )

    return True