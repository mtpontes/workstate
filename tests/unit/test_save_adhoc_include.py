import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.commands.save_command import SaveCommandImpl

def test_save_command_passes_extra_includes_to_service():
    """
    Given: A SaveCommand with extra_includes defined
    When: The command is executed
    Then: It should call select_files on FileService with the extra_includes list
    """
    # Arrange
    mock_console = MagicMock()
    mock_file_svc = MagicMock()
    mock_file_svc.scan_for_sensitive_files.return_value = []
    mock_file_svc.scan_files_for_secrets.return_value = []
    mock_file_svc.calculate_total_files_in_bytes.return_value = 100
    dummy_zip = MagicMock()
    dummy_zip.stat.return_value.st_size = 100
    mock_file_svc.zip_files.return_value = dummy_zip
    mock_state_svc = MagicMock()
    mock_state_svc.save_state_file = MagicMock()
    
    command = SaveCommandImpl(
        state_name="test-state",
        console=mock_console,
        file_service=mock_file_svc,
        state_service=mock_state_svc,
        extra_includes=["adhoc.txt"]
    )
    
    # Act
    with patch("src.commands.save_command.s3_client.validate_credentials", return_value=True):
        command.execute()
    
    # Assert
    mock_file_svc.select_files.assert_called_with(extra_includes=["adhoc.txt"])
