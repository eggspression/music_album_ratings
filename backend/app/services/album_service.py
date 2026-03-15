from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc,asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from datetime import date

from app.models.album import Album
from app.models.savedalbum import SavedAlbum
from app.models.user import User


def get_albums(db: Session,
               sort: str | None = None,
               search: str | None = None,
               genre: str | None = None,
               artist_id: int | None = None,
               start_date: date | None = None,
               end_date: date | None = None,
               limit: int = 10,
               offset: int = 0,
               ):
    query = db.query(Album)
    if search:
        query = query.filter(Album.title.ilike(f"%{search}%"))
    if genre:
        query = query.filter(Album.genre.ilike(f"%{genre}%"))
    if artist_id:
        query = query.filter(Album.artist_id == artist_id)
    if start_date and end_date:
        query = query.filter(Album.release_date >= start_date, Album.release_date < end_date)
    if sort == "newest":
        query = query.order_by(desc(Album.release_date))
    if sort == "oldest":
        query = query.order_by(asc(Album.release_date))

    albums = query.offset(offset).limit(limit).all()

    return albums

def get_album_by_id(db: Session, album_id: int):
    album = db.query(Album).filter(Album.id == album_id).first()

    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return album


def save_album_for_user(db: Session, album_id: int, current_user: User) -> SavedAlbum:
    album = db.query(Album).filter(Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")

    existing_saved_album = (
        db.query(SavedAlbum)
        .filter(SavedAlbum.album_id == album_id, SavedAlbum.user_id == current_user.id)
        .first()
    )
    if existing_saved_album is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Album already saved for this user",
        )

    saved_album = SavedAlbum(user_id=current_user.id, album_id=album_id)
    db.add(saved_album)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Album already saved for this user",
        )

    return (
        db.query(SavedAlbum)
        .options(joinedload(SavedAlbum.album).joinedload(Album.artist))
        .filter(SavedAlbum.user_id == current_user.id, SavedAlbum.album_id == album_id)
        .first()
    )


def delete_saved_album_for_user(db: Session, album_id: int, current_user: User) -> None:
    album = db.query(Album).filter(Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")

    saved_album = (
        db.query(SavedAlbum)
        .filter(SavedAlbum.album_id == album_id, SavedAlbum.user_id == current_user.id)
        .first()
    )
    if saved_album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved album not found")

    db.delete(saved_album)
    db.commit()
