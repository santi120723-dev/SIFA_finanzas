import pandas as pd

from src.logger import logger


def clean_accounting_records(
    df: pd.DataFrame,
) -> pd.DataFrame:

    logger.info(
        "Aplicando reglas de negocio para Libro Mayor..."
    )

    # Detectar cabeceras contables
    header_mask = (
        df["cdigo"].notna()
        & df["fecha"].isna()
    )

    logger.info(
        f"Cabeceras detectadas: "
        f"{header_mask.sum()}"
    )

    # Crear columnas analíticas
    df["codigo_cuenta"] = None
    df["nombre_cuenta"] = None

    # Copiar información desde cabeceras
    df.loc[
        header_mask,
        "codigo_cuenta"
    ] = df.loc[
        header_mask,
        "cdigo"
    ]

    df.loc[
        header_mask,
        "nombre_cuenta"
    ] = df.loc[
        header_mask,
        "cuenta"
    ]

    # Propagar cuenta a movimientos
    df["codigo_cuenta"] = (
        df["codigo_cuenta"]
        .ffill()
    )

    df["nombre_cuenta"] = (
        df["nombre_cuenta"]
        .ffill()
    )

    # Conservar detalle original
    df["detalle_movimiento"] = (
        df["cuenta"]
    )

    df["valor_movimiento"] = (
        df["debe"]
        -df["haber"]
    )

    # Balance inicial
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

    # Eliminar filas Total
    total_mask = (
        df["cuenta"]
        .str.contains(
            "^total",
            case=False,
            regex=True,
            na=False,
        )
    )

    df = df[
        ~total_mask
    ]

    # Recalcular cabeceras después de eliminar totales
    header_rows_to_remove = (
        df["cdigo"].notna()
        & df["fecha"].isna()
    )

    logger.info(
        f"Cabeceras eliminadas: "
        f"{header_rows_to_remove.sum()}"
    )

    df = df[
        ~header_rows_to_remove
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

    df["fecha"] = pd.to_datetime(
        df["fecha"],
        format="%d/%m/%Y",
    )

    # ==========================
    # JERARQUÍA CONTABLE PUC
    # ==========================

    codigo_str = (
        df["codigo_cuenta"]
        .astype(str)
        .str.replace(".0", "", regex=False)
    )

    df["clase"] = (
        codigo_str.str[:1]
    )

    df["grupo"] = (
        codigo_str.str[:2]
    )

    df["cuenta_puc"] = (
    codigo_str.str[:4]
    )

    df["subcuenta"] = (
        codigo_str.str[:6]
    )

    # ==========================
    # CALENDARIO FINANCIERO
    # ==========================

    df["anio"] = (
        df["fecha"]
        .dt.year
    )

    df["mes"] = (
        df["fecha"]
        .dt.month
    )

    df["trimestre"] = (
        df["fecha"]
    .dt.quarter
    )

    df["periodo_contable"] = (
        df["fecha"]
        .dt.strftime("%Y-%m")
    )

    return df