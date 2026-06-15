import pandas as pd
import unicodedata
import re


def load_clientes(file_path: str) -> pd.DataFrame:
    """
    Carga la hoja de clientes desde el archivo maestro
    de terceros y asigna el rol CLIENTE.

    Objetivo:
    - Identificar terceros que participan como clientes.
    - Preparar la información para construir
      el maestro unificado de terceros.
    """

    clientes = pd.read_excel(
        file_path,
        sheet_name="Clientes",
        dtype=str
    )

    clientes["tipo_tercero"] = "CLIENTE"

    return clientes


def load_proveedores(file_path: str) -> pd.DataFrame:
    """
    Carga la hoja de proveedores desde el archivo maestro
    de terceros y asigna el rol PROVEEDOR.

    Objetivo:
    - Identificar terceros que participan como proveedores.
    - Preparar la información para construir
      el maestro unificado de terceros.
    """

    proveedores = pd.read_excel(
        file_path,
        sheet_name="Proveedores",
        dtype=str
    )

    proveedores["tipo_tercero"] = "PROVEEDOR"

    return proveedores

def normalize_name(name):
    """
    Normaliza un nombre para procesos de matching.

    Reglas:
    - Mayúsculas
    - Sin acentos
    - Sin puntuación
    - Sin espacios duplicados
    """

    if pd.isna(name):
        return None

    name = str(name).upper().strip()

    name = "".join(
        c for c in unicodedata.normalize("NFKD", name)
        if not unicodedata.combining(c)
    )

    name = re.sub(
        r"[.,;:]",
        "",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name


def normalize_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza todos los nombres del DataFrame
    para procesos de matching.
    """

    df = df.copy()

    df["nombre_normalizado"] = (
        df["nombre_real"]
        .apply(normalize_name)
    )

    return df


def build_master_terceros(file_path: str) -> pd.DataFrame:
    """
    Construye el maestro unificado de terceros.

    Proceso:
    1. Cargar clientes.
    2. Cargar proveedores.
    3. Estandarizar nombres de columnas.
    4. Consolidar ambas fuentes.
    5. Generar nombre_normalizado.
    6. Retornar maestro listo para validaciones.

    Objetivo:
    Crear una única fuente de verdad para la identificación
    de terceros dentro del proyecto.
    """

    clientes = load_clientes(file_path)
    proveedores = load_proveedores(file_path)

    clientes = clientes.rename(
        columns={
            "Nombre completo": "nombre_real",
            "Número de Identificación": "documento",
            "País": "pais"
        }
    )

    proveedores = proveedores.rename(
        columns={
            "Nombre completo": "nombre_real",
            "Número de Identificación": "documento",
            "País": "pais"
        }
    )

    master = pd.concat(
        [clientes, proveedores],
        ignore_index=True
    )

    master = normalize_names(master)

    return master


def find_ambiguous_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detecta nombres normalizados asociados
    a múltiples documentos distintos.

    Estos casos no deben ser enriquecidos
    automáticamente porque generan ambigüedad.

    Ejemplo:

    JUAN DAVID GOMEZ
    -> CC 1001

    JUAN DAVID GOMEZ
    -> CC 2002

    Resultado:
    El nombre queda marcado como ambiguo
    y requiere revisión manual.
    """

    ambiguos = (
        df.groupby("nombre_normalizado")["documento"]
        .nunique()
        .reset_index()
    )

    ambiguos = ambiguos[
        ambiguos["documento"] > 1
    ]

    return ambiguos

def classify_names(df: pd.DataFrame) -> dict:
    """
    Clasifica los nombres del maestro de terceros según
    su nivel de confiabilidad para procesos de matching.

    Categorías:

    UNICO:
    - El nombre normalizado está asociado
      a un único documento.
    - Puede utilizarse para matching automático.

    AMBIGUO:
    - El nombre normalizado está asociado
      a múltiples documentos.
    - Requiere revisión manual antes de asignar
      un documento.

    INVALIDO:
    - Nombre vacío o documento vacío.
    - No debe participar en procesos de matching.

    Resultado:
    Retorna métricas resumidas para monitorear
    la calidad del maestro de terceros.
    """

    df = df.copy()

    # Registros inválidos
    invalidos = df[
        (df["nombre_normalizado"].isna()) |
        (df["nombre_normalizado"] == "") |
        (df["documento"].isna()) |
        (df["documento"] == "")
    ]

    # Conteo de documentos únicos por nombre
    conteo_documentos = (
        df.groupby("nombre_normalizado")["documento"]
        .nunique()
    )

    # Nombres ambiguos
    ambiguos = conteo_documentos[
        conteo_documentos > 1
    ]

    # Nombres únicos
    unicos = conteo_documentos[
        conteo_documentos == 1
    ]

    resumen = {

        # Universo de registros
        "total_registros": len(df),

        # Universo de nombres distintos
        "total_nombres": len(conteo_documentos),

        # Clasificación
        "nombres_unicos": len(unicos),
        "nombres_ambiguos": len(ambiguos),
        "registros_invalidos": len(invalidos),

        # Métricas de matching
        "matching_automatico_posible": len(unicos),
        "matching_manual_requerido": len(ambiguos),

        # Porcentajes sobre nombres distintos
        "porcentaje_unicos": round(
            (len(unicos) / len(conteo_documentos)) * 100,
            2
        ) if len(conteo_documentos) > 0 else 0,

        "porcentaje_ambiguos": round(
            (len(ambiguos) / len(conteo_documentos)) * 100,
            2
        ) if len(conteo_documentos) > 0 else 0,

        # Porcentaje sobre registros
        "porcentaje_invalidos": round(
            (len(invalidos) / len(df)) * 100,
            2
        ) if len(df) > 0 else 0
    }

    return resumen

def print_classification_summary(resumen: dict) -> None:
    """
    Imprime un resumen de calidad del maestro de terceros.
    """

    print("\n=== RESUMEN MAESTRO DE TERCEROS ===")

    print(
        f"Total registros: "
        f"{resumen['total_registros']:,}"
    )

    print(
        f"Total nombres distintos: "
        f"{resumen['total_nombres']:,}"
    )

    print(
        f"Nombres únicos: "
        f"{resumen['nombres_unicos']:,} "
        f"({resumen['porcentaje_unicos']}%)"
    )

    print(
        f"Nombres ambiguos: "
        f"{resumen['nombres_ambiguos']:,} "
        f"({resumen['porcentaje_ambiguos']}%)"
    )

    print(
        f"Registros inválidos: "
        f"{resumen['registros_invalidos']:,} "
        f"({resumen['porcentaje_invalidos']}%)"
    )

    print(
        f"Matching automático posible: "
        f"{resumen['matching_automatico_posible']:,}"
    )

    print(
        f"Matching manual requerido: "
        f"{resumen['matching_manual_requerido']:,}"
    )