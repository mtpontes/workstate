"""
Module responsible for displaying an interactive prompt for `.zip` file selection available in a Bucket S3.

Uses the Funserpy libraries for interactive prompt and Rich for console output.
Presents details such as file size and modification date.

Function:
    - select_zip_file (zip_files): Displays an interactive list of zip files for user selection.
"""

import typer
from pathlib import Path
from InquirerPy import inquirer
from rich.console import Console
from InquirerPy.utils import get_style
from mypy_boto3_s3.service_resource import ObjectSummary

from src.utils import utils
from src.clients import s3_client
from src.api.commands.command import CommandI
from src.services import file_service, state_service
from src.constants.constants import DATE_PATTERN, SPACE


class DownloadCommandImpl(CommandI):
    def __init__(
        self, only_download: bool, console: Console, s3_client: s3_client, state_service: state_service
    ) -> None:
        self.only_download = only_download
        self.console = console
        self.s3_client = s3_client
        self.state_service = state_service

    def execute(self) -> None:
        """
        Displays an interactive menu for the user to select a zip file from the listed files.

        Each option displays the file name, formatted size, and last modified date.

        Args:
        zip_files (list[str]): List of objects containing zip file information (key, size, last_modified).

        Returns:
            str: Name (key) of the selected zip file.
        """
        s3_objects: list[ObjectSummary] = self.s3_client.list_objects()
        zip_files: list[ObjectSummary] = self.state_service.filter_zip_files(s3_objects)
        if not zip_files:
            self.console.print("[yellow]No ZIP files found in the S3 bucket.[/yellow]")
            raise typer.Exit(0)

        choices = [
            {
                "name": f"{obj.key.ljust(40, SPACE)} | Size: {utils.format_file_size(obj.size).ljust(10)} | Last Modified: {obj.last_modified.strftime(DATE_PATTERN)}",
                "value": obj.key,
            }
            for obj in zip_files
        ]

        custom_style = get_style(
            {
                "questionmark": "#ef42f5 bold",
                "selected": "cyan bold",
                "pointer": "#58d1e6 bold",
                "instruction": "grey italic",
                "answer": "#ef42f5 bold",
                "question": "",
            }
        )
        selected_zip_file = inquirer.select(
            message="Select a zip file to download:",
            choices=choices,
            instruction="Use ↑/↓ to navigate and Enter to select",
            vi_mode=True,
            style=custom_style,
        ).execute()

        zip_file: Path = self.state_service.download_zip_file(selected_zip_file)
        self.console.print(f"\n[green]Downloaded:[/green] {zip_file}")

        if not self.only_download:
            file_service.unzip(zip_file)
            zip_file.unlink()
            self.console.print("[green]✔ State restored successfully.[/green]\n")
        else:
            self.console.print("[blue]Only downloaded file. Skipped unpacking.[/blue]")
