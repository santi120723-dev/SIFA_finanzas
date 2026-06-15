import pandas as pd


def build_dim_terceros(
    df: pd.DataFrame
) -> pd.DataFrame:

    dim_df = (
        df[
            [
                "tercero_id",
                "tipo_tercero",
                "estado_matching",
            ]
        ]
        .dropna(subset=["tercero_id"])
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return dim_df