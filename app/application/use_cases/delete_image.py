from uuid import UUID
from app.domain.repositories.image_repository import ImageRepository
from app.domain.services.image_uploader import ImageUploader
from app.domain.exceptions import NotFoundError, BadRequestError

class DeleteImageUseCase:
    def __init__(self, image_repo: ImageRepository, uploader: ImageUploader):
        self.image_repo = image_repo
        self.uploader = uploader

    def execute(self, user_id: UUID, image_id: UUID) -> None:
        image = self.image_repo.get_by_id(image_id)
        if not image:
            raise NotFoundError("Image not found")

        if image.owner_id != user_id:
            raise BadRequestError("You are not allowed to delete this image")

        key = self.uploader.extract_key_from_url(image.data_url)
        self.uploader.delete(key)

        self.image_repo.delete(image_id)
