"""
User Models
===========

Pydantic models for user data validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserSignup(BaseModel):
    """User signup request."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    full_name: str


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response (no password)."""
    id: str
    email: str
    full_name: Optional[str] = None
    plan: str = "free"
    created_at: datetime


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UsageStats(BaseModel):
    """User usage statistics."""
    files_analyzed: int
    rows_processed: int
    plan: str
    limit_files: int
    limit_rows: int