from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.commands.command import CommandI
from src.services.report_service import ReportService
from src.utils import utils

class ReportCommandImpl(CommandI):
    def __init__(
        self,
        console: Console,
        tags: str = None
    ) -> None:
        self.console = console
        # Convert comma-separated string to list
        self.group_tags = [t.strip() for t in tags.split(",")] if tags else ["Project"]

    def execute(self) -> None:
        with self.console.status("[bold green]Generating storage report...", spinner="dots"):
            try:
                report = ReportService.get_storage_report(group_by_tags=self.group_tags)
            except Exception as e:
                utils.handle_error(self.console, e)
                return

        if not report["groups"]:
            self.console.print("[yellow]No backups found in the bucket.[/yellow]")
            return

        # Display header
        self.console.print(
            Panel(
                f"[bold blue]Storage Consumption Report[/bold blue]\n"
                f"Grouped by: [cyan]{', '.join(self.group_tags)}[/cyan]",
                expand=False
            )
        )

        # Create table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Grouping (" + " | ".join(self.group_tags) + ")", style="dim")
        table.add_column("Objects", justify="right")
        table.add_column("Size", justify="right")
        table.add_column("Est. Monthly Cost", justify="right", style="green")

        # Sort groups by size descending
        sorted_groups = sorted(
            report["groups"].items(), 
            key=lambda x: x[1]["size_bytes"], 
            reverse=True
        )

        for group_key, data in sorted_groups:
            size_formatted = utils.format_file_size(data["size_bytes"])
            gb = data["size_bytes"] / (1024**3)
            cost = gb * 0.023 # Match service value
            
            table.add_row(
                group_key,
                str(data["object_count"]),
                size_formatted,
                f"${cost:.4f}"
            )

        self.console.print(table)

        # Totals Panel
        totals = report["totals"]
        total_size = utils.format_file_size(totals["total_size_bytes"])
        
        self.console.print(
            Panel(
                f"[bold]Total Objects:[/bold] {totals['total_objects']}\n"
                f"[bold]Total Size:[/bold] {total_size}\n"
                f"[bold]Estimated Monthly Cost:[/bold] [green]${totals['total_cost_est']:.4f}[/green]\n\n"
                f"[dim]* Est. cost based on $0.023/GB (S3 Standard)[/dim]",
                title="Grand Totals",
                border_style="blue",
                expand=False
            )
        )
