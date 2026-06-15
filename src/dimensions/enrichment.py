import pandas as pd
from src.dimensions.terceros import normalize_name

def extract_unique_third_parties(
    libro_mayor: pd.DataFrame,
    third_party_column: str
) -> pd.DataFrame:
    """
    Extrae terceros únicos del Libro Mayor.

    Parámetros
    ----------
    libro_mayor : pd.DataFrame
        Libro Mayor cargado en memoria.

    third_party_column : str
        Nombre de la columna donde viene el tercero.

    Retorna
    -------
    pd.DataFrame
        DataFrame con terceros únicos.
    """

    terceros = (
        libro_mayor[[third_party_column]]
        .dropna()
        .drop_duplicates()
        .rename(
            columns={
                third_party_column: "nombre_real"
            }
        )
    )

    return terceros


def match_third_parties(
    terceros_df: pd.DataFrame,
    master_terceros: pd.DataFrame
) -> pd.DataFrame:
    """
    Realiza matching entre terceros encontrados
    en Libro Mayor y el maestro de terceros.

    Estados posibles
    ----------------
    MATCH
        El nombre está asociado a un único documento.

    AMBIGUO
        El nombre está asociado a múltiples documentos.

    NO_ENCONTRADO
        El nombre no existe en el maestro.

    Caso especial
    -------------
    Si un mismo documento aparece como
    CLIENTE y PROVEEDOR, se clasifica como:

    CLIENTE_PROVEEDOR

    Retorna
    -------
    pd.DataFrame

    Columnas:
    - nombre_real
    - documento
    - tipo_tercero
    - estado_matching
    """

    terceros_df = terceros_df.copy()

    terceros_df["nombre_normalizado"] = (
        terceros_df["nombre_real"]
        .apply(normalize_name)
    )

    master_tmp = master_terceros.copy()

    conteo_documentos = (
        master_tmp.groupby(
            "nombre_normalizado"
        )["documento"]
        .nunique()
    )

    resultado = []

    for _, row in terceros_df.iterrows():

        nombre = row["nombre_normalizado"]

        # No existe en maestro
        if nombre not in conteo_documentos.index:

            resultado.append({
                "nombre_real": row["nombre_real"],
                "documento": None,
                "tipo_tercero": None,
                "estado_matching": "NO_ENCONTRADO"
            })

            continue

        # Existe pero asociado
        # a múltiples documentos
        if conteo_documentos[nombre] > 1:

            resultado.append({
                "nombre_real": row["nombre_real"],
                "documento": None,
                "tipo_tercero": None,
                "estado_matching": "AMBIGUO"
            })

            continue

        matches = master_tmp[
            master_tmp["nombre_normalizado"] == nombre
        ]

        documento = (
            matches["documento"]
            .iloc[0]
        )

        roles = sorted(
            matches["tipo_tercero"]
            .drop_duplicates()
            .tolist()
        )

        tipo_tercero = "_".join(roles)

        resultado.append({
            "nombre_real": row["nombre_real"],
            "documento": documento,
            "tipo_tercero": tipo_tercero,
            "estado_matching": "MATCH"
        })

    return pd.DataFrame(resultado)

def enrich_third_parties(
    df: pd.DataFrame,
    master_terceros: pd.DataFrame,
    third_party_column: str
) -> pd.DataFrame:
    """
    Enriquece un dataset transaccional con información
    proveniente del maestro de terceros.

    Proceso:
    1. Extraer terceros únicos.
    2. Ejecutar matching.
    3. Hacer merge contra el dataset original.

    Resultado:
    Agrega:

    - documento
    - tipo_tercero
    - estado_matching
    """

    df = df.copy()

    terceros = extract_unique_third_parties(
        df,
        third_party_column
    )

    matched = match_third_parties(
        terceros,
        master_terceros
    )

    enriched = df.merge(
        matched,
        left_on=third_party_column,
        right_on="nombre_real",
        how="left"
    )

    enriched = enriched.drop(
        columns=["nombre_real"],
        errors="ignore"
    )

    return enriched

def calculate_matching_metrics(
    matched_df: pd.DataFrame
) -> dict:
    """
    Calcula métricas de cobertura
    del proceso de matching.
    """

    total = len(matched_df)

    encontrados = (
        matched_df["estado_matching"]
        .eq("MATCH")
        .sum()
    )

    ambiguos = (
        matched_df["estado_matching"]
        .eq("AMBIGUO")
        .sum()
    )

    no_encontrados = (
        matched_df["estado_matching"]
        .eq("NO_ENCONTRADO")
        .sum()
    )

    return {
        "total_terceros": total,
        "encontrados": encontrados,
        "ambiguos": ambiguos,
        "no_encontrados": no_encontrados,
        "cobertura": round(
            encontrados / total * 100,
            2
        ) if total > 0 else 0
    }

def enrich_third_parties(
    df: pd.DataFrame,
    master_terceros: pd.DataFrame,
    third_party_column: str
) -> pd.DataFrame:
    """
    Enriquece un dataset con información
    proveniente del maestro de terceros.

    Agrega:

    - documento
    - tipo_tercero
    - estado_matching
    """

    df = df.copy()

    terceros = extract_unique_third_parties(
        df,
        third_party_column
    )

    matched = match_third_parties(
        terceros,
        master_terceros
    )

    enriched = df.merge(
        matched,
        left_on=third_party_column,
        right_on="nombre_real",
        how="left"
    )

    enriched = enriched.drop(
        columns=["nombre_real"],
        errors="ignore"
    )

    return enriched