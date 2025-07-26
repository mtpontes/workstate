"""
Module responsible for implementing the State Download and Restoration Command.

This module contains the concrete implementation of the command to download files
compacted state of remote storage and optionally unzip them
locally. The command offers an interactive interface for file selection
and manages the entire download and restoration process.

The module allows both simple files and restoration download
complete of the state, including automatic unzipping and file cleaning
temporary after successful extraction.
"""

from pathlib import Path
from rich.console import Console

from src.clients import s3_client
from src.api.commands.command import CommandI
from src.services import file_service, state_service
from src.api.prompters.download_prompter import ZipFileSelectorStringPrompterImpl


class DownloadCommandImpl(CommandI):
    def __init__(
        self,
        only_download: bool,
        console: Console,
        prompter: ZipFileSelectorStringPrompterImpl,
        state_service: state_service,
    ) -> None:
        self.only_download = only_download
        self.console = console
        self.prompter = prompter
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
        selected_zip_file: str = self.prompter.prompt()
        zip_file: Path = self.state_service.download_state_file(selected_zip_file)
        self.console.print(f"\n[green]Downloaded:[/green] {zip_file}")

        if self.only_download:
            self.console.print("[blue]Only downloaded file. Skipped unpacking.[/blue]")
        else:
            file_service.unzip(zip_file)
            zip_file.unlink()
            self.console.print("[green]✔ State restored successfully.[/green]\n")
