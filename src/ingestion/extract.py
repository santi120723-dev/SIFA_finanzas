import pandas as pd

from pathlib import Path
from typing import Optional

from src.logger import logger

from src.config import (
    LIBRO_MAYOR,
    MOVIMIENTOS_INVENTARIO,
    ORDENES_FABRICACION
)

# Columnas mínimas esperadas por tipo de archivo
REQUIRED_COLUMNS = {
    "libro_mayor": ["Fecha", "Cuenta", "Debe", "Haber"],
    "inventario": ["Codigo", "Cantidad", "Costo"],
    "ordenes": ["ID_Orden", "Estado"]
}

# =========================
# FUNCIÓN GENERAL
# =========================

def load_file(
    file_path: Path,
    file_type: Optional[str] = None
) -> Optional[pd.DataFrame]:

    try:

        # =========================
        # VALIDAR EXISTENCIA
        # =========================

        if not file_path.exists():

            raise FileNotFoundError(
                f"No existe: {file_path}"
            )

        extension = (
            file_path.suffix.lower()
        )

        # =========================
        # LEER ARCHIVO
        # =========================

        if extension == ".xlsx":

            df = pd.read_excel(
                file_path,
                engine="openpyxl"
            )

        elif extension == ".csv":

            df = pd.read_csv(
                file_path,
                encoding="utf-8"
            )

        elif extension == ".txt":

            df = pd.read_csv(
                file_path,
                sep="\t",
                encoding="utf-8"
            )

        else:

            raise ValueError(
                f"Formato no soportado: {extension}"
            )

        # =========================
        # VALIDAR VACÍO
        # =========================

        if df.empty:

            raise ValueError(
                f"Archivo vacío: {file_path.name}"
            )

        # =========================
        # VALIDAR COLUMNAS (Práctica de mañana)
        # =========================
        if file_type in REQUIRED_COLUMNS:
            missing = [col for col in REQUIRED_COLUMNS[file_type] if col not in df.columns]
            if missing:
               
                raise ValueError(
                    f"Columnas faltantes en {file_path.name}: {missing}. "
                    f"Columnas encontradas: {list(df.columns)}"
                )

        logger.info(
            (
                f"Archivo cargado: "
                f"{file_path.name} | "
                f"Filas: {df.shape[0]} | "
                f"Columnas: {df.shape[1]}"
            )
        )

        return df

    except Exception as e:

        logger.error(
            f"Error cargando {file_path.name}: {e}"
        )

        return None


# =========================
# FUNCIONES ESPECÍFICAS
# =========================

def load_libro_mayor() -> Optional[pd.DataFrame]:

    return load_file(LIBRO_MAYOR)


def load_movimientos_inventario() -> Optional[pd.DataFrame]:

    return load_file(
        MOVIMIENTOS_INVENTARIO
    )


def load_ordenes_fabricacion() -> Optional[pd.DataFrame]:

    return load_file(
        ORDENES_FABRICACION
    )