from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True)

    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(255), nullable=False)
    track_number = Column(Integer, nullable=False)
    duration = Column(Integer)