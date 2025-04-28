from uuid import UUID
from app.domain.repositories.image_repository import ImageRepository
from app.domain.entities.image import Image


class GetMyImagesUseCase:
    def __init__(self, image_repo: ImageRepository):
        self.image_repo = image_repo

    def execute(self, user_id: UUID) -> list[Image]:
        return self.image_repo.get_all_by_owner(user_id) 