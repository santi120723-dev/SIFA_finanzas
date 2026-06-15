from pathlib import Path

from src.orchestration.run_pipeline import (
    run_pipeline
)


def test_anonymized_dataset():

    _, anon_df, _, _, _ = run_pipeline(
        file_path=Path(
            r"data\bronze\accounting\libro_mayor_2025.xlsx"
        ),
        file_type="libro_mayor",
    )

    assert "tercero_id" in anon_df.columns

    assert "contacto" not in anon_df.columns

    assert anon_df["tercero_id"].notna().sum() > 0