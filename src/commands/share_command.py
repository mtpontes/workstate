"""Share Command Implementation.

This module implements the share command that generates pre-signed URLs
for AWS S3 objects, allowing secure temporary access to project states
without requiring AWS credentials.
"""

from datetime import datetime, timedelta

from rich.text import Text
from rich.console import Console

from src.services import state_service
from src.views import share_info_view
from src.prompts.zip_file_selector_prompter import ZipFileSelectorPrompter


class ShareCommandImpl:
    def __init__(
        self,
        console: Console,
        prompter: ZipFileSelectorPrompter,
        state_service: state_service,
        view: share_info_view,
        expiration_hours: int = 24,
    ):
        self.console = console
        self.prompter = prompter
        self.state_service = state_service
        self.view = view
        self.expiration_hours = expiration_hours

    def execute(self) -> None:
        try:
            selected_state: str | None = self.prompter.prompt()
            if not selected_state:
                self.console.print("[yellow]No state selected.[/yellow]")
                return

            presigned_url: str = self._generate_pre_signed_key(selected_state)
            expiration_time: datetime = datetime.now() + timedelta(hours=self.expiration_hours)
            self._display_share_info(selected_state, presigned_url, expiration_time)
        except Exception as e:
            raise e

    def _generate_pre_signed_key(self, selected_state) -> str:
        with self.console.status("[bold blue]Generating pre-signed URL..."):
            presigned_url = self.state_service.generate_presigned_url(
                object_key=selected_state, expiration_seconds=self.expiration_hours * 3600
            )

        return presigned_url

    def _display_share_info(self, selected_state: str, presigned_url: str, expiration_time: datetime) -> None:
        panel = self.view.share_info_panel(selected_state, presigned_url, expiration_time)
        self.console.print(panel)

        instructions: Text = self.view.usage_instructions(presigned_url, self.expiration_hours)
        self.console.print(instructions)
