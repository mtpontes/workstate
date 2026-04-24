"""
Module responsible for manipulating files and directories for Workstate-related operations.

Operations:
    - Creation of the `.workstateignore` file based on the selected tool.
    - Selection of project files, disregarding the defaults defined in `.workstateignore`.
    - Compression of files into a `.zip` file.
    - Extraction of `.zip` files, automatically handling filename conflicts.
    - Calculation of the total size (in bytes) of the selected files.

Functions:
    - create_workstateignore(tool)
    - select_files()
    - zip_files(files)
    - unzip(zip_file)
    - calculate_total_files_in_bytes(files)
"""

import json
import math
import re
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile

import pathspec

from src.constants.constants import (
    DOT_ZIP,
    IGNORE_FILE,
    READ_OPERATOR,
    SENSITIVE_PATTERNS,
    WRITE_BINARY_OPERATOR,
    WRITE_OPERATOR,
)
from src.templates.code_tool import CodeTool
from src.templates.workstate_templates import TEMPLATES_WORKSTATE
from src.utils.logs import log


def scan_for_sensitive_files(files: list[Path]) -> list[Path]:
    """
    Scans the list of files for patterns known to be sensitive (credentials, private keys, etc.).

    Args:
        files (list[Path]): List of files to scan.

    Returns:
        list[Path]: List of sensitive files found.
    """
    sensitive_files = []
    for file in files:
        # Check if the filename or any part of the path matches the sensitive patterns
        # We check the relative path to the current directory
        try:
            relative_path = str(file.relative_to(Path.cwd()))
        except ValueError:
            relative_path = str(file)

        for pattern in SENSITIVE_PATTERNS:
            if pattern in relative_path:
                sensitive_files.append(file)
                break
    return sensitive_files



def create_workstateignore(tool: CodeTool) -> None:
    """
    Creates a `.workstateignore` file with the default content of the specified tool,
    if the file does not already exist.

    Args:
        tool (CodeTool): Code tool (e.g., Terraform, Serverless) used as the basis for generating the template.
    """
    ignore_file: Path = Path(IGNORE_FILE)
    if not ignore_file.exists():
        with ignore_file.open(mode=WRITE_OPERATOR, encoding="utf-8") as f:
            worstateignore_content: str = TEMPLATES_WORKSTATE[tool]
            f.write(f"{worstateignore_content}\n")


def select_files() -> list[Path]:
    """
    Selects all files in the project, ignoring the defaults defined in `.workstateignore`.
    If `.workstateignore` does not exist, all files are returned.

    Returns:
        list[Path]: List of files to be considered.
    """
    root = Path.cwd().resolve()
    all_files = [path for path in root.rglob("*") if path.is_file()]

    ignore_file = root / IGNORE_FILE
    if ignore_file.exists():
        patterns = ignore_file.read_text().splitlines()
        spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
        # Filters ignored files
        ignored = set(root / p for p in spec.match_tree(root))
        files = [file for file in all_files if file not in ignored]
    else:
        log.warning("No %s file found. All files will be selected.", IGNORE_FILE)
        files = all_files

    return files


def zip_files(files: list[Path], metadata: dict = None) -> Path:
    """
    Creates a `.zip` file containing the specified files.

    The generated file is temporary and returns the path for later use.

    Args:
        files(list[Path]): List of files to include in the `.zip`.
        metadata(dict, optional): Metadata to be saved in a `.metadata.json` file inside the ZIP.

    Returns:
        Path: Full path to the created `.zip` file.
    """
    root = Path.cwd().resolve()
    with NamedTemporaryFile(suffix=DOT_ZIP, delete=False) as tmp_file:
        with ZipFile(tmp_file, WRITE_OPERATOR, compression=ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file, arcname=file.relative_to(root))
            
            if metadata:
                zipf.writestr(".metadata.json", json.dumps(metadata, indent=2))
                
        tmp_file_path = Path(tmp_file.name)
        return tmp_file_path


def unzip(zip_file: Path, extract_to: Path = None, path_filters: list[str] = None) -> None:
    """
    Extracts the contents of a .zip file into the specified directory (defaults to current).

    If the extracted file already exists, a new name is automatically generated to prevent overwriting.
    Optional path_filters can be provided to extract only specific files or directories (glob patterns supported).

    Args:
        zip_file (Path): Path to the .zip file to be extracted.
        extract_to (Path, optional): Path where files should be extracted. Defaults to current directory.
        path_filters (list[str], optional): List of glob patterns or path prefixes to extract.
    """
    import fnmatch
    if extract_to is None:
        extract_to = Path.cwd()

    with ZipFile(zip_file, READ_OPERATOR) as zip_ref:
        for member in zip_ref.infolist():
            # Skip metadata file if present and not explicitly requested
            if member.filename == ".metadata.json" and (not path_filters or ".metadata.json" not in path_filters):
                continue
                
            # Filtering logic
            if path_filters:
                match_found = False
                for pattern in path_filters:
                    # Direct prefix match (for directories ending with /)
                    if pattern.endswith("/") and member.filename.startswith(pattern):
                        match_found = True
                        break
                    # Exact match or Glob match
                    if member.filename == pattern or fnmatch.fnmatch(member.filename, pattern):
                        match_found = True
                        break
                
                if not match_found:
                    continue

            extracted_path = extract_to / member.filename

            if member.is_dir():
                extracted_path.mkdir(parents=True, exist_ok=True)
                continue

            extracted_path.parent.mkdir(parents=True, exist_ok=True)

            final_path = _resolve_conflict(extracted_path)

            with zip_ref.open(member) as source_file:
                with final_path.open(WRITE_BINARY_OPERATOR) as target_file:
                    target_file.write(source_file.read())


