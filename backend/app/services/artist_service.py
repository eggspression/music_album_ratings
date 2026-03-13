from sqlalchemy.orm import Session, joinedload
from app.models.artist import Artist
from app.models.album import Album


def get_artists(db: Session):
    return db.query(Artist).all()


def get_artist_by_id(db: Session, artist_id: int):
    return (
        db.query(Artist)
        .filter(Artist.id == artist_id)
        .first()
    )


def get_artist_albums(db: Session, artist_id: int):
    return (
        db.query(Album)
        .filter(Album.artist_id == artist_id)
        .all()
    )