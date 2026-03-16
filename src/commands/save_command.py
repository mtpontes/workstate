"""
Module responsible for implementing the state rescue command.

This module contains the concrete implementation of the command to create and save
SNAPSHOTS OF THE CURRENT STATE OF PROJECT IN REMOTE STORAGE. The command
selects relevant files, compact in an ZIP file and performs
Upload to preserve the state of the project.

The module manages the entire backup process, including smart selection
files, temporary compaction, upload for remote storage and
Cleaning temporary files after the rescue process.
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
from rich.table import Table
from rich.panel import Panel

from src.utils import utils
from src.services import file_service, state_service
from src.commands.command import CommandI


class SaveCommandImpl(CommandI):
    def __init__(
        self,
        state_name: str,
        console: Console,
        file_service: file_service,
        state_service: state_service,
        dry_run: bool = False,
        encrypt: bool = False,
        password: str = None,
        force: bool = False,
        description: str = None,
        tags: list[str] = None,
    ) -> None:
        self.state_name = state_name
        self.console = console
        self.file_service = file_service
        self.state_service = state_service
        self.dry_run = dry_run
        self.encrypt = encrypt
        self.password = password
        self.force = force
        self.description = description
        self.tags = tags


    def execute(self) -> None:
        files_to_save: list[Path] = self.file_service.select_files()

        # Sensitive files scan
        sensitive_files = self.file_service.scan_for_sensitive_files(files_to_save)
        if sensitive_files and not self.force:
            self.console.print(
                Panel(
                    "[bold red]DANGER:[/bold red] Sensitive files detected in the backup list!\n\n"
                    + "\n".join([f"- [yellow]{f.relative_to(Path.cwd())}[/yellow]" for f in sensitive_files])
                    + "\n\n[bold white]Uploading these files to the cloud can be dangerous.[/bold white]",
                    title="Security Warning",
                    border_style="red",
                )
            )
            import typer
            if not typer.confirm("Do you want to proceed anyway?", default=False):
                self.console.print("[red]Operation aborted by user.[/red]")
                return

        total_size_bytes = self.file_service.calculate_total_files_in_bytes(files_to_save)
        formatted_size = utils.format_file_size(total_size_bytes)


        if total_size_bytes > 500 * 1024 * 1024:
            self.console.print(
                Panel(
                    f"[bold yellow]WARNING:[/bold yellow] The total size of selected files ({formatted_size}) exceeds the recommended limit of 500MB.\n"
                    "Upload and download may be slow.",
                    border_style="yellow",
                )
            )

        if self.dry_run:
            self.console.print(f"\n[bold blue]DRY-RUN MODE[/bold blue]")
            self.console.print(f"Files that would be saved for state [green]'{self.state_name}'[/green]:\n")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("File Path", style="dim")
            table.add_column("Size", justify="right")

            for file in files_to_save:
                table.add_row(str(file.relative_to(Path.cwd())), utils.format_file_size(file.stat().st_size))

            self.console.print(table)
            self.console.print(f"\n[bold]Total files:[/bold] {len(files_to_save)}")
            self.console.print(f"[bold]Estimated total size:[/bold] {formatted_size}")
            self.console.print(f"\n[blue]No files were zipped or uploaded.[/blue]\n")
            return

        with self.console.status("[bold green]Zipping files...", spinner="dots"):
            # Prepare metadata for .metadata.json inside ZIP
            system_info = utils.get_system_info()
            git_info = utils.get_git_info()
            
            metadata = {
                "state_name": self.state_name,
                "description": self.description,
                "system": system_info,
                "git": git_info,
                "timestamp": utils.get_current_timestamp() if hasattr(utils, 'get_current_timestamp') else None
            }
            
            # Process custom tags
            custom_tags_dict = {}
            if self.tags:
                for tag_str in self.tags:
                    if "=" in tag_str:
                        key, value = tag_str.split("=", 1)
                        custom_tags_dict[key.strip()] = value.strip()
            
            metadata["custom_tags"] = custom_tags_dict

            temporary_file_to_upload: Path = self.file_service.zip_files(files_to_save, metadata=metadata)

        zip_file_name: str = utils.define_zip_file_name(self.state_name)

        if self.encrypt and self.password:
            with self.console.status("[bold green]Encrypting data...", spinner="dots"):
                original_zip = temporary_file_to_upload
                temporary_file_to_upload = utils.encrypt_file(original_zip, self.password)
                original_zip.unlink() # Remove the unencrypted zip
                zip_file_name += ".enc"

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
            upload_task = progress.add_task(
                f"Uploading {zip_file_name}", total=temporary_file_to_upload.stat().st_size
            )

            def progress_callback(bytes_amount):
                progress.update(upload_task, advance=bytes_amount)

            # Collect metadata for S3 tags
            s3_tags = {
                "System": system_info,
            }
            s3_tags.update(git_info)
            if self.description:
                s3_tags["Description"] = self.description[:255] # S3 tag value limit
            
            s3_tags.update(custom_tags_dict)

            self.state_service.save_state_file(
                temporary_file_to_upload, zip_file_name, callback=progress_callback, tags=s3_tags
            )

        temporary_file_to_upload.unlink()

        self.console.print(
            f"\n[bold green]✔ State '{self.state_name}' saved successfully to S3 as '{zip_file_name}'[/bold green]\n"
        )
