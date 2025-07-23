"""
Module responsible for managing the Workstate application configuration file.

The configuration file is stored in `~/.workstate/config.json`.
This service allows you to save, load, and verify the existence of AWS credentials used by the application.

Main responsibilities:
    - Create the configuration directory if it doesn't exist.
    - Read and write configuration files in JSON format.
    - Store and retrieve AWS credentials.

Class:
    - ConfigService: Provides utilities for managing the Workstate application configuration.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

from src.constants.constants import (
    ACCESS_KEY_ID,
    AWS,
    BUCKET_NAME,
    READ_OPERATOR,
    REGION,
    SECRET_ACCESS_KEY,
    WRITE_OPERATOR,
)


class ConfigService:
    """
    Service responsible for managing the Workstate application configuration file.

    Manages AWS credentials and other relevant information persisted in `~/.workstate/config.json`.
    """

    CONFIG_DIR = Path.home() / ".workstate"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    @classmethod
    def save_config(cls, config: Dict[str, Any]) -> None:
        """Saves configuration to the config file

        Args:
            config (Dict[str, Any]): Configuration dictionary to save
        """
        cls.ensure_config_dir_exists()

        with open(cls.CONFIG_FILE, WRITE_OPERATOR) as f:
            json.dump(config, f, indent=2)

    @classmethod
    def ensure_config_dir_exists(cls) -> None:
        """Creates the config directory if it doesn't exist"""
        cls.CONFIG_DIR.mkdir(exist_ok=True)

    @classmethod
    def get_aws_credentials(cls) -> Optional[Dict[str, str]]:
        """Gets AWS credentials from config

        Returns:
            Optional[Dict[str, str]]: AWS credentials or None if not configured
        """
        config = cls.load_config()
        aws_config = config.get(AWS, {})

        required_keys = [ACCESS_KEY_ID, SECRET_ACCESS_KEY, REGION, BUCKET_NAME]
        if all(key in aws_config for key in required_keys):
            return {
                ACCESS_KEY_ID: aws_config[ACCESS_KEY_ID],
                SECRET_ACCESS_KEY: aws_config[SECRET_ACCESS_KEY],
                REGION: aws_config[REGION],
                BUCKET_NAME: aws_config[BUCKET_NAME],
            }

        return None

    @classmethod
    def save_aws_credentials(cls, access_key_id: str, secret_access_key: str, region: str, bucket_name: str) -> None:
        """
        Saves AWS credentials to config

        Args:
            access_key_id (str): AWS Access Key ID
            secret_access_key (str): AWS Secret Access Key
            region (str): AWS Region
            bucket_name (str): S3 Bucket name
        """
        config = cls.load_config()

        config[AWS] = {
            ACCESS_KEY_ID: access_key_id,
            SECRET_ACCESS_KEY: secret_access_key,
            REGION: region,
            BUCKET_NAME: bucket_name,
        }

        cls.save_config(config)

    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """
        Loads configuration from the config file

        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        if not cls.CONFIG_FILE.exists():
            return {}

        with open(cls.CONFIG_FILE, READ_OPERATOR) as f:
            return json.load(f)

    @classmethod
    def has_aws_credentials(cls) -> bool:
        """
        Checks if AWS credentials are configured

        Returns:
            bool: True if credentials are configured, False otherwise
        """
        return cls.get_aws_credentials() is not None
