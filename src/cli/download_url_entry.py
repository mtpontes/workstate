import typer
from rich.console import Console

from src.views import config_view
from src.utils.utils import handle_error
from src.commands.download_url_command import DownloadUrlCommandImpl


def register(app: typer, console: Console, config_view: config_view):
    @app.command("download-url", help="Downloads a project state from a shared pre-signed URL")
    def download_from_parts(
        base_url: str = typer.Argument(..., help="Base URL without signature or expires"),
        signature: str = typer.Argument(..., help="Signature part of the pre-signed URL"),
        expires: str = typer.Argument(..., help="Expiration timestamp of the pre-signed URL"),
        no_extract: bool = typer.Option(False, "--no-extract", help="Don't extract the ZIP file after download"),
        output: str = typer.Option(None, "--output", "-o", help="Custom output path for downloaded file"),
    ) -> None:
        """Downloads a project state from a shared pre-signed URL

        This command allows team members to download project states shared
        via pre-signed URLs without requiring AWS credentials. The downloaded
        ZIP file can be automatically extracted to restore the project state.

        Args:
            url (str): The pre-signed URL shared by a team member
            no_extract (bool): If True, keeps the ZIP file without extracting
            output (str): Custom path/filename for the downloaded file

        Examples:
            ```bash
            # Download and extract automatically
            $ workstate download-url "https://s3.amazonaws.com/bucket/file.zip?..."

            # Download without extracting
            $ workstate download-url "https://s3.amazonaws.com/..." --no-extract

            # Download to custom location
            $ workstate download-url "https://s3.amazonaws.com/..." --output /path/to/myfile.zip

            # Download with custom name and no extraction
            $ workstate download-url "https://s3.amazonaws.com/..." -o shared-state.zip --no-extract
            ```

        Process:
            1. Validates the provided URL
            2. Downloads the file with progress indication
            3. Optionally extracts the ZIP contents
            4. Offers to clean up the ZIP file after extraction

        Notes:
            - Works with any valid pre-signed URL from Workstate
            - Automatically detects filename from URL
            - Shows download progress for large files
            - Validates ZIP integrity before extraction
            - URLs may have expiration times set by the sharer
        """
        full_url = f"{base_url}&Signature={signature}&Expires={expires}"

        try:
            DownloadUrlCommandImpl(console=console, url=full_url, extract=not no_extract, output_path=output).execute()
        except KeyboardInterrupt:
            console.print("\n[yellow]Download cancelled by user[/yellow]")
            raise typer.Exit(0)
        except Exception as e:
            handle_error(console, e)
