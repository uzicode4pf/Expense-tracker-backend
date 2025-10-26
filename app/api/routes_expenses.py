from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.models.expense_model import Expense
from app.schemas.expense_schema import ExpenseCreate, ExpenseResponse
from app.utils.security import get_current_user

router = APIRouter(
    prefix="",
    tags=["Expenses"]
)

@router.post("/{user_id}", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, user_id: str, db: Session = Depends(get_db)):
    # Make sure the expense belongs to the current authenticated user
    new_expense = Expense(
        user_id=user_id,
        title=expense.title,
        amount=expense.amount,
        type=expense.type,
        category=expense.category,
        description=expense.description,
        date=expense.date
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/{user_id}", response_model=List[ExpenseResponse])
def get_expenses(user_id: str, db: Session = Depends(get_db)):
    expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
    return expenses

@router.delete("/{user_id}/{expense_id}")
def delete_expense(user_id: str, expense_id: str, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == user_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"success": True, "message": "Expense deleted successfully"}