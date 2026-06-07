import pandas as pd

from src.logger import logger


def clean_accounting_records(
    df: pd.DataFrame,
) -> pd.DataFrame:

    logger.info(
        "Aplicando reglas de negocio para Libro Mayor..."
    )

    balance_mask = (
        df["cuenta"]
        .str.contains(
            "balance inicial",
            case=False,
            na=False,
        )
    )

    balances_found = balance_mask.sum()

    logger.info(
        f"Balances iniciales encontrados: "
        f"{balances_found}"
    )

    df.loc[
    balance_mask,
    "fecha"
    ] = "31/12/2024"

    rows_before = len(df)

    df = df[
        df["fecha"].notna()
    ]

    rows_removed = (
        rows_before - len(df)
    )

    logger.info(
        f"Filas eliminadas por reglas accounting: "
        f"{rows_removed}"
    )

    logger.info(
        "Transformaciones contables completadas."
    )

    return df