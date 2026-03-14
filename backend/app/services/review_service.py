from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.album import Album
from app.models.review import Review
from app.models.user import User
from app.schemas import ReviewCreate


def create_album_review(
    db: Session,
    album_id: int,
    current_user: User,
    review_data: ReviewCreate,
) -> Review:
    album = db.query(Album).filter(Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")

    existing_review = (
        db.query(Review)
        .filter(Review.album_id == album_id, Review.user_id == current_user.id)
        .first()
    )
    if existing_review is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Review already exists for this user on this album",
        )

    new_review = Review(
        user_id=current_user.id,
        album_id=album_id,
        rating=review_data.rating,
        comment=review_data.content,
    )

    db.add(new_review)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Review already exists for this user on this album",
        )

    db.refresh(new_review)
    return new_review
