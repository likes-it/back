from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

from app.domain.exceptions import NotFoundError, BadRequestError
from app.domain.exceptions import InvalidImageFormatError


from app.infrastructure.db.repositories.sqlalchemy_image_like_repository import SQLAlchemyImageLikeRepository
from app.infrastructure.db.repositories.sqlalchemy_image_repository import SQLAlchemyImageRepository
from app.infrastructure.uploader.minio_image_uploader import MinioImageUploader
from app.infrastructure.db.session import get_db

from app.application.use_cases.like_image import LikeImageUseCase
from app.application.use_cases.post_image import PostImageUseCase
from app.application.use_cases.unlike_image import UnlikeImageUseCase
from app.application.use_cases.delete_image import DeleteImageUseCase

from app.interfaces.api.auth_dependency import get_current_user_id
from app.interfaces.api.schema.image_schema import ImageResponse

router = APIRouter(prefix="/images", tags=["images"])

@router.post("/{image_id}/like")
def like_image(
    image_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    image_repo = SQLAlchemyImageRepository(db)
    like_repo = SQLAlchemyImageLikeRepository(db)
    use_case = LikeImageUseCase(image_repo, like_repo)

    try:
        use_case.execute(user_id=user_id, image_id=image_id)
        return {"message": "Image liked"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{image_id}/unlike")
def unlike_image(
    image_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    image_repo = SQLAlchemyImageRepository(db)
    like_repo = SQLAlchemyImageLikeRepository(db)
    use_case = UnlikeImageUseCase(image_repo, like_repo)

    try:
        use_case.execute(user_id=user_id, image_id=image_id)
        return {"message": "Image unliked"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/upload")
def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    image_repo = SQLAlchemyImageRepository(db)
    uploader = MinioImageUploader()
    use_case = PostImageUseCase(image_repo, uploader)

    try:
        with file.file as f:
            image = use_case.execute(user_id=user_id, file=f, filename=file.filename)
        return {
            "id": str(image.id),
            "owner_id": str(image.owner_id),
            "data_url": image.data_url,
            "like_count": image.like_count
        }
    except InvalidImageFormatError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/{image_id}", response_model=ImageResponse)
def get_image_by_id(
    image_id: UUID,
    db: Session = Depends(get_db)
):
    image_repo = SQLAlchemyImageRepository(db)
    image = image_repo.get_by_id(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@router.get("/", response_model=list[ImageResponse])
def list_images(db: Session = Depends(get_db)):
    image_repo = SQLAlchemyImageRepository(db)
    return image_repo.get_all()

@router.delete("/{image_id}")
def delete_image(
    image_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    image_repo = SQLAlchemyImageRepository(db)
    uploader = MinioImageUploader()
    use_case = DeleteImageUseCase(image_repo, uploader)

    try:
        use_case.execute(user_id=user_id, image_id=image_id)
        return {"message": "Image deleted"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")