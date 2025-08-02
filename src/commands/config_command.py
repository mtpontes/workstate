"""
Module responsible for implementing the AWS credentials configuration command.

This module contains the concrete implementation of the command to display and validate
the system's AWS credentials settings. The command verifies that the
credentials are correctly configured and displays the current status
through a rich and interactive command-line interface.

The module manages credential validation, error handling, and
presentation of configuration information in an organized manner,
including informative tables and help panels when necessary.
"""

from pathlib import Path
from datetime import datetime

import typer
from rich.table import Table
from rich.panel import Panel
from rich.console import Console

from src.views import config_view
from src.commands.command import CommandI
from src.constants.constants import DATE_PATTERN
from src.services.config_service import ConfigService
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
from src.exception.credentials_validation_exception import CredentialsValidationException


class ConfigCommandImpl(CommandI):
    def __init__(self, console: Console, view: config_view) -> None:
        self.console = console
        self.view = view

    def execute(self) -> None:
        try:
            credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
            errors: dict = None
            try:
                credentials.to_aws_credentials_model()
            except CredentialsValidationException as e:
                errors = e.errors

            if errors is None:
                self._show_current_configurations(credentials)
            else:
                self._show_configurations_with_errors(errors)

        except Exception as e:
            self._show_config_error_panel(e)
            raise typer.Exit(1)

    def _show_current_configurations(self, credentials: AWSCredentialsDTO) -> None:
        # Main table with information
        table: Table = self.view.configurations_table(credentials)
        self.console.print(table)

        # Additional Information
        info_panel = self.view.config_file_info_panel()
        self.console.print(info_panel)

        # General status
        self.console.print("\n[bold green]All AWS credentials are properly configured![/bold green]")
        self.console.print("[dim]You can now use Workstate commands that require AWS access.[/dim]\n")

    def _show_configurations_with_errors(self, errors: dict[str, str]) -> None:
        config_errors_table: Table = self.view.configurations_with_errors_table(errors)
        self.console.print(config_errors_table)
        self._show_help_panel()

    def _get_config_last_modified(self, config_file: str) -> str:
        try:
            path = Path(config_file)
            if path.exists():
                timestamp = path.stat().st_mtime
                return datetime.fromtimestamp(timestamp).astimezone().strftime(DATE_PATTERN)
            else:
                return "File not found"
        except Exception:
            return "Unknown"

    def _show_help_panel(self):
        help_panel: Panel = self.view.help_panel()
        self.console.print(help_panel)
        self.console.print()

    def _show_config_error_panel(self, error: Exception) -> None:
        error_panel: Panel = self.view.error_panel(error)
        self.console.print(error_panel)
