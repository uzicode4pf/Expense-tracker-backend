# app/schemas/expense_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema for creating a new expense
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    type: str  # "income" or "expense"
    category: Optional[str] = None
    description: Optional[str] = None
    date: datetime

# Schema for returning an expense
class ExpenseResponse(BaseModel):
    id: str
    user_id: str
    title: str
    amount: float
    type: str
    category: Optional[str] = None
    description: Optional[str] = None
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
