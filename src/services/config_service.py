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
from typing import Any, Dict

from src.constants.constants import AWS, READ_OPERATOR, WRITE_OPERATOR
from src.model.aws_credentials import AWSCredentials
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO


class ConfigService:
    """
    Service responsible for managing the Workstate application configuration file.

    Manages AWS credentials and other relevant information persisted in `~/.workstate/config.json`.
    """

    CONFIG_DIR = Path.home() / ".workstate"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    @classmethod
    def get_aws_credentials(cls) -> AWSCredentialsDTO:
        """Gets AWS credentials from config

        Returns:
            AWSCredentialsDTO: AWS credentials or None if not configured
        """
        config: dict = cls.load_config()
        return AWSCredentialsDTO(**config.get(AWS, {}))

    @classmethod
    def save_aws_credentials(cls, credentials: AWSCredentials) -> None:
        """
        Saves AWS credentials to file config.json
        """
        config = cls.load_config()
        config[AWS] = credentials.__dict__
        cls.save_config(config)

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Alias for load_config for semantic clarity"""
        return cls.load_config()

    @classmethod
    def save_config(cls, config: Dict[str, Any]) -> None:
        """
        Saves the complete configuration dictionary to file.
        """
        cls.ensure_config_dir_exists()
        with open(cls.CONFIG_FILE, WRITE_OPERATOR) as f:
            json.dump(config, f, indent=2)

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
    def ensure_config_dir_exists(cls) -> None:
        """Creates the config directory if it doesn't exist"""
        cls.CONFIG_DIR.mkdir(exist_ok=True)
