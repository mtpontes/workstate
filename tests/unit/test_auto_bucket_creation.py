import pytest
from src.commands.configure_command import ConfigureCommandImpl
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
from unittest.mock import MagicMock, patch
from rich.console import Console
from botocore.exceptions import ClientError

@patch("src.clients.s3_client.create_s3_resource")
@patch("src.clients.s3_client.create_bucket")
@patch("src.clients.s3_client.put_public_access_block")
@patch("typer.confirm")
def test_create_bucket_on_404(mock_confirm, mock_put_block, mock_create, mock_resource, monkeypatch):
    """Garante que o bucket é criado se não existir (404)."""
    console = Console()
    credentials = AWSCredentialsDTO(
        access_key_id="key",
        secret_access_key="secret",
        region="us-east-1",
        bucket_name="new-bucket"
    )
    
    # Simular 404 no head_bucket
    mock_s3 = MagicMock()
    mock_s3.meta.client.head_bucket.side_effect = ClientError(
        {"Error": {"Code": "404"}}, "head_bucket"
    )
    mock_resource.return_value = mock_s3
    
    # Usuário confirma criação
    mock_confirm.return_value = True
    
    cmd = ConfigureCommandImpl(
        interactive=True,
        console=console,
        prompter=MagicMock(),
        credentials=credentials
    )
    
    # Mock do save para não tocar no disco
    monkeypatch.setattr(cmd, "_save_credentials", lambda x: None)
    # Mock do prompt para retornar as mesmas credenciais
    cmd.prompter.prompt.return_value = credentials
    
    cmd.execute()
    
    mock_create.assert_called_once_with("new-bucket", "us-east-1")
    mock_put_block.assert_called_once_with("new-bucket", "us-east-1")

@patch("src.clients.s3_client.create_s3_resource")
@patch("src.clients.s3_client.create_bucket")
def test_no_create_if_bucket_exists(mock_create, mock_resource, monkeypatch):
    """Garante que não tenta criar se o bucket já existe (200)."""
    console = Console()
    credentials = AWSCredentialsDTO(bucket_name="existing-bucket", region="us-east-1")
    
    # Simular sucesso no head_bucket (não levanta exceção)
    mock_s3 = MagicMock()
    mock_resource.return_value = mock_s3
    
    cmd = ConfigureCommandImpl(
        interactive=True, console=console, prompter=MagicMock(), credentials=credentials
    )
    monkeypatch.setattr(cmd, "_save_credentials", lambda x: None)
    cmd.prompter.prompt.return_value = credentials
    
    cmd.execute()
    
    mock_create.assert_not_called()
