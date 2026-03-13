from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AlbumRead
from app.services.album_service import get_albums, get_album_by_id

router = APIRouter(prefix="/albums", tags=["albums"])


@router.get("/", response_model=list[AlbumRead])
def list_albums(sort: str | None = None, 
              search: str | None = None,
              limit: int = 10,
              db: Session = Depends(get_db)):
    return get_albums(db, sort, search, limit)

@router.get("/{album_id}", response_model= AlbumRead)
def get_album(album_id: int, db: Session = Depends(get_db)):
    return get_album_by_id(db, album_id)

