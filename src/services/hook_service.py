import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

class HookService:
    def __init__(self, console: Console):
        self.console = console
        self.hook_file = ".workstate-hooks"

    def find_hooks(self, root_path: Path) -> list[str]:
        """
        Looks for the .workstate-hooks file in the given path.
        Returns a list of commands to execute.
        """
        hook_path = root_path / self.hook_file
        if not hook_path.exists():
            return []
        
        with open(hook_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        # Filter empty lines and comments
        commands = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        return commands

    def execute_hooks(self, commands: list[str], auto_confirm: bool = False) -> None:
        """
        Executes a list of shell commands.
        """
        if not commands:
            return

        self.console.print(Panel(
            "\n".join([f"[cyan]> {cmd}[/cyan]" for cmd in commands]),
            title="Post-Restore Hooks Detected",
            border_style="blue"
        ))

        if not auto_confirm:
            import typer
            if not typer.confirm("Do you want to execute these hooks?", default=True):
                self.console.print("[yellow]Hooks skipped by user.[/yellow]")
                return

        for cmd in commands:
            self.console.print(f"[bold blue]Running:[/bold blue] {cmd}")
            try:
                # Use shell=True to allow complex commands (pipes, etc.)
                result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=False)
                if result.returncode == 0:
                    self.console.print(f"[green]✔ Command finished successfully.[/green]")
            except subprocess.CalledProcessError as e:
                self.console.print(f"[bold red]Error executing command:[/bold red] {cmd}")
                self.console.print(f"[red]{str(e)}[/red]")
                if not auto_confirm:
                    if not typer.confirm("Continue with next hooks?", default=False):
                        break
