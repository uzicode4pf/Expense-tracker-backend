from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# SessionLocal will be used for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all our models
Base = declarative_base()

# Dependency for creating and closing DB sessions in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()