import typer
from rich.console import Console

from src.utils.utils import handle_error
from src.commands.configure_command import ConfigureCommandImpl
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
from src.prompts.aws_credentials_setup_prompter import AWSCredentialsSetupPrompter


def register(app: typer, console: Console):
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
            credentials = AWSCredentialsDTO(
                access_key_id=access_key_id, secret_access_key=secret_access_key, bucket_name=bucket_name, region=region
            )
            prompter = AWSCredentialsSetupPrompter(console=console, new_credentials=credentials)

            ConfigureCommandImpl(
                interactive=interactive, console=console, prompter=prompter, credentials=credentials
            ).execute()

        except KeyboardInterrupt:
            console.print("\n[yellow]Configuration cancelled by user[/yellow]")
            raise typer.Exit(0)
        except Exception as e:
            handle_error(console, e)
