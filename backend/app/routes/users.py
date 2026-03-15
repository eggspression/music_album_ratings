from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas import UserReviewRead
from app.security import get_current_user
from app.services.user_service import get_current_user_reviews

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/reviews", response_model=list[UserReviewRead])
def list_current_user_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_current_user_reviews(db, current_user)
