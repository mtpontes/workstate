import time
import json
from pathlib import Path
import pytest
from src.services.cache_service import CacheService

def test_cache_save_and_load(tmp_path, monkeypatch):
    """Garante que o cache salva e recupera dados corretamente."""
    cache_file = tmp_path / "metadata.json"
    monkeypatch.setattr(CacheService, "CACHE_FILE", cache_file)
    monkeypatch.setattr(CacheService, "CACHE_DIR", tmp_path)
    
    project = "test-project"
    states = [{"key": "a", "size": 10, "last_modified": "2024-01-01T00:00:00"}]
    
    CacheService.save_states_to_cache(project, states)
    
    loaded = CacheService.get_cached_states(project)
    assert loaded == states
    assert len(loaded) == 1

def test_cache_expiration(tmp_path, monkeypatch):
    """Garante que o cache expira após o TTL."""
    cache_file = tmp_path / "metadata.json"
    monkeypatch.setattr(CacheService, "CACHE_FILE", cache_file)
    monkeypatch.setattr(CacheService, "CACHE_DIR", tmp_path)
    monkeypatch.setattr(CacheService, "DEFAULT_TTL", 1) # 1 second TTL
    
    project = "test-project"
    states = [{"key": "a"}]
    
    CacheService.save_states_to_cache(project, states)
    assert CacheService.get_cached_states(project) == states
    
    time.sleep(1.1)
    assert CacheService.get_cached_states(project) is None

def test_cache_invalidation(tmp_path, monkeypatch):
    """Garante que a invalidação remove o projeto do cache."""
    cache_file = tmp_path / "metadata.json"
    monkeypatch.setattr(CacheService, "CACHE_FILE", cache_file)
    monkeypatch.setattr(CacheService, "CACHE_DIR", tmp_path)
    
    project = "test-project"
    CacheService.save_states_to_cache(project, [{"key": "a"}])
    
    CacheService.invalidate_project_cache(project)
    assert CacheService.get_cached_states(project) is None
