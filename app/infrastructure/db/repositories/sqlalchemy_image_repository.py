from uuid import UUID
from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.entities.image import Image
from app.domain.repositories.image_repository import ImageRepository
from app.infrastructure.db.models.image_model import ImageModel


class SQLAlchemyImageRepository(ImageRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, image_id: UUID) -> Optional[Image]:
        row = self.session.query(ImageModel).filter_by(id=image_id).first()
        if row:
            return Image(id=row.id, owner_id=row.owner_id, data_url=row.data_url, like_count=row.like_count)
        return None

    def save(self, image: Image) -> None:
        model = ImageModel(
            id=image.id,
            owner_id=image.owner_id,
            data_url=image.data_url,
            like_count=image.like_count
        )
        self.session.add(model)
        self.session.commit()

    def update_like_count(self, image_id: UUID, count: int) -> None:
        self.session.query(ImageModel).filter_by(id=image_id).update({"like_count": count})
        self.session.commit()

    def list_by_user(self, user_id: UUID) -> List[Image]:
        rows = self.session.query(ImageModel).filter_by(owner_id=user_id).all()
        return [
            Image(id=r.id, owner_id=r.owner_id, data_url=r.data_url, like_count=r.like_count)
            for r in rows
        ]

    def get_all(self) -> list[Image]:
        return self.session.query(ImageModel).all()
    
    def delete(self, image_id: UUID) -> None:
        image = self.session.query(ImageModel).filter_by(id=image_id).first()
        if image:
            self.session.delete(image)
            self.session.commit()