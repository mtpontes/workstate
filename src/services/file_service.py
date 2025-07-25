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

from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile

import pathspec

from src.constants.constants import DOT_ZIP, IGNORE_FILE, READ_OPERATOR, WRITE_BINARY_OPERATOR, WRITE_OPERATOR
from src.templates.code_tool import CodeTool
from src.templates.workstate_templates import TEMPLATES_WORKSTATE
from src.utils.logs import log


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


def zip_files(files: list[Path]) -> Path:
    """
    Creates a `.zip` file containing the specified files.

    The generated file is temporary and returns the path for later use.

    Args:
        files(list[Path]): List of files to include in the `.zip`.

    Returns:
        Path: Full path to the created `.zip` file.
    """
    root = Path.cwd().resolve()
    with NamedTemporaryFile(suffix=DOT_ZIP, delete=False) as tmp_file:
        with ZipFile(tmp_file, WRITE_OPERATOR, compression=ZIP_DEFLATED) as zipf:
            for file in files:
                zipf.write(file, arcname=file.relative_to(root))
        tmp_file_path = Path(tmp_file.name)
        return tmp_file_path


def unzip(zip_file: Path) -> None:
    """
    Extracts the contents of a .zip file into the current directory.

    If the extracted file already exists, a new name is automatically generated to prevent overwriting.

    Args:
        zip_file(Path): Path to the .zip file to be extracted.
    """
    extract_to = Path.cwd()

    with ZipFile(zip_file, READ_OPERATOR) as zip_ref:
        for member in zip_ref.infolist():
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
