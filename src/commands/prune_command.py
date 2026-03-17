import typer
from rich.console import Console
from src.services.pruning_service import PruningService
from src.utils import utils



def prune(
    older_than: str = typer.Option(
        "30d", "--older-than", help="Duration to keep backups (e.g. 7d, 1mo, 24h). States older than this will be deleted."
    ),
    all_projects: bool = typer.Option(
        False, "--all", "-a", help="Prune states from all projects in the bucket. Default is current project only."
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Skip confirmation prompt."
    ),
    console: Console = Console(),
):
    """
    Remove old state files from S3, respecting protected states.
    """
    try:
        service = PruningService(console)
        
        scope = "all projects" if all_projects else f"project '{utils.get_project_name()}'"
        console.print(f"Searching for states older than [bold cyan]{older_than}[/bold cyan] in {scope}...")
        
        candidates = service.get_candidates(older_than, global_scan=all_projects)
        
        if not candidates:
            console.print("[green]No candidates found for pruning.[/green]")
            return

        console.print(f"\n[bold yellow]Found {len(candidates)} candidates for deletion:[/bold yellow]")
        for cand in candidates:
            console.print(f" - {cand.key} ({utils.format_file_size(cand.size)})")

        if not force:
            if not utils.confirm_action(console, f"\nAre you sure you want to delete these {len(candidates)} states?", default=False):
                console.print("[yellow]Aborted.[/yellow]")
                raise typer.Exit()

        deleted_count = service.prune(candidates)
        console.print(f"\n[bold green]Success![/bold green] Deleted {deleted_count} state files.")

    except Exception as e:
        utils.handle_error(console, e)
