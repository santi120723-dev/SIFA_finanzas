import logging
from typing import List, Dict

from .generic_validations import (
    validate_required_columns,
    validate_dates,
)

from .business_rules import (
    validate_debe_haber
)

from .warning_validations import (
    validate_nulls,
    validate_empty_dataframe,
    validate_duplicates,
)

log = logging.getLogger(__name__)


CRITICAL_VALIDATIONS = [
    validate_required_columns,
    validate_dates,
    validate_debe_haber,
]


WARNING_VALIDATIONS = [
    validate_nulls,
    validate_empty_dataframe,
    validate_duplicates,
]


def run_validations(df) -> List[Dict]:

    results = []

    # =========================
    # CRITICAL VALIDATIONS
    # =========================
    for validator in CRITICAL_VALIDATIONS:

        try:

            validator(df)

            results.append(
                {
                    "validator": validator.__name__,
                    "severity": "CRITICAL",
                    "status": "passed",
                }
            )

        except ValueError as e:

            log.error(
                f"[CRITICAL] {validator.__name__}: {e}"
            )

            raise

    # =========================
    # WARNING VALIDATIONS
    # =========================
    for validator in WARNING_VALIDATIONS:

        try:

            warning_result = validator(df)

            if warning_result:

                results.extend(warning_result)

        except Exception as e:

            log.warning(
                f"[WARNING] {validator.__name__}: {e}"
            )

    return results