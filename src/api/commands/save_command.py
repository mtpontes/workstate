"""
Module responsible for implementing the state rescue command.

This module contains the concrete implementation of the command to create and save
SNAPSHOTS OF THE CURRENT STATE OF PROJECT IN REMOTE STORAGE. The command
selects relevant files, compact in an ZIP file and performs
Upload to preserve the state of the project.

The module manages the entire backup process, including smart selection
files, temporary compaction, upload for remote storage and
Cleaning temporary files after the rescue process.
"""

from pathlib import Path

from rich.console import Console

from src.utils import utils
from src.api.commands.command import CommandI
from src.services import state_service, file_service


class SaveCommandImpl(CommandI):
    def __init__(
        self,
        state_name: str,
        console: Console,
        file_service: file_service,
        state_service: state_service,
    ) -> None:
        self.state_name = state_name
        self.console = console
        self.file_service = file_service
        self.state_service = state_service

    def execute(self) -> None:
        files_to_save: list[Path] = self.file_service.select_files()
        temporary_zip_file: Path = self.file_service.zip_files(files_to_save)
        zip_file_name: str = utils.define_zip_file_name(self.state_name)

        with self.console.status("[bold green]Saving state...", spinner="dots"):
            self.state_service.save_state_file(temporary_zip_file, zip_file_name)
        temporary_zip_file.unlink()

        self.console.print(
            f"\n[bold green]✔ State '{self.state_name}' saved successfully to S3 as '{zip_file_name}'[/bold green]\n"
        )
