"""Clipboard utilities for copying text to the system clipboard.

This module provides a cross-platform way to copy text to the clipboard
using the pyperclip library.
"""

import pyperclip
from rich.console import Console


def copy_to_clipboard(text: str, console: Console | None = None) -> bool:
    """Copies the given text to the system clipboard.

    Args:
        text (str): The text to copy.
        console (Console, optional): Rich console for printing status messages.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        pyperclip.copy(text)
        if console:
            console.print("[green]Link copied to clipboard automatically![/green]")
        return True
    except Exception as e:
        if console:
            console.print(f"[yellow]Warning: Could not copy to clipboard: {e}[/yellow]")
            console.print("[yellow]You may need to install 'xclip' or 'xsel' on Linux.[/yellow]")
        return False
