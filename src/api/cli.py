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

import typer
from rich.console import Console

from src.api.commands.config_command import ConfigCommandImpl
from src.api.commands.configure_command import ConfigureCommandImpl
from src.api.commands.save_command import SaveCommandImpl
from src.api.commands.status_command import StatusCommandImpl
from src.api.commands.list_command import ListCommandImpl
from src.api.commands.init_command import InitCommandImpl
from src.api.commands.download_command import DownloadCommandImpl
from src.clients import s3_client
from src.services import state_service
from src.templates.code_tool import CodeTool
from src.constants.messages import VALID_CODE_TOOLS_OPTIONS
from src.services import file_service
from src.utils import utils
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO


# Main instance of the Typer application
app = typer.Typer(name="workstate", help="Portable development environment management tool", add_completion=False)
console = Console()


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
        InitCommandImpl(tool, console, file_service).execute()
    except Exception as e:
        _handle_error(e)


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
        print(access_key_id, secret_access_key, bucket_name, region)
        credentials = AWSCredentialsDTO(
            access_key_id=access_key_id, secret_access_key=secret_access_key, bucket_name=bucket_name, region=region
        )
        ConfigureCommandImpl(console, interactive, credentials).execute()

    except KeyboardInterrupt:
        console.print("\n[yellow]Configuration cancelled by user[/yellow]")
        raise typer.Exit(0)
    except Exception as e:
        _handle_error(e)


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
        ConfigCommandImpl(console).execute()

    except Exception as e:
        _handle_error(e)


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
        StatusCommandImpl(console, file_service).execute()
    except Exception as e:
        _handle_error(e)


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
        SaveCommandImpl(state_name, console, s3_client, file_service, state_service).execute()

    except Exception as e:
        _handle_error(e)


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
        ListCommandImpl(console, s3_client, state_service).execute()
    except Exception as e:
        _handle_error(e)


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
        DownloadCommandImpl(only_download, console, s3_client, state_service).execute()
    except Exception as e:
        _handle_error(e)


def _handle_error(e):
    message: str = utils.format_error_message(e)
    console.print(message)
    raise typer.Exit(1)
