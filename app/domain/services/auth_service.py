from abc import ABC, abstractmethod
from uuid import UUID

class AuthService(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool:
        pass

    @abstractmethod
    def create_token(self, user_id: UUID) -> str:
        pass

    @abstractmethod
    def decode_token(self, token: str) -> UUID:
        pass
