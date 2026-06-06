import pandas as pd

from src.logger import logger


def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str] | None = None
) -> bool:
    """
    Valida que existan columnas requeridas.
    """

    if required_columns is None:
        required_columns = [
            "cuenta",
            "debe",
            "haber",
            "fecha",
        ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Columnas faltantes: {missing}"
        )

    logger.info(
        "Validación de columnas requerida completada."
    )

    return True


def validate_dates(
    df: pd.DataFrame,
    date_column: str = "fecha"
) -> bool:
    """
    Valida que la columna de fechas exista,
    no tenga nulos y pueda convertirse a datetime.
    """

    if date_column not in df.columns:

        raise ValueError(
            f"Columna de fechas '{date_column}' no encontrada."
        )

    if df[date_column].isna().any():

        raise ValueError(
            f"La columna '{date_column}' contiene valores nulos."
        )

    try:

        pd.to_datetime(
            df[date_column],
            errors="raise"
        )

    except Exception as e:

        raise ValueError(
            f"Fechas inválidas encontradas en "
            f"'{date_column}': {e}"
        )

    logger.info(
        f"Validación de fechas en "
        f"'{date_column}' completada."
    )

    return True