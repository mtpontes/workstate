import os
from pathlib import Path
from src.constants.constants import WORKSTATE_DIR

def test_log_directory_is_in_home():
    """
    Given the application starts
    When logs are initialized
    Then the log directory should be inside the user's home .workstate folder
    """
    # Arrange
    expected_log_dir = Path.home() / ".workstate" / "logs"
    
    # Act - The import of logs already triggers the directory creation
    from src.utils.logs import LOG_DIR
    
    # Assert
    assert LOG_DIR == expected_log_dir
    assert LOG_DIR.exists()
    assert LOG_DIR.is_dir()
    
    # Additional check: ensure it matches WORKSTATE_DIR from constants
    assert LOG_DIR == WORKSTATE_DIR / "logs"
