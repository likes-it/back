from pydantic import BaseModel
from uuid import UUID

class ImageResponse(BaseModel):
    id: UUID
    owner_id: UUID
    data_url: str
    like_count: int

    class Config:
        orm_mode = True

class ImageLikeResponse(BaseModel):
    id: UUID
    image_id: UUID
    user_id: UUID
    liked: bool

    class Config:
        orm_mode = True