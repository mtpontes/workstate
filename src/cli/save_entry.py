import typer
from rich.console import Console

from src.services import file_service, state_service
from src.utils.utils import handle_error
from src.commands.save_command import SaveCommandImpl


def register(app: typer, console: Console, file_service: file_service, state_service: state_service):
    @app.command("save", help="Saves the current state of the project to AWS S3")
    def save_state(
        state_name: str,
        dry_run: bool = typer.Option(
            False, "--dry-run", help="Simulates the save process without uploading"
        ),
        encrypt: bool = typer.Option(
            False, "--encrypt", help="Encrypts the backup before uploading"
        ),
        force: bool = typer.Option(
            False, "--force", "-f", help="Ignores warnings about sensitive files"
        ),
        description: str = typer.Option(
            None, "--description", "-m", help="Motivo ou descrição do backup"
        ),
        tags: list[str] = typer.Option(
            None, "--tag", help="Tags customizadas no formato key=value"
        ),
        protect: bool = typer.Option(
            False, "--protect", "-p", help="Protege o estado contra deleção acidental"
        ),
    ) -> None:
        """Saves the current state of the project to AWS S3

        Performs the complete development environment backup process:
        1. Analyzes the .workstateignore file to determine included files
        2. Scans for sensitive files and alerts the user if found
        3. Creates a temporary ZIP file with the selected files
        4. Uploads the ZIP file to the configured S3 bucket
        5. Removes the local temporary file

        Args:
            state_name (str): Unique identifier name for the project state.
                This will be the name of the ZIP file on S3.
            dry_run (bool): If True, only lists the files that would be saved.
            encrypt (bool): If True, requests a password to encrypt the backup.
            force (bool): If True, ignores warnings about sensitive files.

        Examples:
            ```bash
            $ workstate save my-django-project
            $ workstate save my-secret-project --encrypt
            $ workstate save my-project --force
            ```


        Notes:
            - Requires .workstateignore file valid in the current directory
            - Project name is sanitized for compatibility S3
            - Timestamp is automatically added to the final name of the file
            - Temporary files are automatically cleaned in case of error
        """
        try:
            password = None
            if encrypt:
                import os
                password = os.getenv("WORKSTATE_ENCRYPTION_PASSWORD")
                if not password:
                    password = typer.prompt("Encryption password", hide_input=True, confirmation_prompt=True)

            SaveCommandImpl(
                state_name=state_name,
                console=console,
                file_service=file_service,
                state_service=state_service,
                dry_run=dry_run,
                encrypt=encrypt,
                password=password,
                force=force,
                description=description,
                tags=tags,
                protect=protect,
            ).execute()


        except Exception as e:
            handle_error(console, e)
