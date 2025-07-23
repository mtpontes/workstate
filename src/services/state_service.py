"""
Module responsible for manipulating .zip files stored in S3 buckets.

Provides utilities to:
    - Filter S3 objects, returning only .zip files.
    - Download .zip files from an S3 bucket to the local directory.

Functions:
    - filter_zip_files(s3_objects): Returns only .zip objects from a list of S3 objects.
    - download_zip_file(object_name): Downloads a .zip file to the local downloads folder.
"""

from pathlib import Path
from typing import Iterable

from mypy_boto3_s3.service_resource import ObjectSummary

from src.clients import s3_client
from src.constants.constants import DOT_ZIP, DOWNLOADS


def filter_zip_files(s3_objects: Iterable[ObjectSummary]) -> list[ObjectSummary]:
    """
    Filters and returns only `.zip` files from the list of S3 objects.

    Args:
        s3_objects(Iterable[ObjectSummary]): List of S3 objects (ObjectSummary) available in the bucket.

    Returns:
        list[ObjectSummary]: List containing only objects with the `.zip` suffix.
    """
    return [obj for obj in s3_objects if obj.key.endswith(DOT_ZIP)]


def download_zip_file(object_name: str) -> Path:
    """
    Downloads a .zip file from the S3 bucket to the local downloads folder.

    Args:
        object_name (str): Name (key) of the object in the S3 bucket.

    Returns:
        Path: Absolute path of the locally saved .zip file.
    """
    destination = Path(DOWNLOADS) / object_name
    return s3_client.download_zip_file(object_name, destination)
