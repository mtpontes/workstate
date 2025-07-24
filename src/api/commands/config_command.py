"""
Module responsible for displaying the current AWS settings used by the Workstate application.

This module uses the Rich library to display visually pleasant information on the terminal,
showing credential status, configuration file information and error messages if
Settings are absent or corrupted.

Functions:
    - show_Current_Configuractions(credentials): Show the configured AWS settings.
    - show_Configuration_status(): Shows the absence of configuration and guides the user.
    - show_config_error(error): Displays detailed error message if you can't read the setting.
"""

from pathlib import Path
from datetime import datetime

import typer
from rich import box
from rich.table import Table
from rich.panel import Panel
from rich.console import Console

from src.api.commands.command import CommandI
from src.services.config_service import ConfigService
from src.constants.constants import ACCESS_KEY_ID, BUCKET_NAME, REGION


class ConfigCommandImpl(CommandI):
    def __init__(self, console: Console) -> None:
        self.console = console

    def execute(self) -> None:
        try:
            credentials = ConfigService.get_aws_credentials()
            if credentials:
                self._show_current_configurations(credentials)
            else:
                self._show_configuration_status()

        except Exception as e:
            self._show_config_error(e)
            raise typer.Exit(1)

    def _show_current_configurations(self, credentials: dict) -> None:
        """
        Displays the current AWS settings that are properly configured.

        The information is presented in a table format, masking part of the access key.
        It also displays the path and date of the last modification of the configuration file.

        Args:
            credentials (dict): Dictionary containing the AWS credentials (Access Key ID, Region, and Bucket Name).
        """
        # Main table with information
        table = Table(
            title="\nAWS Configuration", title_style="bold cyan", box=box.ROUNDED, show_header=False, padding=(0, 1)
        )

        table.add_column("Setting", style="cyan", width=20)
        table.add_column("Value", style="white")
        table.add_column("Status", justify="center", width=12)

        # Mask access key
        masked_key = f"{credentials[ACCESS_KEY_ID][:8]}***"

        # Add lines to the table
        table.add_row("Access Key ID", masked_key, "[green]✓[/green]")
        table.add_row("Region", credentials[REGION], "[green]✓[/green]")
        table.add_row("Bucket Name", credentials[BUCKET_NAME], "[green]✓[/green]")

        self.console.print(table)

        # Additional Information
        info_panel = Panel(
            f"[dim]Configuration file: {ConfigService.CONFIG_FILE}[/dim]\n"
            f"[dim]Last modified: {self._get_config_last_modified(ConfigService.CONFIG_FILE)}[/dim]",
            title="File Information",
            title_align="left",
            border_style="dim",
            padding=(0, 1),
        )
        self.console.print(info_panel)

        # General status
        self.console.print("\n[bold green]All AWS credentials are properly configured![/bold green]")
        self.console.print("[dim]You can now use Workstate commands that require AWS access.[/dim]\n")

    def _show_configuration_status(self) -> None:
        """
        Displays a message stating that AWS credentials have not yet been configured.

        Displays a table highlighting missing configurations and presents a panel with next steps
        so the user can configure the configuration correctly.
        """
        # Configuration not found
        error_table = Table(
            title="\nConfiguration Status", title_style="bold red", box=box.ROUNDED, show_header=False, padding=(0, 1)
        )

        error_table.add_column("Setting", style="cyan", width=20)
        error_table.add_column("Status", justify="center", width=20)

        error_table.add_row("Access Key ID", "[red]✗ Not configured[/red]")
        error_table.add_row("Region", "[red]✗ Not configured[/red]")
        error_table.add_row("Bucket Name", "[red]✗ Not configured[/red]")

        self.console.print(error_table)

        # Configuration Instructions
        help_panel = Panel(
            "[bold]Next Steps:[/bold]\n\n"
            "1. Run [bold cyan]workstate configure[/bold cyan] to set up your AWS credentials\n"
            "2. Make sure you have valid AWS access keys\n"
            "3. Choose an appropriate S3 bucket for state storage\n\n"
            "[dim]Tip: You can get AWS credentials from the AWS Console → IAM → Users → Security credentials[/dim]",
            title="Getting Started",
            title_align="left",
            border_style="yellow",
            padding=(1, 1),
        )
        self.console.print(help_panel)
        self.console.print()

    def _get_config_last_modified(self, config_file: str) -> str:
        """
        Returns the date of the last modification of the configuration file.

        Returns:
            str: Date and time of the last modification in "%y-%m-%d%h:%m:%s" format.
                If the file does not exist, it returns "File Not Found".
                If any error occurs, it returns "Unknown".
        """
        try:
            path = Path(config_file)
            if path.exists():
                timestamp = path.stat().st_mtime
                return datetime.fromtimestamp(timestamp).astimezone().strftime("%Y-%m-%d %H:%M:%S")
            else:
                return "File not found"
        except Exception:
            return "Unknown"

    def _show_config_error(self, error: Exception) -> None:
        """
        Displays a stylized error message when you cannot access the configuration file.

        Informs the expected path of the file, error details and suggestions to solve.
        """
        config_path = Path.home() / ".workstate" / "config.json"
        error_panel = Panel(
            f"[red]Failed to read configuration file[/red]\n\n"
            f"[dim]Expected location: {config_path}[/dim]\n"
            f"[dim]Error details: {str(error)}[/dim]\n\n"
            f"[yellow]Possible solutions:[/yellow]\n"
            f"• Check if the config file exists at the expected location\n"
            f"• Run [bold]workstate configure[/bold] to create the configuration\n"
            f"• Verify file permissions on the config directory\n"
            f"• Ensure the ~/.workstate directory exists",
            title="🚨 Configuration Error",
            title_align="left",
            border_style="red",
            padding=(1, 1),
        )
        self.console.print(error_panel)
