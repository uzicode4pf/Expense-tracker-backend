from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from app.database.connection import Base
from datetime import datetime

class Income(Base):
    __tablename__ = "incomes"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    source = Column(String, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)