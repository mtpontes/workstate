import typer
from rich.console import Console

from src.services import state_service
from src.views import share_info_view
from src.utils.utils import handle_error
from src.commands.share_command import ShareCommandImpl
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter


def register(app: typer, console: Console, state_service: state_service, share_info_view: share_info_view):
    @app.command("share", help="Generates a shareable pre-signed URL for a project state")
    def share_state(
        expiration_hours: int = typer.Option(24, "--expiration", "-e", help="Hours until URL expires (default: 24)"),
    ) -> None:
        """Generates a shareable pre-signed URL for a project state

        Creates a temporary secure URL that allows team members to download
        a specific project state without requiring AWS credentials.
        The URL automatically expires after the specified time period.

        Args:
            expiration_hours (int): Number of hours until the URL expires.
                Valid range: 1-168 hours (1 week). Default: 24 hours.

        Examples:
            ```bash
            # Generate URL that expires in 24 hours (default)
            $ workstate share

            # Generate URL that expires in 2 hours
            $ workstate share --expiration 2

            # Generate URL that expires in 1 week
            $ workstate share -e 168
            ```

        Security Notes:
            - Anyone with the URL can download the state file
            - URLs are temporary and automatically expire
            - No AWS credentials are required for download
            - Consider the sensitivity of your project data when sharing

        Interactive Process:
            1. Lists all available states in your S3 bucket
            2. Allows interactive selection of the desired state
            3. Generates a secure pre-signed URL
            4. Displays the URL with usage instructions
        """
        try:
            if not 1 <= expiration_hours <= 168:  # 1 hour to 1 week
                console.print("[red]Error: Expiration hours must be between 1 and 168 (1 week)[/red]")
                raise typer.Exit(1)

            prompter = ZipFileSelectorPrompter(console=console, state_service=state_service)
            ShareCommandImpl(
                console=console,
                prompter=prompter,
                state_service=state_service,
                view=share_info_view,
                expiration_hours=expiration_hours,
            ).execute()

        except KeyboardInterrupt:
            console.print("\n[yellow]Share operation cancelled by user[/yellow]")
            raise typer.Exit(0)
        except Exception as e:
            handle_error(console, e)
