"""
Module responsible for implementing the State Download and Restoration Command.

This module contains the concrete implementation of the command to download files
compacted state of remote storage and optionally unzip them
locally. The command offers an interactive interface for file selection
and manages the entire download and restoration process.

The module allows both simple files and restoration download
complete of the state, including automatic unzipping and file cleaning
temporary after successful extraction.
"""

from pathlib import Path

from rich.console import Console
from rich.progress import (
    BarColumn,
    FileSizeColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TransferSpeedColumn,
)

import os
import typer
from src.commands.command import CommandI
from src.services import file_service, state_service
from src.clients import s3_client
from src.utils import utils, system_info
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter


class DownloadCommandImpl(CommandI):
    def __init__(
        self,
        only_download: bool,
        console: Console,
        prompter: ZipFileSelectorPrompter,
        state_service: state_service,
    ) -> None:
        self.only_download = only_download
        self.console = console
        self.prompter = prompter
        self.state_service = state_service

    def execute(self) -> None:
        """
        Displays an interactive menu for the user to select a zip file from the listed files.

        Each option displays the file name, formatted size, and last modified date.

        Args:
        zip_files (list[str]): List of objects containing zip file information (key, size, last_modified).

        Returns:
            str: Name (key) of the selected zip file.
        """
        selected_zip_file: str = self.prompter.prompt()

        s3_resource = s3_client.create_s3_resource()
        obj = s3_resource.Object(selected_zip_file)
        file_size = obj.content_length

        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
        )

        with progress:
            download_task = progress.add_task(f"Downloading {selected_zip_file}", total=file_size)

            def progress_callback(bytes_amount):
                progress.update(download_task, advance=bytes_amount)

            zip_file: Path = self.state_service.download_state_file(
                selected_zip_file, callback=progress_callback
            )
        self.console.print(f"\n[green]Downloaded:[/green] {zip_file}")

        # Environment and Git Traceability Validation
        try:
            from src.utils import git_utils
            metadata = obj.metadata
            remote_system = metadata.get("system")
            remote_arch = metadata.get("architecture")
            remote_branch = metadata.get("git-branch")
            remote_commit = metadata.get("git-commit")
            
            # Display Traceability Info
            if remote_branch or remote_commit:
                trace_msg = "Restoration based on "
                if remote_branch:
                    trace_msg += f"branch [bold cyan]{remote_branch}[/bold cyan] "
                if remote_commit:
                    short_hash = git_utils.get_commit_short_hash(remote_commit)
                    trace_msg += f"(commit [bold magenta]{short_hash}[/bold magenta])"
                
                from rich.panel import Panel
                self.console.print(
                    Panel(
                        trace_msg,
                        title="Git Traceability",
                        border_style="blue",
                        expand=False
                    )
                )

            if remote_system or remote_arch:
                current_info = system_info.get_system_info()
                
                mismatch = []
                if remote_system and remote_system != current_info["system"]:
                    mismatch.append(f"System (Remote: [yellow]{remote_system}[/yellow], Local: [yellow]{current_info['system']}[/yellow])")
                if remote_arch and remote_arch != current_info["architecture"]:
                    mismatch.append(f"Architecture (Remote: [yellow]{remote_arch}[/yellow], Local: [yellow]{current_info['architecture']}[/yellow])")
                
                if mismatch:
                    from rich.panel import Panel
                    self.console.print(
                        Panel(
                            "[bold yellow]ENVIRONMENT MISMATCH WARNING:[/bold yellow]\n\n"
                            + "This backup was created in a different environment:\n"
                            + "\n".join([f"- {m}" for m in mismatch])
                            + "\n\n[white]Restoring might lead to path or permission issues.[/white]",
                            title="Compatibility Warning",
                            border_style="yellow",
                        )
                    )
                    if not typer.confirm("Do you want to proceed with restoration?", default=True):
                        zip_file.unlink()
                        self.console.print("[red]Restoration aborted by user.[/red]")
                        return
        except Exception as e:
            self.console.print(f"[dim]Note: Could not verify environment/traceability ({str(e)}). Proceeding...[/dim]")

        if zip_file.name.endswith(".enc"):
            self.console.print("[yellow]Encrypted file detected.[/yellow]")
            password = os.getenv("WORKSTATE_ENCRYPTION_PASSWORD")
            if not password:
                password = typer.prompt("Encryption password", hide_input=True)
            
            with self.console.status("[bold green]Decrypting data...", spinner="dots"):
                try:
                    encrypted_zip = zip_file
                    zip_file = utils.decrypt_file(encrypted_zip, password)
                    encrypted_zip.unlink() # Remove the encrypted file
                except Exception as e:
                    self.console.print("[red]Decryption failed. Check your password.[/red]")
                    encrypted_zip.unlink()
                    raise e

        if self.only_download:
            self.console.print("[blue]Only downloaded file. Skipped unpacking.[/blue]")
        else:
            file_service.unzip(zip_file)
            zip_file.unlink()
            self.console.print("[green]✔ State restored successfully.[/green]\n")
