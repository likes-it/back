from uuid import UUID
from dataclasses import dataclass

@dataclass
class ImageLike:
    id: UUID
    image_id: UUID
    user_id: UUID
    liked: bool = True
