from pathlib import Path

from src.ingestion.extract import (
    load_file,
    load_libro_mayor,
)

from src.utils.cleaning import clean_dataframe
from src.utils.export_silver import export_silver
from src.validations.validation_runner import (
    run_validations,
)


def run_pipeline(
    file_path: Path,
    file_type: str = None,
):

    raw_df = load_libro_mayor()

    print("\n========== RAW LIBRO MAYOR ==========")

    print(
        raw_df.iloc[:40]
    )

    cleaned_df = clean_dataframe(
        raw_df,
        file_type=file_type,
    )

    print("\n========== MUESTRA SILVER ==========")

    print(
        cleaned_df[
            ["cdigo", "cuenta", "fecha"]
        ].head(30)
    )

    print("\n========== MOVIMIENTOS SIN CODIGO ==========")

    print(
        cleaned_df[
            cleaned_df["cdigo"].isna()
        ][
            ["cdigo", "cuenta", "fecha"]
        ].head(30)
    )

    print("\n========== TOTAL MOVIMIENTOS SIN CODIGO ==========")

    print(
        cleaned_df["cdigo"].isna().sum()
    )

    validation_results = run_validations(
        cleaned_df
    )

    silver_path = export_silver(
        df=cleaned_df,
        output_dir=Path(
            "data/silver/accounting"
        ),
        file_name=file_path.stem,
    )

    return (
        cleaned_df,
        validation_results,
        silver_path,
    )