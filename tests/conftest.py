import os
import pytest
import boto3
from moto import mock_aws
from testcontainers.localstack import LocalStackContainer

# Configurações Dummy para AWS
@pytest.fixture(scope="session")
def aws_credentials():
    """Credenciais dummy para evitar chamadas reais à AWS."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="session")
def localstack(aws_credentials):
    """Fixture que levanta o LocalStack via Testcontainers."""
    with LocalStackContainer("localstack/localstack:latest") as localstack:
        yield localstack

@pytest.fixture
def s3_client(aws_credentials):
    """Fixture para testes unitários usando Moto."""
    with mock_aws():
        yield boto3.client("s3", region_name="us-east-1")

@pytest.fixture
def s3_localstack(localstack):
    """Fixture para testes de integração usando LocalStack real."""
    return boto3.client(
        "s3",
        endpoint_url=localstack.get_url(),
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
