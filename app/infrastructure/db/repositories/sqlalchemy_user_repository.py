from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.db.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> Optional[User]:
        user_row = self.session.query(UserModel).filter_by(email=email).first()
        if user_row:
            return User(id=user_row.id, email=user_row.email, password=user_row.password)
        return None

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        user_row = self.session.query(UserModel).filter_by(id=user_id).first()
        if user_row:
            return User(id=user_row.id, email=user_row.email, password=user_row.password)
        return None

    def save(self, user: User) -> None:
        user_model = UserModel(id=user.id, email=user.email, password=user.password)
        self.session.add(user_model)
        self.session.commit()
