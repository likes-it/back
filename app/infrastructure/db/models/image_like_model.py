from sqlalchemy import Column, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid
from app.infrastructure.db.models.base import Base

class ImageLikeModel(Base):
    __tablename__ = "image_likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id", ondelete="CASCADE"), nullable=False)  
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    liked = Column(Boolean, default=True)

    image = relationship("ImageModel", back_populates="likes")
