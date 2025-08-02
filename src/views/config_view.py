from pathlib import Path
from datetime import datetime

from rich import box
from rich.table import Table
from rich.panel import Panel

from src.constants.constants import ACCESS_KEY_ID, BUCKET_NAME, DATE_PATTERN, REGION, SECRET_ACCESS_KEY
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
from src.services.config_service import ConfigService


def configurations_table(credentials: AWSCredentialsDTO) -> Table:
    table = Table(
        title="\nAWS Configuration", title_style="bold cyan", box=box.ROUNDED, show_header=False, padding=(0, 1)
    )

    table.add_column("Setting", style="cyan", width=20)
    table.add_column("Value", style="white")
    table.add_column("Status", justify="center", width=3)

    # Mask access key
    masked_access_key = f"{credentials.access_key_id[:3]}***"
    masked_secret_key = f"{credentials.secret_access_key[:3]}***"

    # Add lines to the table
    table.add_row("Access Key ID", masked_access_key, "[green]✓[/green]")
    table.add_row("Secret Access Key", masked_secret_key, "[green]✓[/green]")
    table.add_row("Region", credentials.region, "[green]✓[/green]")
    table.add_row("Bucket Name", credentials.bucket_name, "[green]✓[/green]")

    return table


def config_file_info_panel() -> Panel:
    return Panel(
        f"[dim]Configuration file: {ConfigService.CONFIG_FILE}[/dim]\n"
        f"[dim]Last modified: {_get_config_last_modified(ConfigService.CONFIG_FILE)}[/dim]",
        title="File Information",
        title_align="left",
        border_style="dim",
        padding=(0, 1),
    )


def _get_config_last_modified(config_file: str) -> str:
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
            return datetime.fromtimestamp(timestamp).astimezone().strftime(DATE_PATTERN)
        else:
            return "File not found"
    except Exception:
        return "Unknown"


def configurations_with_errors_table(errors: dict[str, str]) -> Table:
    error_table = Table(
        title="\nConfiguration Status", title_style="bold red", box=box.ROUNDED, show_header=False, padding=(0, 1)
    )

    error_table.add_column("Setting", style="cyan", width=20)
    error_table.add_column("Status", justify="left", width=20)

    def add_rows(table, errors):
        fields: dict = {
            "Access Key Id": errors.get(ACCESS_KEY_ID, None),
            "Secret Access Key": errors.get(SECRET_ACCESS_KEY, None),
            "Region": errors.get(REGION, None),
            "Bucket Name": errors.get(BUCKET_NAME, None),
        }

        for key, value in fields.items():
            if value is None:
                table.add_row(key, "[green]✓ Configured[/green]")
                continue

            if key.upper() == "Region".upper():
                if "Invalid region" in value:
                    table.add_row(key.title(), "[red]✗ Invalid region[/red]")
                    continue
            key_formatted: str = key.replace("_", " ").title()
            table.add_row(key_formatted, "[red]✗ Not configured[/red]")

    add_rows(error_table, errors)
    return error_table


def help_panel() -> Panel:
    return Panel(
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


def error_panel(error: Exception) -> Panel:
    config_path = Path.home() / ".workstate" / "config.json"
    return Panel(
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
