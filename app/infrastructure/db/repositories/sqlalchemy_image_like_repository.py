from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session

from app.domain.entities.image_like import ImageLike
from app.domain.repositories.image_like_repository import ImageLikeRepository
from app.infrastructure.db.models.image_like_model import ImageLikeModel


class SQLAlchemyImageLikeRepository(ImageLikeRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, image_id: UUID, user_id: UUID) -> Optional[ImageLike]:
        row = self.session.query(ImageLikeModel).filter_by(image_id=image_id, user_id=user_id).first()
        if row:
            return ImageLike(id=row.id, image_id=row.image_id, user_id=row.user_id, liked=row.liked)
        return None

    def save(self, image_like: ImageLike) -> None:
        model = ImageLikeModel(
            id=image_like.id,
            image_id=image_like.image_id,
            user_id=image_like.user_id,
            liked=image_like.liked
        )
        self.session.merge(model)
        self.session.commit()

    def delete(self, image_like: ImageLike) -> None:
        self.session.query(ImageLikeModel).filter_by(id=image_like.id).delete()
        self.session.commit()

    def count_active_likes(self, image_id: UUID) -> int:
        return self.session.query(ImageLikeModel).filter_by(image_id=image_id, liked=True).count()

