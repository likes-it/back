from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from app.domain.entities.image_like import ImageLike

class ImageLikeRepository(ABC):
    @abstractmethod
    def get(self, image_id: UUID, user_id: UUID) -> Optional[ImageLike]:
        pass

    @abstractmethod
    def save(self, image_like: ImageLike) -> None:
        pass

    @abstractmethod
    def delete(self, image_like: ImageLike) -> None:
        pass

    @abstractmethod
    def count_active_likes(self, image_id: UUID) -> int:
        pass
