# Standard library imports for datetime handling
from datetime import datetime, timedelta
from typing import Optional

# Security related imports
from passlib.context import CryptContext  # For password hashing
from jose import JWTError, jwt            # For JWT handling

# Application settings
from app.core.config import get_settings

# Initialize settings and password context
settings = get_settings()
pwd_context = CryptContext(
    schemes=["bcrypt"],  # Use bcrypt for password hashing
    deprecated="auto"    # Automatically handle deprecated hash methods
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The password in plain text
        hashed_password: The hashed password to compare against
    
    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a password hash using bcrypt.
    
    Args:
        password: Plain text password to hash
    
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload to encode in the token
        expires_delta: Optional expiration time, defaults to 15 minutes
    
    Returns:
        str: Encoded JWT token
    
    Note:
        The token includes an expiration time and is signed with
        the secret key using the HS256 algorithm.
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    # Add expiration claim to payload
    to_encode.update({"exp": expire})
    
    # Create and sign the JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt 