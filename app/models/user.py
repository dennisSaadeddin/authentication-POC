# SQLAlchemy imports for database column types and utilities
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

# Import base class for SQLAlchemy models
from app.db.base import Base

class User(Base):
    """
    SQLAlchemy model for the users table.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        username: Unique username, indexed for faster lookups
        hashed_password: Bcrypt hashed password
        created_at: Timestamp of user creation
        updated_at: Timestamp of last user update
    """
    __tablename__ = "users"  # Database table name

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Username field with unique constraint and index
    username = Column(String, unique=True, index=True, nullable=False)
    
    # Hashed password field
    hashed_password = Column(String, nullable=False)
    
    # Timestamps for record tracking
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # Automatically set to current time on creation
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),  # Automatically updated when record changes
        nullable=True
    ) 