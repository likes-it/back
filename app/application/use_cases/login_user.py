from app.domain.repositories.user_repository import UserRepository
from app.domain.services.auth_service import AuthService
from app.domain.exceptions import BadRequestError


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def execute(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise BadRequestError("Invalid credentials")

        if not self.auth_service.verify_password(password, user.password):
            raise BadRequestError("Invalid credentials")

        return self.auth_service.create_token(user.id)
