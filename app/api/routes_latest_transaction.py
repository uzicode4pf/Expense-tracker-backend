# app/api/routes/latest_transactions.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.expense_model import Expense
from app.models.user import User
from app.utils.security import get_current_user

router = APIRouter(
    prefix="",
    tags=["latest_transactions"]
)

@router.get("/")
def latest_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    latest = db.query(Expense)\
               .filter(Expense.user_id == current_user.id)\
               .order_by(Expense.date.desc())\
               .limit(3)\
               .all()
    return {"latest": latest}