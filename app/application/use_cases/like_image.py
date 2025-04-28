from uuid import UUID, uuid4
from app.domain.repositories.image_repository import ImageRepository
from app.domain.repositories.image_like_repository import ImageLikeRepository
from app.domain.entities.image_like import ImageLike
from app.domain.exceptions import NotFoundError


class LikeImageUseCase:
    def __init__(self, image_repo: ImageRepository, like_repo: ImageLikeRepository):
        self.image_repo = image_repo
        self.like_repo = like_repo

    def execute(self, user_id: UUID, image_id: UUID) -> None:
        image = self.image_repo.get_by_id(image_id)
        if not image:
            raise NotFoundError("Image not found")

        existing_like = self.like_repo.get(image_id, user_id)

        if existing_like:
            if not existing_like.liked:
                existing_like.liked = True
                self.like_repo.save(existing_like)
        else:
            new_like = ImageLike(id=uuid4(), image_id=image_id, user_id=user_id, liked=True)
            self.like_repo.save(new_like)

        # on recalcule les likes actifs
        updated_count = self.like_repo.count_active_likes(image_id)
        self.image_repo.update_like_count(image_id, updated_count)
