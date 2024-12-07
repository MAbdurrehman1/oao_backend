from .i_storage import StorageInterface


class S3Storage(StorageInterface):
    def __init__(self, bucket_name: str, client):
        self.bucket_name = bucket_name
        self.client = client

    def store_file(self, file_data: bytes, file_name: str, content_type: str) -> str:
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=file_name,
            Body=file_data,
            ContentType=content_type,
        )
        url = f"{self.bucket_name}/{file_name}"
        return url
