import os
import mimetypes
from uuid import uuid4, UUID
from typing import BinaryIO
from app.domain.entities.image import Image
from app.domain.repositories.image_repository import ImageRepository
from app.domain.services.image_uploader import ImageUploader
from app.domain.exceptions import InvalidImageFormatError

class PostImageUseCase:
    allowed_mimetypes = {"image/jpeg", "image/png", "image/webp", "image/gif"}
    allowed_extensions = {".jpg", ".png", ".webp", ".gif"}

    def __init__(self, image_repo: ImageRepository, uploader: ImageUploader):
        self.image_repo = image_repo
        self.uploader = uploader

    def execute(self, user_id: UUID, file: BinaryIO, filename: str) -> Image:
        if not self._is_valid_format(filename):
            raise InvalidImageFormatError("Unsupported image format")
        unique_name = f"{uuid4().hex}{os.path.splitext(filename)[1].lower()}"
        url = self.uploader.upload(file, unique_name)
        image = Image(id=uuid4(), owner_id=user_id, data_url=url, like_count=0)
        self.image_repo.save(image)
        return image

    def _is_valid_format(self, filename: str) -> bool:
        ext = os.path.splitext(filename)[1].lower()
        mime, _ = mimetypes.guess_type(filename)
        return ext in self.allowed_extensions and mime in self.allowed_mimetypes
