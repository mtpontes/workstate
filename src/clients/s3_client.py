import boto3
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.service_resource import Bucket


from src.services.config_service import ConfigService
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO
from src.exception.credentials_validation_exception import CredentialsValidationException


def validate_credentials(require_bucket: bool = True):
    """Public validation of credentials before creating S3/STS clients."""
    credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
    errors = {}
    if not credentials.access_key_id:
        errors["access_key_id"] = "Access Key ID is missing"
    if not credentials.secret_access_key:
        errors["secret_access_key"] = "Secret Access Key is missing"
    if require_bucket and not credentials.bucket_name:
        errors["bucket_name"] = "S3 Bucket Name is missing"
    
    if errors:
        raise CredentialsValidationException(errors)


def create_s3_resource() -> Bucket:
    """Creates S3 resource with proper configuration"""
    credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
    validate_credentials()
    
    s3_resource = boto3.resource(
        "s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=credentials.region,
        endpoint_url=getattr(credentials, "endpoint_url", None),
    )
    return s3_resource.Bucket(credentials.bucket_name)


def create_s3_client() -> S3Client:
    """Creates S3 resource with proper configuration"""
    credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
    validate_credentials()
    
    return boto3.client(
        "s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=credentials.region,
        endpoint_url=getattr(credentials, "endpoint_url", None),
    )


def create_sts_client():
    """Creates STS client for identity verification"""
    credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
    validate_credentials(require_bucket=False)
    
    return boto3.client(
        "sts",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=credentials.region,
    )


def create_bucket(bucket_name: str, region: str) -> None:
    """Creates an S3 bucket with the specified name and region."""
    credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
    client = boto3.client(
        "s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=region,
        endpoint_url=getattr(credentials, "endpoint_url", None),
    )
    
    if region == "us-east-1":
        client.create_bucket(Bucket=bucket_name)
    else:
        client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region},
        )


def put_public_access_block(bucket_name: str, region: str) -> None:
    """Configures public access block for the bucket."""
    credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
    client = boto3.client(
        "s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=region,
        endpoint_url=getattr(credentials, "endpoint_url", None),
    )
    client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True,
        },
    )


def list_workstate_buckets() -> list[str]:
    """Lists all S3 buckets that match the Workstate prefix."""
    credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()
    client = boto3.client(
        "s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=credentials.region,
        endpoint_url=getattr(credentials, "endpoint_url", None),
    )
    
    try:
        response = client.list_buckets()
        buckets = [b["Name"] for b in response.get("Buckets", [])]
        return [b for b in buckets if b.startswith("workstate-storage-")]
    except Exception:
        return []
