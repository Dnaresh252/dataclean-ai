"""
Email Service
=============

Send transactional emails (verification, password reset, etc.)
"""

import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# For now, we'll just log emails (you'll add real email service later)
async def send_verification_email(email: str, user_id: str) -> bool:
    """
    Send email verification link.
    
    Args:
        email: User's email address
        user_id: User's ID for verification token
        
    Returns:
        True if sent successfully
    """
    try:
        # Generate verification token
        from app.core.auth import create_access_token
        from datetime import timedelta
        
        # Token valid for 24 hours
        verification_token = create_access_token(
            data={"sub": user_id, "type": "email_verification"},
            expires_delta=timedelta(hours=24)
        )
        
        # Verification URL
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        verification_url = f"{frontend_url}/auth/verify-email?token={verification_token}"
        
        # Email content
        subject = "Verify your DataClean.AI email"
        body = f"""
        <h2>Welcome to DataClean.AI!</h2>
        <p>Thanks for signing up. Please verify your email address by clicking the link below:</p>
        <p><a href="{verification_url}" style="background: #10B981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Verify Email</a></p>
        <p>Or copy this link: {verification_url}</p>
        <p>This link expires in 24 hours.</p>
        <p>If you didn't create an account, you can safely ignore this email.</p>
        """
        
        # For now, just log (we'll add real email service after deployment)
        logger.info(f"📧 Verification email for {email}")
        logger.info(f"🔗 Verification URL: {verification_url}")
        
        # TODO: When deployed, use real email service (Resend/SendGrid)
        # Example:
        # import resend
        # resend.api_key = os.getenv("RESEND_API_KEY")
        # resend.Emails.send({
        #     "from": "noreply@dataclean.ai",
        #     "to": email,
        #     "subject": subject,
        #     "html": body
        # })
        
        return True
        
    except Exception as e:
        logger.error(f"Email send error: {e}")
        return False


async def send_password_reset_email(email: str, user_id: str) -> bool:
    """
    Send password reset link.
    """
    try:
        from app.core.auth import create_access_token
        from datetime import timedelta
        
        # Token valid for 1 hour
        reset_token = create_access_token(
            data={"sub": user_id, "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        reset_url = f"{frontend_url}/auth/reset-password?token={reset_token}"
        
        subject = "Reset your DataClean.AI password"
        body = f"""
        <h2>Password Reset Request</h2>
        <p>Click the link below to reset your password:</p>
        <p><a href="{reset_url}" style="background: #10B981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Reset Password</a></p>
        <p>Or copy this link: {reset_url}</p>
        <p>This link expires in 1 hour.</p>
        <p>If you didn't request this, you can safely ignore this email.</p>
        """
        
        logger.info(f"📧 Password reset email for {email}")
        logger.info(f"🔗 Reset URL: {reset_url}")
        
        return True
        
    except Exception as e:
        logger.error(f"Email send error: {e}")
        return False