from pathlib import Path

import pandas as pd


def export_anonymized_dataset(
    df: pd.DataFrame,
    output_path: Path,
):
    """
    Exporta dataset anonimizado.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        output_path,
        index=False
    )