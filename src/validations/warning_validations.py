import logging

log = logging.getLogger(__name__)


def validate_nulls(df):
    """
    Detecta nulos relevantes para calidad de datos.

    Algunas columnas pueden contener nulos
    válidos por diseño y se excluyen
    del cálculo.
    """

    ALLOWED_NULL_COLUMNS = [
        "contacto",
        "documento",
        "tipo_tercero",
        "estado_matching",
        "cdigo",
    ]

    columnas_a_validar = [
        col
        for col in df.columns
        if col not in ALLOWED_NULL_COLUMNS
    ]

    df_validacion = df[
        columnas_a_validar
    ]

    if df_validacion.isnull().any().any():

        null_pct = (
            df_validacion.isnull()
            .sum()
            .sum()
            / df_validacion.size
        )

        if null_pct > 0.05:

            cols = (
                df_validacion.columns[
                    df_validacion.isnull().any()
                ]
                .tolist()
            )

            log.warning(
                f"Nulls en columnas {cols}: "
                f"{null_pct:.2%}"
            )

            return [
                {
                    "severity": "WARNING",
                    "message": (
                        f"Nulls en "
                        f"{len(cols)} columnas (>5%)"
                    )
                }
            ]

    return []


def validate_empty_dataframe(df):
    """Marca como WARNING si el DataFrame está vacío después de la 
    carga."""
    if df.empty:

        return [
            {
                "severity": "WARNING",
                "message": (
                    "DataFrame vacío después de la ingestión"
                )
            }
        ]
    return []

def validate_duplicates(df):
    """
    Detecta registros duplicados y genera un WARNING.
    """

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        log.warning(
            f"Duplicados detectados: {duplicate_count}"
        )

        return [
            {
                "severity": "WARNING",
                "message": (
                    f"{duplicate_count} registros duplicados detectados"
                )
            }
        ]

    return []