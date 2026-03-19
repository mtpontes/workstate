import typer
from rich.console import Console

from src.services import state_service
from src.utils.utils import handle_error
from src.commands.inspect_command import InspectCommandImpl
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter


def register(app: typer, console: Console, state_service: state_service):
    @app.command("inspect", help="Inspects the contents of a state ZIP file on S3")
    def inspect_state(
        state_name: str = typer.Argument(None, help="Name of the state file to inspect"),
    ) -> None:
        """Inspects the contents of a state ZIP file on S3
        
        Downloads the specified state file to a temporary location,
        reads its internal structure, and displays a table with all
        contained files, their sizes, and modification dates.
        
        If no state name is provided, an interactive selector will be shown.
        
        Examples:
            ```bash
            $ workstate inspect my-project-2025.zip
            ```
        """
        try:
            prompter = ZipFileSelectorPrompter(console, state_service)
            InspectCommandImpl(
                console, 
                state_service, 
                prompter=prompter, 
                state_name=state_name
            ).execute()
        except Exception as e:
            handle_error(console, e)
