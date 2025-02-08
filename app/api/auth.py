# Standard library imports
from datetime import timedelta
from typing import Any

# FastAPI imports
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Database imports
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Application imports
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, Token, User as UserSchema, LoginResponse

# Initialize router and settings
router = APIRouter()
settings = get_settings()

@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def signup(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user endpoint.
    
    Args:
        db: Async database session
        user_in: User creation data (username and password)
    
    Returns:
        Created user information
    
    Raises:
        HTTPException: If username is already registered
    """
    # Check if user exists in database
    result = await db.execute(select(User).where(User.username == user_in.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Create new user with hashed password
    user = User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login", response_model=LoginResponse)
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    User login endpoint.
    
    Args:
        db: Async database session
        form_data: OAuth2 form containing username and password
    
    Returns:
        JWT token and success message
    
    Raises:
        HTTPException: If credentials are invalid or user doesn't exist
    """
    # Check if user exists in database
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    # Handle non-existent user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to sign up!"
        )
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate access token with configured expiration
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},  # Subject claim in JWT
        expires_delta=access_token_expires
    )
    
    # Return token with success message
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Successfully logged in!"
    } 