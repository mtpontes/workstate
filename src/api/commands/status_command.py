"""
This module displays the files to be saved in the terminal, showing the number and size in a readable format.

It uses the Rich library to display a stylized table containing file information, such as name and size.
It also displays a final summary with the total number of files and their cumulative size.

Function:
    - print_status(files_to_save): Displays the files to be saved and basic statistics.
"""

from pathlib import Path

from rich.table import Table
from rich.console import Console

from src.utils import utils


console = Console()


def print_status(files_to_save: list[Path]) -> None:
    """
    Displays a table in the terminal containing the files or directories to be saved, showing their name and size.

    If no files exist, it indicates that no files were found.

    Args:
        files_to_save(list[Path]): List of paths (Path) of the files or directories to be processed.
    """
    if not files_to_save:
        console.print("[bold green]✔ No files found.[/bold green]")
        return

    table = Table(title="\nFiles to save", show_header=True, header_style="bold white")
    table.add_column("File/Directory", style="cyan", no_wrap=True)
    table.add_column("Size", style="yellow3", justify="left")

    total_files = 0
    total_size_bytes = 0
    for path in files_to_save:
        size_bytes = path.stat().st_size if path.is_file() else 0
        size_human = utils.format_file_size(size_bytes) if size_bytes > 0 else "-"
        table.add_row(str(path), size_human)
        total_files += 1
        total_size_bytes += size_bytes

    console.print(table)
    total_size_human = utils.format_file_size(total_size_bytes)

    console.print(f"[bold yellow]Total:[/bold yellow] {total_files} files ({total_size_human})\n")
