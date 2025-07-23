"""
Module responsible for interactively requesting and collecting the AWS credentials required for the Workstate application.

This module uses Typer for interactive prompts and Rich for improved visual display in the terminal.
If the user already has a saved configuration, the current values are displayed as a suggestion.

Function:
    - prompt_credencials(access_key_id, secret_access_key, region, bucket_name):
    Interactively prompts the user for AWS credentials.
"""

import typer
from rich.text import Text
from rich.panel import Panel
from rich.console import Console

from src.constants.envs import DEFAULT_AWS_REGION
from src.services.config_service import ConfigService
from src.constants.constants import ACCESS_KEY_ID, BLANK, BUCKET_NAME, REGION, SECRET_ACCESS_KEY


console = Console()


def prompt_credencials(
    access_key_id: str, secret_access_key: str, region: str, bucket_name: str
) -> tuple[str, str, str, str]:
    """
    Interactively prompts the user for AWS credentials and settings via the terminal.

    Displays previously configured values, if any, as suggestions. Uses `typer.prompt` to collect
    input and Rich for visual formatting of the text.

    Args:
        access_key_id (str): AWS Access Key ID (can be empty and the user will be prompted).
        secret_access_key (str): AWS Secret Access Key (can be empty and the user will be prompted).
        region (str): AWS Region (can be empty and the user will be prompted).
        bucket_name (str): S3 bucket name (can be empty and the user will be prompted).

    Returns:
        tuple[str, str, str, str]: A tuple containing the provided or confirmed credentials:
        (access_key_id, secret_access_key, region, bucket_name)
    """
    existing_config = ConfigService.get_aws_credentials() or {}

    # Stylized banner
    title = Text("AWS Configuration Setup", style="bold blue")
    subtitle = Text("Configure your AWS credentials and settings", style="dim")
    console.print(Panel.fit(f"{title}\n{subtitle}", border_style="blue"))

    if not access_key_id:
        current_key = existing_config.get(ACCESS_KEY_ID, BLANK)
        display_key = f"{current_key[:8]}..." if current_key else "Not configured"

        # Styled text before the prompt
        console.print("\n[bold cyan]AWS Access Key ID[/bold cyan]")
        console.print(f"[dim]Current: {display_key}[/dim]")

        access_key_id = typer.prompt(
            "Enter Access Key ID",
            default=current_key if current_key else BLANK,
            hide_input=False,
        )

    if not secret_access_key:
        current_secret = existing_config.get(SECRET_ACCESS_KEY, BLANK)
        display_secret = "***configured***" if current_secret else "Not configured"

        console.print("\n[bold cyan]AWS Secret Access Key[/bold cyan]")
        console.print(f"[dim]Current: {display_secret}[/dim]")

        secret_access_key = typer.prompt(
            "Enter Secret Access Key",
            default=current_secret if current_secret else BLANK,
            hide_input=True,
        )

    if not region or region.strip() == BLANK:
        current_region = existing_config.get(REGION, BLANK)

        console.print("\n[bold cyan]AWS Region[/bold cyan]")
        console.print(f"[dim]Current: {current_region or 'Not configured'}[/dim]")
        console.print("[dim]Common regions: us-east-1, us-west-2, eu-west-1, ap-southeast-1[/dim]")

        region = typer.prompt(
            "Enter AWS Region",
            default=current_region if current_region else DEFAULT_AWS_REGION,
        )

    if not bucket_name:
        current_bucket = existing_config.get(BUCKET_NAME, BLANK)

        console.print("\n[bold cyan]S3 Bucket Name[/bold cyan]")
        console.print(f"[dim]Current: {current_bucket or 'Not configured'}[/dim]")
        console.print("[dim]Must be globally unique and follow S3 naming conventions[/dim]")

        bucket_name = typer.prompt(
            "Enter S3 Bucket Name",
            default=current_bucket if current_bucket else BLANK,
        )

    # Stylized final summary
    console.print("\n")
    console.print("[bold green]Configuration Summary[/bold green]")
    console.print(f"[cyan]Access Key:[/cyan] {access_key_id[:8]}...")
    console.print(f"[cyan]Region:[/cyan] {region}")
    console.print(f"[cyan]Bucket:[/cyan] {bucket_name}")

    return (access_key_id, secret_access_key, region, bucket_name)
