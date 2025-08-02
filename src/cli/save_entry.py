import typer
from rich.console import Console

from src.services import file_service, state_service
from src.utils.utils import handle_error
from src.commands.save_command import SaveCommandImpl


def register(app: typer, console: Console, file_service: file_service, state_service: state_service):
    @app.command("save", help="Saves the current state of the project to AWS S3")
    def save_state(state_name: str) -> None:
        """Saves the current state of the project to AWS S3

        Performs the complete development environment backup process:
        1. Analyzes the .workstateignore file to determine included files
        2. Creates a temporary ZIP file with the selected files
        3. Uploads the ZIP file to the configured S3 bucket
        4. Removes the local temporary file

        Args:
            state_name (str): Unique identifier name for the project state.
                This will be the name of the ZIP file on S3.

        Examples:
            ```bash
            $ workstate save my-django-project
            $ workstate save "project with spaces"
            ```

        Notes:
            - Requires .workstateignore file valid in the current directory
            - Project name is sanitized for compatibility S3
            - Timestamp is automatically added to the final name of the file
            - Temporary files are automatically cleaned in case of error
        """
        try:
            SaveCommandImpl(
                state_name=state_name, console=console, file_service=file_service, state_service=state_service
            ).execute()

        except Exception as e:
            handle_error(console, e)
