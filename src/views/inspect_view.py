from rich.table import Table
from datetime import datetime
from src.utils import utils

def state_content_table(state_name: str, contents: list[dict]) -> Table:
    """
    Creates a table displaying the contents of a state ZIP file.
    
    Args:
        state_name (str): Name of the state file being inspected.
        contents (list[dict]): List of file metadata from the ZIP.
        
    Returns:
        Table: A rich table with file information.
    """
    table = Table(title=f"\nContents of State: [bold cyan]{state_name}[/bold cyan]", show_header=True, header_style="bold white")
    table.add_column("File Path", style="green")
    table.add_column("Size", style="yellow3", justify="right")
    table.add_column("Compressed", style="dim", justify="right")
    table.add_column("Modified", style="magenta")

    for file_info in contents:
        # zipfile.ZipInfo.date_time is a tuple (year, month, day, hour, minute, second)
        dt = datetime(*file_info["date_time"])
        
        table.add_row(
            file_info["filename"],
            utils.format_file_size(file_info["file_size"]),
            utils.format_file_size(file_info["compress_size"]),
            dt.strftime("%Y-%m-%d %H:%M:%S")
        )

    return table
