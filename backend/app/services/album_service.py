from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.album import Album


def get_albums(db: Session,
               sort: str | None = None,
               search: str | None = None,
               limit: int = 10,
               ):
    query = db.query(Album)
    if search:
        query = query.filter(Album.title.ilike(f"%{search}"))
    if sort == "newest":
        query = query.order_by(desc(Album.release_date))

    albums = query.limit(limit).all()

    return albums

def get_album_by_id(db: Session, album_id: int):
    album = db.query(Album).filter(Album.id == album_id).first()

    return album
