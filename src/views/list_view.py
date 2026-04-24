from rich.table import Table
from src.model.dto.state_dto import StateDTO
from src.utils import utils


def zip_files_table(zip_files: list[StateDTO]) -> Table:
    table = Table(title="\nStates on S3 (Organized by Project)", show_header=True, header_style="bold white")
    table.add_column("Project", style="green", no_wrap=True)
    table.add_column("State File", style="cyan")
    table.add_column("Size", style="yellow3")
    table.add_column("Last Modified", style="magenta")

    for state in zip_files:
        protected_label = " [bold red]🔒[/bold red]" if state.is_protected else ""
        
        table.add_row(
            state.project,
            f"{state.filename}{protected_label}", 
            utils.format_file_size(state.size), 
            str(state.last_modified.strftime("%Y-%m-%d %H:%M:%S"))
        )

    return table
