import pytest
from unittest.mock import MagicMock, patch
from src.commands.list_command import ListCommandImpl

def test_list_command_defaults_to_global_scan():
    """
    Given: A ListCommand without specific filters
    When: The command is executed
    Then: It should call list_states with global_scan=True by default
    """
    # Arrange
    mock_console = MagicMock()
    mock_views = MagicMock()
    mock_state_svc = MagicMock()
    
    command = ListCommandImpl(
        console=mock_console,
        views=mock_views,
        state_service=mock_state_svc
    )
    
    # Act
    with patch("src.commands.list_command.s3_client.validate_credentials", return_value=True):
        command.execute()
    
    # Assert
    mock_state_svc.list_states.assert_called_with(
        system=None,
        branch=None,
        older_than=None,
        use_cache=True,
        global_scan=True
    )
