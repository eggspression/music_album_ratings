from sqlalchemy.orm import Session, joinedload

from app.models.album import Album
from app.models.review import Review
from app.models.savedalbum import SavedAlbum
from app.models.user import User


def get_current_user_reviews(db: Session, current_user: User) -> list[Review]:
    reviews = (
        db.query(Review)
        .options(joinedload(Review.album).joinedload(Album.artist))
        .filter(Review.user_id == current_user.id)
        .order_by(Review.created_at.desc())
        .all()
    )

    return reviews


def get_current_user_saved_albums(db: Session, current_user: User) -> list[SavedAlbum]:
    saved_albums = (
        db.query(SavedAlbum)
        .options(joinedload(SavedAlbum.album).joinedload(Album.artist))
        .filter(SavedAlbum.user_id == current_user.id)
        .order_by(SavedAlbum.saved_at.desc())
        .all()
    )

    return saved_albums
