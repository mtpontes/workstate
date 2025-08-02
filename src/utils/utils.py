"""
Utilities for manipulating and formatting files related to zip files and file sizes.

Functions:
    - define_zip_file_name(project_name: str) -> str:
        Generates the name of the zipped file based on the project name.
    - format_file_size(size_bytes: int) -> str:
        Formats the size in bytes to a readable unit (KB, MB, GB, etc.).
"""

import typer
from rich.prompt import Confirm
from rich.console import Console

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
