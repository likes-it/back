import boto3
import mimetypes
import os
from typing import BinaryIO
from app.domain.services.image_uploader import ImageUploader

class MinioImageUploader(ImageUploader):
    def __init__(self):
        self.bucket_name = os.getenv("MINIO_BUCKET", "images")
        self.region = os.getenv("MINIO_REGION", "us-east-1")

        self.s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("MINIO_ENDPOINT"),
            aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
            region_name=self.region,
        )
    
    def _guess_mime_type(self, filename: str) -> str:
        mime, _ = mimetypes.guess_type(filename)
        return mime or "application/octet-stream"

    def extract_key_from_url(self, url: str) -> str:
        return url.split(f"{self.bucket_name}/")[-1]

    def upload(self, file: BinaryIO, filename: str) -> str:
        self.s3.upload_fileobj(
            Fileobj=file,
            Bucket=self.bucket_name,
            Key=filename,
            ExtraArgs={"ContentType": self._guess_mime_type(filename), "ContentDisposition": "inline"}
        )
        public_url = f"{os.getenv('MINIO_PUBLIC_URL')}/{self.bucket_name}/{filename}"
        return public_url

    def delete(self, object_key: str) -> None:
        self.s3.delete_object(Bucket=self.bucket_name, Key=object_key)
