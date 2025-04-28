from uuid import UUID
from app.domain.repositories.image_like_repository import ImageLikeRepository
from app.domain.entities.image_like import ImageLike

class GetMyLikesUseCase:
    def __init__(self, like_repo: ImageLikeRepository):
        self.like_repo = like_repo
    
    def execute(self, user_id: UUID) -> list[ImageLike]:
        return self.like_repo.get_all_liked_by_user(user_id)