import pytest
from src.services.dashboard_service import DashboardService
from src.model.dto.state_dto import StateDTO
from datetime import datetime

def test_dashboard_html_contains_critical_data():
    """Garante que o HTML gerado contém os nomes dos projetos e estados."""
    states = [
        StateDTO(key="proj1/state.zip", size=1024, last_modified=datetime.now(), is_protected=True),
        StateDTO(key="proj2/backup.zip", size=2048, last_modified=datetime.now(), is_protected=False)
    ]
    
    html = DashboardService.generate_dashboard_html(states, "test-bucket")
    
    # Verificações básicas de conteúdo
    assert "test-bucket" in html
    assert "proj1" in html
    assert "proj2" in html
    assert "proj1/state.zip" in html
    assert "Protected" in html
    assert "Standard" in html
    # Verificações de estilo (premium tokens)
    assert "--bg-color" in html
    assert "glass-border" in html
    assert "backdrop-filter" in html

def test_project_grouping(monkeypatch):
    """Garante que os estados são agrupados corretamente por projeto."""
    states = [
        StateDTO(key="auth/v1.zip", size=100, last_modified=datetime.now(), is_protected=False),
        StateDTO(key="auth/v2.zip", size=200, last_modified=datetime.now(), is_protected=False),
        StateDTO(key="db/init.zip", size=500, last_modified=datetime.now(), is_protected=True)
    ]
    
    html = DashboardService.generate_dashboard_html(states, "my-bkt")
    
    # O projeto 'auth' deve aparecer uma vez como cabeçalho
    # O projeto 'db' deve aparecer uma vez como cabeçalho
    assert html.count("<h2>auth</h2>") == 1
    assert html.count("<h2>db</h2>") == 1
    assert "2 states • Total: 300.0 B" in html # auth meta
    assert "1 states • Total: 500.0 B" in html # db meta
