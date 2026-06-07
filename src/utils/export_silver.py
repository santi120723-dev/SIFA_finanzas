from pathlib import Path

import pandas as pd

from src.logger import logger


def export_silver(
    df: pd.DataFrame,
    output_dir: Path,
    file_name: str,
) -> Path:
    """
    Exporta un DataFrame limpio a Silver Layer
    en formato Parquet.
    """

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        output_dir /
        f"{file_name}.parquet"
    )

    df.to_parquet(
        file_path,
        index=False,
    )

    logger.info(
        f"Dataset exportado a Silver: "
        f"{file_path}"
    )

    return file_path