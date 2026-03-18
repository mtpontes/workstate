"""
Module responsible for the implementation of the Project Startup Command.

Este módulo contém a implementação concreta do comando para inicializar
Projects with specific development tool settings.
The command creates necessary configuration files based on the type of
user -specified tool.

The module manages the creation of customs files customs to
different development tools, validating the options provided
and displaying appropriate feedback messages to the user.
"""

from rich.text import Text
from rich.console import Console
from InquirerPy import inquirer
from InquirerPy.utils import get_style

from src.services import file_service
from src.templates.code_tool import CodeTool
from src.commands.command import CommandI


class InitCommandImpl(CommandI):
    def __init__(self, tool: str, console: Console, file_service: file_service, profile: str = None):
        self.console = console
        self.tool = tool
        self.file_service = file_service
        self.profile = profile

    def execute(self) -> None:
        try:
            selected_tool: CodeTool = None
            profile_content: str = None

            # 1. Check if a profile was requested
            if self.profile:
                from src.services.profile_service import ProfileService
                profile_content = ProfileService.get_local_profile(self.profile)
                if not profile_content:
                    self.console.print(f"[red]Error: Profile '{self.profile}' not found locally.[/red]")
                    self.console.print("[italic dim]Tip: Use 'workstate profile pull <name>' if it's on S3.[/italic dim]")
                    return
                self.console.print(f"[bold green]Using Profile:[/bold green] [cyan]{self.profile}[/cyan]")
            
            # 2. If no profile, use tool or auto-detection
            if not profile_content:
                if self.tool == "auto" or self.tool is None:
                    detected_tools = CodeTool.detect_tools()

                    if len(detected_tools) == 1:
                        selected_tool = detected_tools[0]
                        self.console.print(f"[bold green]Detected stack:[/bold green] [cyan]{selected_tool.value}[/cyan]")
                    elif len(detected_tools) > 1:
                        selected_tool = self._prompt_for_tool(detected_tools)
                    else:
                        self.console.print("[yellow]No specific stack detected. Using default generic template.[/yellow]")
                        selected_tool = CodeTool.DEFAULT
                else:
                    selected_tool = CodeTool(self.tool)

            # 3. Create the file
            if profile_content:
                # Manual creation if it's a profile
                from pathlib import Path
                from src.constants.constants import IGNORE_FILE, WRITE_OPERATOR
                ignore_file = Path(IGNORE_FILE)
                if not ignore_file.exists():
                    with ignore_file.open(mode=WRITE_OPERATOR, encoding="utf-8") as f:
                        f.write(f"{profile_content}\n")
                tool_name = self.profile
            else:
                file_service.create_workstateignore(selected_tool)
                tool_name = selected_tool.value

            self.console.print(
                Text(f"\n✔ .workstateignore created for tool/profile '{tool_name}' \n", style="bold green")
            )

        except ValueError as e:
            if "is not a valid CodeTool" in str(e):
                self._print_invalid_tool_error()
            else:
                raise

    def _prompt_for_tool(self, detected_tools: list[CodeTool]) -> CodeTool:
        """Exibe um prompt interativo para o usuário escolher entre as stacks detectadas."""
        choices = [{"name": tool.value, "value": tool} for tool in detected_tools]
        choices.append({"name": "generic (default)", "value": CodeTool.DEFAULT})

        custom_style = get_style(
            {
                "questionmark": "#ef42f5 bold",
                "selected": "cyan bold",
                "pointer": "#58d1e6 bold",
                "instruction": "grey italic",
                "answer": "#ef42f5 bold",
                "question": "",
            }
        )

        selected = inquirer.select(
            message="Multiple stacks detected. Which one would you like to use?",
            choices=choices,
            style=custom_style,
            vi_mode=True,
        ).execute()

        return selected

    def _print_invalid_tool_error(self) -> None:
        message = Text()
        message.append("Error: Invalid tool. Use one of the valid options: ", style="red")
        message.append(CodeTool.get_valid_values(), style="bold magenta")
        message.append("\nOr leave empty for automatic detection.", style="italic dim")
        self.console.print(message)
