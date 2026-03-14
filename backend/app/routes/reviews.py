from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas import ReviewCreate, ReviewRead
from app.security import get_current_user
from app.services.review_service import delete_review, update_review

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.put("/{review_id}", response_model=ReviewRead)
def update_review_endpoint(
    review_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_review(db, review_id, current_user, review_data)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review_endpoint(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_review(db, review_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
