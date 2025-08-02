import typer
from rich.console import Console

from src.services import state_service
from src.utils.utils import handle_error
from src.commands.download_command import DownloadCommandImpl
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter


def register(app: typer, console: Console, state_service: state_service):
    @app.command("download", help="Restores a saved project state from AWS S3")
    def download_state(
        only_download: bool = typer.Option(
            False, "--only-download", help="Only downloads the state, without unpacking it"
        ),
    ) -> None:
        """Restores a saved project state from AWS S3

        An interactive restore process that:
        1. Lists all available states in S3
        2. Allows interactive selection of the desired state
        3. Downloads the selected ZIP file
        4. Unzips the files in the current directory
        5. Removes the temporary ZIP file

        Examples:
            ```bash
            $ workstate download
            ? Select a zip file to download: Use ↑/↓ to navigate and Enter to select
            ❯ my-project-2024-01-15.zip               | Size: 14.3 KB    | Last Modified: 2024-01-15 12:34:56
            other-project-2024-01-14.zip            | Size: 10.3 KB    | Last Modified: 2024-01-15 12:34:56
            old-project-2024-01-10.zip              | Size: 1.1 KB     | Last Modified: 2024-01-15 12:34:56
            ```

        Warning:
            - Existing files may be overwritten during unpacking.
            - It is recommended to back up the current state before restoring.
            - This operation cannot be undone automatically.

        Notes:
            - Interactive interface using keyboard arrows for selection
            - Displays detailed file information before confirmation
            - Preserves the project's original directory structure
        """
        try:
            prompter = ZipFileSelectorPrompter(console=console, state_service=state_service)
            DownloadCommandImpl(
                only_download=only_download,
                console=console,
                prompter=prompter,
                state_service=state_service,
            ).execute()
        except Exception as e:
            handle_error(console, e)
