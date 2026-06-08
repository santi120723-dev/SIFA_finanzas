import pytest
import pandas as pd

from src.validations.data_type_validations import (
    validate_data_types,
)


def test_validate_data_types_ok():

    df = pd.DataFrame(
        {
            "debe": [100.0],
            "haber": [50.0],
            "valor_final": [50.0],
            "valor_movimiento": [50.0],
            "fecha": pd.to_datetime(
                ["2025-01-01"]
            ),
        }
    )

    assert validate_data_types(df) is True


def test_validate_debe_not_numeric():

    df = pd.DataFrame(
        {
            "debe": ["texto"],
            "haber": [50.0],
            "valor_final": [50.0],
            "valor_movimiento": [50.0],
            "fecha": pd.to_datetime(
                ["2025-01-01"]
            ),
        }
    )

    with pytest.raises(ValueError):
        validate_data_types(df)


def test_validate_haber_not_numeric():

    df = pd.DataFrame(
        {
            "debe": [100.0],
            "haber": ["texto"],
            "valor_final": [50.0],
            "valor_movimiento": [50.0],
            "fecha": pd.to_datetime(
                ["2025-01-01"]
            ),
        }
    )

    with pytest.raises(ValueError):
        validate_data_types(df)


def test_validate_valor_final_not_numeric():

    df = pd.DataFrame(
        {
            "debe": [100.0],
            "haber": [50.0],
            "valor_final": ["texto"],
            "valor_movimiento": [50.0],
            "fecha": pd.to_datetime(
                ["2025-01-01"]
            ),
        }
    )

    with pytest.raises(ValueError):
        validate_data_types(df)


def test_validate_valor_movimiento_not_numeric():

    df = pd.DataFrame(
        {
            "debe": [100.0],
            "haber": [50.0],
            "valor_final": [50.0],
            "valor_movimiento": ["texto"],
            "fecha": pd.to_datetime(
                ["2025-01-01"]
            ),
        }
    )

    with pytest.raises(ValueError):
        validate_data_types(df)


def test_validate_fecha_not_datetime():

    df = pd.DataFrame(
        {
            "debe": [100.0],
            "haber": [50.0],
            "valor_final": [50.0],
            "valor_movimiento": [50.0],
            "fecha": ["01/01/2025"],
        }
    )

    with pytest.raises(ValueError):
        validate_data_types(df)