from pydantic import BaseModel
from uuid import UUID

class ImageResponse(BaseModel):
    id: UUID
    owner_id: UUID
    data_url: str
    like_count: int

    class Config:
        orm_mode = True
