from rich.console import Console
from src.services.hook_service import HookService
from src.utils import git_utils
from src.exception.workstate_exception import WorkstateException

class GitHookCommandImpl:
    def __init__(self, console: Console, hook_service: HookService):
        self.console = console
        self.hook_service = hook_service

    def execute(self, checkout: bool = True, push: bool = True) -> None:
        """
        Executes the git-hook install command.
        """
        self.console.print("[bold blue]Checking Git repository...[/bold blue]")
        
        git_root = git_utils.get_git_root()
        if not git_root:
            raise WorkstateException("Not a git repository (or any of the parent directories).")

        self.console.print(f"[green][OK] Git repository found at:[/green] {git_root}")
        
        with self.console.status("[bold blue]Installing hooks...[/bold blue]"):
            installed_hooks = self.hook_service.install_git_hooks(
                git_root, 
                install_post_checkout=checkout, 
                install_pre_push=push
            )

        if not installed_hooks:
            self.console.print("[yellow]! No hooks were installed (they might be already present or none selected).[/yellow]")
        else:
            self.console.print("[green][OK] Git hooks installed successfully:[/green]")
            for hook in installed_hooks:
                self.console.print(f"  - {hook}")
            
            self.console.print("\n[dim]Note: Hooks are stored in .git/hooks/ and will run during git operations.[/dim]")

    def uninstall(self) -> None:
        """
        Executes the git-hook uninstall command.
        """
        self.console.print("[bold blue]Checking Git repository...[/bold blue]")
        
        git_root = git_utils.get_git_root()
        if not git_root:
            raise WorkstateException("Not a git repository (or any of the parent directories).")

        self.console.print(f"[green][OK] Git repository found at:[/green] {git_root}")
        
        with self.console.status("[bold blue]Removing hooks...[/bold blue]"):
            removed_hooks = self.hook_service.uninstall_git_hooks(git_root)

        if not removed_hooks:
            self.console.print("[yellow]! No Workstate hooks were found to remove.[/yellow]")
        else:
            self.console.print("[green][OK] Git hooks removed successfully:[/green]")
            for hook in removed_hooks:
                self.console.print(f"  - {hook}")
