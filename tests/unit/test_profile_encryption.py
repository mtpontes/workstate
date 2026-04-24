import pytest
from src.utils import utils

def test_string_encryption_decryption():
    """Garante que a criptografia de strings é reversível e segura."""
    content = "my secret ignore rules\nnode_modules/"
    password = "safe-password"
    
    encrypted = utils.encrypt_string(content, password)
    assert isinstance(encrypted, bytes)
    assert len(encrypted) > len(content)
    
    decrypted = utils.decrypt_string(encrypted, password)
    assert decrypted == content

def test_decryption_with_wrong_password():
    """Garante que falha com a senha errada."""
    content = "secret"
    encrypted = utils.encrypt_string(content, "pass1")
    
    with pytest.raises(Exception):
        utils.decrypt_string(encrypted, "wrong-pass")
