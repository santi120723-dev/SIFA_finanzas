import pandas as pd
from pathlib import Path

from src.config import (
    LIBRO_MAYOR,
    MOVIMIENTOS_INVENTARIO,
    ORDENES_FABRICACION_2025
)


def load_file(file_path):
    """
    Carga archivos financieros en distintos formatos.

    Soporta:
    - Excel (.xlsx, .xls)
    - CSV (.csv)
    - TXT (.txt)

    Returns:
        pd.DataFrame | None
    """

    try:
        # =========================
        # VALIDAR EXISTENCIA
        # =========================
        if not file_path.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo: {file_path}"
            )

        # =========================
        # DETECTAR EXTENSIÓN
        # =========================
        extension = file_path.suffix.lower()

        formatos_validos = [
            ".xlsx",
            ".xls",
            ".csv",
            ".txt"
        ]

        if extension not in formatos_validos:
            raise ValueError(
                f"Formato no soportado: {extension}"
            )

        # =========================
        # LEER SEGÚN FORMATO
        # =========================

        # Excel
        if extension in [".xlsx", ".xls"]:

            df = pd.read_excel(
                file_path,
                header=None,
                engine="openpyxl"
            )

        # CSV
        elif extension == ".csv":

            df = pd.read_csv(
                file_path,
                header=None,
                encoding="utf-8"
            )

        # TXT
        elif extension == ".txt":

            df = pd.read_csv(
                file_path,
                header=None,
                sep="\t",
                encoding="utf-8"
            )

        # =========================
        # VALIDAR VACÍO
        # =========================
        if df.empty:
            raise ValueError(
                f"El archivo está vacío: {file_path.name}"
            )

        print(f"[OK] Archivo cargado: {file_path.name}")
        print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

        return df

    # =========================
    # MANEJO DE ERRORES
    # =========================

    except FileNotFoundError as e:
        print(f"[ERROR ARCHIVO] {e}")

    except PermissionError:
        print(
            f"[ERROR PERMISOS] No se puede acceder a: {file_path.name}"
        )

    except UnicodeDecodeError:
        print(
            f"[ERROR ENCODING] Problema de codificación en: {file_path.name}"
        )

    except ValueError as e:
        print(f"[ERROR VALIDACIÓN] {e}")

    except ImportError:
        print(
            "[ERROR DEPENDENCIA] Falta instalar openpyxl"
        )

    except Exception as e:
        print(f"[ERROR INESPERADO] {e}")

    return None


# =========================
# FUNCIONES ESPECÍFICAS
# =========================

def load_libro_mayor():
    return load_file(LIBRO_MAYOR)


def load_movimientos_inventario():
    return load_file(MOVIMIENTOS_INVENTARIO)


def load_ordenes_fabricacion():
    return load_file(ORDENES_FABRICACION)