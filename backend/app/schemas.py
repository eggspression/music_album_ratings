from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


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
    release_date: date | None
    genre: str
    cover_url: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ReviewCreate(BaseModel):
    rating: int
    content: str = Field(min_length=1)

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, value: int) -> int:
        if not 1 <= value <= 10:
            raise ValueError("Rating must be between 1 and 10")
        return value

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Content must not be empty")
        return cleaned_value


class ReviewRead(BaseModel):
    id: int
    album_id: int
    user_id: int
    username: str
    rating: int
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
