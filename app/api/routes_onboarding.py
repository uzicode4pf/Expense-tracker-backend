from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from app.utils.security import get_current_user

router = APIRouter(
    prefix="/api/onboarding",
    tags=["onboarding"]
)

@router.put("/")
def complete_onboarding(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.has_seen_onboarding = True  # type: ignore
    db.commit()
    db.refresh(current_user)
    return {"success": True, "message": "Onboarding completed"}