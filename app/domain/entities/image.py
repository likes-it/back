from uuid import UUID
from dataclasses import dataclass

@dataclass
class Image:
    id: UUID
    owner_id: UUID
    data_url: str
    like_count: int = 0
