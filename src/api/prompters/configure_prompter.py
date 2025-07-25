"""
Module responsible for the implementation of the AWS credential configuration prompter.

This module contains the concrete implementation of the interactive prompt system
To collect User Credentials and AWS settings through the terminal.
The module offers a validation guided interface, security masks
For sensitive data and presentation of current values as a reference.

The module manages the sequential collection of AWS (Access Key ID,
Secret Access Key, Region and Bucket S3), displaying masked current values
when appropriate and providing contextual suggestions to facilitate
User configuration.
"""

import typer
from rich.text import Text
from rich.panel import Panel
from rich.console import Console

from src.services.config_service import ConfigService
from src.constants.constants import DEFAULT_AWS_REGION, BLANK
from src.api.prompters.string_prompter import StringPrompterI
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO


class ConfigureStringPrompterImpl(StringPrompterI):
    def __init__(self, console: Console, new_credentials: AWSCredentialsDTO):
        self.console = console
        self.new_credentials = new_credentials

    def prompt(self, new_credentials: AWSCredentialsDTO) -> str:
        self._print_banner()
        current_credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()

        access_key_id = self._access_key_prompt(new_credentials, current_credentials)
        secret_access_key = self._secret_access_key_prompt(new_credentials, current_credentials)
        region = self._region_prompt(new_credentials, current_credentials)
        bucket_name = self._bucket_name_prompt(new_credentials, current_credentials)

        self._print_final_summary(access_key_id, region, bucket_name)
        return AWSCredentialsDTO(access_key_id, secret_access_key, region, bucket_name)

    def _print_banner(self):
        title = Text("AWS Configuration Setup", style="bold blue")
        subtitle = Text("Configure your AWS credentials and settings", style="dim")
        self.console.print(Panel.fit(f"{title}\n{subtitle}", border_style="blue"))

    def _access_key_prompt(self, new_credentials, current_credentials):
        if not new_credentials.access_key_id:
            current_key = current_credentials.access_key_id
            display_key = f"{current_key[:8]}..." if current_key else "Not configured"

            self.console.print("\n[bold cyan]AWS Access Key ID[/bold cyan]")
            self.console.print(f"[dim]Current: {display_key}[/dim]")

            access_key_id = typer.prompt(
                "Enter Access Key ID",
                default=current_key if current_key else BLANK,
                hide_input=False,
            )

        return access_key_id

    def _secret_access_key_prompt(self, new_credentials, current_credentials):
        if not new_credentials.secret_access_key:
            current_secret = current_credentials.secret_access_key
            display_secret = "***configured***" if current_secret else "Not configured"

            self.console.print("\n[bold cyan]AWS Secret Access Key[/bold cyan]")
            self.console.print(f"[dim]Current: {display_secret}[/dim]")

            secret_access_key = typer.prompt(
                "Enter Secret Access Key",
                default=current_secret if current_secret else BLANK,
                hide_input=True,
            )

        return secret_access_key

    def _region_prompt(self, new_credentials, current_credentials):
        if not new_credentials.region or new_credentials.region.strip() == BLANK:
            current_region = current_credentials.region

            self.console.print("\n[bold cyan]AWS Region[/bold cyan]")
            self.console.print(f"[dim]Current: {current_region or 'Not configured'}[/dim]")
            self.console.print("[dim]Common regions: us-east-1, us-west-2, eu-west-1, ap-southeast-1[/dim]")

            region = typer.prompt(
                "Enter AWS Region",
                default=current_region if current_region else DEFAULT_AWS_REGION,
            )

        return region

    def _bucket_name_prompt(self, new_credentials, current_credentials):
        if not new_credentials.bucket_name:
            current_bucket = current_credentials.bucket_name

            self.console.print("\n[bold cyan]S3 Bucket Name[/bold cyan]")
            self.console.print(f"[dim]Current: {current_bucket or 'Not configured'}[/dim]")
            self.console.print("[dim]Must be globally unique and follow S3 naming conventions[/dim]")

            bucket_name = typer.prompt(
                "Enter S3 Bucket Name",
                default=current_bucket if current_bucket else BLANK,
            )

        return bucket_name

    def _print_final_summary(self, access_key_id, region, bucket_name):
        self.console.print("\n")
        self.console.print("[bold green]Configuration Summary[/bold green]")
        self.console.print(f"[cyan]Access Key:[/cyan] {access_key_id[:8]}...")
        self.console.print(f"[cyan]Region:[/cyan] {region}")
        self.console.print(f"[cyan]Bucket:[/cyan] {bucket_name}")
