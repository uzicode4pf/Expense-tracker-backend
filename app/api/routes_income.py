from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.income import Income
from app.schemas.income_schema import IncomeCreate, IncomeResponse
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/income", tags=["Income"])

# CREATE
@router.post("/{user_id}", response_model=IncomeResponse)
def create_income(user_id: str, income: IncomeCreate, db: Session = Depends(get_db)):
    new_income = Income(
        id=str(uuid.uuid4()),
        user_id=user_id,
        amount=income.amount,
        source=income.source,
        description=income.description,
        date=income.date or datetime.utcnow(),
    )
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return IncomeResponse(success=True, message="Income added successfully", data=new_income)

# READ
@router.get("/{user_id}", response_model=IncomeResponse)
def get_income(user_id: str, db: Session = Depends(get_db)):
    incomes = db.query(Income).filter(Income.user_id == user_id).all()
    if not incomes:
        raise HTTPException(status_code=404, detail="No income records found")
    return IncomeResponse(success=True, message="Incomes fetched successfully", data=incomes)

# DELETE
@router.delete("/{user_id}/{income_id}", response_model=IncomeResponse)
def delete_income(user_id: str, income_id: str, db: Session = Depends(get_db)):
    income = db.query(Income).filter(
        Income.id == income_id, Income.user_id == user_id
    ).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    db.delete(income)
    db.commit()
    return IncomeResponse(success=True, message="Income deleted successfully")