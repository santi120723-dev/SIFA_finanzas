import pandas as pd

from src.transformations.accounting_cleaning import (
    clean_accounting_records,
)


def test_forward_fill_accounts():

    df = pd.DataFrame(
        {
            "cdigo": [
                110505,
                None,
            ],
            "cuenta": [
                "Efectivo",
                "Pago proveedor",
            ],
            "fecha": [
                None,
                "01/01/2025",
            ],
            "contacto": [
                None,
                "Proveedor A",
            ],
            "debe": [
                0,
                1000,
            ],
            "haber": [
                0,
                0,
            ],
            "valor_final": [
                0,
                1000,
            ],
        }
    )

    result = clean_accounting_records(df)

    row = result.iloc[0]

    assert row["codigo_cuenta"] == 110505
    assert row["nombre_cuenta"] == "Efectivo"


def test_balance_inicial_date():

    df = pd.DataFrame(
        {
            "cdigo": [
                110505,
                None,
            ],
            "cuenta": [
                "Caja General",
                "Balance inicial",
            ],
            "fecha": [
                None,
                None,
            ],
            "contacto": [
                None,
                None,
            ],
            "debe": [
                0,
                0,
            ],
            "haber": [
                0,
                0,
            ],
            "valor_final": [
                0,
                0,
            ],
        }
    )

    result = clean_accounting_records(df)

    balance_row = result.iloc[0]

    assert (
        balance_row["fecha"]
        == pd.Timestamp("2024-12-31")
    )


def test_remove_total_rows():

    df = pd.DataFrame(
        {
            "cdigo": [
                110505,
                None,
                None,
            ],
            "cuenta": [
                "Efectivo",
                "Pago proveedor",
                "Total Efectivo",
            ],
            "fecha": [
                None,
                "01/01/2025",
                "01/01/2025",
            ],
            "contacto": [
                None,
                None,
                None,
            ],
            "debe": [
                0,
                100,
                100,
            ],
            "haber": [
                0,
                0,
                0,
            ],
            "valor_final": [
                0,
                100,
                100,
            ],
        }
    )

    result = clean_accounting_records(df)

    assert (
        result["detalle_movimiento"]
        .str.contains(
            "Total",
            case=False,
            na=False,
        )
        .sum()
        == 0
    )


def test_puc_hierarchy():

    df = pd.DataFrame(
        {
            "cdigo": [
                11050501,
                None,
            ],
            "cuenta": [
                "Caja General",
                "Movimiento",
            ],
            "fecha": [
                None,
                "01/01/2025",
            ],
            "contacto": [
                None,
                None,
            ],
            "debe": [
                0,
                100,
            ],
            "haber": [
                0,
                0,
            ],
            "valor_final": [
                0,
                100,
            ],
        }
    )

    result = clean_accounting_records(df)

    row = result.iloc[0]

    assert row["clase"] == "1"
    assert row["grupo"] == "11"
    assert row["cuenta_puc"] == "1105"
    assert row["subcuenta"] == "110505"


def test_financial_calendar():

    df = pd.DataFrame(
        {
            "cdigo": [
                110505,
                None,
            ],
            "cuenta": [
                "Efectivo",
                "Movimiento",
            ],
            "fecha": [
                None,
                "15/08/2025",
            ],
            "contacto": [
                None,
                None,
            ],
            "debe": [
                0,
                100,
            ],
            "haber": [
                0,
                0,
            ],
            "valor_final": [
                0,
                100,
            ],
        }
    )

    result = clean_accounting_records(df)

    row = result.iloc[0]

    assert row["anio"] == 2025
    assert row["mes"] == 8
    assert row["trimestre"] == 3
    assert row["periodo_contable"] == "2025-08"