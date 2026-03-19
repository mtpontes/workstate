import subprocess
from pathlib import Path
from typing import Dict, Optional

def get_git_info() -> Dict[str, str]:
    """
    Returns the current Git branch and full commit hash if in a Git repository.
    
    Returns:
        Dict[str, str]: {
            "Git-Branch": str,
            "Git-Commit": str
        } (Keys missing if not in a Git repo)
    """
    info = {}
    try:
        # Check if it's a git repo
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.STDOUT)
        
        info["Git-Branch"] = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], 
            stderr=subprocess.STDOUT
        ).decode().strip()
        
        info["Git-Commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], 
            stderr=subprocess.STDOUT
        ).decode().strip()
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
        
    return info

def get_git_root() -> Optional[Path]:
    """
    Returns the absolute path to the root of the Git repository.
    """
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], 
            stderr=subprocess.STDOUT
        ).decode().strip()
        return Path(root)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def get_commit_short_hash(commit_hash: str) -> str:
    """Returns the first 7 characters of a commit hash."""
    if not commit_hash or len(commit_hash) < 7:
        return commit_hash
    return commit_hash[:7]
