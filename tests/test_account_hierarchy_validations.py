import pandas as pd

import pytest

from src.validations.account_hierarchy_validations import (
    validate_account_hierarchy_consistency,
)


def test_hierarchy_ok():

    df = pd.DataFrame(
        {
            "codigo_cuenta": ["11050501"],
            "clase": ["1"],
            "grupo": ["11"],
            "cuenta_puc": ["1105"],
            "subcuenta": ["110505"],
        }
    )

    assert (
        validate_account_hierarchy_consistency(df)
        is True
    )


def test_invalid_clase():

    df = pd.DataFrame(
        {
            "codigo_cuenta": ["11050501"],
            "clase": ["2"],
            "grupo": ["11"],
            "cuenta_puc": ["1105"],
            "subcuenta": ["110505"],
        }
    )

    with pytest.raises(ValueError):

        validate_account_hierarchy_consistency(df)


def test_invalid_grupo():

    df = pd.DataFrame(
        {
            "codigo_cuenta": ["11050501"],
            "clase": ["1"],
            "grupo": ["22"],
            "cuenta_puc": ["1105"],
            "subcuenta": ["110505"],
        }
    )

    with pytest.raises(ValueError):

        validate_account_hierarchy_consistency(df)


def test_invalid_cuenta_puc():

    df = pd.DataFrame(
        {
            "codigo_cuenta": ["11050501"],
            "clase": ["1"],
            "grupo": ["11"],
            "cuenta_puc": ["9999"],
            "subcuenta": ["110505"],
        }
    )

    with pytest.raises(ValueError):

        validate_account_hierarchy_consistency(df)


def test_invalid_subcuenta():

    df = pd.DataFrame(
        {
            "codigo_cuenta": ["11050501"],
            "clase": ["1"],
            "grupo": ["11"],
            "cuenta_puc": ["1105"],
            "subcuenta": ["999999"],
        }
    )

    with pytest.raises(ValueError):

        validate_account_hierarchy_consistency(df)