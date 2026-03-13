from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class SavedAlbum(Base):
    __tablename__ = "saved_albums"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"), primary_key=True)

    saved_at = Column(TIMESTAMP, server_default=func.now())