from pathlib import Path
import pandas as pd

TEST_DATA_DIR = Path("tests/data")


def create_valid_dataset() -> pd.DataFrame:
    """
    Dataset válido.
    """
    return pd.DataFrame(
        {
            "Fecha": [
                "2024-01-01",
                "2024-01-02",
            ],
            "Cuenta": ["1000", "2000"],
            "Debe": [100.0, 200.0],
            "Haber": [100.0, 200.0],
        }
    )


def create_missing_columns_dataset() -> pd.DataFrame:
    """
    Dataset con columna faltante.
    """
    return pd.DataFrame(
        {
            "Fecha": ["2024-01-01"],
            "Cuenta": ["1000"],
            "Debe": [100.0],
        }
    )


def create_unbalanced_dataset() -> pd.DataFrame:
    """
    Dataset desbalanceado.
    """
    return pd.DataFrame(
        {
            "Fecha": ["2024-01-01"],
            "Cuenta": ["1000"],
            "Debe": [100.0],
            "Haber": [50.0],
        }
    )


def save_datasets() -> None:
    """
    Guarda datasets dummy.
    """
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)

    valid_df = create_valid_dataset()
    missing_df = create_missing_columns_dataset()
    unbalanced_df = create_unbalanced_dataset()

    valid_df.to_csv(
        TEST_DATA_DIR / "bronze_test.csv",
        index=False,
    )

    valid_df.to_excel(
        TEST_DATA_DIR / "bronze_test.xlsx",
        index=False,
        engine="openpyxl",
    )

    missing_df.to_excel(
        TEST_DATA_DIR / "bronze_test_missing.xlsx",
        index=False,
        engine="openpyxl",
    )

    unbalanced_df.to_excel(
        TEST_DATA_DIR / "bronze_test_unbalanced.xlsx",
        index=False,
        engine="openpyxl",
    )

    print("Datasets dummy generados correctamente.")


if __name__ == "__main__":
    save_datasets()