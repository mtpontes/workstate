import boto3
from mypy_boto3_s3.service_resource import Bucket

from src.services.config_service import ConfigService
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO


def create_s3_resource() -> Bucket:
    """Creates S3 resource with proper configuration"""
    credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
    s3_resource = boto3.resource(
        "s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=credentials.region,
    )
    return s3_resource.Bucket(credentials.bucket_name)
