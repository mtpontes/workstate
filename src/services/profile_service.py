"""
Module responsible for managing Workstate profiles.
Profiles are named sets of .workstateignore rules that can be stored locally
or shared via S3.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from src.constants.constants import (
    PROFILES_FILE,
    READ_OPERATOR,
    S3_PROFILES_PREFIX,
    WRITE_OPERATOR,
    DOT_ZIP
)
from src.services.config_service import ConfigService
from src.clients import s3_client


class ProfileService:
    """
    Service to manage Workstate profiles locally (~/.workstate/profiles.json)
    and remotely (S3 prefix _profiles/).
    """

    PROFILES_PATH = ConfigService.CONFIG_DIR / PROFILES_FILE

    @classmethod
    def save_local_profile(cls, name: str, content: str) -> None:
        """Saves a profile content to the local storage."""
        profiles = cls.load_local_profiles()
        profiles[name] = content
        ConfigService.ensure_config_dir_exists()
        
        with open(cls.PROFILES_PATH, WRITE_OPERATOR, encoding="utf-8") as f:
            json.dump(profiles, f, indent=2)

    @classmethod
    def get_local_profile(cls, name: str) -> Optional[str]:
        """Returns the content of a local profile or None if not found."""
        profiles = cls.load_local_profiles()
        return profiles.get(name)

    @classmethod
    def list_local_profiles(cls) -> List[str]:
        """Returns a list of all local profile names."""
        return list(cls.load_local_profiles().keys())

    @classmethod
    def delete_local_profile(cls, name: str) -> bool:
        """Deletes a local profile. Returns True if deleted."""
        profiles = cls.load_local_profiles()
        if name in profiles:
            del profiles[name]
            with open(cls.PROFILES_PATH, WRITE_OPERATOR, encoding="utf-8") as f:
                json.dump(profiles, f, indent=2)
            return True
        return False

    @classmethod
    def load_local_profiles(cls) -> Dict[str, str]:
        """Loads all profiles from the local JSON file."""
        if not cls.PROFILES_PATH.exists():
            return {}
        try:
            with open(cls.PROFILES_PATH, READ_OPERATOR, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    @classmethod
    def push_profile(cls, name: str) -> None:
        """Uploads a local profile content to S3."""
        content = cls.get_local_profile(name)
        if not content:
            raise ValueError(f"Local profile '{name}' not found.")

        aws_credentials = ConfigService.get_aws_credentials()
        if not aws_credentials.bucket_name:
            raise Exception("AWS Bucket not configured. Run 'workstate configure' first.")

        bucket = s3_client.create_s3_resource()
        key = f"{S3_PROFILES_PREFIX}{name}.txt"
        
        try:
            # bucket is already a s3.Bucket resource
            bucket.Object(key).put(
                Body=content.encode("utf-8")
            )
        except Exception as e:
            raise Exception(f"S3 Upload failed: {str(e)}")

    @classmethod
    def pull_profile(cls, name: str) -> None:
        """Downloads a profile from S3 and saves it locally."""
        aws_credentials = ConfigService.get_aws_credentials()
        if not aws_credentials.bucket_name:
            raise Exception("AWS Bucket not configured.")

        bucket = s3_client.create_s3_resource()
        key = f"{S3_PROFILES_PREFIX}{name}.txt"
        
        try:
            response = bucket.Object(key).get()
            content = response['Body'].read().decode("utf-8")
            cls.save_local_profile(name, content)
        except Exception as e:
            raise Exception(f"Failed to pull profile '{name}' from S3: {str(e)}")

    @classmethod
    def list_remote_profiles(cls) -> List[str]:
        """Lists profile names available in S3."""
        aws_credentials = ConfigService.get_aws_credentials()
        if not aws_credentials.bucket_name:
            return []

        try:
            bucket = s3_client.create_s3_resource()
            
            profiles = []
            for obj in bucket.objects.filter(Prefix=S3_PROFILES_PREFIX):
                # Extract name: _profiles/name.txt -> name
                key = obj.key
                if key == S3_PROFILES_PREFIX: # Skip the prefix itself if it's an object
                    continue
                
                name = key.replace(S3_PROFILES_PREFIX, "")
                if name.endswith(".txt"):
                    name = name[:-4]
                
                if name:
                    profiles.append(name)
            return profiles
        except Exception:
            return []

    @classmethod
    def delete_remote_profile(cls, name: str) -> None:
        """Deletes a profile from S3."""
        aws_credentials = ConfigService.get_aws_credentials()
        if not aws_credentials.bucket_name:
            raise Exception("AWS Bucket not configured.")

        bucket = s3_client.create_s3_resource()
        key = f"{S3_PROFILES_PREFIX}{name}.txt"
        bucket.Object(key).delete()
