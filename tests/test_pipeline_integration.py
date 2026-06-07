from src.config import LIBRO_MAYOR

from src.orchestration.run_pipeline import (
    run_pipeline
)

cleaned_df, validation_results, silver_path = run_pipeline(
    file_path=LIBRO_MAYOR,
    file_type="libro_mayor",
)

print("Archivo Silver generado:")
print(silver_path)

print("\nResultados de validación:")
print(validation_results)

cleaned_df.head()