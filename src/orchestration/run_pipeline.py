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

from src.dimensions.terceros import (
    build_master_terceros
)

from src.dimensions.enrichment import (
    enrich_third_parties,
    calculate_matching_metrics
)

from src.privacy.anonymization import (
    generate_third_party_mapping,
    anonymize_third_parties,
    export_mapping
)

from src.privacy.export_anonymized import (
    export_anonymized_dataset
)

from src.dimensions.dim_terceros import (
    build_dim_terceros
)

from src.dimensions.export_dimensions import (
    export_dimension
)

from src.config import (
    TERCEROS_MASTER,
    THIRD_PARTY_MAPPING,
    ANONYMIZED_ACCOUNTING,
    DIM_TERCEROS,
)

def run_pipeline(
    file_path: Path,
    file_type: str = None,
):

    # ==========================
    # LOAD
    # ==========================

    raw_df = load_libro_mayor()

    # ==========================
    # CLEANING + TRANSFORMATIONS
    # ==========================

    cleaned_df = clean_dataframe(
        raw_df,
        file_type=file_type,
    )

    # ==========================
    # ENRIQUECIMIENTO TERCEROS
    # ==========================

    master_terceros = build_master_terceros(
        TERCEROS_MASTER
    )

    cleaned_df = enrich_third_parties(
        cleaned_df,
        master_terceros,
        third_party_column="contacto"
    )

    # ==========================
    # ANONIMIZACION
    # ==========================

    mapping_df = generate_third_party_mapping(
        cleaned_df
    )

    export_mapping(
        mapping_df,
        THIRD_PARTY_MAPPING
    )

    anon_df = anonymize_third_parties(
        cleaned_df,
        mapping_df
    )

    export_anonymized_dataset(
        anon_df,
        ANONYMIZED_ACCOUNTING
    )

    print(
        "\n========== DATASET ANONIMIZADO =========="
    )

    print(
        anon_df.head(20)
    )

    # ==========================
    # DIMENSION TERCEROS
    # ==========================

    print(anon_df.columns.tolist())

    dim_terceros = build_dim_terceros(
        anon_df
    )

    export_dimension(
        dim_terceros,
        DIM_TERCEROS
    )

    print(
        "\n========== DIMENSION TERCEROS =========="
    )

    print(
        dim_terceros.head(20)
    )

    print(
        "\n========== TOTAL TERCEROS =========="
    )

    print(
        len(dim_terceros)
    )

    print(
        "\n========== DIMENSION EXPORTADA =========="
    )

    print(
        DIM_TERCEROS
    )

    matching_metrics = calculate_matching_metrics(
        cleaned_df[
            [
                "contacto",
                "estado_matching"
            ]
        ]
        .drop_duplicates()
    )

    print(
        "\n========== MATCHING TERCEROS =========="
    )

    print(
        f"""
Cobertura Matching: {matching_metrics['cobertura']}%

Total terceros: {matching_metrics['total_terceros']}
Encontrados: {matching_metrics['encontrados']}
Ambiguos: {matching_metrics['ambiguos']}
No encontrados: {matching_metrics['no_encontrados']}
"""
    )

    print(
        "\n========== ENRIQUECIMIENTO =========="
    )

    print(
        cleaned_df[
            [
                "contacto",
                "documento",
                "tipo_tercero",
                "estado_matching"
            ]
        ]
        .dropna(subset=["contacto"])
        .head(20)
        .to_string()
    )

    print(
        "\n========== COLUMNAS SILVER =========="
    )

    print(
        cleaned_df.columns.tolist()
    )

    print(
        "\n========== TIPOS DE DATOS =========="
    )

    print(
        cleaned_df.dtypes
    )

    print(
        "\n========== COLUMNAS TERCEROS =========="
    )

    print(
        cleaned_df[
            [
                "contacto",
                "documento",
                "tipo_tercero",
                "estado_matching"
            ]
        ]
        .head(20)
        .to_string()
    )

    # ==========================
    # VALIDACIONES
    # ==========================

    validation_results = run_validations(
        cleaned_df
    )

    validation_summary(
        validation_results
    )

    # ==========================
    # EXPORTA SILVER
    # ==========================

    silver_path = export_silver(
        df=cleaned_df,
        output_dir=Path(
            "data/silver/accounting"
        ),
        file_name=file_path.stem,
    )

    return (
        cleaned_df,
        anon_df,
        validation_results,
        silver_path,
        matching_metrics,
    )