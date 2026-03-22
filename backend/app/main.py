from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models
from app.routes.auth import router as auth_router
from app.routes.albums import router as album_router
from app.routes.artists import router as artist_router
from app.routes.reviews import router as review_router
from app.routes.users import router as user_router
from app.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create tables on startup so a fresh server can boot without a manual SQL step.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(album_router)
app.include_router(artist_router)
app.include_router(review_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Music API running"}
