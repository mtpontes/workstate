import typer
from rich.console import Console

from src.services import state_service, file_service
from src.utils.utils import handle_error
from src.commands.sync_command import SyncCommandImpl


def register(app: typer, console: Console, state_service: state_service, file_service: file_service):
    @app.command("sync", help="Performs a smart rolling backup (checkpoint) with automatic retention")
    def sync_project(
        retention: int = typer.Option(5, "--retention", "-r", help="Maximum number of checkpoints to keep on S3"),
    ) -> None:
        """Performs a smart rolling backup (checkpoint) with automatic retention.
        
        This command:
        1. Compares the local state with the latest remote checkpoint.
        2. Uploads a new 'checkpoint-TIMESTAMP.zip' only if changes are detected.
        3. Deletes oldest checkpoints if the count exceeds the retention limit.
        
        It is designed for automation (CRON/Task Scheduler) as it skips 
        interactive confirmations and manages storage space automatically.
        
        Examples:
            ```bash
            $ workstate sync --retention 10
            ```
        """
        try:
            SyncCommandImpl(
                console, 
                state_service, 
                file_service,
                retention=retention
            ).execute()
        except Exception as e:
            handle_error(console, e)
