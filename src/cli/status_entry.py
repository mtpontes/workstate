import typer
from rich.console import Console

from src.services import file_service
from src.views import status_view
from src.utils.utils import handle_error
from src.commands.status_command import StatusCommandImpl


def register(app: typer, console: Console, status_view: status_view, file_service: file_service):
    @app.command("status", help="Displays detailed status of files tracked by Workstate")
    def status() -> None:
        """Displays detailed status of files tracked by Workstate.

        Analyzes the current .workstateignore file and displays a complete list
        of all files and directories that will be included in the next
        backup. Useful for validating exclusion rules before executing
        the save command.

        Examples:
            ```bash
            $ workstate status
                                Files to save
            ┌────────────────────────────────────────────┬───────┐
            │ File/Directory                             │ Size  │
            ├────────────────────────────────────────────┼───────┤
            │ src/main.py                                │ 2.1KB │
            │ config/settings.json                       │ 0.8KB │
            │ requirements.txt                           │ 0.3KB │
            │ ultralight_file.txt                        │     - │
            └────────────────────────────────────────────┴───────┘
            Total: 127 files (45.2 MB)
            ```

        Notes:
            - Requires .workstateignore file valid in the current directory
            - Does not perform modification operations, only consultation
            - Useful for complex exclusion rules
            - Shows both files and directories that will be included
            - Sizes are recursively calculated for directories
        """
        try:
            StatusCommandImpl(console=console, view=status_view, file_service=file_service).execute()
        except Exception as e:
            handle_error(console, e)
