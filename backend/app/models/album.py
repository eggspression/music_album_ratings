from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)

    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"), nullable=False)

    release_date = Column(Date)
    genre = Column(String(100))
    cover_url = Column(Text)
    description = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())

    artist = relationship("Artist", back_populates="albums")
    reviews = relationship("Review", back_populates="album", cascade="all, delete")

    __table_args__ = (
        UniqueConstraint("title", "artist_id", name="uq_album_title_artist"),
    )

    @property
    def artist_name(self) -> str | None:
        if self.artist is None:
            return None

        return self.artist.name
