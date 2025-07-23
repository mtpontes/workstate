"""Workstate - Portable Development Environment Management Tool.

This module implements a CLI (Command Line Interface) for managing and synchronizing
development environments through AWS S3. Workstate allows developers
to preserve and restore the complete state of their projects, including configurations,
dependencies, and development data.

Main features:
    - Creation of custom .workstateignore templates per tool
    - Selective file compression based on exclusion rules
    - Automatic upload/download to AWS S3
    - Interactive listing and selection of saved states
    - Viewing the status of tracked files

The system uses a .workstateignore file (similar to .gitignore) to map
files and directories relevant to the development environment, creating a ZIP file
that is stored in AWS S3. This allows the developer to continue work
exactly where they left off, keeping development settings and data intact.

Dependencies:
    - typer: Framework for creating CLIs
    - rich: Library for terminal formatting
    - boto3: AWS SDK for Python
    - pathlib: File path manipulation

Example of use:
    $ workstate init --tool python
    $ workstate list
    $ workstate download
    $ workstate save my-project
    $ workstate status
    $ workstate configure
    $ workstate config

Author: mtpontes
"""

from pathlib import Path

import typer
from rich.text import Text
from mypy_boto3_s3.service_resource import ObjectSummary

from src.utils import utils
from src.clients import s3_client
from src.services import state_service
from src.templates.code_tool import CodeTool
from src.validators import credentials_validators
from src.services.config_service import ConfigService
from src.constants.messages import VALID_CODE_TOOLS_OPTIONS
from src.services import console_service, file_service
from src.api.commands import (
    config_command,
    configure_command,
    download_command,
    list_command,
    status_command,
)


# Main instance of the Typer application
app = typer.Typer(name="workstate", help="Portable development environment management tool", add_completion=False)


@app.command("init", help="Initializes a new Workstate project with .workstateignore file template")
def init(tool: str = typer.Option(CodeTool.DEFAULT.value, "--tool", "-t", help=VALID_CODE_TOOLS_OPTIONS)) -> None:
    """Initializes a new Workstate project with .workstateignore file template

    Creates a .workstateignore file in the current directory with a pre-configured template
    based on the specified development tool.
    The template contains exclusion rules optimized for each project type.

    Args:
        tool (str): Development tool type. Valid options include
            'python', 'node', 'java', 'go', etc. Default: 'generic'.

    Examples:
        ```bash
        $ workstate init --tool python
        $ workstate init -t node
        $ workstate init  # uses generic template
        ```

    Notes:
        - If a .workstateignore file already exists, nothing will be done.
        - Each tool has specific optimized exclusion rules.
        - The template can be manually edited after creation.
    """
    try:
        tool: CodeTool = CodeTool(tool)
        file_service.create_workstateignore(tool)
    except Exception as e:
        if isinstance(e, ValueError) and "is not a valid CodeTool" in str(e):
            message = Text()
            message.append("Error: Invalid tool. Use one of the valid options: ", style="red")
            message.append(CodeTool.get_valid_values(), style="bold magenta")
            console_service.print_message(message)
        else:
            console_service.print_error("Unexpected error:", e)
        raise typer.Exit(1)


@app.command("list", help="Lists all project states available in AWS S3")
def list_state_zips() -> None:
    """Lists all project states available in AWS S3

    Connects to the configured S3 bucket and retrieves a list of all
    previously saved state ZIP files. Displays information such as
    file name, size, and modification date in tabular format.

    Examples:
        ```bash
        $ workstate list
        ┌─────────────────────────┬──────────┬─────────────────────┐
        │ Name                    │ Size     │ Last Modified       │
        ├─────────────────────────┼──────────┼─────────────────────┤
        │ my-project-2025.zip     │ 15.2 MB  │ 2025-01-15 14:30:00 │
        │ other-project-2025.zip  │ 8.7 MB   │ 2025-01-14 09:15:22 │
        └─────────────────────────┴──────────┴─────────────────────┘
        ```

    Notes:
        - Only files with a .zip extension are displayed
        - Requires valid AWS credentials
        - List is sorted by modification date (most recent first)
    """
    try:
        s3_objects: list[ObjectSummary] = s3_client.list_objects()
        zip_files: list[ObjectSummary] = state_service.filter_zip_files(s3_objects)
        list_command.print_zip_list(zip_files)
    except Exception as e:
        console_service.print_message(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)


