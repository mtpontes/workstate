from pathlib import Path
from typing import Callable, Iterable

from mypy_boto3_s3.service_resource import Bucket, ObjectSummary

from src.clients import s3_client
from src.constants.constants import DOT_ZIP, DOWNLOADS
from src.services.config_service import ConfigService
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO


from src.utils import utils


def _get_prefix() -> str:
    """Returns the S3 prefix for the current project."""
    return f"{utils.get_project_name()}/"


def list_states(
    system: str = None, 
    branch: str = None, 
    older_than: str = None
) -> list[ObjectSummary]:
    """
    Retrieve all `.zip` and `.enc` files from the configured S3 bucket.
    Includes objects in the current project's prefix and legacy root objects.

    Returns:
        list[ObjectSummary]: A list of S3 objects representing state files.
    """
    bucket_client: Bucket = s3_client.create_s3_resource()
    # List all objects and filter locally to avoid complex S3 Delimiter/Prefix logic issues
    all_objects = list(bucket_client.objects.all())
    # Normalize filters: empty strings become None
    system = system if system else None
    branch = branch if branch else None
    older_than = older_than if older_than else None

    prefix = _get_prefix()
    filtered_objects = []
    
    # Pre-parse duration for older_than filter
    cutoff_date = None
    if older_than:
        cutoff_date = utils.parse_duration_to_datetime(older_than)

    for obj in all_objects:
        # Include if it's in the current project's prefix OR it's at the root (legacy)
        is_in_project = obj.key.startswith(prefix)
        is_at_root = "/" not in obj.key
        
        if not ((is_in_project or is_at_root) and (obj.key.endswith(DOT_ZIP) or obj.key.endswith(".enc"))):
            continue

        # Apply older_than filter based on S3 LastModified
        if cutoff_date and obj.last_modified > cutoff_date:
            continue

        # If system or branch filters are provided, we need to check metadata/tags
        if system or branch:
            try:
                # ObjectSummary needs to get the actual Object to fetch Metadata
                response = obj.Object().get()
                metadata = response.get("Metadata", {})
                
                if system:
                    remote_system = metadata.get("system", "").lower()
                    if system.lower() != remote_system:
                        continue
                
                if branch:
                    remote_branch = metadata.get("git-branch", "").lower()
                    # If not in metadata, check tags (as some versions might use tags)
                    if not remote_branch:
                        try:
                            tags_response = bucket_client.meta.client.get_object_tagging(Bucket=bucket_client.name, Key=obj.key)
                            tags = {t['Key']: t['Value'] for t in tags_response.get('TagSet', [])}
                            remote_branch = tags.get("Git-Branch", "").lower()
                        except:
                            pass
                    
                    if branch.lower() != remote_branch:
                        continue
            except Exception as e:
                # print(f"Warning: Could not fetch metadata for {obj.key}: {str(e)}")
                # If we have filters and metadata fetch fails, we skip it by default (safer)
                continue

        filtered_objects.append(obj)

    # Sort most recent first
    filtered_objects.sort(key=lambda x: x.last_modified, reverse=True)
    return filtered_objects


def download_state_file(object_name: str, callback: Callable[[int], None] = None) -> Path:
    """
    Download a specific `.zip` file from the S3 bucket.

    Args:
        object_name (str): The key (filename or prefix/filename) of the object to download.
        callback (Callable[[int], None], optional): Progress callback function for Boto3.

    Returns:
        Path: The local path where the file was saved.
    """
    # Destination filename should be just the basename
    local_filename = object_name.split("/")[-1]
    destination = Path(DOWNLOADS) / local_filename
    destination.parent.mkdir(parents=True, exist_ok=True)

    bucket_client: Bucket = s3_client.create_s3_resource()
    bucket_client.download_file(object_name, str(destination), Callback=callback)

    return destination


def save_state_file(
    zip_file: Path,
    object_name: str,
    callback: Callable[[int], None] = None,
    tags: dict[str, str] = None,
    metadata: dict[str, str] = None,
) -> None:
    """
    Upload a local `.zip` file to the S3 bucket inside the project prefix.

    Args:
        zip_file (Path): Path to the local `.zip` file to upload.
        object_name (str): The target filename for the object.
        callback (Callable[[int], None], optional): Progress callback function for Boto3.
        tags (dict[str, str], optional): Dictionary of tags to apply to the S3 object.
        metadata (dict[str, str], optional): Dictionary of metadata to apply to the S3 object.
    """
    import os
    from src.utils import git_utils
    full_key = f"{_get_prefix()}{object_name}"
    
    # Ensure mandatory tags for report analysis
    mandatory_tags = {
        "Project": utils.get_project_name(),
        "Environment": os.getenv("WORKSTATE_ENV", "production")
    }
    
    git_info = git_utils.get_git_info()
    if git_info.get("Git-Branch"):
        mandatory_tags["Branch"] = git_info["Git-Branch"]
    if git_info.get("Git-Commit"):
        mandatory_tags["Git-Commit"] = git_info["Git-Commit"]

    final_tags = mandatory_tags.copy()
    if tags:
        final_tags.update(tags)

    extra_args = {}
    if final_tags:
        # Boto3 expects tags in 'key1=value1&key2=value2' format for ExtraArgs
        extra_args["Tagging"] = "&".join([f"{k}={v}" for k, v in final_tags.items()])

    if metadata:
        extra_args["Metadata"] = metadata
        # Also ensure git info is in metadata for easy access without tag fetching
        if git_info.get("Git-Branch"):
            extra_args["Metadata"]["git-branch"] = git_info["Git-Branch"]
        if git_info.get("Git-Commit"):
            extra_args["Metadata"]["git-commit"] = git_info["Git-Commit"]

    s3_client.create_s3_resource().upload_file(
        str(zip_file), full_key, ExtraArgs=extra_args, Callback=callback
    )


def delete_state_file(s3_object_name: str) -> None:
    """
    Delete a specific state file from S3.
    Args:
        s3_object_name (str): Full key of the object to delete.
    """
    s3_client.create_s3_resource().Object(s3_object_name).delete()


def generate_presigned_url(object_key: str, expiration_seconds: int = 3600) -> str:
    """Generate a pre-signed URL for downloading an S3 object."""
    try:
        aws_credentials: AWSCredentialsDTO = ConfigService.get_aws_credentials()

        presigned_url = s3_client.create_s3_client().generate_presigned_url(
            "get_object",
            Params={"Bucket": aws_credentials.bucket_name, "Key": object_key},
            ExpiresIn=expiration_seconds,
        )

        return presigned_url

    except Exception as e:
        raise Exception(f"Failed to generate pre-signed URL: {str(e)}")
