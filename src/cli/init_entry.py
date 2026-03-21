import typer
from rich.console import Console

from src.services import file_service
from src.utils.utils import handle_error
from src.constants.messages import VALID_CODE_TOOLS_OPTIONS
from src.templates.code_tool import CodeTool
from src.commands.init_command import InitCommandImpl


def register(app: typer, console: Console, file_service: file_service):
    @app.command("init", help="Initializes a new Workstate project with .workstateignore file template")
    def init(
        tool: str = typer.Option("auto", "--tool", "-t", help=VALID_CODE_TOOLS_OPTIONS),
        profile: str = typer.Option(None, "--profile", "-p", help="Use a specific saved profile instead of default templates")
    ) -> None:
        """Initializes a new Workstate project with .workstateignore file template

        Creates a .workstateignore file in the current directory with a pre-configured template
        based on the specified development tool.
        The template contains exclusion rules optimized for each project type.

        Args:
            tool (str): Development tool type. Valid options include
                'python', 'node', 'java', 'go', etc. Default: 'generic'.

        Examples:
            ```bash
            $ workstate init --tool python
            $ workstate init -t node
            $ workstate init  # uses generic template
            ```

        Notes:
            - If a .workstateignore file already exists, nothing will be done.
            - Each tool has specific optimized exclusion rules.
            - The template can be manually edited after creation.
        """
        try:
            InitCommandImpl(tool=tool, console=console, file_service=file_service, profile=profile).execute()
        except Exception as e:
            handle_error(console, e)
