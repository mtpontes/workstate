from rich.console import Console

from src.services import state_service
from src.api.commands.command import CommandI
from src.api.prompters.zip_file_selector_prompter import ZipFileSelectorPrompter


class DeleteCommandImpl(CommandI):
    def __init__(
        self,
        console: Console,
        prompter: ZipFileSelectorPrompter,
        state_service: state_service,
    ) -> None:
        self.console = console
        self.prompter = prompter
        self.state_service = state_service

    def execute(self) -> None:
        selected_zip_file: str = self.prompter.prompt()

        with self.console.status("[bold green]Deleting state...", spinner="dots"):
            self.state_service.delete_state_file(selected_zip_file)

        self.console.print(f"\n[green]Deleted:[/green] {selected_zip_file}\n")
