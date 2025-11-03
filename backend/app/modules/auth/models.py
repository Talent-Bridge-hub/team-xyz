"""
Pydantic models for User authentication and management
Request/response schemas for auth endpoints
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


# ========== Request Models ==========

class UserRegister(BaseModel):
    """User registration request"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name")
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenRefresh(BaseModel):
    """Token refresh request"""
    refresh_token: str = Field(..., description="Refresh token")


class UserUpdate(BaseModel):
    """User profile update request"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = Field(None, min_length=8)
    
    @validator('new_password')
    def password_strength(cls, v):
        """Validate new password strength"""
        if v is not None:
            if not any(char.isdigit() for char in v):
                raise ValueError('Password must contain at least one digit')
            if not any(char.isupper() for char in v):
                raise ValueError('Password must contain at least one uppercase letter')
        return v


# ========== Response Models ==========

class UserResponse(BaseModel):
    """User information response"""
    id: int
    email: str
    full_name: str
    created_at: datetime
    
    @classmethod
    def model_validate(cls, obj):
        """Custom validation to map 'name' to 'full_name'"""
        if isinstance(obj, dict):
            # Map 'name' from DB to 'full_name' for API response
            if 'name' in obj and 'full_name' not in obj:
                obj['full_name'] = obj['name']
        return super().model_validate(obj)
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response after login/register"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


# ========== Database Models (for internal use) ==========

class UserInDB(BaseModel):
    """User model as stored in database"""
    id: int
    email: str
    full_name: str
    password_hash: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
