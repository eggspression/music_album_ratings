from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas import UserCreate
from app.security import hash_password, verify_password

def create_user(db: Session, user_data: UserCreate) -> User:
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(user_data.password)
    print("HASHED OK")
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_pw
    )
    print("CREATED USER")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("ADDED USER")
    return new_user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
