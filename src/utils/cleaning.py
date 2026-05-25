import re

import pandas as pd

from src.logger import logger


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names:
    - strip whitespace
    - convert to lowercase
    - replace spaces with '_'
    - remove special characters
    """

    logger.info("Normalizando nombres de columnas...")

    def _norm(col: str) -> str:
        col = col.strip().lower()
        col = col.replace(" ", "_")
        col = re.sub(r"[^a-z0-9_]", "", col)

        return col

    df = df.rename(columns=_norm)

    logger.info("Nombres de columnas normalizados.")

    return df


def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean string (object) columns:
    - strip leading/trailing whitespace
    - preserve null values
    """

    logger.info("Limpiando columnas de tipo string...")

    str_cols = df.select_dtypes(include=["object"]).columns

    for col in str_cols:
        df[col] = df[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    logger.info("Columnas de tipo string limpiadas.")

    return df


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize common null representations to pandas NA:
    - empty string
    - 'null'
    - 'n/a'
    - 'none'
    """

    logger.info("Estandarizando valores nulos...")

    df = df.copy()

    null_pattern = re.compile(
        r"^\s*(null|n/a|none)?\s*$",
        re.IGNORECASE,
    )

    string_cols = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for col in string_cols:

        df[col] = df[col].apply(
            lambda x: (
                pd.NA
                if isinstance(x, str)
                and null_pattern.match(x)
                else x
            )
        )

    logger.info("Valores nulos estandarizados.")

    return df


def clean_dataframe(
    df: pd.DataFrame,
    file_type: str = None,
) -> pd.DataFrame:
    """
    Generic Silver-layer cleaning pipeline.
    """

    logger.info(
        f"Iniciando limpieza genérica para dataset: "
        f"{file_type if file_type else 'desconocido'}"
    )

    df = normalize_column_names(df)

    df = clean_strings(df)

    df = handle_nulls(df)

    logger.info(
        f"Limpieza genérica completada. "
        f"Filas: {df.shape[0]}, "
        f"Columnas: {df.shape[1]}"
    )

    return df