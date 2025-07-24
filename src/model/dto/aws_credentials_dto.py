from typing import Optional
from dataclasses import dataclass

from src.model.aws_credentials import AWSCredentials


@dataclass
class AWSCredentialsDTO:
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    region: Optional[str] = None
    bucket_name: Optional[str] = None

    def to_aws_credentials_model(self) -> AWSCredentials:
        return AWSCredentials(**self.__dict__)
