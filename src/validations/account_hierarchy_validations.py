import pandas as pd

from src.logger import logger


def validate_account_hierarchy_consistency(
    df: pd.DataFrame,
) -> bool:
    """
    Verifica que la jerarquía PUC
    coincida con codigo_cuenta.
    """

    required_columns = [
        "codigo_cuenta",
        "clase",
        "grupo",
        "cuenta_puc",
        "subcuenta",
    ]

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Columnas faltantes para validar "
            f"jerarquía PUC: {missing}"
        )

    for idx, row in df.iterrows():

        if pd.isna(
            row["codigo_cuenta"]
        ):
            continue

        codigo = str(
            row["codigo_cuenta"]
        )

        expected_clase = codigo[:1]
        expected_grupo = codigo[:2]
        expected_cuenta = codigo[:4]
        expected_subcuenta = codigo[:6]

        if str(row["clase"]) != expected_clase:

            raise ValueError(
                f"Clase incorrecta "
                f"en fila {idx}"
            )

        if str(row["grupo"]) != expected_grupo:

            raise ValueError(
                f"Grupo incorrecto "
                f"en fila {idx}"
            )

        if str(row["cuenta_puc"]) != expected_cuenta:

            raise ValueError(
                f"Cuenta PUC incorrecta "
                f"en fila {idx}"
            )

        if str(row["subcuenta"]) != expected_subcuenta:

            raise ValueError(
                f"Subcuenta incorrecta "
                f"en fila {idx}"
            )

    logger.info(
        "Validación jerarquía PUC completada."
    )

    return True