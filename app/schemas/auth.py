# Pydantic and typing imports
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """
    Base Pydantic model for user data.
    Contains fields common to all user-related schemas.
    """
    username: str

class UserCreate(UserBase):
    """
    Schema for user creation requests.
    Extends UserBase to include password field.
    """
    password: str

class UserLogin(UserBase):
    """
    Schema for user login requests.
    Extends UserBase to include password field.
    """
    password: str

class Token(BaseModel):
    """
    Schema for JWT token response.
    Contains the access token and its type.
    """
    access_token: str
    token_type: str

class LoginResponse(Token):
    """
    Schema for login response.
    Extends Token to include a success message.
    """
    message: str

class TokenData(BaseModel):
    """
    Schema for decoded token data.
    Contains the username extracted from the token.
    """
    username: Optional[str] = None

class User(UserBase):
    """
    Schema for user response.
    Contains all user fields that can be safely returned to clients.
    
    Note:
        Excludes sensitive information like passwords.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        """Configuration for the User model."""
        from_attributes = True  # Allows conversion from SQLAlchemy model 