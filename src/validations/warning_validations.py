import logging

log = logging.getLogger(__name__)


def validate_nulls(df):
    """Devuelve [] si no hay nulos, o una lista de mensajes 
    si superan el umbral."""

    if df.isnull().any().any():
        null_pct = df.isnull().sum().sum() / df.size
        if null_pct > 0.05:
            cols = df.columns[df.isnull().any()].tolist()

            log.warning(
                f"Nulls in columns {cols}: {null_pct:.2%}"
            )

            return [
                {
                    "severity": "WARNING",
                    "message": (
                        f"Nulls en {len(cols)} columnas (>5%)"
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