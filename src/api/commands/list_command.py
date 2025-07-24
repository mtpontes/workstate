from rich.table import Table
from rich.console import Console
from mypy_boto3_s3.service_resource import ObjectSummary

from src.utils import utils
from src.clients import s3_client
from src.services import state_service
from src.api.commands.command import CommandI


class ListCommandImpl(CommandI):
    def __init__(self, console: Console, s3_client: s3_client, state_service: state_service):
        self.console = console
        self.s3_client = s3_client
        self.state_service = state_service

    def execute(self) -> Table:
        s3_objects: list[ObjectSummary] = self.s3_client.list_objects()
        zip_files: list[ObjectSummary] = self.state_service.filter_zip_files(s3_objects)

        table = Table(title="\nZIP files on S3", show_header=True, header_style="bold white")
        table.add_column("File", style="cyan")
        table.add_column("Size", style="yellow3")
        table.add_column("Last Modified", style="magenta")

        for obj in zip_files:
            table.add_row(obj.key, utils.format_file_size(obj.size), str(obj.last_modified.astimezone()))

        self.console.print(table)
        self.console.print()
