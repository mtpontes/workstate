from rich.console import Console
import typer
from src.commands.command import CommandI
from src.services import state_service, file_service
from src.views import compare_view
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter

class CompareCommandImpl(CommandI):
    def __init__(
        self,
        console: Console,
        state_service: state_service,
        file_service: file_service,
        prompter: ZipFileSelectorPrompter = None,
        state_name: str = None,
    ) -> None:
        self.console = console
        self.state_service = state_service
        self.file_service = file_service
        self.prompter = prompter
        self.state_name = state_name

    def execute(self) -> None:
        if not self.state_name:
            if not self.prompter:
                raise Exception("State name not provided and prompter not available.")
            self.state_name = self.prompter.prompt(message="Select a state to compare with:")

        # Handle encryption
        password = None
        if self.state_name.endswith(".enc"):
            import os
            password = os.getenv("WORKSTATE_ENCRYPTION_PASSWORD")
            if not password:
                password = typer.prompt("Encryption password", hide_input=True)

        with self.console.status(f"[bold green]Comparing local project with {self.state_name}...", spinner="dots"):
            try:
                # Get remote contents
                remote_contents = self.state_service.get_state_content(self.state_name, password)
                
                # Get local files
                local_files = self.file_service.select_files()
                
                # Compare
                results = self.file_service.compare_files(local_files, remote_contents)
            except Exception as e:
                self.console.print(f"[red]Error during comparison:[/red] {str(e)}")
                return

        diff_found = any(res["status"] != "EQUAL" for res in results)
        if not diff_found:
            self.console.print(f"\n[bold green][OK] Local project matches {self.state_name} perfectly.[/bold green]")
            return

        table = compare_view.compare_results_table(self.state_name, results)
        self.console.print(table)
        
        # Summary
        added = sum(1 for r in results if r["status"] == "ADDED")
        deleted = sum(1 for r in results if r["status"] == "DELETED")
        modified = sum(1 for r in results if r["status"] == "MODIFIED")
        equal = sum(1 for r in results if r["status"] == "EQUAL")
        
        self.console.print(f"\nSummary: [green]{added} only local[/green], [red]{deleted} only remote[/red], [yellow]{modified} modified[/yellow], [dim]{equal} equal[/dim].")
