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
        
        # Check for protection (this is a bit slow as it does an S3 call per object)
        # However, for a standard list of states, it provides the "wow" factor
        is_protected = False
        try:
            from src.services import state_service
            is_protected = state_service.is_protected(key)
        except:
            pass
            
        protected_label = " [bold red]🔒[/bold red]" if is_protected else ""
        
        table.add_row(
            project,
            f"{filename}{protected_label}", 
            utils.format_file_size(obj.size), 
            str(obj.last_modified.strftime("%Y-%m-%d %H:%M:%S"))
        )

    return table
