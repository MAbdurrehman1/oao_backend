import boto3
from botocore.client import Config
from ..config import configs
from ..constants import StorageType
from .local_storage import LocalStorage
from .s3_storage import S3Storage
from .i_storage import StorageInterface


def _get_storage(storage_type: StorageType) -> StorageInterface:
    if storage_type == StorageType.local_storage:
        return LocalStorage(base_path=configs.media_root, media_url=configs.media_url)
    elif storage_type == StorageType.s3:
        client = boto3.client(
            "s3",
            endpoint_url=configs.s3_endpoint_url,
            aws_access_key_id=configs.s3_access_key_id,
            aws_secret_access_key=configs.s3_secret_access_key,
            config=Config(signature_version="s3v4"),
        )
        return S3Storage(
            bucket_name=configs.s3_bucket_name,
            client=client,
        )
    else:
        raise NotImplementedError


storage = _get_storage(storage_type=configs.storage_type)


__all__ = ["storage"]
