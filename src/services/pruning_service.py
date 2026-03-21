from datetime import datetime
from typing import List
from mypy_boto3_s3.service_resource import ObjectSummary
from rich.console import Console

from src.services import state_service
from src.utils import utils

class PruningService:
    def __init__(self, console: Console = None):
        self.console = console or Console()

    def get_candidates(self, older_than: str, global_scan: bool = False) -> List[ObjectSummary]:
        """
        Identify state files older than the specified duration, respecting protection.
        """
        # list_states already handles the older_than filtering using LastModified
        states = state_service.list_states(older_than=older_than, global_scan=global_scan)
        
        candidates = []
        for state in states:
            # Although list_states filters by time, we re-verify and check for protection
            if not state_service.is_protected(state.key):
                candidates.append(state)
            else:
                if global_scan or not state.key.startswith(state_service._get_prefix()):
                     # If it's global or another project, we don't necessarily log unless it's the one we'd delete
                     pass
                else:
                    self.console.print(f"[yellow]Skipping protected state:[/yellow] {state.key}")
        
        return candidates

    def prune(self, candidates: List[ObjectSummary]) -> int:
        """
        Delete the specified candidate states.
        Returns:
            int: Number of deleted files.
        """
        deleted_count = 0
        for cand in candidates:
            try:
                state_service.delete_state_file(cand.key)
                deleted_count += 1
            except Exception as e:
                self.console.print(f"[red]Error deleting {cand.key}:[/red] {str(e)}")
        
        return deleted_count
