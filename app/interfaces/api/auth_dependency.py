from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_db
from app.infrastructure.db.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.auth.auth_service import JWTAuthService
from uuid import UUID

def get_current_user_id(
    request: Request,
    db: Session = Depends(get_db)
) -> UUID:
    auth_service = JWTAuthService()
    user_repo = SQLAlchemyUserRepository(db)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth_header[len("Bearer "):]
    try:
        user_id = auth_service.decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user_id
