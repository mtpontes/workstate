from rich.console import Console

from src.services import state_service
from src.api.commands.command import CommandI
from src.api.prompters.download_prompter import ZipFileSelectorStringPrompterImpl


class DeleteCommandImpl(CommandI):
    def __init__(
        self,
        console: Console,
        prompter: ZipFileSelectorStringPrompterImpl,
        state_service: state_service,
    ) -> None:
        self.console = console
        self.prompter = prompter
        self.state_service = state_service

    def execute(self) -> None:
        selected_zip_file: str = self.prompter.prompt()
        self.state_service.delete_state_file(selected_zip_file)
        
        self.console.print(f"\n[green]Deleted:[/green] {selected_zip_file}")