@app.command("download", help="Restores a saved project state from AWS S3")
def download_state(
    only_download: bool = typer.Option(False, "--only-download", help="Only downloads the state, without unpacking it"),
) -> None:
    """Restores a saved project state from AWS S3

    An interactive restore process that:
    1. Lists all available states in S3
    2. Allows interactive selection of the desired state
    3. Downloads the selected ZIP file
    4. Unzips the files in the current directory
    5. Removes the temporary ZIP file

    Examples:
        ```bash
        $ workstate download
        ? Select a zip file to download: Use ↑/↓ to navigate and Enter to select
        ❯ my-project-2024-01-15.zip               | Size: 14.3 KB    | Last Modified: 2024-01-15 12:34:56
          other-project-2024-01-14.zip            | Size: 10.3 KB    | Last Modified: 2024-01-15 12:34:56
          old-project-2024-01-10.zip              | Size: 1.1 KB     | Last Modified: 2024-01-15 12:34:56
        ```

    Warning:
        - Existing files may be overwritten during unpacking.
        - It is recommended to back up the current state before restoring.
        - This operation cannot be undone automatically.

    Notes:
        - Interactive interface using keyboard arrows for selection
        - Displays detailed file information before confirmation
        - Preserves the project's original directory structure
    """
    try:
        s3_objects: list[ObjectSummary] = s3_client.list_objects()
        zip_files: list[ObjectSummary] = state_service.filter_zip_files(s3_objects)
        if not zip_files:
            console_service.print_message("[yellow]No ZIP files found in the S3 bucket.[/yellow]")
            raise typer.Exit(0)

        selected_zip_file: str = download_command.select_zip_file(zip_files)
        zip_file: Path = state_service.download_zip_file(selected_zip_file)
        console_service.print_message(f"[green]Downloaded:[/green] {zip_file}")

        if not only_download:
            file_service.unzip(zip_file)
            zip_file.unlink()
            console_service.print_message("[green]State restored successfully.[/green]")
        else:
            console_service.print_message("[blue]Only downloaded file. Skipped unpacking.[/blue]")

    except Exception as e:
        console_service.print_message(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)


@app.command("save", help="Saves the current state of the project to AWS S3")
def save_state(state_name: str) -> None:
    """Saves the current state of the project to AWS S3

    Performs the complete development environment backup process:
    1. Analyzes the .workstateignore file to determine included files
    2. Creates a temporary ZIP file with the selected files
    3. Uploads the ZIP file to the configured S3 bucket
    4. Removes the local temporary file

    Args:
        state_name (str): Unique identifier name for the project state.
            This will be the name of the ZIP file on S3.

    Examples:
        ```bash
        $ workstate save my-django-project
        $ workstate save "project with spaces"
        ```

    Notes:
        - Requires .workstateignore file valid in the current directory
        - Project name is sanitized for compatibility S3
        - Timestamp is automatically added to the final name of the file
        - Temporary files are automatically cleaned in case of error
    """
    try:
        files_to_save: list[Path] = file_service.select_files()
        temporary_zip_file: Path = file_service.zip_files(files_to_save)
        zip_file_name: str = utils.define_zip_file_name(state_name)
        s3_client.save_zip_file(temporary_zip_file, zip_file_name)
        temporary_zip_file.unlink()
    except Exception as e:
        console_service.print_message(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)


@app.command("status", help="Displays detailed status of files tracked by Workstate")
def status() -> None:
    """Displays detailed status of files tracked by Workstate.

    Analyzes the current .workstateignore file and displays a complete list
    of all files and directories that will be included in the next
    backup. Useful for validating exclusion rules before executing
    the save command.

    Examples:
        ```bash
        $ workstate status
                            Files to save
        ┌────────────────────────────────────────────┬───────┐
        │ File/Directory                             │ Size  │
        ├────────────────────────────────────────────┼───────┤
        │ src/main.py                                │ 2.1KB │
        │ config/settings.json                       │ 0.8KB │
        │ requirements.txt                           │ 0.3KB │
        │ ultralight_file.txt                        │     - │
        └────────────────────────────────────────────┴───────┘
        Total: 127 files (45.2 MB)
        ```

    Notes:
        - Requires .workstateignore file valid in the current directory
        - Does not perform modification operations, only consultation
        - Useful for complex exclusion rules
        - Shows both files and directories that will be included
        - Sizes are recursively calculated for directories
    """
    try:
        files_to_save: list[Path] = file_service.select_files()
        status_command.print_status(files_to_save)
    except Exception as e:
        console_service.print_message(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)


