import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.commands.init_command import InitCommandImpl

def test_init_creates_workstateinclude_instead_of_ignore():
    """
    Given: An InitCommand for a new project
    When: The command is executed
    Then: It should create a .workstateinclude file
    And: It should NOT create a legacy .workstateignore file
    """
    # Arrange
    mock_console = MagicMock()
    mock_file_svc = MagicMock()
    
    command = InitCommandImpl(
        tool="default",
        console=mock_console,
        file_service=mock_file_svc
    )

    # Act
    command.execute()
    
    # Assert
    mock_file_svc.create_workstateinclude.assert_called_once()
    mock_file_svc.create_workstateignore.assert_not_called()
