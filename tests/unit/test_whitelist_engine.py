import pytest
from pathlib import Path
from unittest.mock import patch
from src.services.file_service import select_files
from src.constants.constants import IGNORE_FILE, INCLUDE_FILE

def test_select_files_with_include(tmp_path):
    """
    Given: A project with some files and a .workstateinclude file
    When: select_files is called
    Then: Only files listed in .workstateinclude should be returned
    And: .workstateignore should be disregarded
    """
    # Arrange
    root = tmp_path
    (root / "src").mkdir()
    (root / "src" / "main.py").write_text("print('hello')")
    (root / "src" / "utils.py").write_text("def util(): pass")
    (root / "README.md").write_text("# Project")
    (root / "ignored.txt").write_text("ignored content")
    
    # Create include file
    (root / INCLUDE_FILE).write_text("src/main.py\nREADME.md")
    
    # Create ignore file (to ensure it is IGNORED in favor of include)
    (root / IGNORE_FILE).write_text("README.md")

    # We need to patch Path.cwd() inside src.services.file_service
    with patch("src.services.file_service.Path.cwd", return_value=root):
        # Act
        selected_files = select_files()
        
        # Assert
        selected_paths = [str(f.relative_to(root)).replace("\\", "/") for f in selected_files]
        
        # Current logic will fail this because it doesn't know about INCLUDE_FILE
        # It will return [src/main.py, src/utils.py, ignored.txt, .workstateinclude]
        # Because it ignores README.md due to .workstateignore
        assert "src/main.py" in selected_paths
        assert "README.md" in selected_paths
        assert INCLUDE_FILE in selected_paths
        assert "src/utils.py" not in selected_paths
        assert "ignored.txt" not in selected_paths
        assert len(selected_files) == 3


def test_auto_include_critical_files(tmp_path):
    """
    Given: A project with .workstateinclude that does NOT list itself
    When: select_files is called
    Then: .workstateinclude should be automatically included
    """
    # Arrange
    root = tmp_path
    (root / "main.py").write_text("print('hello')")
    # Include main.py but NOT .workstateinclude
    (root / INCLUDE_FILE).write_text("main.py")

    with patch("src.services.file_service.Path.cwd", return_value=root):
        # Act
        selected_files = select_files()
        
        # Assert
        selected_paths = [str(f.relative_to(root)).replace("\\", "/") for f in selected_files]
        
        assert "main.py" in selected_paths
        assert INCLUDE_FILE in selected_paths # This is expected to fail now