@app.command("configure", help="Configure AWS credentials for Workstate")
def configure_aws(
    access_key_id: str = typer.Option(None, "--access-key-id", "-a", help="AWS Access Key ID"),
    secret_access_key: str = typer.Option(None, "--secret-access-key", "-s", help="AWS Secret Access Key"),
    region: str = typer.Option(None, "--region", "-r", help="AWS Region"),
    bucket_name: str = typer.Option(None, "--bucket-name", "-b", help="S3 Bucket name"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", "-i", help="Use interactive mode"),
) -> None:
    """Configure AWS credentials for Workstate

    Sets up AWS credentials that will be stored in ~/.workstate/config.json.
    Can be used in interactive mode (default) or with command-line arguments.

    Args:
        access_key_id (str, optional): AWS Access Key ID
        secret_access_key (str, optional): AWS Secret Access Key
        region (str, optional): AWS Region (e.g., us-east-1, sa-east-1)
        bucket_name (str, optional): S3 Bucket name
        interactive (bool): Whether to use interactive mode

    Examples:
        ```bash
        # Interactive mode (default)
        $ workstate configure

        # Non-interactive mode
        $ workstate configure --access-key-id AKIA... --secret-access-key xxx --region us-east-1 --bucket-name my-bucket

        # Mixed mode (some args, interactive for missing ones)
        $ workstate configure --region sa-east-1 --bucket-name my-workstate-bucket
        ```

    Notes:
        - Credentials are stored locally in ~/.workstate/config.json
        - Interactive mode will prompt for each missing credential
        - Existing credentials will be overwritten
        - Use AWS IAM best practices for credential management
    """
    try:
        console_service.print_message("[bold white]Workstate AWS Configuration[/bold white]\n")

        if interactive or not all([access_key_id, secret_access_key, region, bucket_name]):
            access_key_id, secret_access_key, region, bucket_name = configure_command.prompt_credencials(
                access_key_id, secret_access_key, region, bucket_name
            )

        results: list[str] = credentials_validators.validate_credentials(
            access_key_id, secret_access_key, region, bucket_name
        )
        if results:
            results_str: str = "".join(["\n- " + credencial_key for credencial_key in results])
            console_service.print_error(f"All credentials are required. Missing credencials: {results_str}")
            raise typer.Exit(1)

        ConfigService.save_aws_credentials(
            access_key_id.strip(),
            secret_access_key.strip(),
            region.strip(),
            bucket_name.strip(),
        )

        console_service.print_message(f"Configuration saved to: {ConfigService.CONFIG_FILE}")
        console_service.print_message("[green]✓ AWS credentials configured successfully![/green]\n")

    except KeyboardInterrupt:
        console_service.print_message("\n[yellow]Configuration cancelled by user[/yellow]")
        raise typer.Exit(0)
    except Exception as e:
        console_service.print_message(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)


@app.command("config", help="Show current Workstate configuration")
def show_config() -> None:
    """Show current Workstate configuration

    Displays the current AWS configuration without revealing sensitive information.

    Examples:
        ```bash
        $ workstate config
        ╭─ Workstate Configuration ─────────────────────────╮
        │                                                   │
        │  AWS Credentials                                  │
        │  ├─ Access Key ID: AKIA***...                     │
        │  ├─ Region: us-east-1                             │
        │  └─ Bucket Name: my-workstate-bucket              │
        │                                                   │
        ╰───────────────────────────────────────────────────╯
        ```
    """
    try:
        credentials = ConfigService.get_aws_credentials()

        if credentials:
            config_command.show_current_configurations(credentials)
        else:
            config_command.show_configuration_status()

    except Exception as e:
        config_command.show_config_error(e)
        raise typer.Exit(1)
