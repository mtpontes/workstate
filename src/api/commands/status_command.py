"""
Module responsible for the implementation of the project status verification command.

This module contains the concrete implementation of the command to display the status
Current project files that would be included in rescue operations.
The command analyzes and presents an overview of the selected files,
including size and total counting information.

The module manages file selection based on the filter rules
configured, formatting the information in organized tables and
Calculation of summary statistics on the project files.
"""

from pathlib import Path

from rich.table import Table
from rich.console import Console

from src.utils import utils
from src.services import file_service
from src.api.views import status_view
from src.api.commands.command import CommandI


class StatusCommandImpl(CommandI):
    def __init__(self, console: Console, view: status_view, file_service: file_service) -> None:
        self.console = console
        self.view = view
        self.file_service = file_service

    def execute(self) -> None:
        """
        Displays a table in the terminal containing the files or directories to be saved, showing their name and size.

        If no files exist, it indicates that no files were found.

        Args:
            files_to_save(list[Path]): List of paths (Path) of the files or directories to be processed.
        """
        files_to_save: list[Path] = self.file_service.select_files()

        if not files_to_save:
            self.console.print("[bold green]✔ No files found.[/bold green]")
            return

        table: Table = self.view.status_files(files_to_save)
        total_files: int = len(files_to_save)
        total_size_bytes: int = sum(file.stat().st_size for file in files_to_save if file.is_file())
        total_size_human: str = utils.format_file_size(total_size_bytes)

        self.console.print(table)
        self.console.print(f"[bold yellow]Total:[/bold yellow] {total_files} files ({total_size_human})\n")
