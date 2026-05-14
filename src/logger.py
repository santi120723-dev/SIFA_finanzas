import logging

from src.config import BASE_DIR

# =========================
# CARPETA LOGS
# =========================

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)

# =========================
# ARCHIVO LOG
# =========================

LOG_FILE = LOG_DIR / "pipeline.log"

# =========================
# CONFIG LOGGER
# =========================

logging.basicConfig(
    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),

    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),

        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)