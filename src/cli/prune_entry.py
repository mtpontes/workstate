import typer
from rich.console import Console
from typer import Typer

from src.commands.prune_command import prune as prune_impl

def register(app: Typer, console: Console):
    """
    Register the prune command to the Typer app.
    """
    @app.command(name="prune")
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
    ):
        """
        Remove old state files from S3, respecting protected states.
        """
        prune_impl(older_than, all_projects, force, console)
