"""
Module responsible for implementing the AWS interactive credential configuration command.

This module contains the concrete implementation of the command to collect and
save AWS credentials through interactive terminal prompts. The command allows
users to configure their credentials in a guided manner, with automatic
validation and persistence of configurations.

The module manages interactive data collection, validation of provided
credentials, handling validation errors, and persistence of validated
configurations on the local file system.
"""

import typer
from rich.console import Console

from src.utils import utils
from src.api.commands.command import CommandI
from src.model.aws_credentials import AWSCredentials
from src.services.config_service import ConfigService
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
from src.api.prompters.configure_prompter import ConfigureStringPrompterImpl
from src.exception.credentials_validation_exception import CredentialsValidationException


class ConfigureCommandImpl(CommandI):
    def __init__(
        self, interactive: bool, console: Console, prompter: ConfigureStringPrompterImpl, credentials: AWSCredentialsDTO
    ) -> None:
        self.interactive = interactive
        self.console = console
        self.prompter = prompter
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
            credentials: AWSCredentialsDTO = self.prompter.prompt(self.credentials)

        self._save_credentials(credentials)

        self.console.print(f"Configuration saved to: {ConfigService.CONFIG_FILE}")
        self.console.print("[green]✓ AWS credentials configured successfully![/green]\n")

    def _save_credentials(self, credentials: AWSCredentialsDTO) -> None:
        validated_credentials: AWSCredentials = None
        try:
            validated_credentials = credentials.to_aws_credentials_model()
        except CredentialsValidationException as e:
            self.console.print(utils.format_error_message(str(e)))
            raise typer.Exit(1)

        ConfigService.save_aws_credentials(validated_credentials)
