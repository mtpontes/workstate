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

from src.utils import utils
from src.constants.constants import BLANK
from src.constants.constants import DEFAULT_AWS_REGION
from src.api.commands.command import CommandI
from src.model.aws_credentials import AWSCredentials
from src.services.config_service import ConfigService
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
from src.exception.credentials_validation_exception import CredentialsValidationException


class ConfigureCommandImpl(CommandI):
    def __init__(self, console: Console, interactive: bool, credentials: AWSCredentialsDTO) -> None:
        self.console = console
        self.interactive = interactive
        self.credentials = credentials

    def execute(self) -> None:
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
        self.console.print("[bold white]Workstate AWS Configuration[/bold white]\n")

        if self.interactive:
            credentials: AWSCredentialsDTO = self._prompt_credencials()

        self._save_credentials(credentials)

        self.console.print(f"Configuration saved to: {ConfigService.CONFIG_FILE}")
        self.console.print("[green]✓ AWS credentials configured successfully![/green]\n")

    def _prompt_credencials(self) -> AWSCredentialsDTO:
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
        current_credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()

        # Stylized banner
        title = Text("AWS Configuration Setup", style="bold blue")
        subtitle = Text("Configure your AWS credentials and settings", style="dim")
        self.console.print(Panel.fit(f"{title}\n{subtitle}", border_style="blue"))

        if not self.credentials.access_key_id:
            current_key = current_credentials.access_key_id
            display_key = f"{current_key[:8]}..." if current_key else "Not configured"

            # Styled text before the prompt
            self.console.print("\n[bold cyan]AWS Access Key ID[/bold cyan]")
            self.console.print(f"[dim]Current: {display_key}[/dim]")

            access_key_id = typer.prompt(
                "Enter Access Key ID",
                default=current_key if current_key else BLANK,
                hide_input=False,
            )

        if not self.credentials.secret_access_key:
            current_secret = current_credentials.secret_access_key
            display_secret = "***configured***" if current_secret else "Not configured"

            self.console.print("\n[bold cyan]AWS Secret Access Key[/bold cyan]")
            self.console.print(f"[dim]Current: {display_secret}[/dim]")

            secret_access_key = typer.prompt(
                "Enter Secret Access Key",
                default=current_secret if current_secret else BLANK,
                hide_input=True,
            )

        if not self.credentials.region or self.region.strip() == BLANK:
            current_region = current_credentials.region

            self.console.print("\n[bold cyan]AWS Region[/bold cyan]")
            self.console.print(f"[dim]Current: {current_region or 'Not configured'}[/dim]")
            self.console.print("[dim]Common regions: us-east-1, us-west-2, eu-west-1, ap-southeast-1[/dim]")

            region = typer.prompt(
                "Enter AWS Region",
                default=current_region if current_region else DEFAULT_AWS_REGION,
            )

        if not self.credentials.bucket_name:
            current_bucket = current_credentials.bucket_name

            self.console.print("\n[bold cyan]S3 Bucket Name[/bold cyan]")
            self.console.print(f"[dim]Current: {current_bucket or 'Not configured'}[/dim]")
            self.console.print("[dim]Must be globally unique and follow S3 naming conventions[/dim]")

            bucket_name = typer.prompt(
                "Enter S3 Bucket Name",
                default=current_bucket if current_bucket else BLANK,
            )

        # Stylized final summary
        self.console.print("\n")
        self.console.print("[bold green]Configuration Summary[/bold green]")
        self.console.print(f"[cyan]Access Key:[/cyan] {access_key_id[:8]}...")
        self.console.print(f"[cyan]Region:[/cyan] {region}")
        self.console.print(f"[cyan]Bucket:[/cyan] {bucket_name}")

        return AWSCredentialsDTO(access_key_id, secret_access_key, region, bucket_name)

    def _save_credentials(self, credentials) -> None:
        validated_credentials: AWSCredentials = None
        try:
            validated_credentials = credentials.to_aws_credentials_model()
        except CredentialsValidationException as e:
            self.console.print(utils.format_error_message(str(e)))
            raise typer.Exit(1)

        ConfigService.save_aws_credentials(validated_credentials)
