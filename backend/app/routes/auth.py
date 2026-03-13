from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate, UserRead, UserLogin
from app.services.auth_service import create_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def create_user_endpoint(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)

@router.post("/login", response_model=UserRead)
def user_login_endpoint(login_data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, login_data)