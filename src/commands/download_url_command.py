# src/api/commands/download_url_command.py

"""Download from URL Command Implementation.

This module implements the download-url command that allows users to download
and optionally extract project states from pre-signed URLs shared by team members.
"""

import os
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import requests
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

from src.utils import utils
from src.constants.constants import DOT_ZIP, WRITE_BINARY_OPERATOR


class DownloadUrlCommandImpl:
    def __init__(self, console: Console, url: str, extract: bool = True, output_path: str = None):
        self.console = console
        self.url = url
        self.extract = extract
        self.output_path = output_path

    def execute(self) -> None:
        if not self._is_valid_url(self.url):
            self.console.print("[red]Error: Invalid URL provided[/red]")
            return

        filename: str = self._get_filename_from_url(self.url)
        output_file: Path = self._get_output_file(filename)

        self._download_file(self.url, output_file)
        self.console.print(f"[green]✔ Downloaded successfully: {output_file}[/green]")

        if self.extract and output_file.suffix.lower() == DOT_ZIP:
            self._extract_zip(output_file)
        else:
            self.console.print(f"[blue] File saved as: {output_file}[/blue]")

    def _get_output_file(self, filename) -> Path:
        if self.output_path:
            output_file = Path(self.output_path)
        else:
            output_file = Path.cwd() / filename
        return output_file

    def _is_valid_url(self, url: str) -> bool:
        """Validate if the provided string is a valid URL.

        Args:
            url: URL string to validate

        Returns:
            bool: True if valid URL, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def _get_filename_from_url(self, url: str) -> str:
        """Extract filename from URL or generate a default one.

        Args:
            url: URL to extract filename from

        Returns:
            str: Filename for the downloaded file
        """
        try:
            parsed_url = urlparse(url)
            path = parsed_url.path
            filename = os.path.basename(path)

            if not filename or "." not in filename:
                filename = "workstate-shared.zip"

            return filename
        except Exception:
            return "workstate-shared.zip"

    def _download_file(self, url: str, output_path: Path) -> None:
        self.console.print("[blue] Downloading from shared URL...[/blue]")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task(f"Downloading {output_path.name}...", total=total_size if total_size > 0 else None)

            with open(output_path, WRITE_BINARY_OPERATOR) as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        progress.update(task, advance=len(chunk))

        return True

    def _extract_zip(self, zip_path: Path) -> None:
        try:
            with self.console.status("[bold blue]Extracting files..."):
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    extract_path = zip_path.parent
                    zip_ref.extractall(extract_path)

            self.console.print(f"[green] Extracted to: {zip_path.parent}[/green]")

            if utils.confirm_action(self.console, "Remove the downloaded ZIP file?"):
                zip_path.unlink()
                self.console.print("[dim]ZIP file removed[/dim]")

        except zipfile.BadZipFile:
            self.console.print("[red]Error: Downloaded file is not a valid ZIP file[/red]")
        except Exception as e:
            self.console.print(f"[red]Error extracting ZIP file: {str(e)}[/red]")
