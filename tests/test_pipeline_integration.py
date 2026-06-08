from pathlib import Path

import pandas as pd

from src.utils.cleaning import clean_dataframe
from src.validations.validation_runner import run_validations
from src.utils.export_silver import export_silver


def test_pipeline_integration(tmp_path):

    raw_df = pd.DataFrame(
        {
            "cdigo": [110505, None],
            "cuenta": [
                "Caja General",
                "Movimiento prueba",
            ],
            "fecha": [
                None,
                "01/01/2025",
            ],
            "contacto": [
                None,
                "Cliente A",
            ],
            "debe": [
                1000,
                1000,
            ],
            "haber": [
                1000,
                1000,
            ],
            "valor_final": [
                0,
                0,
            ],
        }
    )

    cleaned_df = clean_dataframe(
        raw_df,
        file_type="libro_mayor",
    )

    validation_results = run_validations(
        cleaned_df
    )

    silver_path = export_silver(
        df=cleaned_df,
        output_dir=tmp_path,
        file_name="test_silver",
    )

    assert len(cleaned_df) > 0

    assert len(validation_results) > 0

    assert silver_path.exists()