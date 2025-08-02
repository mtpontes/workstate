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
    $ workstate configure
    $ workstate config
    $ workstate status
    $ workstate save my-project
    $ workstate list
    $ workstate download
    $ workstate delete

Author: mtpontes
"""

import typer
from rich.console import Console

from src.cli import download_pre_signed_entry
from src.views import share_info_view
from src.views import config_view, list_view, status_view
from src.services import file_service
from src.services import state_service
from src.cli import (
    config,
    configure_entry,
    delete_entry,
    download_entry,
    init_entry,
    list_entry,
    save_entry,
    share_entry,
    status_entry,
)


console = Console()
app = typer.Typer(name="workstate", help="Portable development environment management tool", add_completion=False)

config.register(app, console, config_view)
configure_entry.register(app, console)
init_entry.register(app, console, file_service)
status_entry.register(app, console, status_view, file_service)
save_entry.register(app, console, file_service, state_service)
download_entry.register(app, console, state_service)
delete_entry.register(app, console, state_service)
list_entry.register(app, console, list_view, state_service)
download_pre_signed_entry.register(app, console, config_view)
share_entry.register(app, console, state_service, share_info_view)
