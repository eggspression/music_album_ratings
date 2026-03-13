from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas import UserCreate, UserLogin


def create_user(db: Session, user_data: UserCreate) -> User:
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # For now, keep it simple
    # Later you should hash the password instead of storing raw text
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=user_data.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(db: Session, login_data: UserLogin) -> User:
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="No user associated with this email")
    if user.password_hash != login_data.password:
        raise HTTPException(status_code=400, detail="Wrong password")
    return user
    