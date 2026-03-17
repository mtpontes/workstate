from rich.console import Console
from src.services import state_service
from src.utils import utils
from src.commands.command import CommandI
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter

class ProtectCommandImpl(CommandI):
    def __init__(
        self,
        console: Console,
        prompter: ZipFileSelectorPrompter,
        state_service: state_service,
        protect: bool = True
    ) -> None:
        self.console = console
        self.prompter = prompter
        self.state_service = state_service
        self.protect = protect

    def execute(self) -> None:
        action_name = "protect" if self.protect else "unprotect"
        message = f"Select a zip file to {action_name}:"
        
        selected_zip_file: str = self.prompter.prompt(message=message)
        
        try:
            verb = "Protecting" if self.protect else "Unprotecting"
            self.console.print(f"{verb} state: [bold cyan]{selected_zip_file}[/bold cyan]...")
            self.state_service.set_protection(selected_zip_file, protect=self.protect)
            
            success_msg = "State is now protected and cannot be deleted by prune." if self.protect else "Protection removed."
            self.console.print(f"[bold green]Success![/bold green] {success_msg}")
        except Exception as e:
            utils.handle_error(self.console, e)
