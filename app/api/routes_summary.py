# app/api/routes/summary.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.connection import get_db
from app.models.expense_model import Expense
from app.models.user import User
from app.utils.security import get_current_user

router = APIRouter(
    prefix="/api/summary",
    tags=["summary"]
)

@router.get("/")
def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_income = db.query(func.sum(Expense.amount))\
                     .filter(Expense.user_id == current_user.id, Expense.type == "income")\
                     .scalar() or 0
    total_expense = db.query(func.sum(Expense.amount))\
                      .filter(Expense.user_id == current_user.id, Expense.type == "expense")\
                      .scalar() or 0
    balance = total_income - total_expense
    return {
        "income": total_income,
        "expense": total_expense,
        "balance": balance
    }