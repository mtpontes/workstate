import typer
from rich.console import Console

from src.services import state_service
from src.views import list_view
from src.utils.utils import handle_error
from src.commands.list_command import ListCommandImpl


def register(app: typer, console: Console, list_view: list_view, state_service: state_service):
    @app.command("list", help="Lists all project states available in AWS S3")
    def list_state_zips() -> None:
        """Lists all project states available in AWS S3

        Connects to the configured S3 bucket and retrieves a list of all
        previously saved state ZIP files. Displays information such as
        file name, size, and modification date in tabular format.

        Examples:
            ```bash
            $ workstate list
            ┌─────────────────────────┬──────────┬─────────────────────┐
            │ Name                    │ Size     │ Last Modified       │
            ├─────────────────────────┼──────────┼─────────────────────┤
            │ my-project-2025.zip     │ 15.2 MB  │ 2025-01-15 14:30:00 │
            │ other-project-2025.zip  │ 8.7 MB   │ 2025-01-14 09:15:22 │
            └─────────────────────────┴──────────┴─────────────────────┘
            ```

        Notes:
            - Only files with a .zip extension are displayed
            - Requires valid AWS credentials
            - List is sorted by modification date (most recent first)
        """
        try:
            ListCommandImpl(console, list_view, state_service).execute()
        except Exception as e:
            handle_error(console, e)
