import pandas as pd
import pytest

from src.validations.validation_runner import (
    run_validations,
)


def test_valid_balance():
    """
    Dataset balanceado.
    Debe pasar correctamente.
    """

    df = pd.read_csv(
        "tests/data/critical_imbalanced.csv"
    )

    results = run_validations(df)

    assert results is not None


def test_invalid_balance():
    """
    Dataset desbalanceado.
    Debe bloquear pipeline.
    """

    df = pd.read_csv(
        "tests/data/critical_imbalanced2.csv"
    )

    with pytest.raises(ValueError):

        run_validations(df)


def test_missing_columns():
    """
    Dataset con columnas faltantes.
    Debe bloquear pipeline.
    """

    df = pd.read_csv(
        "tests/data/missing_columns.csv"
    )

    with pytest.raises(ValueError):

        run_validations(df)