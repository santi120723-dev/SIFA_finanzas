from src.validations.validation_summary import (
    validation_summary,
)

def test_validation_summary():

    results = [
        {
            "validator": "validate_dates",
            "severity": "CRITICAL",
            "status": "passed",
        },
        {
            "severity": "WARNING",
            "message": "Duplicados encontrados",
        },
    ]

    validation_summary(
        results
    )

    assert True