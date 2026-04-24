from pathlib import Path
from typing import Callable, Iterable

from mypy_boto3_s3.service_resource import Bucket, ObjectSummary

from src.clients import s3_client
from src.constants.constants import DOT_ZIP, DOWNLOADS
from src.services.config_service import ConfigService
from src.services.cache_service import CacheService
from src.model.dto.aws_credentials_dto import AWSCredentialsDTO


from src.utils import utils


from datetime import datetime
from src.model.dto.state_dto import StateDTO


def _get_prefix() -> str:
    """Returns the S3 prefix for the current project."""
    return f"{utils.get_project_name()}/"


def list_states(
    system: str = None, 
    branch: str = None, 
    older_than: str = None,
    global_scan: bool = False,
    use_cache: bool = True
) -> list[StateDTO]:
    """
    Retrieve all `.zip` and `.enc` files from the configured S3 bucket.
    Includes objects in the current project's prefix and legacy root objects.

    Args:
        system (str, optional): Filter by system metadata.
        branch (str, optional): Filter by branch metadata/tags.
        older_than (str, optional): Filter by age (e.g., '30d').
        global_scan (bool, optional): If True, ignores project prefix and scans everything.
        use_cache (bool, optional): If True, attempts to use local cache before fetching from S3.

    Returns:
        list[StateDTO]: A list of DTOs representing state files.
    """
    project_name = utils.get_project_name()
    
    # Try cache if not a global scan and caching is enabled
    if use_cache and not global_scan and not (system or branch or older_than):
        cached_data = CacheService.get_cached_states(project_name)
        if cached_data:
            states = []
            for item in cached_data:
                # Reconstruct datetime from string
                item_copy = item.copy()
                item_copy["last_modified"] = datetime.fromisoformat(item_copy["last_modified"])
                states.append(StateDTO(**item_copy))
            return states

    bucket_client: Bucket = s3_client.create_s3_resource()
    prefix = _get_prefix()

    if global_scan:
        all_objects = list(bucket_client.objects.all())
    else:
        # Optimization: Fetch only project objects and root (legacy) objects
        project_objects = list(bucket_client.objects.filter(Prefix=prefix))
        root_objects = list(bucket_client.objects.filter(Prefix="", Delimiter="/"))
        all_objects = project_objects + root_objects

    # Normalize filters
    system = system.lower() if system else None
    branch = branch.lower() if branch else None
    
    # Pre-parse duration for older_than filter
    cutoff_date = None
    if older_than:
        cutoff_date = utils.parse_duration_to_datetime(older_than)

    state_dtos = []
    for obj in all_objects:
        if not (obj.key.endswith(DOT_ZIP) or obj.key.endswith(".enc")):
            continue

        # Ignore profiles in state listings
        from src.constants.constants import S3_PROFILES_PREFIX
        if obj.key.startswith(S3_PROFILES_PREFIX):
            continue

        # Apply older_than filter based on S3 LastModified
        if cutoff_date and obj.last_modified > cutoff_date:
            continue

        # If system or branch filters are provided, we need to check metadata/tags
        if system or branch:
            try:
                response = obj.Object().get()
                metadata = response.get("Metadata", {})
                
                if system:
                    remote_system = metadata.get("system", "").lower()
                    if system != remote_system:
                        continue
                
                if branch:
                    remote_branch = metadata.get("git-branch", "").lower()
                    if not remote_branch:
                        try:
                            tags_response = bucket_client.meta.client.get_object_tagging(Bucket=bucket_client.name, Key=obj.key)
                            tags = {t['Key']: t['Value'] for t in tags_response.get('TagSet', [])}
                            remote_branch = tags.get("Git-Branch", "").lower()
                        except:
                            pass
                    
                    if branch != remote_branch:
                        continue
            except:
                continue

        state_dtos.append(StateDTO(
            key=obj.key,
            size=obj.size,
            last_modified=obj.last_modified,
            is_protected=is_protected(obj.key)
        ))

    # Sort most recent first
    state_dtos.sort(key=lambda x: x.last_modified, reverse=True)

    # Save to cache if not global scan and no filters were active (to keep cache "clean" for default list)
    if not global_scan and not (system or branch or older_than):
        cache_items = []
        for dto in state_dtos:
            item = {
                "key": dto.key,
                "size": dto.size,
                "last_modified": dto.last_modified.isoformat(),
                "is_protected": dto.is_protected
            }
            cache_items.append(item)
        CacheService.save_states_to_cache(project_name, cache_items)

    return state_dtos


