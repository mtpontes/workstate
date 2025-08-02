from pathlib import Path

from rich.table import Table

from src.utils import utils


def status_files(files_to_save: list[Path]) -> Table:
    table = Table(title="\nFiles to save", show_header=True, header_style="bold white")
    table.add_column("File/Directory", style="cyan", no_wrap=True)
    table.add_column("Size", style="yellow3", justify="left")

    for path in files_to_save:
        size_bytes = path.stat().st_size if path.is_file() else 0
        size_human = utils.format_file_size(size_bytes) if size_bytes > 0 else "-"
        table.add_row(str(path), size_human)
    return table
