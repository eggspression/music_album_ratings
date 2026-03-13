from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"), nullable=False)

    rating = Column(Integer, nullable=False)
    comment = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="reviews")
    album = relationship("Album", back_populates="reviews")

    __table_args__ = (
        UniqueConstraint("user_id", "album_id", name="uq_user_album_review"),
        CheckConstraint("rating BETWEEN 1 AND 10", name="check_rating_range"),
    )
    