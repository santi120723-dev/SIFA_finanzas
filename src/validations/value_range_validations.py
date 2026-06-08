import pandas as pd

from src.logger import logger


def validate_value_ranges(
    df: pd.DataFrame,
) -> bool:

    if (df["debe"] < 0).any():

        raise ValueError(
            "Se encontraron valores negativos en debe."
        )

    if (df["haber"] < 0).any():

        raise ValueError(
            "Se encontraron valores negativos en haber."
        )

    if df["valor_movimiento"].isna().any():

        raise ValueError(
            "Existen valores nulos en valor_movimiento."
        )

    logger.info(
        "Validación de rangos completada."
    )

    return True