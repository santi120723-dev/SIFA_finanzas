import pandas as pd


def generate_third_party_mapping(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Construye tabla única de terceros
    para anonimización.
    """

    terceros = (
        df[
           [
            "contacto",
            "documento"
           ]
        ]
        .dropna(subset=["contacto"])
        .drop_duplicates()
        .reset_index(drop=True)
    )

    terceros["tercero_id"] = [
        f"TERCERO_{i:06d}"
        for i in range(
            1,
            len(terceros) + 1
        )
    ]

    return terceros[
        [
            "tercero_id",
            "documento",
            "contacto"
        ]
    ]

def anonymize_third_parties(
    df: pd.DataFrame,
    mapping_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Reemplaza información real
    por identificadores anonimizados.
    """

    df = df.copy()

    mapping_df = (
        mapping_df[
            mapping_df["contacto"].notna()
        ]
        .copy()
    )

    df = df.merge(
        mapping_df,
        on=[
            "contacto",
            "documento"
        ],
        how="left"
    )

    df.loc[
        df["contacto"].isna(),
        "tercero_id"
    ] = None

    df = df.drop(
        columns=[
        "contacto",
        "documento",
    ],
        errors="ignore"
    )

    return df

from pathlib import Path


def export_mapping(
    mapping_df: pd.DataFrame,
    output_path: Path
):
    """
    Exporta tabla de trazabilidad.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    mapping_df.to_parquet(
        output_path,
        index=False
    )