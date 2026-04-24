"""
Módulo responsável pela implementação do prompter de seleção de arquivos para download.

Este módulo contém a implementação concreta do sistema de prompts interativos
para permitir que usuários selecionem arquivos de estado do armazenamento
remoto para download. O módulo oferece uma interface de seleção visual com
informações detalhadas sobre cada arquivo disponível.

O módulo gerencia a recuperação da lista de arquivos disponíveis, formatação
das informações (nome, tamanho, data de modificação) em uma interface de
seleção interativa estilizada, e retorna a escolha do usuário para
processamento posterior.
"""

import typer
import typer
from InquirerPy import inquirer
from rich.console import Console
from InquirerPy.utils import get_style
from src.model.dto.state_dto import StateDTO

from src.utils import utils
from src.services import state_service
from src.constants.constants import DATE_PATTERN, SPACE
from src.prompts.string_prompter import StringPrompterI

class ZipFileSelectorPrompter(StringPrompterI):
    def __init__(self, console: Console, state_service: state_service):
        self.console = console
        self.state_service = state_service

    def prompt(self, message: str = "Select a zip file:") -> str:
        with self.console.status("[bold green]Fetching state files from S3...", spinner="dots"):
            zip_files: list[StateDTO] = self.state_service.list_states(global_scan=True)
        if not zip_files:
            self.console.print("[yellow]No ZIP files found in the S3 bucket.[/yellow]")
            raise typer.Exit(0)

        choices = [
            {
                "name": f"{state.key.ljust(40, SPACE)} | Size: {utils.format_file_size(state.size).ljust(10)} | Last Modified: {state.last_modified.strftime(DATE_PATTERN)}",
                "value": state.key,
            }
            for state in zip_files
        ]

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
        method = inquirer.fuzzy if hasattr(inquirer, "fuzzy") else inquirer.select
        return method(
            message=message,
            choices=choices,
            instruction="Use ↑/↓ to navigate, type to filter and Enter to select",
            vi_mode=True,
            style=custom_style,
        ).execute()
