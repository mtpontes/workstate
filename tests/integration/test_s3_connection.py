import pytest
import boto3
from botocore.exceptions import ClientError

def test_localstack_s3_connection(s3_localstack):
    """Garante que o LocalStack está acessível e funcional."""
    bucket_name = "test-workflow-bucket"
    
    # Criar bucket
    s3_localstack.create_bucket(Bucket=bucket_name)
    
    # Listar buckets
    response = s3_localstack.list_buckets()
    buckets = [b["Name"] for b in response["Buckets"]]
    
    assert bucket_name in buckets

def test_localstack_put_get_object(s3_localstack):
    """Teste de fumaça para upload e download no LocalStack."""
    bucket_name = "test-objects-bucket"
    s3_localstack.create_bucket(Bucket=bucket_name)
    
    key = "hello.txt"
    content = b"Workstate Test"
    
    s3_localstack.put_object(Bucket=bucket_name, Key=key, Body=content)
    
    response = s3_localstack.get_object(Bucket=bucket_name, Key=key)
    downloaded_content = response["Body"].read()
    
    assert downloaded_content == content
