import pandas as pd
import pytest

from src.validations.accounting_validations import (
    validate_codigo_cuenta,
    validate_nombre_cuenta,
    validate_fecha_datetime,
    validate_puc_structure,
    validate_valor_movimiento,
)

from src.validations.business_rules import (
    validate_debe_haber,
)


def test_validate_codigo_cuenta_ok():

    df = pd.DataFrame(
        {
            "codigo_cuenta": [110505, 130505]
        }
    )

    assert validate_codigo_cuenta(df) is True


def test_validate_codigo_cuenta_error():

    df = pd.DataFrame(
        {
            "codigo_cuenta": [110505, None]
        }
    )

    with pytest.raises(ValueError):

        validate_codigo_cuenta(df)


def test_validate_nombre_cuenta_ok():

    df = pd.DataFrame(
        {
            "nombre_cuenta": [
                "Efectivo",
                "Caja General",
            ]
        }
    )

    assert validate_nombre_cuenta(df) is True


def test_validate_nombre_cuenta_error():

    df = pd.DataFrame(
        {
            "nombre_cuenta": [
                "Efectivo",
                None,
            ]
        }
    )

    with pytest.raises(ValueError):

        validate_nombre_cuenta(df)


def test_validate_fecha_datetime_ok():

    df = pd.DataFrame(
        {
            "fecha": pd.to_datetime(
                [
                    "2025-01-01",
                    "2025-01-02",
                ]
            )
        }
    )

    assert validate_fecha_datetime(df) is True


def test_validate_fecha_datetime_error():

    df = pd.DataFrame(
        {
            "fecha": [
                "01/01/2025",
                "02/01/2025",
            ]
        }
    )

    with pytest.raises(ValueError):

        validate_fecha_datetime(df)


def test_validate_puc_structure_ok():

    df = pd.DataFrame(
        {
            "codigo_cuenta": [
                110505,
                130505,
            ]
        }
    )

    assert validate_puc_structure(df) is True


def test_validate_puc_structure_error():

    df = pd.DataFrame(
        {
            "codigo_cuenta": [
                11,
                22,
            ]
        }
    )

    with pytest.raises(ValueError):

        validate_puc_structure(df)


def test_validate_valor_movimiento_ok():

    df = pd.DataFrame(
        {
            "debe": [1000],
            "haber": [400],
            "valor_movimiento": [600],
        }
    )

    assert validate_valor_movimiento(df) is True


def test_validate_valor_movimiento_error():

    df = pd.DataFrame(
        {
            "debe": [1000],
            "haber": [400],
            "valor_movimiento": [700],
        }
    )

    with pytest.raises(ValueError):

        validate_valor_movimiento(df)


def test_validate_debe_haber_ok():

    df = pd.DataFrame(
        {
            "cuenta": ["A", "B"],
            "debe": [1000, 500],
            "haber": [1000, 500],
            "fecha": [
                "2025-01-01",
                "2025-01-02",
            ],
        }
    )

    assert validate_debe_haber(df) is True


def test_validate_debe_haber_error():

    df = pd.DataFrame(
        {
            "cuenta": ["A", "B"],
            "debe": [1000, 500],
            "haber": [1000, 100],
            "fecha": [
                "2025-01-01",
                "2025-01-02",
            ],
        }
    )

    with pytest.raises(ValueError):

        validate_debe_haber(df)