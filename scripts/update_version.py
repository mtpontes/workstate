import sys
import re
from pathlib import Path

def update_version(new_version: str):
    """
    Updates the version string in pyproject.toml and src/constants/constants.py
    """
    # 1. Update pyproject.toml
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        content = pyproject.read_text(encoding="utf-8")
        # Match version = "x.x.x" in the [project] section
        new_content = re.sub(r'version = "[^"]+"', f'version = "{new_version}"', content, count=1)
        if content != new_content:
            pyproject.write_text(new_content, encoding="utf-8")
            print(f"✓ Updated pyproject.toml to version {new_version}")
        else:
            print("! No version change detected in pyproject.toml")

    # pyproject.toml is now the single source of truth for versioning.
    # src/constants/constants.py reads it dynamically.
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/update_version.py <new_version>")
        sys.exit(1)
    
    version_to_set = sys.argv[1].replace("v", "") # Remove 'v' prefix if present
    update_version(version_to_set)
