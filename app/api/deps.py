"""
Dependencies module for authentication and authorization.
Contains reusable dependencies that can be injected into routes.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import User

# Initialize OAuth2 scheme with token URL matching the login endpoint
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="Bearer Authentication"
)

# Get application settings
settings = get_settings()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency that validates a Bearer token and returns the corresponding user.
    
    This dependency can be used to protect routes that require authentication.
    The token is expected to be a JWT containing a "sub" claim with the username.
    
    Args:
        token: JWT token from the Authorization header (automatically extracted by OAuth2PasswordBearer)
        db: Database session for user lookup
        
    Returns:
        User: The authenticated user object
        
    Raises:
        HTTPException: If token is invalid, expired, or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and validate the JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Extract username from token payload
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
        
    # Lookup user in database
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    return user 