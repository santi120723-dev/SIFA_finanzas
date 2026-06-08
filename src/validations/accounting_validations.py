import pandas as pd

from src.logger import logger


def validate_codigo_cuenta(
    df: pd.DataFrame,
) -> bool:

    nulls = (
        df["codigo_cuenta"]
        .isna()
        .sum()
    )

    if nulls > 0:

        raise ValueError(
            f"Se encontraron "
            f"{nulls} registros "
            f"sin codigo_cuenta."
        )

    logger.info(
        "Validación codigo_cuenta completada."
    )

    return True

def validate_nombre_cuenta(
    df: pd.DataFrame,
) -> bool:

    nulls = (
        df["nombre_cuenta"]
        .isna()
        .sum()
    )

    if nulls > 0:

        raise ValueError(
            f"Se encontraron "
            f"{nulls} registros "
            f"sin nombre_cuenta."
        )

    logger.info(
        "Validación nombre_cuenta completada."
    )

    return True

def validate_fecha_datetime(
    df: pd.DataFrame,
) -> bool:

    if not pd.api.types.is_datetime64_any_dtype(
        df["fecha"]
    ):

        raise ValueError(
            "La columna fecha "
            "no es datetime."
        )

    logger.info(
        "Validación tipo fecha completada."
    )

    return True

def validate_puc_structure(
    df: pd.DataFrame,
) -> bool:

    invalid = df[
        df["codigo_cuenta"]
        .astype(str)
        .str.len()
        < 4
    ]

    if len(invalid) > 0:

        raise ValueError(
            f"Se encontraron "
            f"{len(invalid)} "
            f"códigos contables inválidos."
        )

    logger.info(
        "Validación estructura PUC completada."
    )

    return True

def validate_valor_movimiento(
    df: pd.DataFrame,
) -> bool:

    calculado = (
        df["debe"]
        - df["haber"]
    )

    diferencias = (
        calculado
        != df["valor_movimiento"]
    )

    if diferencias.any():

        raise ValueError(
            "Existen registros con "
            "valor_movimiento inconsistente."
        )

    logger.info(
        "Validación valor_movimiento completada."
    )

    return True
