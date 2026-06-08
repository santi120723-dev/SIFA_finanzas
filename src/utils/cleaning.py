import re

import pandas as pd

from src.logger import logger
from src.transformations.accounting_cleaning import (
    clean_accounting_records,
)


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizar los nombres de las columnas:
    * eliminar espacios al inicio y al final
    * convertir a minúsculas
    * reemplazar espacios por "_"
    * eliminar caracteres especiales
    """

    logger.info("Normalizando nombres de columnas...")

    def _norm(col: str) -> str:
        col = col.strip().lower()
        col = col.replace(" ", "_")
        col = re.sub(r"[^a-z0-9_]", "", col)

        return col

    df = df.rename(columns=_norm)

    column_mapping = {
        "nombre_de_la_cuenta": "cuenta",
        "fecha_de_factura": "fecha",
    }

    df = df.rename(columns=column_mapping)

    logger.info("Nombres de columnas normalizados.")

    return df


def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia columnas tipo texto.
    """

    logger.info("Limpiando columnas de tipo string...")

    str_cols = df.select_dtypes(include=["object", "string"]).columns

    for col in str_cols:
        df[col] = df[col].apply(
            lambda x: x.strip()
            if isinstance(x, str)
            else x
        )

    logger.info("Columnas de tipo string limpiadas.")

    return df


def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estandariza valores nulos.
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

    if file_type == "libro_mayor":
        df = clean_accounting_records(df)

    logger.info(
        f"Limpieza genérica completada. "
        f"Filas: {df.shape[0]}, "
        f"Columnas: {df.shape[1]}"
    )

    return df