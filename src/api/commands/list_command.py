from zoneinfo import ZoneInfo

from rich.table import Table
from rich.console import Console
from mypy_boto3_s3.service_resource import ObjectSummary

from src.utils import utils


console = Console()


def print_zip_list(zip_files: list[ObjectSummary]) -> Table:
    table = Table(title="\nZIP files on S3", show_header=True, header_style="bold white")
    table.add_column("File", style="cyan")
    table.add_column("Size", style="yellow3")
    table.add_column("Last Modified", style="magenta")

    for obj in zip_files:
        table.add_row(
            obj.key, utils.format_file_size(obj.size), str(obj.last_modified.astimezone(ZoneInfo("America/Sao_Paulo")))
        )

    console.print(table)
