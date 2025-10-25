from app.models.user import User
from app.database.connection import SessionLocal
from app.utils.security import get_password_hash, verify_password, create_access_token
import uuid

def create_user(name: str, email: str, username: str, password: str):
    db = SessionLocal()

    
    existing_user = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()

    if existing_user:
        db.close()
        return None, "User with this email or username already exists"

    
    hashed_password = get_password_hash(str(password))
    user_id = str(uuid.uuid4())

    
    new_user = User(
        id=user_id,
        username=username,
        email=email,
        hashed_password=hashed_password,
        has_seen_onboarding=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    
    token = create_access_token({"sub": user_id})
    return new_user, token


def authenticate_user(email: str, password: str):
    """Check if user exists and verify password."""
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()

    if not user:
        db.close()
        return None

    if not verify_password(password, user.hashed_password):
        db.close()
        return None

    db.close()
    return user