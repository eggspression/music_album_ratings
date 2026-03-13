from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db

from app.services.artist_service import (
    get_artists,
    get_artist_by_id,
    get_artist_albums,
)

router = APIRouter(prefix="/artists", tags=["artists"])


@router.get("/")
def list_artists(db: Session = Depends(get_db)):
    return get_artists(db)


@router.get("/{artist_id}")
def get_artist_endpoint(artist_id: int, db: Session = Depends(get_db)):
    artist = get_artist_by_id(db, artist_id)

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    return artist


@router.get("/{artist_id}/albums")
def get_artist_albums_endpoint(artist_id: int, db: Session = Depends(get_db)):
    artist = get_artist_by_id(db, artist_id)

    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    albums = get_artist_albums(db, artist_id)
    return albums