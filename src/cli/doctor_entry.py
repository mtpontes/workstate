import typer
from rich.console import Console

from src.utils.utils import handle_error
from src.commands.doctor_command import DoctorCommandImpl


def register(app: typer, console: Console):
    @app.command("doctor", help="Check the health of Workstate configuration and AWS connectivity")
    def doctor() -> None:
        """Runs a series of diagnostic tests to ensure Workstate is correctly configured.

        The command checks:
        - Presence and validity of the local configuration file.
        - Validity of AWS credentials (Access Key and Secret Key).
        - Connectivity and permissions for the configured S3 bucket.

        Examples:
            $ workstate doctor
        """
        try:
            DoctorCommandImpl(console=console).execute()
        except Exception as e:
            handle_error(console, e)
