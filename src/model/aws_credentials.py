import boto3

from src.exception.aws_region_exception import RegionValidationError
from src.constants.envs import DEFAULT_AWS_REGION
from src.constants.constants import ACCESS_KEY_ID, BUCKET_NAME, SECRET_ACCESS_KEY


class AWSCredentials:
    VALID_REGIONS = boto3.session.Session().get_available_regions("s3")

    def __init__(self, access_key_id: str, secret_access_key: str, bucket_name: str, region: str = DEFAULT_AWS_REGION):
        self._validate_not_blank(ACCESS_KEY_ID, access_key_id)
        self._validate_not_blank(SECRET_ACCESS_KEY, secret_access_key)
        self._validate_not_blank(BUCKET_NAME, bucket_name)
        self._validate_region(region)

        self.access_key_id = access_key_id.strip()
        self.secret_access_key = secret_access_key.strip()
        self.region = region.strip()
        self.bucket_name = bucket_name.strip()

    @staticmethod
    def _validate_not_blank(field: str, value: str) -> None:
        if not value or not value.strip():
            raise ValueError(f"'{field}' must not be empty or blank")

    def _validate_region(self, region: str) -> None:
        self._validate_not_blank("region", region)
        if region not in self.VALID_REGIONS:
            raise RegionValidationError(region, self.VALID_REGIONS)