def _resolve_conflict(path: Path) -> Path:
    """
    Resolves filename conflicts by generating a new sequential name if necessary.

    Args:
        path: Path of the file to be written.

    Returns:
        Path: Adjusted (unique) path for writing.
    """
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    counter = 1
    while True:
        if suffix:
            new_name = f"{stem} ({counter}){suffix}"
        else:
            new_name = f"{stem} ({counter})"
        candidate = parent / new_name
        if not candidate.exists():
            return candidate
        counter += 1


def calculate_total_files_in_bytes(files: list[Path]) -> int:
    """
    Calculates the total size (in bytes) of all files in the list.

    Args:
        files(list[Path]): List of files.

    Returns:
        int: Sum of the total size of the files in bytes.
    """
    return sum(path.stat().st_size for path in files if path.is_file())


def compare_files(local_files: list[Path], remote_contents: list[dict]) -> list[dict]:
    """
    Compares local files with remote state contents.
    
    Args:
        local_files (list[Path]): List of local file paths (absolute).
        remote_contents (list[dict]): List of remote file metadata (from state_service.get_state_content).
        
    Returns:
        list[dict]: List of comparison results with keys: 'status', 'path', 'info'.
                    Status: 'ADDED' (only local), 'DELETED' (only remote), 'MODIFIED' (both, different size), 'EQUAL'.
    """
    results = []
    root = Path.cwd().resolve()
    
    # Map local files by relative path
    local_map = {}
    for f in local_files:
        try:
            rel_path = str(f.relative_to(root)).replace("\\", "/")
            local_map[rel_path] = f.stat().st_size
        except ValueError:
            continue
            
    # Map remote files
    remote_map = {item["filename"]: item["file_size"] for item in remote_contents}
    
    # Process all paths
    all_paths = set(local_map.keys()) | set(remote_map.keys())
    
    for path in sorted(all_paths):
        local_size = local_map.get(path)
        remote_size = remote_map.get(path)
        
        if local_size is not None and remote_size is not None:
            if local_size == remote_size:
                status = "EQUAL"
            else:
                status = "MODIFIED"
            results.append({"status": status, "path": path, "local_size": local_size, "remote_size": remote_size})
        elif local_size is not None:
            results.append({"status": "ADDED", "path": path, "local_size": local_size, "remote_size": None})
        else:
            results.append({"status": "DELETED", "path": path, "local_size": None, "remote_size": remote_size})
            
    return results


def calculate_sha256(file_path: Path) -> str:
    """Calculates SHA256 hash of a file."""
    import hashlib
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def _calculate_entropy(text: str) -> float:
    """Calculates Shannon entropy of a string."""
    if not text:
        return 0.0
    
    probabilities = [text.count(c) / len(text) for c in set(text)]
    entropy = -sum(p * math.log2(p) for p in probabilities)
    return entropy


def _contains_secrets(text: str) -> bool:
    """Checks if text contains secrets based on Regex patterns."""
    patterns = [
        r"AKIA[0-9A-Z]{16}", # AWS Access Key
        r"ASIA[0-9A-Z]{16}", # AWS Session Key
        r"[a-zA-Z0-9+/]{40}", # Generic High-Entropy (potential Secret Key)
        r"ghp_[a-zA-Z0-9]{36}", # GitHub Personal Access Token
        r"AIza[0-9A-Za-z-_]{35}", # Google API Key
    ]
    for pattern in patterns:
        if re.search(pattern, text):
            # For the generic 40-char pattern, check entropy to avoid false positives
            match = re.search(pattern, text)
            if match and len(match.group(0)) == 40:
                if _calculate_entropy(match.group(0)) > 3.0:
                    return True
                continue
            return True
    return False


def scan_file_for_secrets(file_path: str) -> list[str]:
    """Scans a single file for potential secrets."""
    findings = []
    path = Path(file_path)
    
    # Only scan text files or specific extensions
    text_extensions = {'.txt', '.py', '.js', '.ts', '.env', '.json', '.yml', '.yaml', '.tf', '.sh'}
    if path.suffix.lower() not in text_extensions and path.suffix != '':
        return []

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if _contains_secrets(line):
                findings.append(f"Line {i+1}: Potential secret found in {path.name}")
            
            # Additional check for raw high entropy strings in long lines
            elif len(line) > 32:
                # Simple split by whitespace and quotes
                parts = re.split(r"[\s'\"=]+", line)
                for part in parts:
                    if len(part) > 32 and _calculate_entropy(part) > 3.8:
                        findings.append(f"Line {i+1}: High entropy string detected in {path.name}")
                        break
    except Exception as e:
        log.warning("Could not scan file %s: %s", file_path, str(e))
        
    return findings


def scan_files_for_secrets(files: list[Path]) -> list[str]:
    """Scans multiple files for secrets in their content."""
    all_findings = []
    for f in files:
        if f.is_file():
            findings = scan_file_for_secrets(str(f))
            all_findings.extend(findings)
    return all_findings
