import boto3

from src.exception.credentials_validation_exception import CredentialsValidationException
from src.constants.constants import ACCESS_KEY_ID, BUCKET_NAME, REGION, SECRET_ACCESS_KEY, DEFAULT_AWS_REGION


class AWSCredentials:
    VALID_REGIONS = boto3.session.Session().get_available_regions("s3")

    def __init__(self, access_key_id: str, secret_access_key: str, bucket_name: str, region: str = None):
        if region is None:
            region = DEFAULT_AWS_REGION

        validation_errors = {}
        self._validate_not_blank_accumulative(ACCESS_KEY_ID, access_key_id, validation_errors)
        self._validate_not_blank_accumulative(SECRET_ACCESS_KEY, secret_access_key, validation_errors)
        self._validate_not_blank_accumulative(BUCKET_NAME, bucket_name, validation_errors)
        self._validate_region_accumulative(region, validation_errors)
        if validation_errors:
            raise CredentialsValidationException(validation_errors)

        self.access_key_id = access_key_id.strip()
        self.secret_access_key = secret_access_key.strip()
        self.region = region.strip()
        self.bucket_name = bucket_name.strip()

    def _validate_not_blank_accumulative(self, field: str, value: str, errors: dict[str, str]) -> None:
        if not value or not value.strip():
            errors[field] = f"'{field}' must not be empty or blank"

    def _validate_region_accumulative(self, region: str, errors: dict[str, str]) -> None:
        if not region or not region.strip():
            errors[REGION] = "'region' must not be empty or blank"
            return

        if region not in self.VALID_REGIONS:
            errors[REGION] = f"Invalid region '{region}'. Valid regions include: {', '.join(self.VALID_REGIONS[:5])}..."
