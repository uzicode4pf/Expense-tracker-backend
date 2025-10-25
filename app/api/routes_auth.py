from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.user_service import create_user, authenticate_user
from app.utils.security import create_access_token

router = APIRouter()  # type: ignore

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate):
    new_user, token_or_message = create_user(
        name=user.name,
        email=user.email,
        username=user.username,
        password=user.password
    )
    if not new_user:
        raise HTTPException(status_code=400, detail=token_or_message)

    return UserResponse(
        success=True,
        message="Account created successfully",
        user_id=new_user.id,
        token=token_or_message
    )

@router.post("/login", response_model=UserResponse)
def login(user: UserLogin):
    existing_user = authenticate_user(user.email, user.password)
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"user_id": existing_user.id})
    return UserResponse(
        success=True,
        message="Login successful",
        user_id=existing_user.id,
        token=token
    )