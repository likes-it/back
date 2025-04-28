from uuid import UUID
from app.domain.repositories.image_repository import ImageRepository
from app.domain.repositories.image_like_repository import ImageLikeRepository
from app.domain.exceptions import NotFoundError, BadRequestError

class UnlikeImageUseCase:
    def __init__(self, image_repo: ImageRepository, like_repo: ImageLikeRepository):
        self.image_repo = image_repo
        self.like_repo = like_repo

    def execute(self, user_id: UUID, image_id: UUID) -> None:
        image = self.image_repo.get_by_id(image_id)
        if not image:
            raise NotFoundError("Image not found")

        existing_like = self.like_repo.get(image_id, user_id)
        if not existing_like or not existing_like.liked:
            raise BadRequestError("Image not liked yet")

        self.like_repo.delete(existing_like)

        updated_count = self.like_repo.count_active_likes(image_id)
        self.image_repo.update_like_count(image_id, updated_count)
