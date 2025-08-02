import typer
from rich.console import Console

from src.views import config_view
from src.utils.utils import handle_error
from src.commands.config_command import ConfigCommandImpl


def register(app: typer, console: Console, config_view: config_view):
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
            │  ├─ Secret Access Key ID: AKIA***...              │
            │  ├─ Region: us-east-1                             │
            │  └─ Bucket Name: my-workstate-bucket              │
            │                                                   │
            ╰───────────────────────────────────────────────────╯
            ```
        """
        try:
            ConfigCommandImpl(console, config_view).execute()
        except Exception as e:
            handle_error(console, e)
