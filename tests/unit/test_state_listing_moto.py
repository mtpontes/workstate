import pytest
from src.services import state_service
from src.utils import utils
from moto import mock_aws
import boto3

def test_list_states_with_moto_prefix(s3_client, monkeypatch):
    """Valida a filtragem por prefixo usando Moto (sem dependência de Docker)."""
    bucket_name = "moto-test-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    
    project_name = "project-a"
    other_project = "project-b"
    
    monkeypatch.setattr(utils, "get_project_name", lambda: project_name)
    
    from src.services.config_service import ConfigService
    from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
    
    dummy_creds = AWSCredentialsDTO(
        access_key_id="testing",
        secret_access_key="testing",
        region="us-east-1",
        bucket_name=bucket_name
    )
    monkeypatch.setattr(ConfigService, "get_aws_credentials", lambda: dummy_creds)
    
    # Criar objetos
    s3_client.put_object(Bucket=bucket_name, Key=f"{project_name}/state1.zip", Body=b"zip1")
    s3_client.put_object(Bucket=bucket_name, Key=f"{project_name}/state2.zip", Body=b"zip2")
    s3_client.put_object(Bucket=bucket_name, Key=f"{other_project}/state3.zip", Body=b"zip3")
    s3_client.put_object(Bucket=bucket_name, Key="legacy.zip", Body=b"legacy")
    
    # Listar
    states = state_service.list_states(global_scan=False)
    keys = [obj.key for obj in states]
    
    assert f"{project_name}/state1.zip" in keys
    assert f"{project_name}/state2.zip" in keys
    assert "legacy.zip" in keys
    assert f"{other_project}/state3.zip" not in keys

def test_list_states_moto_global(s3_client, monkeypatch):
    """Valida o global_scan usando Moto."""
    bucket_name = "moto-global-test-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    
    project_name = "project-a"
    monkeypatch.setattr(utils, "get_project_name", lambda: project_name)
    
    from src.services.config_service import ConfigService
    from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
    
    dummy_creds = AWSCredentialsDTO(
        access_key_id="testing",
        secret_access_key="testing",
        region="us-east-1",
        bucket_name=bucket_name
    )
    monkeypatch.setattr(ConfigService, "get_aws_credentials", lambda: dummy_creds)
    
    s3_client.put_object(Bucket=bucket_name, Key="a/1.zip", Body=b"1")
    s3_client.put_object(Bucket=bucket_name, Key="b/2.zip", Body=b"2")
    
    states = state_service.list_states(global_scan=True)
    assert len(states) == 2
