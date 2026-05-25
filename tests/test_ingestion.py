from pathlib import Path

import pytest

from src.ingestion.extract import load_file

TEST_DATA_PATH = Path("tests/data")


def test_load_csv_valid() -> None:
    """
    Verifica carga correcta de CSV.
    """
    df = load_file(
        TEST_DATA_PATH / "bronze_test.csv"
    )

    assert df is not None
    assert df.shape[0] == 2


def test_load_excel_valid() -> None:
    """
    Verifica carga correcta de Excel.
    """
    df = load_file(
        TEST_DATA_PATH / "bronze_test.xlsx"
    )

    assert df is not None
    assert "Fecha" in df.columns


def test_load_missing_file() -> None:
    """
    Verifica archivo inexistente.
    """
    with pytest.raises(FileNotFoundError):
        load_file(
            Path("archivo_no_existe.xlsx")
        )


def test_load_invalid_format(tmp_path: Path) -> None:
    """
    Verifica formato inválido.
    """
    invalid_file = tmp_path / "invalid.txt"

    invalid_file.write_text("archivo invalido")

    with pytest.raises(ValueError):
        load_file(invalid_file)