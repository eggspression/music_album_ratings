from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str | None = None


class AlbumRead(BaseModel):
    id: int
    title: str
    artist_id: int
    release_date: datetime
    genre: str
    cover_url: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}
    
