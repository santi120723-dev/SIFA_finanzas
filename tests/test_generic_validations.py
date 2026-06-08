import pandas as pd
import pytest

from src.validations.generic_validations import (
    validate_required_columns,
    validate_dates,
)


def test_validate_required_columns_ok():

    df = pd.DataFrame(
        {
            "cuenta": ["Caja"],
            "debe": [100],
            "haber": [100],
            "fecha": ["01/01/2025"],
        }
    )

    assert (
        validate_required_columns(df)
        is True
    )


def test_validate_required_columns_error():

    df = pd.DataFrame(
        {
            "cuenta": ["Caja"],
            "debe": [100],
            "fecha": ["01/01/2025"],
        }
    )

    with pytest.raises(ValueError):

        validate_required_columns(df)


def test_validate_dates_ok():

    df = pd.DataFrame(
        {
            "fecha": [
                "01/01/2025",
                "15/02/2025",
            ]
        }
    )

    assert (
        validate_dates(df)
        is True
    )


def test_validate_dates_column_missing():

    df = pd.DataFrame(
        {
            "otra_columna": [1]
        }
    )

    with pytest.raises(ValueError):

        validate_dates(df)


def test_validate_dates_nulls():

    df = pd.DataFrame(
        {
            "fecha": [
                "01/01/2025",
                None,
            ]
        }
    )

    with pytest.raises(ValueError):

        validate_dates(df)


def test_validate_dates_invalid_format():

    df = pd.DataFrame(
        {
            "fecha": [
                "2025-01-01",
            ]
        }
    )

    with pytest.raises(ValueError):

        validate_dates(df)