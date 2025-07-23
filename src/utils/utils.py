"""
Utilities for manipulating and formatting files related to zip files and file sizes.

Functions:
    - define_zip_file_name(project_name: str) -> str:
        Generates the name of the zipped file based on the project name.
    - format_file_size(size_bytes: int) -> str:
        Formats the size in bytes to a readable unit (KB, MB, GB, etc.).
"""

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
