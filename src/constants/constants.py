import sys
from pathlib import Path
from typing import Final

def _get_version() -> str:
    """Extrai a versão do pacote instalado ou do pyproject.toml local."""
    try:
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata
        return metadata.version("workstate")
    except Exception:
        # Fallback para desenvolvimento local via pyproject.toml
        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            import re
            content = pyproject_path.read_text(encoding="utf-8")
            match = re.search(r'version = "([^"]+)"', content)
            if match:
                return match.group(1)
        return "0.0.0"


VERSION: Final[str] = _get_version()

ACCESS_KEY_ID: Final[str] = "access_key_id"
SECRET_ACCESS_KEY: Final[str] = "secret_access_key"
BUCKET_NAME: Final[str] = "bucket_name"
REGION: Final[str] = "region"
DEFAULT_AWS_REGION: Final[str] = "us-east-1"

IGNORE_FILE: Final[str] = ".workstateignore"
DOT_ZIP: Final[str] = ".zip"
DOWNLOADS: Final[str] = "downloads"

WRITE_OPERATOR: Final[str] = "w"
READ_OPERATOR: Final[str] = "r"
WRITE_BINARY_OPERATOR: Final[str] = "wb"

AWS: Final[str] = "aws"
BLANK: Final[str] = ""
SPACE: Final[str] = " "
DATE_PATTERN: Final[str] = "%Y-%m-%d %H:%M"
SENSITIVE_PATTERNS: Final[list[str]] = [
    "id_rsa",
    ".pem",
    ".aws/credentials",
    ".git-credentials",
    ".env",
    "credentials.json",
]

PROFILES_FILE: Final[str] = "profiles.json"
S3_PROFILES_PREFIX: Final[str] = "_profiles/"

