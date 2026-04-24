import pytest
from src.services.config_service import ConfigService
from src.clients import s3_client
from unittest.mock import MagicMock, patch

def test_bucket_history_persistence(tmp_path, monkeypatch):
    """Garante que novos buckets são salvos no histórico."""
    config_file = tmp_path / "config.json"
    monkeypatch.setattr(ConfigService, "CONFIG_FILE", config_file)
    monkeypatch.setattr(ConfigService, "CONFIG_DIR", tmp_path)
    
    ConfigService.add_to_bucket_history("bucket-1")
    ConfigService.add_to_bucket_history("bucket-2")
    ConfigService.add_to_bucket_history("bucket-1") # Duplicado
    
    history = ConfigService.get_bucket_history()
    assert history == ["bucket-1", "bucket-2"]

@patch("boto3.client")
def test_list_workstate_buckets_filtering(mock_boto, monkeypatch):
    """Garante que a descoberta filtra apenas buckets com o prefixo correto."""
    mock_client = MagicMock()
    mock_client.list_buckets.return_value = {
        "Buckets": [
            {"Name": "workstate-storage-abc"},
            {"Name": "my-personal-bucket"},
            {"Name": "workstate-storage-xyz"}
        ]
    }
    mock_boto.return_value = mock_client
    
    # Mock credenciais para não falhar
    monkeypatch.setattr(ConfigService, "get_aws_credentials", lambda: MagicMock())
    
    discovered = s3_client.list_workstate_buckets()
    assert discovered == ["workstate-storage-abc", "workstate-storage-xyz"]
