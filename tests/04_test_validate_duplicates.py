import pandas as pd

from src.validations.warning_validations import (
    validate_duplicates,
)


def test_no_duplicates():

    df = pd.read_csv(
        "tests/data/no_duplicates.csv"
    )

    result = validate_duplicates(df)

    assert result == []


def test_duplicates_detected():

    df = pd.read_csv(
        "tests/data/duplicates.csv"
    )

    result = validate_duplicates(df)

    assert len(result) > 0
    assert result[0]["severity"] == "WARNING"