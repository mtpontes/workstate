import pytest
from pathlib import Path
from src.services import file_service, state_service
from src.commands.download_command import DownloadCommandImpl
from unittest.mock import MagicMock, patch
from rich.console import Console

def test_calculate_sha256_consistency(tmp_path):
    """Garante que o cálculo de SHA256 é consistente."""
    file = tmp_path / "test.txt"
    file.write_text("hello world")
    
    hash1 = file_service.calculate_sha256(file)
    hash2 = file_service.calculate_sha256(file)
    
    assert hash1 == hash2
    assert len(hash1) == 64 # SHA256 hex length

@patch("src.clients.s3_client.create_s3_resource")
def test_download_integrity_failure(mock_s3_resource, tmp_path, monkeypatch):
    """Garante que a restauração falha se o hash não bater."""
    console = Console()
    project = "test-proj"
    zip_name = "state.zip"
    
    # Mock do S3 Object e Metadata
    mock_obj = MagicMock()
    mock_obj.content_length = 100
    mock_obj.metadata = {"state-sha256": "wrong-hash"}
    
    mock_resource = MagicMock()
    mock_resource.Object.return_value = mock_obj
    mock_s3_resource.return_value = mock_resource
    
    # Mock do prompter
    mock_prompter = MagicMock()
    mock_prompter.prompt.return_value = zip_name
    
    # Mock do download do StateService
    local_file = tmp_path / zip_name
    local_file.write_text("corrupted content")
    mock_state_svc = MagicMock()
    mock_state_svc.download_state_file.return_value = local_file
    
    cmd = DownloadCommandImpl(
        only_download=False,
        console=console,
        prompter=mock_prompter,
        state_service=mock_state_svc
    )
    
    # Executar. Deve avisar falha e retornar (cancelar)
    # Redirect stdout para verificar mensagens se necessário, ou apenas checar se o arquivo foi movido.
    
    # Mock da constante DOWNLOADS para usar tmp_path
    monkeypatch.setattr("src.constants.constants.DOWNLOADS", str(tmp_path / "downloads"))
    
    cmd.execute()
    
    # Verificar se o arquivo foi movido para corrupted
    corrupted_file = tmp_path / "downloads" / "corrupted" / zip_name
    assert corrupted_file.exists()
    assert not local_file.exists()
