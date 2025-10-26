# app/api/routes/export.py
from fastapi import APIRouter, Depends
from app.utils.security import get_current_user
from app.models.user import User
from app.utils.pdf_exporter import generate_pdf
from app.database.connection import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="",
    tags=["export"]
)

@router.get("/")
def export_transactions(format: str, 
                        current_user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    # for simplicity, only PDF here
    if format.lower() == "pdf":
        file_url = generate_pdf(user_id=current_user.id, db=db)
        return {"success": True, "fileUrl": file_url}
    return {"success": False, "message": "Unsupported format"}