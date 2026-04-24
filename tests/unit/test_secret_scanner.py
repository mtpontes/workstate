import math
import re
import pytest
from src.services import file_service

def test_entropy_calculation():
    """Valida se a entropia é calculada corretamente."""
    # String de baixa entropia
    low = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    # String de alta entropia (aleatória)
    high = "4vX7p9mK2zQ8wR5jT6nL1yB3hG0fS9aC"
    
    assert file_service._calculate_entropy(low) < 1.0
    assert file_service._calculate_entropy(high) > 3.0

def test_regex_detection():
    """Valida se padrões comuns de segredos são detectados."""
    aws_key = "AKIAEXAMPLE123456789"
    aws_secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    normal_text = "This is a normal sentence without secrets."
    
    assert file_service._contains_secrets(aws_key) is True
    assert file_service._contains_secrets(aws_secret) is True
    assert file_service._contains_secrets(normal_text) is False

def test_scan_file_with_secrets(tmp_path):
    """Teste de integração do scanner em um arquivo real."""
    secret_file = tmp_path / "config.py"
    secret_file.write_text("API_KEY = 'AKIAEXAMPLE123456789'\nSECRET = 'my-secret'")
    
    findings = file_service.scan_file_for_secrets(str(secret_file))
    assert len(findings) > 0
    assert any("Potential secret" in f for f in findings)

def test_scan_file_without_secrets(tmp_path):
    """Garante que arquivos limpos não geram alertas."""
    clean_file = tmp_path / "main.py"
    clean_file.write_text("print('Hello World')\nimport os")
    
    findings = file_service.scan_file_for_secrets(str(clean_file))
    assert len(findings) == 0
