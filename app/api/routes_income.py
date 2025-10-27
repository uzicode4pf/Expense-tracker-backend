from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from typing import List

from app.database.connection import get_db
from app.models.income import Income
from app.models.user import User
from app.schemas.income_schema import IncomeCreate, IncomeResponse, IncomeData
from app.utils.security import get_current_user


router = APIRouter(
    prefix="",
    tags=["Income"]
)

# CREATE income record
@router.post("/", response_model=IncomeResponse)
def create_income(
    income: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_income = Income(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        amount=income.amount,
        source=income.source,
        description=income.description,
        date=income.date or datetime.utcnow(),
    )
    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return IncomeResponse(
        success=True,
        message="Income added successfully",
        data=IncomeData.model_validate(new_income)
    )


# READ all income records for logged-in user
@router.get("/", response_model=IncomeResponse)
def get_incomes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    incomes = db.query(Income).filter(Income.user_id == current_user.id).all()
    if not incomes:
        raise HTTPException(status_code=404, detail="No income records found")

    return IncomeResponse(
        success=True,
        message="Incomes fetched successfully",
        data=[IncomeData.model_validate(i) for i in incomes]
    )


#  DELETE a specific income record by ID
@router.delete("/{income_id}", response_model=IncomeResponse)
def delete_income(
    income_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    income = db.query(Income).filter(
        Income.id == income_id,
        Income.user_id == current_user.id
    ).first()

    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    db.delete(income)
    db.commit()

    return IncomeResponse(
        success=True,
        message=f"Income record '{income.source}' deleted successfully"
    )