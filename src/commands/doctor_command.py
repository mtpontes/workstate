"""
Module responsible for the implementation of the project diagnostic command.

This module contains the concrete implementation of the command that checks
the health of the local configuration and the connectivity with AWS services.
"""

from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from botocore.exceptions import ClientError

from src.clients import s3_client
from src.services.config_service import ConfigService
from src.commands.command import CommandI


class DoctorCommandImpl(CommandI):
    def __init__(self, console: Console) -> None:
        self.console = console

    def execute(self) -> None:
        """Runs diagnostics on the local environment and AWS connectivity."""
        self.console.print("\n[bold white]Workstate Diagnosis[/bold white]\n")

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Check", style="dim", width=30)
        table.add_column("Status", width=10, justify="center")
        table.add_column("Message", width=45)

        # 1. Local Configuration Check
        config_ok, config_msg = self._check_local_config()
        table.add_row("Local Configuration", "[green]OK[/green]" if config_ok else "[red]FAIL[/red]", config_msg)

        # 2. AWS Connectivity Check (STS)
        aws_ok = False
        if config_ok:
            aws_ok, aws_msg = self._check_aws_connectivity()
            table.add_row("AWS Connectivity", "[green]OK[/green]" if aws_ok else "[red]FAIL[/red]", aws_msg)
        else:
            table.add_row("AWS Connectivity", "[yellow]SKIP[/yellow]", "Fix local configuration first")

        # 3. S3 Bucket & Operations Check
        if aws_ok:
            s3_ok, s3_msg = self._check_s3_operations()
            table.add_row("S3 Bucket Access", "[green]OK[/green]" if s3_ok else "[red]FAIL[/red]", s3_msg)
        else:
            table.add_row("S3 Bucket Access", "[yellow]SKIP[/yellow]", "Fix AWS connectivity first")

        self.console.print(table)
        self.console.print("\n")

        if not (config_ok and aws_ok and (not aws_ok or s3_ok)):
            self.console.print(Panel(
                "[bold red]Diagnostics failed.[/bold red]\nPlease follow the suggestions in the 'Message' column.",
                border_style="red"
            ))
        else:
            self.console.print("[bold green][OK] All systems operational![/bold green]\n")

    def _check_local_config(self) -> tuple[bool, str]:
        """Verifies if the configuration file exists and is valid."""
        config_file = ConfigService.CONFIG_FILE
        if not config_file.exists():
            return False, "Config file not found. Run 'workstate configure'"
        
        try:
            config = ConfigService.load_config()
            if not config.get("aws"):
                return False, "AWS credentials not found in config"
            return True, f"Config file valid: {config_file}"
        except Exception as e:
            return False, f"Error reading config: {str(e)}"

    def _check_aws_connectivity(self) -> tuple[bool, str]:
        """Tests AWS connectivity using STS get_caller_identity."""
        try:
            client = s3_client.create_sts_client()
            identity = client.get_caller_identity()
            return True, f"Identified as User/Role: {identity.get('Arn').split('/')[-1]}"
        except ClientError as e:
            return False, f"AWS authentication failed: {e.response['Error']['Message']}"
        except Exception as e:
            return False, f"Unexpected AWS error: {str(e)}"

    def _check_s3_operations(self) -> tuple[bool, str]:
        """Tests bucket existence and basic operations (Put/Delete)."""
        try:
            creds = ConfigService.get_aws_credentials()
            bucket_name = creds.bucket_name
            s3 = s3_client.create_s3_client()

            # Check if bucket exists
            s3.head_bucket(Bucket=bucket_name)

            # Test Write/Delete operation
            test_key = "doctor-connectivity-test.tmp"
            s3.put_object(Bucket=bucket_name, Key=test_key, Body=b"workstate-doctor-test")
            s3.delete_object(Bucket=bucket_name, Key=test_key)

            return True, f"Full access to bucket: {bucket_name}"
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code == "404":
                return False, f"Bucket '{bucket_name}' not found"
            if code == "403":
                return False, "Access denied. Check your IAM permissions"
            return False, f"S3 Error: {e.response['Error']['Message']}"
        except Exception as e:
            return False, f"Unexpected S3 error: {str(e)}"
