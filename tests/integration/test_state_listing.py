import pytest
from src.services import state_service
from src.utils import utils

def test_list_states_with_prefix_filtering(s3_localstack, monkeypatch):
    """Garante que list_states use apenas o prefixo do projeto atual."""
    bucket_name = "test-listing-bucket"
    s3_localstack.create_bucket(Bucket=bucket_name)
    
    project_name = "my-project"
    other_project = "other-project"
    
    # Mockando o nome do projeto e credenciais
    monkeypatch.setattr(utils, "get_project_name", lambda: project_name)
    
    from src.services.config_service import ConfigService
    from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
    
    dummy_creds = AWSCredentialsDTO(
        access_key_id="test",
        secret_access_key="test",
        region="us-east-1",
        bucket_name=bucket_name,
        endpoint_url=s3_localstack.meta.endpoint_url
    )
    monkeypatch.setattr(ConfigService, "get_aws_credentials", lambda: dummy_creds)
    
    # Criar objetos em diferentes prefixos
    s3_localstack.put_object(Bucket=bucket_name, Key=f"{project_name}/state1.zip", Body=b"content")
    s3_localstack.put_object(Bucket=bucket_name, Key=f"{project_name}/state2.zip", Body=b"content")
    s3_localstack.put_object(Bucket=bucket_name, Key=f"{other_project}/state3.zip", Body=b"content")
    s3_localstack.put_object(Bucket=bucket_name, Key="legacy_state.zip", Body=b"content") # Na raiz
    
    # Executar listagem (não global)
    states = state_service.list_states(global_scan=False)
    
    keys = [obj.key for obj in states]
    
    # Deve conter os do projeto e o da raiz (legacy)
    assert f"{project_name}/state1.zip" in keys
    assert f"{project_name}/state2.zip" in keys
    assert "legacy_state.zip" in keys
    
    # NÃO deve conter o de outro projeto
    assert f"{other_project}/state3.zip" not in keys

def test_list_states_global_scan(s3_localstack, monkeypatch):
    """Garante que o global_scan traga tudo."""
    bucket_name = "test-global-listing-bucket"
    s3_localstack.create_bucket(Bucket=bucket_name)
    
    project_name = "my-project"
    other_project = "other-project"
    
    monkeypatch.setattr(utils, "get_project_name", lambda: project_name)
    
    from src.services.config_service import ConfigService
    from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
    
    dummy_creds = AWSCredentialsDTO(
        access_key_id="test",
        secret_access_key="test",
        region="us-east-1",
        bucket_name=bucket_name,
        endpoint_url=s3_localstack.meta.endpoint_url
    )
    monkeypatch.setattr(ConfigService, "get_aws_credentials", lambda: dummy_creds)
    
    s3_localstack.put_object(Bucket=bucket_name, Key=f"{project_name}/state1.zip", Body=b"content")
    s3_localstack.put_object(Bucket=bucket_name, Key=f"{other_project}/state2.zip", Body=b"content")
    
    states = state_service.list_states(global_scan=True)
    keys = [obj.key for obj in states]
    
    assert f"{project_name}/state1.zip" in keys
    assert f"{other_project}/state2.zip" in keys
