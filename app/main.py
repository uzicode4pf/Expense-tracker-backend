from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    routes_onboarding,
    routes_auth,
    routes_expenses,
    routes_currency,
    routes_data_management,
    routes_export,
    routes_latest_transaction,
    routes_summary,
    routes_income
)

app = FastAPI(
    title="Expense Tracker API",
    description="Backend for tracking personal expenses and income with authentication, analytics, and PDF export.",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://trackraid.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(routes_onboarding.router, prefix="/api/onboarding", tags=["Onboarding"])
app.include_router(routes_auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(routes_expenses.router, prefix="/api/expenses", tags=["Expenses"])
app.include_router(routes_summary.router, prefix="/api/summary", tags=["Summary"])
app.include_router(routes_export.router, prefix="/api/export", tags=["Export"])
app.include_router(routes_latest_transaction.router, prefix="/api/latest", tags=["Latest Transactions"])
app.include_router(routes_currency.router, prefix="/api/currency", tags=["Currency"])
app.include_router(routes_data_management.router, prefix="/api/data", tags=["Data Management"])
app.include_router(routes_income.router, prefix="/api/income", tags=["Income"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Expense Tracker API is running"}

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": "Expense Tracker API"}