import pandas as pd

def normalize_libro_mayor(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # limpiar espacios en columnas
    df.columns = df.columns.str.strip()

    # renombrar a esquema interno
    df = df.rename(columns={
        "Fecha de factura": "fecha",
        "Nombre de la cuenta": "cuenta",
        "Debe": "debe",
        "Haber": "haber"
    })

    return df