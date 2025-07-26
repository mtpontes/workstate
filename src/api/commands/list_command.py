"""
Module responsible for implementing the state file listing command.

This module contains the concrete implementation of the command to list files
of state available in remote storage. The command recovers information
stored files and presents them in organized tabular format for
Facilitate visualization and selection by the user.

The module manages the metadata recovery of the files, formatting
information in structured tables and data presentation through
an interface of rich and informative console.
"""

from rich.table import Table
from rich.console import Console
from mypy_boto3_s3.service_resource import ObjectSummary

from src.api.views import list_view
from src.services import state_service
from src.api.commands.command import CommandI


class ListCommandImpl(CommandI):
    def __init__(self, console: Console, views: list_view, state_service: state_service):
        self.console = console
        self.views = views
        self.state_service = state_service

    def execute(self) -> Table:
        with self.console.status("[bold green]Fetching state files from S3...", spinner="dots"):
            zip_files: list[ObjectSummary] = self.state_service.get_state_files()

        table: Table = self.views.zip_files_table(zip_files)
        self.console.print(table)
        self.console.print()
