import logging

log = logging.getLogger(__name__)


def validate_matching_coverage(df):
    """
    WARNING si la cobertura de matching
    es inferior al 95%.
    """

    if (
        "contacto" not in df.columns
        or "estado_matching" not in df.columns
    ):
        return []

    terceros = (
        df[
            ["contacto", "estado_matching"]
        ]
        .drop_duplicates()
    )

    total = len(terceros)

    if total == 0:
        return []

    encontrados = (
        terceros["estado_matching"]
        .eq("MATCH")
        .sum()
    )

    cobertura = (
        encontrados / total
    ) * 100

    if cobertura < 95:

        log.warning(
            f"Cobertura de matching baja: {cobertura:.2f}%"
        )

        return [
            {
                "severity": "WARNING",
                "message": (
                    f"Cobertura de matching inferior al 95% "
                    f"({cobertura:.2f}%)"
                )
            }
        ]

    return []


def validate_ambiguous_third_parties(df):
    """
    WARNING si más del 2% de terceros
    son ambiguos.
    """

    if (
        "contacto" not in df.columns
        or "estado_matching" not in df.columns
    ):
        return []

    terceros = (
        df[
            ["contacto", "estado_matching"]
        ]
        .drop_duplicates()
    )

    total = len(terceros)

    if total == 0:
        return []

    ambiguos = (
        terceros["estado_matching"]
        .eq("AMBIGUO")
        .sum()
    )

    porcentaje = (
        ambiguos / total
    ) * 100

    if porcentaje > 2:

        log.warning(
            f"Terceros ambiguos: {porcentaje:.2f}%"
        )

        return [
            {
                "severity": "WARNING",
                "message": (
                    f"{ambiguos} terceros ambiguos "
                    f"({porcentaje:.2f}%)"
                )
            }
        ]

    return []


def validate_unmatched_third_parties(df):
    """
    WARNING si más del 5% de terceros
    no fueron encontrados.
    """

    if (
        "contacto" not in df.columns
        or "estado_matching" not in df.columns
    ):
        return []

    terceros = (
        df[
            ["contacto", "estado_matching"]
        ]
        .drop_duplicates()
    )

    total = len(terceros)

    if total == 0:
        return []

    no_encontrados = (
        terceros["estado_matching"]
        .eq("NO_ENCONTRADO")
        .sum()
    )

    porcentaje = (
        no_encontrados / total
    ) * 100

    if porcentaje > 5:

        log.warning(
            f"No encontrados: {porcentaje:.2f}%"
        )

        return [
            {
                "severity": "WARNING",
                "message": (
                    f"{no_encontrados} terceros no encontrados "
                    f"({porcentaje:.2f}%)"
                )
            }
        ]

    return []

def validate_missing_documents(df):
    """
    WARNING si existen terceros
    sin documento.
    """

    required = {
        "contacto",
        "documento"
    }

    if not required.issubset(df.columns):
        return []

    missing = (
        df[
            df["contacto"].notna()
            & df["documento"].isna()
        ]
        ["contacto"]
        .nunique()
    )

    if missing > 0:

        return [
            {
                "severity": "WARNING",
                "message": (
                    f"{missing} terceros sin documento"
                )
            }
        ]

    return []

def validate_orphan_third_parties(df):
    """
    WARNING si existen terceros
    sin clasificación.
    """

    required = {
        "contacto",
        "tipo_tercero"
    }

    if not required.issubset(df.columns):
        return []

    orphan = (
        df[
            df["contacto"].notna()
            & df["tipo_tercero"].isna()
        ]
        ["contacto"]
        .nunique()
    )

    if orphan > 0:

        return [
            {
                "severity": "WARNING",
                "message": (
                    f"{orphan} terceros sin tipo_tercero"
                )
            }
        ]

    return []
