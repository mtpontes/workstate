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
from InquirerPy import inquirer
from rich.console import Console
from InquirerPy.utils import get_style
from mypy_boto3_s3.service_resource import ObjectSummary

from src.utils import utils
from src.services import state_service
from src.constants.constants import DATE_PATTERN, SPACE
from src.api.prompters.string_prompter import StringPrompterI


class ZipFileSelectorPrompter(StringPrompterI):
    def __init__(self, console: Console, state_service: state_service):
        self.console = console
        self.state_service = state_service

    def prompt(self) -> str:
        with self.console.status("[bold green]Fetching state files from S3...", spinner="dots"):
            zip_files: list[ObjectSummary] = self.state_service.get_state_files()
        if not zip_files:
            self.console.print("[yellow]No ZIP files found in the S3 bucket.[/yellow]")
            raise typer.Exit(0)

        choices = [
            {
                "name": f"{obj.key.ljust(40, SPACE)} | Size: {utils.format_file_size(obj.size).ljust(10)} | Last Modified: {obj.last_modified.strftime(DATE_PATTERN)}",
                "value": obj.key,
            }
            for obj in zip_files
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
        return inquirer.select(
            message="Select a zip file to download:",
            choices=choices,
            instruction="Use ↑/↓ to navigate and Enter to select",
            vi_mode=True,
            style=custom_style,
        ).execute()
