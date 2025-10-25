# app/utils/pdf_exporter.py

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.models.expense_model import Expense

EXPORT_DIR = "exports"

def generate_pdf(user_id, db):
    """
    Generates a simple PDF export of user transactions.
    Returns the file path (or URL).
    """
    # Create export folder if it doesn’t exist
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    # Fetch user transactions
    transactions = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .order_by(Expense.date.desc())
        .all()
    )

    # Define file path
    filename = f"{user_id}transactions{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(EXPORT_DIR, filename)

    # Create PDF canvas
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Expense Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Table header
    y = height - 120
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Date")
    c.drawString(150, y, "Title")
    c.drawString(300, y, "Type")
    c.drawString(400, y, "Amount")
    c.setFont("Helvetica", 10)
    y -= 20

    # Table content
    for t in transactions:
        c.drawString(50, y, t.date.strftime('%Y-%m-%d'))
        c.drawString(150, y, t.title[:20])  # Limit long titles
        c.drawString(300, y, t.type)
        c.drawString(400, y, f"{t.amount:.2f}")
        y -= 20

        # New page if reaching bottom
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

    return f"/{filepath}"