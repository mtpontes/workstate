import typer
from rich.console import Console
from src.services.hook_service import HookService
from src.commands.git_hook_command import GitHookCommandImpl
from src.utils.utils import handle_error

def register(app: typer.Typer, console: Console, hook_service: HookService):
    git_hook_app = typer.Typer(help="Manage Git hooks for automatic environment state tracking")
    app.add_typer(git_hook_app, name="git-hook")

    @git_hook_app.command("install", help="Install Workstate git hooks (post-checkout, pre-push)")
    def install_hooks(
        checkout: bool = typer.Option(True, "--checkout/--no-checkout", help="Install post-checkout hook (branch change)"),
        push: bool = typer.Option(True, "--push/--no-push", help="Install pre-push hook (git push)")
    ) -> None:
        """
        Installs Workstate git hooks in the current repository.
        
        Hooks:
        - post-checkout: Reminds to restore state after branch change (covers checkout and switch).
        - pre-push: Reminds to save state before pushing.
        """
        try:
            GitHookCommandImpl(console, hook_service).execute(checkout=checkout, push=push)
        except Exception as e:
            handle_error(console, e)

    @git_hook_app.command("uninstall", help="Remove Workstate git hooks from the current repository")
    def uninstall_hooks() -> None:
        """
        Removes Workstate git hooks from the current repository.
        """
        try:
            GitHookCommandImpl(console, hook_service).uninstall()
        except Exception as e:
            handle_error(console, e)
