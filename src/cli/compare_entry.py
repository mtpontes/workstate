import typer
from rich.console import Console

from src.services import state_service, file_service
from src.utils.utils import handle_error
from src.commands.compare_command import CompareCommandImpl
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter


def register(app: typer, console: Console, state_service: state_service, file_service: file_service):
    @app.command("compare", help="Compares local project with a remote state on S3")
    def compare_state(
        state_name: str = typer.Argument(None, help="Name of the state file to compare with"),
    ) -> None:
        """Compares local project with a remote state on S3
        
        Fetches the metadata of the remote state and compares it with
        the current local project files (respecting .workstateignore).
        Outputs a diff table showing which files are new, modified,
        or missing compared to the remote backup.
        
        If no state name is provided, an interactive selector will be shown.
        
        Examples:
            ```bash
            $ workstate compare my-project-2025.zip
            ```
        """
        try:
            prompter = ZipFileSelectorPrompter(console, state_service)
            CompareCommandImpl(
                console, 
                state_service, 
                file_service,
                prompter=prompter, 
                state_name=state_name
            ).execute()
        except Exception as e:
            handle_error(console, e)
