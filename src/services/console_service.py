from rich.text import Text
from rich.console import Console


console = Console()


def print_message(message: str | Text) -> None:
    console.print(message)


def print_error(content: str, error: Exception = None) -> str:
    if error is None:
        console.print(f"[red] Error: {content} [/red]")
    else:
        console.print(f"[red] Error: {content} [/red] {error}")
