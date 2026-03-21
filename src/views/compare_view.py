from rich.table import Table
from src.utils import utils

def compare_results_table(state_name: str, results: list[dict]) -> Table:
    """
    Creates a table displaying the comparison between local files and a remote state.
    
    Args:
        state_name (str): Name of the remote state.
        results (list[dict]): List of comparison results.
        
    Returns:
        Table: A rich table with comparison information.
    """
    table = Table(title=f"\nComparison: Local vs [bold cyan]{state_name}[/bold cyan]", show_header=True, header_style="bold white")
    table.add_column("Status", style="bold")
    table.add_column("File Path", style="green")
    table.add_column("Local Size", style="yellow3", justify="right")
    table.add_column("Remote Size", style="dim", justify="right")

    status_styles = {
        "ADDED": "[bold green]ONLY LOCAL[/bold green]",
        "DELETED": "[bold red]ONLY REMOTE[/bold red]",
        "MODIFIED": "[bold yellow]MODIFIED[/bold yellow]",
        "EQUAL": "[dim]EQUAL[/dim]"
    }

    for res in results:
        status = res["status"]
        if status == "EQUAL":
            continue # Skip equal files to reduce noise, or show them dimmed? 
            # Decision: Skip equal by default, or show count at the end.
            
        local_size = utils.format_file_size(res["local_size"]) if res["local_size"] is not None else "-"
        remote_size = utils.format_file_size(res["remote_size"]) if res["remote_size"] is not None else "-"
        
        table.add_row(
            status_styles.get(status, status),
            res["path"],
            local_size,
            remote_size
        )

    return table
