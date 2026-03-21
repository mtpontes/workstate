import os
import stat
import subprocess
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel

class HookService:
    def __init__(self, console: Console):
        self.console = console
        self.hook_file = ".workstate-hooks"

    def find_hooks(self, root_path: Path) -> list[str]:
        # ... (no changes needed here) ...
        hook_path = root_path / self.hook_file
        if not hook_path.exists():
            return []
        
        with open(hook_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        # Filter empty lines and comments
        commands = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        return commands

    def execute_hooks(self, commands: list[str], auto_confirm: bool = False) -> None:
        """
        Executes a list of shell commands.
        """
        if not commands:
            return

        self.console.print(Panel(
            "\n".join([f"[cyan]> {cmd}[/cyan]" for cmd in commands]),
            title="Post-Restore Hooks Detected",
            border_style="blue"
        ))

        if not auto_confirm:
            if not typer.confirm("Do you want to execute these hooks?", default=True):
                self.console.print("[yellow]Hooks skipped by user.[/yellow]")
                return

        for cmd in commands:
            self.console.print(f"[bold blue]Running:[/bold blue] {cmd}")
            try:
                # Use shell=True to allow complex commands (pipes, etc.)
                result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=False)
                if result.returncode == 0:
                    self.console.print(f"[green]✔ Command finished successfully.[/green]")
            except subprocess.CalledProcessError as e:
                self.console.print(f"[bold red]Error executing command:[/bold red] {cmd}")
                self.console.print(f"[red]{str(e)}[/red]")
                if not auto_confirm:
                    if not typer.confirm("Continue with next hooks?", default=False):
                        break

    def install_git_hooks(self, git_root: Path, install_post_checkout: bool = True, install_pre_push: bool = True) -> list[str]:
        """
        Installs git hooks in the .git/hooks directory.
        Returns a list of installed hooks.
        """
        hooks_dir = git_root / ".git" / "hooks"
        if not hooks_dir.exists():
            os.makedirs(hooks_dir, exist_ok=True)

        installed = []
        
        # post-checkout
        if install_post_checkout:
            post_checkout_path = hooks_dir / "post-checkout"
            self._write_hook(post_checkout_path, self._get_post_checkout_content())
            installed.append("post-checkout")

        # pre-push
        if install_pre_push:
            pre_push_path = hooks_dir / "pre-push"
            self._write_hook(pre_push_path, self._get_pre_push_content())
            installed.append("pre-push")

        return installed

    def _write_hook(self, path: Path, content: str) -> None:
        """Writes hook content and makes it executable."""
        # If exists, we could append, but for now we'll overwrite with a warning or just provide the tool.
        # User global says: "A implementação deve ser resiliente a hooks já existentes"
        # I'll check if it exists and wrap the existing one if needed, or just append.
        
        hook_exists = path.exists()
        
        if hook_exists:
            with open(path, "r", encoding="utf-8") as f:
                existing_content = f.read()
            if "workstate" in existing_content:
                # Already installed
                return
            
            # Append mode
            with open(path, "a", encoding="utf-8") as f:
                f.write("\n\n# Workstate Hook\n")
                f.write(content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write("#!/bin/sh\n\n")
                f.write("# Workstate Hook\n")
                f.write(content)

        # Make executable (UNIX)
        if os.name != "nt":
            import stat
            st = os.stat(path)
            os.chmod(path, st.st_mode | stat.S_IEXEC)

    def _get_post_checkout_content(self) -> str:
        return """
echo ""
echo "--------------------------------------------------------------------------------"
echo "  [Workstate] Branch changed. Remember to restore your state if needed:"
echo "  > $ workstate download"
echo "--------------------------------------------------------------------------------"
echo ""
"""

    def _get_pre_push_content(self) -> str:
        return """
echo ""
echo "--------------------------------------------------------------------------------"
echo "  [Workstate] Pushing changes. Did you remember to save your environment state?"
echo "  > $ workstate save <name>"
echo "  > $ workstate sync"
echo "--------------------------------------------------------------------------------"
echo ""
# Future: Add logic to block if strict_hooks=true and status is not clean
"""

    def uninstall_git_hooks(self, git_root: Path) -> list[str]:
        """
        Removes Workstate scripts from git hooks.
        """
        hooks_dir = git_root / ".git" / "hooks"
        if not hooks_dir.exists():
            return []

        removed = []
        for hook_name in ["post-checkout", "pre-push"]:
            hook_path = hooks_dir / hook_name
            if hook_path.exists():
                if self._remove_workstate_from_hook(hook_path):
                    removed.append(hook_name)
        
        return removed

    def _remove_workstate_from_hook(self, path: Path) -> bool:
        """Removes Workstate specific section from a hook file."""
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "# Workstate Hook" not in content:
            return False

        # If it only contains our hook, just delete the file
        if content.strip().startswith("#!/bin/sh") and "Workstate Hook" in content and content.count("\n") < 20:
             # This is a bit risky but we check for workstate content
             if "$ workstate" in content:
                 path.unlink()
                 return True

        # Otherwise, remove the specific section (this is a simple heuristic)
        # We look for "# Workstate Hook" and remove everything after it if it was appended
        new_content = []
        in_workstate_block = False
        for line in content.splitlines():
            if "# Workstate Hook" in line:
                in_workstate_block = True
                continue
            if in_workstate_block:
                # Basic check to see if we reached next block or end
                # For now, we assume it's at the end or marked.
                # Since we append at the end, this simple approach works.
                continue
            new_content.append(line)
        
        if not new_content or (len(new_content) == 1 and new_content[0].startswith("#!")):
            path.unlink()
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(new_content))
        
        return True
