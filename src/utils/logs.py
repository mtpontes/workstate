import sys
import logging
from pathlib import Path
from datetime import UTC, datetime

# Directory where the .py or .exe is located
if getattr(sys, "frozen", False):
    # When packaged with PyInstaller
    BASE_DIR = Path(sys.executable).parent
else:
    # When running as a regular .py script
    BASE_DIR = Path.cwd()

# Create the logs folder relative to the executable or script location
LOG_DIR = BASE_DIR / "logs"
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
