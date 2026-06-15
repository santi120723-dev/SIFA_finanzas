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

from src.validations.accounting_validations import (
    validate_codigo_cuenta,
    validate_nombre_cuenta,
    validate_fecha_datetime,
    validate_puc_structure,
    validate_valor_movimiento,
)

from src.validations.data_type_validations import (
    validate_data_types,
)

from src.validations.value_range_validations import (
    validate_value_ranges,
)

from src.validations.account_hierarchy_validations import (
    validate_account_hierarchy_consistency,
)

from src.validations.third_party_validations import (
    validate_matching_coverage,
    validate_ambiguous_third_parties,
    validate_unmatched_third_parties,
    validate_missing_documents,
    validate_orphan_third_parties,
)
log = logging.getLogger(__name__)


CRITICAL_VALIDATIONS = [
    validate_required_columns,
    validate_dates,
    validate_debe_haber,
    validate_codigo_cuenta,
    validate_nombre_cuenta,
    validate_fecha_datetime,
    validate_puc_structure,
    validate_account_hierarchy_consistency,
    validate_valor_movimiento,
    validate_data_types,
    validate_value_ranges,
]

WARNING_VALIDATIONS = [

    validate_nulls,
    validate_empty_dataframe,
    validate_duplicates,

    validate_matching_coverage,
    validate_ambiguous_third_parties,
    validate_unmatched_third_parties,

    validate_missing_documents,
    validate_orphan_third_parties,
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