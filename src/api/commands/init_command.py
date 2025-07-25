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

from src.services import file_service
from src.api.commands.command import CommandI
from src.templates.code_tool import CodeTool


class InitCommandImpl(CommandI):
    def __init__(self, tool: str, console: Console, file_service: file_service):
        self.console = console
        self.tool = tool
        self.file_service = file_service

    def execute(self) -> None:
        try:
            tool: CodeTool = CodeTool(self.tool)
            file_service.create_workstateignore(tool)

            self.console.print(Text(f"\n✔ .workstateignore created for tool '{self.tool}' \n", style="bold green"))

        except ValueError as e:
            if "is not a valid CodeTool" in str(e):
                message = Text()
                message.append("Error: Invalid tool. Use one of the valid options: ", style="red")
                message.append(CodeTool.get_valid_values(), style="bold magenta")
                self.console.print(message)
            else:
                raise
