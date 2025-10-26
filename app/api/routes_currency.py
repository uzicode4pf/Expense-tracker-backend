# app/api/routes/currency.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.database.connection import get_db
from app.utils.security import get_current_user

router = APIRouter(
    prefix="",
    tags=["currency"]
)

@router.put("/currency")
def update_currency(currency: str,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    current_user.currency = currency
    db.commit()
    db.refresh(current_user)
    return {"success": True, "message": "Currency updated successfully", "currency": currency}