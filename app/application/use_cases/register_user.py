from uuid import uuid4
from app.domain.repositories.user_repository import UserRepository
from app.domain.exceptions import BadRequestError
from app.domain.services.auth_service import AuthService
from app.domain.entities.user import User

class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def execute(self, email: str, password: str, confirm_password: str) -> str:
        if password != confirm_password:
            raise BadRequestError("Passwords do not match")
        
        if self.user_repo.get_by_email(email):
            raise BadRequestError("User already exists")

        hashed = self.auth_service.hash_password(password)
        user = User(id=uuid4(), email=email, password=hashed)
        self.user_repo.save(user)

        return self.auth_service.create_token(user.id)
