import sys
import logging
from pathlib import Path
from datetime import UTC, datetime

from src.constants.constants import WORKSTATE_DIR

# Create the logs folder in ~/.workstate/logs
LOG_DIR = WORKSTATE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Generate log filename with timestamp
timestamp = datetime.now(UTC).astimezone().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = LOG_DIR / f"app_{timestamp}.log"

# Configure the logger
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[file_handler, console_handler],
)

logger = logging.getLogger(__name__)
log = logger
