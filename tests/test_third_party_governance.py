from pathlib import Path

from src.orchestration.run_pipeline import (
    run_pipeline
)


def test_third_party_matching_quality():

    _, _, _, _, metrics = run_pipeline(
        file_path=Path(
            r"data\bronze\accounting\libro_mayor_2025.xlsx"
        ),
        file_type="libro_mayor",
    )

    assert metrics["cobertura"] > 95

    assert metrics["encontrados"] > 10000