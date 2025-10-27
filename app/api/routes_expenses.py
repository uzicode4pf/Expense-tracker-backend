from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.models.expense_model import Expense
from app.schemas.expense_schema import ExpenseCreate, ExpenseResponse
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/api/expenses",
    tags=["Expenses"]
)

#  Create Expense
@router.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_expense = Expense(
        user_id=current_user.id,
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

#  Get all expenses for logged-in user
@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    return expenses

#  Delete a specific expense by ID
@router.delete("/{expense_id}")
def delete_expense(expense_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(
        Expense.id == expense_id, Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"success": True, "message": f"Expense '{expense.title}' deleted successfully"}