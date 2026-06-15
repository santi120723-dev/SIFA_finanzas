from pathlib import Path

import pandas as pd


def export_dimension(
    df: pd.DataFrame,
    output_path: Path,
):
    """
    Exporta dimensión a Parquet.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_parquet(
        output_path,
        index=False,
    )