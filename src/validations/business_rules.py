import pandas as pd

from src.logger import logger

from src.validations.generic_validations import (
    validate_required_columns
)


def validate_debe_haber(
    df: pd.DataFrame,
    tolerance: float = 1.0
) -> bool:

    validate_required_columns(df)

    debe_sum = df["debe"].sum()
    haber_sum = df["haber"].sum()

    diferencia = abs(
        debe_sum - haber_sum
    )

    logger.info(
        f"Validate Debe/Haber | "
        f"Debe={debe_sum:.2f} | "
        f"Haber={haber_sum:.2f} | "
        f"Diff={diferencia:.2f}"
    )

    if diferencia > tolerance:

        raise ValueError(
            f"Desbalance contable detectado | "
            f"Debe={debe_sum:.2f} | "
            f"Haber={haber_sum:.2f} | "
            f"Diferencia={diferencia:.2f}"
        )

    logger.info(
        "Validación Debe/Haber completada."
    )

    return True