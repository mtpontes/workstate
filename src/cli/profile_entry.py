import typer
from rich.console import Console

from src.commands.profile_command import ProfileCommandImpl
from src.utils.utils import handle_error


def register(app: typer.Typer, console: Console):
    profile_app = typer.Typer(help="Manage Workstate profiles (.workstateignore templates)")
    app.add_typer(profile_app, name="profile")

    command_impl = ProfileCommandImpl(console=console)

    @profile_app.command("save", help="Saves the current .workstateignore as a local profile")
    def save(name: str) -> None:
        """Saves current .workstateignore as a local profile."""
        try:
            command_impl.save_profile(name)
        except Exception as e:
            handle_error(console, e)

    @profile_app.command("list", help="Lists all local and remote profiles")
    def list_profiles() -> None:
        """Lists all local and remote profiles."""
        try:
            command_impl.list_profiles()
        except Exception as e:
            handle_error(console, e)

    @profile_app.command("delete", help="Deletes a profile")
    def delete(name: str, remote: bool = typer.Option(False, "--remote", "-r", help="Delete from S3 instead of local")) -> None:
        """Deletes a profile from local or S3."""
        try:
            command_impl.delete_profile(name, remote)
        except Exception as e:
            handle_error(console, e)

    @profile_app.command("push", help="Uploads a local profile to S3")
    def push(name: str) -> None:
        """Uploads a local profile to S3."""
        try:
            command_impl.push_profile(name)
        except Exception as e:
            handle_error(console, e)

    @profile_app.command("pull", help="Downloads a profile from S3 and saves it locally")
    def pull(name: str) -> None:
        """Downloads a profile from S3 and saves it locally."""
        try:
            command_impl.pull_profile(name)
        except Exception as e:
            handle_error(console, e)
