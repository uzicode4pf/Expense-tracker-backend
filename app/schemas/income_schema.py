from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

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

    class Config:
        from_attributes = True  


class IncomeResponse(BaseModel):
    success: bool
    message: str
    data: Optional[IncomeData | List[IncomeData]] = None