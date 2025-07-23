import logging
from datetime import UTC, datetime
from pathlib import Path

# Creating logs directory
LOG_DIR = "logs"
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# File name with timestamp (ex: app_2025-06-22_13-02-30.log)
timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"{LOG_DIR}/app_{timestamp}.log"

# Configure logger
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[file_handler, console_handler],
)

logger = logging.getLogger(__name__)

log = logger
