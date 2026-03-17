import typer
from rich.console import Console
from typer import Typer

from src.services import state_service
from src.commands.protect_command import ProtectCommandImpl
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter

def register(app: Typer, console: Console, state_service: state_service):
    """
    Register the protect and unprotect commands to the Typer app.
    """
    @app.command("protect", help="Mark a state file as protected to prevent deletion")
    def protect():
        prompter = ZipFileSelectorPrompter(console=console, state_service=state_service)
        ProtectCommandImpl(
            console=console,
            prompter=prompter,
            state_service=state_service,
            protect=True
        ).execute()

    @app.command("unprotect", help="Remove protection from a state file")
    def unprotect():
        prompter = ZipFileSelectorPrompter(console=console, state_service=state_service)
        ProtectCommandImpl(
            console=console,
            prompter=prompter,
            state_service=state_service,
            protect=False
        ).execute()
