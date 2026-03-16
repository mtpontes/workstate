import typer
from rich.console import Console

from src.commands.report_command import ReportCommandImpl

def register(app: typer.Typer, console: Console) -> None:
    @app.command(name="report")
    def report(
        tags: str = typer.Option(
            "Project", 
            "--tags", "-t", 
            help="Comma-separated list of S3 tags to group by (e.g., Project,Branch,Environment)"
        )
    ):
        """
        Generate a report of storage consumption and estimated costs.
        """
        command = ReportCommandImpl(console, tags=tags)
        command.execute()
