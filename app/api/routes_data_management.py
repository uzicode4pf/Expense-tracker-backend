# app/api/routes/data_management.py
from fastapi import APIRouter, Depends
from app.models.expense_model import Expense
from app.utils.security import get_current_user
from app.database.connection import get_db
from sqlalchemy.orm import Session
from app.models.user import User

router = APIRouter(
    prefix="",
    tags=["data_management"]
)

@router.delete("/data")
def delete_all_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Expense).filter(Expense.user_id == current_user.id).delete()
    db.commit()
    return {"success": True, "message": "All user data deleted successfully"}