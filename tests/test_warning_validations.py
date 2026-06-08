import pandas as pd

from src.validations.warning_validations import (
    validate_nulls,
    validate_empty_dataframe,
    validate_duplicates,
)


def test_validate_nulls_without_warning():

    df = pd.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [4, 5, 6],
        }
    )

    result = validate_nulls(df)

    assert result == []


def test_validate_nulls_with_warning():

    df = pd.DataFrame(
        {
            "a": [1, None, None],
            "b": [None, None, 3],
        }
    )

    result = validate_nulls(df)

    assert len(result) == 1

    assert (
        result[0]["severity"]
        == "WARNING"
    )


def test_validate_empty_dataframe_warning():

    df = pd.DataFrame()

    result = validate_empty_dataframe(df)

    assert len(result) == 1

    assert (
        result[0]["severity"]
        == "WARNING"
    )


def test_validate_empty_dataframe_ok():

    df = pd.DataFrame(
        {
            "a": [1]
        }
    )

    result = validate_empty_dataframe(df)

    assert result == []


def test_validate_duplicates_warning():

    df = pd.DataFrame(
        {
            "id": [1, 1, 2]
        }
    )

    result = validate_duplicates(df)

    assert len(result) == 1

    assert (
        result[0]["severity"]
        == "WARNING"
    )


def test_validate_duplicates_ok():

    df = pd.DataFrame(
        {
            "id": [1, 2, 3]
        }
    )

    result = validate_duplicates(df)

    assert result == []