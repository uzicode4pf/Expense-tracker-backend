from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any

class IncomeCreate(BaseModel):
    source: str
    description: Optional[str] = None
    amount: float
    date: Optional[datetime] = None

class IncomeData(BaseModel):
    id: str
    user_id: str
    source: str
    description: Optional[str]
    amount: float
    date: datetime

class IncomeResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None