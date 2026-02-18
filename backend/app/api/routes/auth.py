"""
Authentication Routes
=====================

Signup, login, and user management endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
import logging
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os
from pydantic import BaseModel, EmailStr, Field  # Add Field here
from app.models.user import UserSignup, UserLogin, Token, UserResponse, UsageStats
from app.core.database import get_supabase
from app.core.email import send_verification_email, send_password_reset_email
from app.core.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)

logger = logging.getLogger(__name__)

router = APIRouter()


async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    Get current user from JWT token.
    
    Args:
        authorization: Bearer token from header
        
    Returns:
        User data dict
        
    Raises:
        HTTPException: If token is invalid
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Get user from database
    supabase = get_supabase()
    result = supabase.table("users").select("*").eq("id", user_id).execute()
    
    if not result.data:
        raise HTTPException(status_code=401, detail="User not found")
    
    return result.data[0]


@router.post("/signup")
async def signup(user_data: UserSignup):
    """
    Create new user account with email verification.
    """
    try:
        supabase = get_supabase()
        
        # Check if user already exists
        existing = supabase.table("users").select("id,email_verified").eq("email", user_data.email).execute()
        
        if existing.data:
            user = existing.data[0]
            if user.get("email_verified"):
                raise HTTPException(status_code=400, detail="Email already registered")
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="Email already registered but not verified. Please check your email."
                )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user (not verified yet)
        result = supabase.table("users").insert({
            "email": user_data.email,
            "password_hash": hashed_password,
            "full_name": user_data.full_name,
            "plan": "free",
            "email_verified": False
        }).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        user = result.data[0]
        
        # Send verification email
        try:
            await send_verification_email(user["email"], user["id"])
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
        
        logger.info(f"New user signed up: {user['email']} (verification pending)")
        
        # DON'T return token - user must verify email first
        return {
            "message": "Account created! Please check your email to verify your account.",
            "email": user["email"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login user.
    
    Args:
        credentials: Email and password
        
    Returns:
        JWT token and user data
    """
    try:
        supabase = get_supabase()
        
        # Get user by email
        result = supabase.table("users").select("*").eq("email", credentials.email).execute()
        
        if not result.data:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user = result.data[0]
        
        # Verify password
        if not verify_password(credentials.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create access token
        access_token = create_access_token(data={"sub": user["id"]})
        
        # Return token and user data
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            plan=user["plan"],
            created_at=user["created_at"]
        )
        
        logger.info(f"User logged in: {user['email']}")
        
        return Token(access_token=access_token, user=user_response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Get current user profile.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User data
    """
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        plan=current_user["plan"],
        created_at=current_user["created_at"]
    )


@router.get("/usage", response_model=UsageStats)
async def get_usage(current_user: dict = Depends(get_current_user)):
    """
    Get user's current usage statistics.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Usage statistics
    """
    try:
        supabase = get_supabase()
        
        # Call helper function
        result = supabase.rpc("get_current_usage", {"user_uuid": current_user["id"]}).execute()
        
        if not result.data:
            # No usage yet
            usage_data = {
                "files_analyzed": 0,
                "rows_processed": 0,
                "plan": current_user["plan"]
            }
        else:
            usage_data = result.data[0]
        
        # Define limits based on plan
        limits = {
            "free": {"files": 2, "rows": 1000},
            "pro": {"files": 50, "rows": 10000}
        }
        
        plan_limits = limits.get(usage_data["plan"], limits["free"])
        
        return UsageStats(
            files_analyzed=usage_data["files_analyzed"],
            rows_processed=usage_data["rows_processed"],
            plan=usage_data["plan"],
            limit_files=plan_limits["files"],
            limit_rows=plan_limits["rows"]
        )
        
    except Exception as e:
        logger.error(f"Usage fetch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/google/login")
async def google_login():
    """
    Redirect to Google OAuth consent screen.
    
    Returns:
        Redirect URL for Google login
    """
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    
    # Google OAuth URL
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={google_client_id}"
        f"&redirect_uri={redirect_uri}"
        "&response_type=code"
        "&scope=openid email profile"
        "&access_type=offline"
        "&prompt=consent"
    )
    
    return {"url": google_auth_url}


@router.get("/google/callback")
async def google_callback(code: str):
    """
    Handle Google OAuth callback.
    
    Args:
        code: Authorization code from Google
        
    Returns:
        JWT token and user data
    """
    try:
        import requests
        
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        
        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": google_client_id,
            "client_secret": google_client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
        
        token_response = requests.post(token_url, data=token_data)
        tokens = token_response.json()
        
        if "id_token" not in tokens:
            raise HTTPException(status_code=400, detail="Failed to get ID token from Google")
        
        # Verify and decode ID token
        id_info = id_token.verify_oauth2_token(
            tokens["id_token"],
            google_requests.Request(),
            google_client_id
        )
        
        email = id_info.get("email")
        name = id_info.get("name")
        google_id = id_info.get("sub")
        
        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by Google")
        
        # Check if user exists
        supabase = get_supabase()
        result = supabase.table("users").select("*").eq("email", email).execute()
        
        if result.data:
            # User exists - login
            user = result.data[0]
        else:
            # Create new user
            # Generate random password (won't be used, but required by schema)
            import secrets
            random_password = secrets.token_urlsafe(32)
            hashed_password = get_password_hash(random_password)
            
            new_user = supabase.table("users").insert({
                "email": email,
                "password_hash": hashed_password,
                "full_name": name,
                "plan": "free",
                "email_verified": True
            }).execute()
            
            if not new_user.data:
                raise HTTPException(status_code=500, detail="Failed to create user")
            
            user = new_user.data[0]
            logger.info(f"New user created via Google: {email}")
        
        # Create access token
        access_token = create_access_token(data={"sub": user["id"]})
        
        # Return token and user data
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            plan=user["plan"],
            created_at=user["created_at"]
        )
        
        # Redirect to frontend with token
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        
        # For now, return JSON (we'll make it redirect properly)
        return Token(access_token=access_token, user=user_response)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/verify-email")
async def verify_email(token: str):
    """
    Verify user's email address.
    
    Args:
        token: Email verification token
        
    Returns:
        Success message
    """
    try:
        # Decode token
        payload = decode_access_token(token)
        
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid or expired verification link")
        
        # Check token type
        if payload.get("type") != "email_verification":
            raise HTTPException(status_code=400, detail="Invalid verification token")
        
        user_id = payload.get("sub")
        
        # Update user as verified
        supabase = get_supabase()
        result = supabase.table("users").update({
            "email_verified": True
        }).eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"Email verified for user {user_id}")
        
        return {"message": "Email verified successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
from pydantic import BaseModel, EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """
    Send password reset email.
    
    Args:
        request: Email address
        
    Returns:
        Success message (always, for security)
    """
    try:
        supabase = get_supabase()
        
        # Find user by email
        result = supabase.table("users").select("id,email").eq("email", request.email).execute()
        
        if result.data:
            user = result.data[0]
            
            # Send reset email
            try:
                await send_password_reset_email(user["email"], user["id"])
                logger.info(f"Password reset email sent to {user['email']}")
            except Exception as e:
                logger.error(f"Failed to send password reset email: {e}")
        
        # Always return success (don't reveal if email exists)
        return {"message": "If that email exists, we sent a password reset link"}
        
    except Exception as e:
        logger.error(f"Forgot password error: {e}")
        # Still return success for security
        return {"message": "If that email exists, we sent a password reset link"}
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=72)


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """
    Reset user password with token.
    """
    try:
        # Decode token
        payload = decode_access_token(request.token)
        
        if not payload:
            raise HTTPException(status_code=400, detail="Invalid or expired reset link")
        
        # Check token type
        if payload.get("type") != "password_reset":
            raise HTTPException(status_code=400, detail="Invalid reset token")
        
        user_id = payload.get("sub")
        
        # Hash new password
        hashed_password = get_password_hash(request.new_password)
        
        # Update password
        supabase = get_supabase()
        result = supabase.table("users").update({
            "password_hash": hashed_password
        }).eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"Password reset for user {user_id}")
        
        return {"message": "Password reset successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        raise HTTPException(status_code=500, detail=str(e))