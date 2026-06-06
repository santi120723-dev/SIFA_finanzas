import pandas as pd
import pytest

from src.validations.generic_validations import (
    validate_dates,
)


def test_valid_dates():

    df = pd.read_csv(
        "tests/data/critical_imbalanced.csv"
    )

    assert validate_dates(df)


def test_invalid_dates():

    df = pd.read_csv(
        "tests/data/invalid_dates.csv"
    )

    with pytest.raises(ValueError):

        validate_dates(df)


def test_null_dates():

    df = pd.read_csv(
        "tests/data/null_dates.csv"
    )

    with pytest.raises(ValueError):

        validate_dates(df)