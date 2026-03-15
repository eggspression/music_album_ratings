from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from datetime import date

from app.database import get_db
from app.models.user import User
from app.schemas import (
    ReviewCreate,
    ReviewRead,
    AlbumDetailRead,
    AlbumSummaryRead,
    AlbumStatsRead,
    SavedAlbumRead,
    TrackRead,
)
from app.security import get_current_user
from app.services.album_service import (
    get_albums,
    get_album_by_id,
    get_album_stats,
    get_album_tracks,
    save_album_for_user,
    delete_saved_album_for_user,
)
from app.services.review_service import create_album_review, get_album_reviews

router = APIRouter(prefix="/albums", tags=["albums"])


@router.get("/", response_model=list[AlbumSummaryRead])
def list_albums(sort: str | None = None,
                search: str | None = None,
                genre: str | None = None,
                artist_id: int | None = None,
                start_date: date | None = None,
                end_date: date | None = None,
                limit: int = 10,
                offset: int = 0,
                db: Session = Depends(get_db)):
    return get_albums(db, sort, search, genre, artist_id, start_date, end_date, limit, offset)

@router.get("/{album_id}", response_model= AlbumDetailRead)
def get_album(album_id: int, db: Session = Depends(get_db)):
    return get_album_by_id(db, album_id)


@router.get("/{album_id}/stats", response_model=AlbumStatsRead)
def get_album_stats_endpoint(album_id: int, db: Session = Depends(get_db)):
    return get_album_stats(db, album_id)


@router.get("/{album_id}/tracks", response_model=list[TrackRead])
def list_album_tracks(album_id: int, db: Session = Depends(get_db)):
    return get_album_tracks(db, album_id)


@router.get("/{album_id}/reviews", response_model=list[ReviewRead])
def list_album_reviews(album_id: int, db: Session = Depends(get_db)):
    return get_album_reviews(db, album_id)


@router.post("/{album_id}/reviews", response_model=ReviewRead, status_code=201)
def create_review_for_album(
    album_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_album_review(db, album_id, current_user, review_data)


@router.post("/{album_id}/save", response_model=SavedAlbumRead, status_code=status.HTTP_201_CREATED)
def save_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return save_album_for_user(db, album_id, current_user)


@router.delete("/{album_id}/save", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_saved_album_for_user(db, album_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

