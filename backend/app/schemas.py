from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


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


class ReviewUserRead(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str | None = None


class AlbumBase(BaseModel):
    title: str
    artist_id: int
    release_date: date | None
    genre: str | None
    cover_url: str | None
    description: str | None

    model_config = {"from_attributes": True}


class AlbumSummaryRead(BaseModel):
    id: int
    title: str
    artist_name: str
    cover_url: str | None

    model_config = {"from_attributes": True}


class AlbumDetailRead(AlbumSummaryRead):
    artist_id: int
    release_date: date | None
    genre: str | None
    description: str | None
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
    rating: int
    comment: str | None
    user: ReviewUserRead
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserReviewRead(BaseModel):
    id: int
    album_id: int
    rating: int
    comment: str | None
    created_at: datetime
    updated_at: datetime
    album: AlbumSummaryRead

    model_config = {"from_attributes": True}


class SavedAlbumRead(BaseModel):
    album_id: int
    saved_at: datetime
    album: AlbumSummaryRead

    model_config = {"from_attributes": True}
