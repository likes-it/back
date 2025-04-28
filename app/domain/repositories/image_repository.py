from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List
from app.domain.entities.image import Image

class ImageRepository(ABC):
    @abstractmethod
    def get_by_id(self, image_id: UUID) -> Optional[Image]:
        pass

    @abstractmethod
    def save(self, image: Image) -> None:
        pass

    @abstractmethod
    def update_like_count(self, image_id: UUID, count: int) -> None:
        pass

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> List[Image]:
        pass

    @abstractmethod
    def get_all(self) -> list[Image]:
        pass
