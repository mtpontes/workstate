import typer
from rich.console import Console

from src.services import state_service
from src.views import list_view
from src.utils.utils import handle_error
from src.commands.list_command import ListCommandImpl
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter


def register(app: typer, console: Console, list_view: list_view, state_service: state_service):
    @app.command("list", help="Lists all project states available in AWS S3")
    def list_state_zips(
        system: str = typer.Option(None, "--system", "-s", help="Filter by system (e.g., Windows, Linux)"),
        branch: str = typer.Option(None, "--branch", "-b", help="Filter by git branch"),
        older_than: str = typer.Option(None, "--older-than", "-o", help="Filter states older than duration (e.g., 7d, 1m)"),
        interactive: bool = typer.Option(
            False, "--interactive", "-i", help="Interactive mode with fuzzy search"
        ),
        use_cache: bool = typer.Option(True, "--cache/--no-cache", help="Use local metadata cache (default: True)"),
    ) -> None:
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
            prompter = ZipFileSelectorPrompter(console, state_service)
            ListCommandImpl(
                console, 
                list_view, 
                state_service, 
                prompter=prompter, 
                interactive=interactive,
                system_filter=system,
                branch_filter=branch,
                older_than_filter=older_than,
                use_cache=use_cache
            ).execute()
        except Exception as e:
            handle_error(console, e)
