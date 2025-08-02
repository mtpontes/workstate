from datetime import datetime

from rich.panel import Panel
from rich.text import Text

from src.utils import utils


def share_info_panel(selected_state: str, presigned_url: str, expiration_time: datetime) -> None:
    """Display the shareable URL and instructions."""
    info_text = Text()
    info_text.append("State: ", style="bold blue")
    info_text.append(f"{selected_state}\n", style="white")
    info_text.append("Expires: ", style="bold blue")
    info_text.append(f"{expiration_time.strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n", style="white")

    info_text.append("Workstate CLI args:\n", style="bold green")
    base_url, signature, expires = utils.destructure_pre_signed_url(presigned_url)
    info_text.append("  • Base url: " + base_url + "\n", style="cyan")
    info_text.append("  • Signature: " + signature + "\n", style="cyan")
    info_text.append("  • Expires: " + expires + "\n", style="cyan")

    info_text.append("Browser URL:\n", style="bold green")
    info_text.append(presigned_url + "\n", style="cyan")

    return Panel(
        info_text,
        title="[bold green]✔ Share URL Generated Successfully",
        title_align="left",
        border_style="green",
        padding=(1, 2),
    )


def usage_instructions(url: str, expiration_hours: int):
    instructions = Text()
    instructions.append("\nUsage Instructions:\n", style="bold yellow")
    instructions.append("  • Paste the browser URL in any web browser\n", style="white")
    instructions.append("  • Use the terminal-safe version in PowerShell/CMD scripts\n", style="white")
    instructions.append("  • Download with curl:\n", style="white")
    instructions.append("  • Or use Workstate CLI:\n", style="white")

    base_url, signature, expires = utils.destructure_pre_signed_url(url)
    instructions.append(
        f'    workstate download-url --base-url "{base_url} --signature "{signature}" --expires "{expires}" \n',
        style="dim",
    )

    instructions.append(f"\n  • URL expires in {expiration_hours} hours\n", style="white")

    instructions.append("\nSecurity Note: ", style="bold red")
    instructions.append("Anyone with this URL can download the state file until it expires.\n", style="white")
    return instructions
