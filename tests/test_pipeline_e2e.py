from pathlib import Path

from src.orchestration.run_pipeline import (
    run_pipeline
)


def test_pipeline_runs_successfully():

    cleaned_df, anon_df, validations, silver_path, metrics = run_pipeline(
        file_path=Path(
            r"data\bronze\accounting\libro_mayor_2025.xlsx"
        ),
        file_type="libro_mayor",
    )

    assert len(cleaned_df) > 0

    assert len(validations) > 0

    assert silver_path.exists()