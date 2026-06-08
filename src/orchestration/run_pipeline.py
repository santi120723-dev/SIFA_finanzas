from pathlib import Path

from src.ingestion.extract import (
    load_libro_mayor,
)

from src.utils.cleaning import clean_dataframe
from src.utils.export_silver import export_silver
from src.validations.validation_runner import (
    run_validations,
)

from src.validations.validation_summary import (
    validation_summary,
)


def run_pipeline(
    file_path: Path,
    file_type: str = None,
):

    raw_df = load_libro_mayor()

    cleaned_df = clean_dataframe(
        raw_df,
        file_type=file_type,
    )

    print("\n========== COLUMNAS SILVER ==========")

    print(
        cleaned_df.columns.tolist()
    )

    print("\n========== TIPOS DE DATOS ==========")

    print(
        cleaned_df.dtypes
    )

    print("\n========== SILVER ACCOUNTING ==========")

    print(
        cleaned_df[
            [
                "codigo_cuenta",
                "nombre_cuenta",
                "clase",
                "grupo",
                "cuenta_puc",
                "subcuenta",
                "anio",
                "mes",
                "trimestre",
                "periodo_contable",
                "detalle_movimiento",
                "fecha",
            ]
        ].head(40)
    )

    print("\n========== JERARQUIA PUC ==========")

    print(
        cleaned_df[
            [
                "codigo_cuenta",
                "clase",
                "grupo",
                "cuenta_puc",
                "subcuenta",
            ]
        ]
        .drop_duplicates()
        .head(20)
    )

    print("\n========== PERIODOS CONTABLES ==========")

    print(
        cleaned_df[
            [
                "anio",
                "mes",
                "trimestre",
                "periodo_contable",
            ]
        ]
        .drop_duplicates()
        .sort_values(
            by=[
                "anio",
                "mes",
            ]
        )
        .head(20)
    )

    print("\n========== MOVIMIENTOS SIN CODIGO_CUENTA ==========")

    print(
        cleaned_df[
            cleaned_df[
                "codigo_cuenta"
            ].isna()
        ][
            [
                "codigo_cuenta",
                "nombre_cuenta",
                "detalle_movimiento",
                "valor_movimiento",
                "fecha",
            ]
        ].head(20)
    )

    print("\n========== TOTAL SIN CODIGO_CUENTA ==========")

    print(
        cleaned_df[
            "codigo_cuenta"
        ]
        .isna()
        .sum()
    )

    print("\n========== MOVIMIENTOS SIN NOMBRE_CUENTA ==========")

    print(
        cleaned_df[
            cleaned_df[
                "nombre_cuenta"
            ].isna()
        ][
            [
                "codigo_cuenta",
                "nombre_cuenta",
                "detalle_movimiento",
                "fecha",
            ]
        ].head(20)
    )

    print("\n========== TOTAL SIN NOMBRE_CUENTA ==========")

    print(
        cleaned_df[
            "nombre_cuenta"
        ]
        .isna()
        .sum()
    )

    validation_results = run_validations(
        cleaned_df
    )

    validation_summary(
        validation_results
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