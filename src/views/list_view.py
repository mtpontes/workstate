from rich.table import Table
from mypy_boto3_s3.service_resource import ObjectSummary

from src.utils import utils


def zip_files_table(zip_files: list[ObjectSummary]) -> Table:
    table = Table(title="\nStates on S3 (Organized by Project)", show_header=True, header_style="bold white")
    table.add_column("Project", style="green", no_wrap=True)
    table.add_column("State File", style="cyan")
    table.add_column("Size", style="yellow3")
    table.add_column("Last Modified", style="magenta")

    for obj in zip_files:
        key = str(obj.key)
        if "/" in key:
            segments = key.split("/")
            project = segments[0]
            filename = "/".join(segments[1:])
        else:
            project = "[Legacy]"
            filename = key
            
        table.add_row(
            project,
            filename, 
            utils.format_file_size(obj.size), 
            str(obj.last_modified.strftime("%Y-%m-%d %H:%M:%S"))
        )

    return table
