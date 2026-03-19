from rich.console import Console
import typer
from src.commands.command import CommandI
from src.services import state_service
from src.views import inspect_view
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter

class InspectCommandImpl(CommandI):
    def __init__(
        self,
        console: Console,
        state_service: state_service,
        prompter: ZipFileSelectorPrompter = None,
        state_name: str = None,
    ) -> None:
        self.console = console
        self.state_service = state_service
        self.prompter = prompter
        self.state_name = state_name

    def execute(self) -> None:
        if not self.state_name:
            if not self.prompter:
                raise Exception("State name not provided and prompter not available.")
            self.state_name = self.prompter.prompt(message="Select a state to inspect:")

        # Handle encryption
        password = None
        if self.state_name.endswith(".enc"):
            import os
            password = os.getenv("WORKSTATE_ENCRYPTION_PASSWORD")
            if not password:
                password = typer.prompt("Encryption password", hide_input=True)

        with self.console.status(f"[bold green]Inspecting {self.state_name}...", spinner="dots"):
            try:
                contents = self.state_service.get_state_content(self.state_name, password)
            except Exception as e:
                self.console.print(f"[red]Error inspecting state:[/red] {str(e)}")
                return

        if not contents:
            self.console.print(f"[yellow]State {self.state_name} appears to be empty.[/yellow]")
            return

        table = inspect_view.state_content_table(self.state_name, contents)
        self.console.print(table)
