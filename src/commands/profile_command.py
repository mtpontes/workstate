"""
Module responsible for the implementation of the Profile management command.
"""

from rich.console import Console
from rich.table import Table
from rich.text import Text

from src.commands.command import CommandI
from src.services.profile_service import ProfileService
from src.constants.constants import IGNORE_FILE


class ProfileCommandImpl(CommandI):
    def __init__(self, console: Console):
        self.console = console

    def execute(self) -> None:
        # This base class might not be used directly if we use Typer subcommands,
        # but we follow the pattern for consistency or for a general help.
        pass

    def save_profile(self, name: str) -> None:
        """Saves current .workstateignore as a local profile."""
        ignore_path = Path(IGNORE_FILE)
        if not ignore_path.exists():
            self.console.print(f"[red]Error: {IGNORE_FILE} not found in current directory.[/red]")
            return

        content = ignore_path.read_text(encoding="utf-8")
        ProfileService.save_local_profile(name, content)
        self.console.print(f"[bold green][OK] Profile '{name}' saved locally.[/bold green]")

    def list_profiles(self) -> None:
        """Lists local and remote profiles."""
        local_profiles = ProfileService.list_local_profiles()
        
        try:
            remote_profiles = ProfileService.list_remote_profiles()
        except Exception:
            self.console.print("[yellow]Warning: Could not fetch remote profiles from S3.[/yellow]")
            remote_profiles = []

        table = Table(title="Workstate Profiles")
        table.add_column("Profile Name", style="cyan")
        table.add_column("Local", justify="center")
        table.add_column("Remote (S3)", justify="center")

        all_names = sorted(list(set(local_profiles + remote_profiles)))
        
        if not all_names:
            self.console.print("[yellow]No profiles found.[/yellow]")
            return

        for name in all_names:
            is_local = "[OK]" if name in local_profiles else "-"
            is_remote = "[OK]" if name in remote_profiles else "-"
            table.add_row(name, is_local, is_remote)

        self.console.print(table)

    def delete_profile(self, name: str, remote: bool = False) -> None:
        """Deletes a profile."""
        deleted_local = False
        if not remote:
            deleted_local = ProfileService.delete_local_profile(name)
            if deleted_local:
                self.console.print(f"[green][OK] Local profile '{name}' deleted.[/green]")
            else:
                self.console.print(f"[yellow]Local profile '{name}' not found.[/yellow]")

        if remote:
            try:
                ProfileService.delete_remote_profile(name)
                self.console.print(f"[green][OK] Remote profile '{name}' deleted from S3.[/green]")
            except Exception as e:
                self.console.print(f"[red]Error deleting remote profile: {str(e)}[/red]")

    def push_profile(self, name: str) -> None:
        """Uploads a local profile to S3."""
        import typer
        try:
            password = None
            if typer.confirm("Would you like to protect this profile with a password?", default=False):
                password = typer.prompt("Enter password for profile", hide_input=True, confirmation_prompt=True)

            ProfileService.push_profile(name, password)
            self.console.print(f"[bold green][OK] Profile '{name}' pushed to S3.[/bold green]")
        except ValueError as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
        except Exception as e:
            self.console.print(f"[red]Failed to push profile: {str(e)}[/red]")

    def pull_profile(self, name: str) -> None:
        """Downloads a profile from S3."""
        import typer
        try:
            try:
                ProfileService.pull_profile(name)
            except Exception as e:
                if "is encrypted" in str(e) or "Password required" in str(e):
                    password = typer.prompt(f"Profile '{name}' is protected. Enter password", hide_input=True)
                    ProfileService.pull_profile(name, password)
                else:
                    raise e

            self.console.print(f"[bold green][OK] Profile '{name}' pulled from S3.[/bold green]")
        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

from pathlib import Path
