from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    bio = Column(Text)
    image_url = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    albums = relationship("Album", back_populates="artist", cascade="all, delete")