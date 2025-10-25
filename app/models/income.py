from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.connection import Base
import uuid

class Income(Base):
    __tablename__ = "incomes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    source = Column(String, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ Relationship to User
    user = relationship("User", back_populates="incomes")
