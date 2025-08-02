import typer
from rich.console import Console

from src.services import state_service
from src.utils.utils import handle_error
from src.commands.delete_command import DeleteCommandImpl
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter


def register(app: typer, console: Console, state_service: state_service):
    @app.command("delete", help="Deletes a saved project state from AWS S3")
    def delete_state() -> None:
        try:
            prompter = ZipFileSelectorPrompter(console=console, state_service=state_service)
            DeleteCommandImpl(
                console=console,
                prompter=prompter,
                state_service=state_service,
            ).execute()
        except Exception as e:
            handle_error(console, e)
