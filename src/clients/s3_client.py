from pathlib import Path
from typing import Iterable

import boto3
from mypy_boto3_s3.service_resource import ObjectSummary, Bucket

from src.services.config_service import ConfigService
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO


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
    credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
    s3_resource = boto3.resource(
        "s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=credentials.region,
    )
    return s3_resource.Bucket(credentials.bucket_name)
