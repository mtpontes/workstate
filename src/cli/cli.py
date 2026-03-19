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

import threading
import typer
from rich.console import Console

from src.cli import download_pre_signed_entry
from src.views import share_info_view
from src.views import config_view, list_view, status_view
from src.services import file_service, state_service, hook_service, update_service, config_service
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
    doctor_entry,
    report_entry,
    prune_entry,
    protect_entry,
    profile_entry,
    inspect_entry,
    compare_entry,
    sync_entry,
    git_hook_entry,
)


console = Console()
app = typer.Typer(
    name="workstate",
    help="Portable development environment management tool",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

@app.callback()
def global_callback():
    """
    Global setup for all commands.
    Runs update check in the background.
    """
    config_svc = config_service.ConfigService()
    update_svc = update_service.UpdateService(console, config_svc)
    
    # Run update check in background
    thread = threading.Thread(target=update_svc.check_for_updates)
    thread.daemon = True
    thread.start()

config.register(app, console, config_view)
configure_entry.register(app, console)
init_entry.register(app, console, file_service)
status_entry.register(app, console, status_view, file_service)
save_entry.register(app, console, file_service, state_service)
hook_svc = hook_service.HookService(console)
download_entry.register(app, console, state_service, hook_svc)
delete_entry.register(app, console, state_service)
list_entry.register(app, console, list_view, state_service)
download_pre_signed_entry.register(app, console, config_view)
share_entry.register(app, console, state_service, share_info_view)
doctor_entry.register(app, console)
report_entry.register(app, console)
prune_entry.register(app, console)
protect_entry.register(app, console, state_service)
profile_entry.register(app, console)
inspect_entry.register(app, console, state_service)
compare_entry.register(app, console, state_service, file_service)
sync_entry.register(app, console, state_service, file_service)
git_hook_entry.register(app, console, hook_svc)
