from uuid import UUID
from dataclasses import dataclass

@dataclass
class User:
    id: UUID
    email: str
    password: str