def get_state_content(object_key: str, password: str = None) -> list[dict]:
    """
    Retrieve the list of files inside a state ZIP on S3.
    
    Args:
        object_key (str): S3 key of the state file.
        password (str, optional): Password if the file is encrypted.
        
    Returns:
        list[dict]: List of file metadata (filename, size, compress_size, date_time).
    """
    import zipfile
    import io
    from tempfile import NamedTemporaryFile
    from src.utils import utils

    bucket_client: Bucket = s3_client.create_s3_resource()
    obj = bucket_client.Object(object_key)
    
    # For large files, we download to a temp file instead of reading into memory
    with NamedTemporaryFile(suffix=DOT_ZIP, delete=False) as tmp_file:
        tmp_path = Path(tmp_file.name)
        tmp_file.close()  # Close the handle immediately to avoid conflicts on Windows
        
        bucket_client.download_file(object_key, str(tmp_path))
        
        try:
            target_zip = tmp_path
            if object_key.endswith(".enc"):
                if not password:
                    raise Exception("Password required for encrypted state.")
                target_zip = utils.decrypt_file(tmp_path, password)
            
            with zipfile.ZipFile(target_zip, 'r') as zf:
                info_list = zf.infolist()
                contents = [
                    {
                        "filename": info.filename,
                        "file_size": info.file_size,
                        "compress_size": info.compress_size,
                        "date_time": info.date_time
                    }
                    for info in info_list
                    if not info.is_dir()
                ]
            
            if object_key.endswith(".enc") and target_zip != tmp_path:
                target_zip.unlink()
                
            return contents
        finally:
            if tmp_path.exists():
                tmp_path.unlink()


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
    protected: bool = False,
) -> None:
    """
    Upload a local `.zip` file to the S3 bucket inside the project prefix.

    Args:
        zip_file (Path): Path to the local `.zip` file to upload.
        object_name (str): The target filename for the object.
        callback (Callable[[int], None], optional): Progress callback function for Boto3.
        tags (dict[str, str], optional): Dictionary of tags to apply to the S3 object.
        metadata (dict[str, str], optional): Dictionary of metadata to apply to the S3 object.
        protected (bool, optional): If True, marks the state as protected.
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
    else:
        extra_args["Metadata"] = {}

    if protected:
        extra_args["Metadata"]["protected"] = "true"

    # Also ensure git info is in metadata for easy access without tag fetching
    if git_info.get("Git-Branch"):
        extra_args["Metadata"]["git-branch"] = git_info["Git-Branch"]
    if git_info.get("Git-Commit"):
        extra_args["Metadata"]["git-commit"] = git_info["Git-Commit"]

    # Calculate and store SHA256 for integrity check
    from src.services import file_service
    extra_args["Metadata"]["state-sha256"] = file_service.calculate_sha256(zip_file)

    s3_client.create_s3_resource().upload_file(
        str(zip_file), full_key, ExtraArgs=extra_args, Callback=callback
    )
    
    CacheService.invalidate_project_cache(utils.get_project_name())


def delete_state_file(s3_object_name: str, force: bool = False) -> None:
    """
    Delete a specific state file from S3.
    Args:
        s3_object_name (str): Full key of the object to delete.
        force (bool): If True, bypass protection check.
    """
    if not force and is_protected(s3_object_name):
        raise Exception(f"Cannot delete protected state: {s3_object_name}. Use --force or unprotect it first.")
        
    s3_client.create_s3_resource().Object(s3_object_name).delete()
    CacheService.invalidate_project_cache(utils.get_project_name())


def is_protected(s3_object_name: str) -> bool:
    """
    Check if a state file is protected via metadata.
    Args:
        s3_object_name (str): Full key of the object.
    Returns:
        bool: True if protected, False otherwise.
    """
    try:
        bucket_client: Bucket = s3_client.create_s3_resource()
        obj = bucket_client.Object(s3_object_name)
        response = obj.get()
        metadata = response.get("Metadata", {})
        return metadata.get("protected", "false").lower() == "true"
    except Exception:
        # If we can't fetch metadata (e.g. object doesn't exist), assume not protected
        return False


def set_protection(s3_object_name: str, protect: bool = True) -> None:
    """
    Enable or disable protection for an existing state file.
    Args:
        s3_object_name (str): Full key of the object.
        protect (bool): True to protect, False to unprotect.
    """
    bucket_client: Bucket = s3_client.create_s3_resource()
    obj = bucket_client.Object(s3_object_name)
    
    # Fetch existing metadata
    response = obj.get()
    metadata = response.get("Metadata", {})
    
    # Update protection flag
    metadata["protected"] = "true" if protect else "false"
    
    # Copy object to itself with updated metadata
    aws_credentials = ConfigService.get_aws_credentials()
    copy_source = {
        'Bucket': aws_credentials.bucket_name,
        'Key': s3_object_name
    }
    
    obj.copy_from(
        CopySource=copy_source,
        Metadata=metadata,
        MetadataDirective='REPLACE'
    )


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
