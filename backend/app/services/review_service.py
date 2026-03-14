from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

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

    return (
        db.query(Review)
        .options(joinedload(Review.user))
        .filter(Review.id == new_review.id)
        .first()
    )


def get_album_reviews(db: Session, album_id: int) -> list[Review]:
    album = db.query(Album).filter(Album.id == album_id).first()
    if album is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")

    reviews = (
        db.query(Review)
        .options(joinedload(Review.user))
        .filter(Review.album_id == album_id)
        .order_by(Review.created_at.desc())
        .all()
    )

    return reviews


def get_review_by_id(db: Session, review_id: int) -> Review:
    review = (
        db.query(Review)
        .options(joinedload(Review.user))
        .filter(Review.id == review_id)
        .first()
    )
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    return review


def update_review(
    db: Session,
    review_id: int,
    current_user: User,
    review_data: ReviewCreate,
) -> Review:
    review = get_review_by_id(db, review_id)

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this review",
        )

    review.rating = review_data.rating
    review.comment = review_data.content

    db.commit()

    return (
        db.query(Review)
        .options(joinedload(Review.user))
        .filter(Review.id == review.id)
        .first()
    )


def delete_review(db: Session, review_id: int, current_user: User) -> None:
    review = get_review_by_id(db, review_id)

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review",
        )

    db.delete(review)
    db.commit()
