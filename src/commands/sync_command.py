import os
from datetime import datetime
from rich.console import Console

from src.commands.command import CommandI
from src.services import state_service, file_service
from src.utils import utils

class SyncCommandImpl(CommandI):
    def __init__(
        self,
        console: Console,
        state_service: state_service,
        file_service: file_service,
        retention: int = 5
    ) -> None:
        self.console = console
        self.state_service = state_service
        self.file_service = file_service
        self.retention = retention

    def execute(self) -> None:
        self.console.print("[bold blue]Starting environment sync...[/bold blue]")

        # 1. Check for changes compared to the last state
        with self.console.status("[bold green]Checking for changes...", spinner="dots"):
            # Get states to find the latest one for comparison
            states = self.state_service.list_states()
            if states:
                latest_state = states[0]
                # Check if it's already identical to save bandwidth
                try:
                    remote_contents = self.state_service.get_state_content(latest_state.key)
                    local_files = self.file_service.select_files()
                    diff = self.file_service.compare_files(local_files, remote_contents)
                    
                    if not any(res["status"] != "EQUAL" for res in diff):
                        self.console.print("[green]✔ No changes detected since last backup. Skipping sync.[/green]")
                        return
                except Exception as e:
                    self.console.print(f"[dim]Note: Could not perform deep comparison ({str(e)}). Proceeding with backup...[/dim]")
            
        # 2. Perform Save
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        sync_name = f"checkpoint-{timestamp}"
        
        from src.commands.save_command import SaveCommandImpl
        save_cmd = SaveCommandImpl(
            state_name=sync_name,
            console=self.console,
            file_service=self.file_service,
            state_service=self.state_service,
            encrypt=False, 
            protect=False,
            force=True  # Ensure it doesn't block on sensitive files during sync
        )
        
        self.console.print(f"Creating checkpoint: [bold cyan]{sync_name}[/bold cyan]")
        save_cmd.execute()

        # 3. Handle Retention
        with self.console.status("[bold yellow]Applying retention policy...", spinner="dots"):
            all_states = self.state_service.list_states()
            checkpoints = [s for s in all_states if "checkpoint-" in s.key]
            
            if len(checkpoints) > self.retention:
                to_delete = checkpoints[self.retention:]
                for state in to_delete:
                    try:
                        self.state_service.delete_state_file(state.key, force=True)
                        self.console.print(f"[dim]Deleted old checkpoint: {state.key}[/dim]")
                    except Exception as e:
                        self.console.print(f"[red]Failed to delete old checkpoint {state.key}:[/red] {str(e)}")

        self.console.print("\n[bold green]✔ Sync completed successfully.[/bold green]")
