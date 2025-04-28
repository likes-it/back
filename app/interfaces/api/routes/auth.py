from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.domain.exceptions import BadRequestError
from app.infrastructure.db.session import get_db
from app.infrastructure.db.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.auth.auth_service import JWTAuthService
from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    confirm_password: str = Field(min_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(db)
    auth_service = JWTAuthService()
    use_case = RegisterUserUseCase(user_repo, auth_service)

    try:
        token = use_case.execute(data.email, data.password, data.confirm_password)
        return {"access_token": token}
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user_repo = SQLAlchemyUserRepository(db)
    auth_service = JWTAuthService()
    use_case = LoginUserUseCase(user_repo, auth_service)

    try:
        token = use_case.execute(data.email, data.password)
        return {"access_token": token}
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
