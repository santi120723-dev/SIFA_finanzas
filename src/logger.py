import logging
from src.config import BASE_DIR

# ----------------------------------------------------------------------
# Directorio y archivo de log
# ----------------------------------------------------------------------
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)                     # crea carpeta si no existe
LOG_FILE = LOG_DIR / "pipeline.log"

# ----------------------------------------------------------------------
# Logger específico del proyecto (evita usar el root logger)
# ----------------------------------------------------------------------
logger = logging.getLogger("etl_pipeline")

# Configuramos el logger solo la primera vez que se importe
if not logger.handlers:
    logger.setLevel(logging.INFO)

    _formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    _file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    _file_handler.setFormatter(_formatter)

    _stream_handler = logging.StreamHandler()
    _stream_handler.setFormatter(_formatter)

    logger.addHandler(_file_handler)
    logger.addHandler(_stream_handler)

    # Evita que los mensajes suban al root logger (previene doble salida)
    logger.propagate = False