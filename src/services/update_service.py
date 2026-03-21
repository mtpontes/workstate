import requests
import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from src.constants import constants
from src.services.config_service import ConfigService

class UpdateService:
    GITHUB_API_URL = "https://api.github.com/repos/mtpontes/workstate/releases/latest"
    
    def __init__(self, console: Console, config_service: ConfigService):
        self.console = console
        self.config_service = config_service

    def check_for_updates(self) -> None:
        """
        Main entry point for update checking.
        Checks if a check is needed (once a day) and performs it.
        """
        if not self._should_check():
            return

        try:
            # Short timeout to avoid blocking startup too long if network is slow
            response = requests.get(self.GITHUB_API_URL, timeout=2.0)
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("tag_name", "").replace("v", "")
                
                if self._is_newer(latest_version, constants.VERSION):
                    self._display_update_message(latest_version)
                
                # Update last check timestamp
                self._update_last_check_timestamp()
        except Exception:
            # Silent fail for network errors
            pass

    def _should_check(self) -> bool:
        """Checks if 24h have passed since last check."""
        config = self.config_service.get_config()
        last_check = config.get("last_update_check")
        
        if not last_check:
            return True
        
        try:
            last_date = datetime.datetime.fromisoformat(last_check)
            return (datetime.datetime.now() - last_date).total_seconds() > 86400
        except (ValueError, TypeError):
            return True

    def _update_last_check_timestamp(self) -> None:
        """Updates the timestamp in the config file."""
        config = self.config_service.get_config()
        config["last_update_check"] = datetime.datetime.now().isoformat()
        # Note: ConfigService needs a save method or we call it here if available
        # I'll check ConfigService to see how it saves.
        self.config_service.save_config(config)

    def _is_newer(self, latest: str, current: str) -> bool:
        """Simple SemVer comparison."""
        try:
            l_parts = [int(p) for p in latest.split(".")]
            c_parts = [int(p) for p in current.split(".")]
            return l_parts > c_parts
        except (ValueError, AttributeError):
            return False

    def _display_update_message(self, latest_version: str) -> None:
        self.console.print(Panel(
            f"[bold yellow]New version available: {latest_version}[/bold yellow]\n"
            f"You are currently using version {constants.VERSION}.\n\n"
            "Download it at: [link=https://github.com/mtpontes/workstate/releases]https://github.com/mtpontes/workstate/releases[/link]",
            title="Update Notification",
            border_style="yellow"
        ))
