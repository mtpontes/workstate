"""
Simple AWS credential validation, checking for non-empty required fields.

Function:
    - validate_credentials: Returns a list of missing or empty fields.
"""

from src.constants.constants import ACCESS_KEY_ID, BUCKET_NAME, REGION, SECRET_ACCESS_KEY


def validate_credentials(access_key_id, secret_access_key, region, bucket_name) -> list[str]:
    """
    Checks if AWS credentials are filled in correctly (not empty or only spaces).

    Args:
        access_key_id (str): AWS Access Key ID.
        secret_access_key (str): AWS Secret Access Key.
        region (str): AWS Region.
        bucket_name (str): S3 bucket name.

    Returns:
        list[str]: List of keys (field names) that are missing or empty.
    """
    credentials: dict = {
        ACCESS_KEY_ID: access_key_id,
        SECRET_ACCESS_KEY: secret_access_key,
        REGION: region,
        BUCKET_NAME: bucket_name,
    }
    return [key for key, value in credentials.items() if not value or not value.strip()]
