from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas import ReviewCreate, ReviewRead, AlbumDetailRead, AlbumSummaryRead
from app.security import get_current_user
from app.services.album_service import get_albums, get_album_by_id
from app.services.review_service import create_album_review, get_album_reviews

router = APIRouter(prefix="/albums", tags=["albums"])


@router.get("/", response_model=list[AlbumSummaryRead])
def list_albums(sort: str | None = None, 
              search: str | None = None,
              limit: int = 10,
              db: Session = Depends(get_db)):
    return get_albums(db, sort, search, limit)

@router.get("/{album_id}", response_model= AlbumDetailRead)
def get_album(album_id: int, db: Session = Depends(get_db)):
    return get_album_by_id(db, album_id)


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

