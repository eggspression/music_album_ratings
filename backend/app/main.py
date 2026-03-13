from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.albums import router as album_router
from app.routes.artists import router as artist_router
import app.models

app = FastAPI()

app.include_router(auth_router)
app.include_router(album_router)
app.include_router(artist_router)

@app.get("/")
def root():
    return {"message": "Music API running"}