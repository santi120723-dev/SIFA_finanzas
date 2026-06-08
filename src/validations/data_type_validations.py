import pandas as pd

from src.logger import logger


def validate_data_types(
    df: pd.DataFrame,
) -> bool:

    numeric_columns = [
        "debe",
        "haber",
        "valor_final",
        "valor_movimiento",
    ]

    for col in numeric_columns:

        if col not in df.columns:

            raise ValueError(
                f"La columna '{col}' no existe."
            )

        if not pd.api.types.is_numeric_dtype(
            df[col]
        ):

            raise ValueError(
                f"La columna '{col}' debe ser numérica."
            )

    if "fecha" not in df.columns:

        raise ValueError(
            "La columna fecha no existe."
        )

    if not pd.api.types.is_datetime64_any_dtype(
        df["fecha"]
    ):

        raise ValueError(
            "La columna fecha debe ser datetime."
        )

    logger.info(
        "Validación de tipos de datos completada."
    )

    return True