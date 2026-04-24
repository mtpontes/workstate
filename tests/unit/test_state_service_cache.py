import pytest
from src.services import state_service
from src.services.cache_service import CacheService
from src.model.dto.state_dto import StateDTO
from datetime import datetime
from unittest.mock import MagicMock

def test_list_states_uses_cache(monkeypatch):
    """Garante que list_states use o CacheService se disponível."""
    project = "my-project"
    monkeypatch.setattr("src.utils.utils.get_project_name", lambda: project)
    
    # Mock do retorno do cache (serializado como JSON)
    cached_states = [{
        "key": f"{project}/state1.zip",
        "size": 100,
        "last_modified": datetime.now().isoformat(),
        "is_protected": False
    }]
    
    mock_get_cache = MagicMock(return_value=cached_states)
    monkeypatch.setattr(CacheService, "get_cached_states", mock_get_cache)
    
    # Executar listagem com cache habilitado
    # Não deve chamar o S3 (mockamos o s3_client lá embaixo para garantir)
    monkeypatch.setattr("src.clients.s3_client.create_s3_resource", lambda: MagicMock())
    
    states = state_service.list_states(use_cache=True)
    
    assert len(states) == 1
    assert states[0].key == f"{project}/state1.zip"
    mock_get_cache.assert_called_with(project)

def test_list_states_bypasses_cache_when_disabled(monkeypatch):
    """Garante que list_states ignore o cache se use_cache=False."""
    project = "my-project"
    monkeypatch.setattr("src.utils.utils.get_project_name", lambda: project)
    
    mock_get_cache = MagicMock()
    monkeypatch.setattr(CacheService, "get_cached_states", mock_get_cache)
    
    # Deve chamar o S3
    mock_s3 = MagicMock()
    monkeypatch.setattr("src.clients.s3_client.create_s3_resource", lambda: mock_s3)
    # Mock do retorno do S3 para não quebrar
    mock_s3.objects.filter.return_value = []
    
    state_service.list_states(use_cache=False)
    
    mock_get_cache.assert_not_called()
