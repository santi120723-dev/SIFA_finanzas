import pytest
import pandas as pd

from src.validations.value_range_validations import (
    validate_value_ranges,
)


def test_validate_value_ranges_ok():

    df = pd.DataFrame(
        {
            "debe": [100, 200],
            "haber": [50, 100],
            "valor_movimiento": [50, 100],
        }
    )

    assert (
        validate_value_ranges(df)
        is True
    )

def test_validate_debe_negative():

    df = pd.DataFrame(
        {
            "debe": [-100],
            "haber": [50],
            "valor_movimiento": [-150],
        }
    )

    with pytest.raises(ValueError):

        validate_value_ranges(df)

def test_validate_haber_negative():

    df = pd.DataFrame(
        {
            "debe": [100],
            "haber": [-50],
            "valor_movimiento": [150],
        }
    )

    with pytest.raises(ValueError):

        validate_value_ranges(df)

def test_validate_valor_movimiento_null():

    df = pd.DataFrame(
        {
            "debe": [100],
            "haber": [50],
            "valor_movimiento": [None],
        }
    )

    with pytest.raises(ValueError):

        validate_value_ranges(df)