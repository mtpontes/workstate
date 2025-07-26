from pathlib import Path
from typing import Iterable

from mypy_boto3_s3.service_resource import ObjectSummary, Bucket

from src.clients import s3_client
from src.constants.constants import DOT_ZIP, DOWNLOADS


def get_state_files() -> list[ObjectSummary]:
    """
    Retrieve all `.zip` files from the configured S3 bucket.

    Returns:
        list[ObjectSummary]: A list of S3 objects representing `.zip` files.
    """
    bucket_client: Bucket = s3_client.create_s3_resource()
    s3_objects: Iterable[ObjectSummary] = bucket_client.objects.all()

    def only_zip_files(files: Iterable[ObjectSummary]):
        return [file for file in files if file.key.endswith(DOT_ZIP)]

    return only_zip_files(s3_objects)


def download_state_file(object_name: str) -> Path:
    """
    Download a specific `.zip` file from the S3 bucket to the local `downloads` directory.

    Args:
        object_name (str): The key (filename) of the object to download from S3.

    Returns:
        Path: The local path where the file was saved.
    """
    destination = Path(DOWNLOADS) / object_name
    destination.parent.mkdir(parents=True, exist_ok=True)

    bucket_client: Bucket = s3_client.create_s3_resource()
    bucket_client.download_file(object_name, str(destination))

    return destination


def save_state_file(zip_file: Path, object_name: str) -> None:
    """
    Upload a local `.zip` file to the S3 bucket with the given object name.

    Args:
        zip_file (Path): Path to the local `.zip` file to upload.
        object_name (str): The target key (filename) for the object in S3.
    """
    s3_client.create_s3_resource().upload_file(str(zip_file), object_name)


def delete_state_file(s3_object_name: str) -> None:
    s3_client.create_s3_resource().Object(s3_object_name).delete()
