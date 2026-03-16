"""
Utilities for manipulating and formatting files related to zip files and file sizes.

Functions:
    - define_zip_file_name(project_name: str) -> str:
        Generates the name of the zipped file based on the project name.
    - format_file_size(size_bytes: int) -> str:
        Formats the size in bytes to a readable unit (KB, MB, GB, etc.).
"""

import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm

import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from src.constants.constants import DOT_ZIP


def define_zip_file_name(project_name: str) -> str:
    file_extension: str = DOT_ZIP
    return f"{project_name}{file_extension}"


def format_file_size(size_bytes: int) -> str:
    """Formats size in bytes to KB, MB, GB, etc."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def format_error_message(error: Exception = None) -> str:
    if error is None:
        return "\n[red]Error:[/red]\n"
    else:
        return f"\n[red]Error:[/red] {error}\n"


def handle_error(console: Console, e):
    message: str = format_error_message(e)
    console.print(message)
    raise typer.Exit(1)


def confirm_action(console: Console, message: str, default: bool = False) -> bool:
    """Ask user for yes/no confirmation.

    Args:
        console: Rich console instance for output
        message: The confirmation message to display
        default: Default value if user just presses Enter (default: False)

    Returns:
        bool: True if user confirms (yes), False otherwise (no)

    Examples:
        >>> console = Console()
        >>> if confirm_action(console, "Delete this file?"):
        ...     print("File deleted")
        ... else:
        ...     print("Operation cancelled")

        >>> # With default value
        >>> if confirm_action(console, "Continue?", default=True):
        ...     print("Continuing...")
    """
    try:
        return Confirm.ask(message, console=console, default=default)
    except Exception:
        return default


def destructure_pre_signed_url(url: str) -> tuple[str, str, str]:
    """Return base url and args Signature and Expires"""
    url_split: list[str] = url.split("&")
    return (url_split[0], url_split[1].split("=")[1], url_split[2].split("=")[1])


def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a cryptographic key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def encrypt_file(file_path: Path, password: str) -> Path:
    """Encrypts a file and returns the path to the encrypted file."""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    fernet = Fernet(key)

    with open(file_path, "rb") as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    encrypted_file_path = file_path.with_suffix(file_path.suffix + ".enc")
    with open(encrypted_file_path, "wb") as f:
        # Store salt at the beginning of the file (16 bytes)
        f.write(salt)
        f.write(encrypted_data)

    return encrypted_file_path


def decrypt_file(file_path: Path, password: str) -> Path:
    """Decrypts a file and returns the path to the decrypted file."""
    with open(file_path, "rb") as f:
        salt = f.read(16)
        encrypted_data = f.read()

    key = derive_key(password, salt)
    fernet = Fernet(key)

    decrypted_data = fernet.decrypt(encrypted_data)

    decrypted_file_path = file_path.with_suffix("").with_suffix(file_path.suffixes[-2])
    # If it was state.zip.enc -> state.zip
    
    # Let's be more robust with naming
    if file_path.name.endswith(".enc"):
        decrypted_file_path = file_path.parent / file_path.name[:-4]
    else:
        decrypted_file_path = file_path.with_suffix(".decrypted")

    with open(decrypted_file_path, "wb") as f:
        f.write(decrypted_data)

    return decrypted_file_path
