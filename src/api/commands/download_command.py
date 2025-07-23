"""
Module responsible for displaying an interactive prompt for `.zip` file selection available in a Bucket S3.

Uses the Funserpy libraries for interactive prompt and Rich for console output.
Presents details such as file size and modification date.

Function:
    - select_zip_file (zip_files): Displays an interactive list of zip files for user selection.
"""

from InquirerPy import inquirer
from rich.console import Console
from InquirerPy.utils import get_style

from src.utils import utils
from src.constants.constants import DATE_PATTERN, SPACE


console = Console()


def select_zip_file(zip_files: list[str]) -> str:
    """
    Displays an interactive menu for the user to select a zip file from the listed files.

    Each option displays the file name, formatted size, and last modified date.

    Args:
    zip_files (list[str]): List of objects containing zip file information (key, size, last_modified).

    Returns:
        str: Name (key) of the selected zip file.
    """
    choices = [
        {
            "name": f"{obj.key.ljust(40, SPACE)} | Size: {utils.format_file_size(obj.size).ljust(10)} | Last Modified: {obj.last_modified.strftime(DATE_PATTERN)}",
            "value": obj.key,
        }
        for obj in zip_files
    ]

    custom_style = get_style(
        {
            "questionmark": "#ef42f5 bold",
            "selected": "cyan bold",
            "pointer": "#58d1e6 bold",
            "instruction": "grey italic",
            "answer": "#ef42f5 bold",
            "question": "",
        }
    )
    selected_zip_file = inquirer.select(
        message="Select a zip file to download:",
        choices=choices,
        instruction="Use ↑/↓ to navigate and Enter to select",
        vi_mode=True,
        style=custom_style,
    ).execute()

    return selected_zip_file
