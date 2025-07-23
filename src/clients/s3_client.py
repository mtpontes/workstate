import os
from pathlib import Path
from typing import Iterable

import boto3
from mypy_boto3_s3.service_resource import ObjectSummary, Bucket

from src.services.config_service import ConfigService
from src.constants.constants import ACCESS_KEY_ID, BUCKET_NAME, REGION, SECRET_ACCESS_KEY
from src.constants.envs import (
    DEFAULT_AWS_REGION,
    ENV_WORK_STATE_AWS_REGION,
    ENV_WORKSTATE_AWS_ACCESS_KEY_ID,
    ENV_WORKSTATE_AWS_SECRET_ACCESS_KEY,
    ENV_WORKSTATE_S3_BUCKET_NAME,
)


def list_objects() -> Iterable[ObjectSummary]:
    """Lists all objects in the configured S3 bucket

    Returns:
        Iterable[ObjectSummary]: All objects in the bucket

    Raises:
        ValueError: If AWS credentials are not configured
    """
    return _create_s3_resource().objects.all()


def save_zip_file(zip_file: Path, object_name: str) -> None:
    """Uploads a zip file to S3

    Args:
        zip_file (Path): Local path to the zip file
        object_name (str): Name to use for the object in S3

    Raises:
        ValueError: If AWS credentials are not configured
    """
    return _create_s3_resource().upload_file(str(zip_file), object_name)


def download_zip_file(object_name: str, destination: Path) -> Path:
    """Downloads a zip file from S3

    Args:
        object_name (str): Name of the object in S3
        destination (Path): Local path where to save the file

    Returns:
        Path: Path to the downloaded file

    Raises:
        ValueError: If AWS credentials are not configured
    """
    destination.parent.mkdir(parents=True, exist_ok=True)

    bucket_client: Bucket = _create_s3_resource()
    bucket_client.download_file(object_name, str(destination))
    return destination


def _create_s3_resource() -> Bucket:
    """Creates S3 resource with proper configuration"""
    access_key_id, secret_access_key, region, bucket_name = _get_aws_config()

    if access_key_id and secret_access_key:
        s3_resource = boto3.resource(
            "s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name=region
        )
    else:
        # Uses Standard Boto3 credentials (AMI Roles, ~/.Aws/Credentials, etc.)
        s3_resource = boto3.resource("s3", region_name=region)

    return s3_resource.Bucket(bucket_name)


def _get_aws_config() -> tuple[str, str, str, str]:
    """Gets AWS configuration from config file or environment variables

    Returns:
        Tuple[str, str, str]: (access_key_id, secret_access_key, region, bucket_name)

    Raises:
        ValueError: If required configuration is missing
    """
    try:
        credentials = ConfigService.get_aws_credentials()  # load config file first
        if credentials:
            return (
                credentials[ACCESS_KEY_ID],
                credentials[SECRET_ACCESS_KEY],
                credentials[REGION],
                credentials[BUCKET_NAME],
            )
    except ImportError:
        # ConfigService não está disponível, usa variáveis de ambiente
        pass

    # Fallback to environment variables
    bucket_name = os.getenv(ENV_WORKSTATE_S3_BUCKET_NAME)
    region = os.getenv(ENV_WORK_STATE_AWS_REGION, DEFAULT_AWS_REGION)
    access_key_id = os.getenv(ENV_WORKSTATE_AWS_ACCESS_KEY_ID)
    secret_access_key = os.getenv(ENV_WORKSTATE_AWS_SECRET_ACCESS_KEY)

    # Validação das credenciais necessárias
    if not bucket_name:
        raise ValueError(
            "S3 bucket name not configured. "
            "Run 'workstate configure' to set up AWS credentials or set WORKSTATE_S3_BUCKET_NAME environment variable."
        )

    # Se não tem credenciais explícitas, boto3 tentará usar credenciais padrão (IAM roles, ~/.aws/credentials, etc.)
    return access_key_id, secret_access_key, region, bucket_name
