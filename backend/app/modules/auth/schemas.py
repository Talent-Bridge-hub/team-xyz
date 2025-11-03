"""
Authentication Schemas

Pydantic models for request/response validation in the auth module.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


# ========== Request Schemas ==========

class UserRegisterSchema(BaseModel):
    """Schema for user registration request"""
    email: EmailStr = Field(..., description="User email address", example="user@example.com")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name")
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password has digit and uppercase letter"""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123",
                "full_name": "John Doe"
            }
        }


class UserLoginSchema(BaseModel):
    """Schema for user login request"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123"
            }
        }


class TokenRefreshSchema(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str = Field(..., description="JWT refresh token")


class UserUpdateSchema(BaseModel):
    """Schema for user profile update request"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="Updated full name")
    email: Optional[EmailStr] = Field(None, description="Updated email address")
    current_password: Optional[str] = Field(None, description="Current password (required for password change)")
    new_password: Optional[str] = Field(None, min_length=8, description="New password")
    
    @validator('new_password')
    def validate_new_password_strength(cls, v):
        """Validate new password has digit and uppercase letter"""
        if v is not None:
            if not any(char.isdigit() for char in v):
                raise ValueError('New password must contain at least one digit')
            if not any(char.isupper() for char in v):
                raise ValueError('New password must contain at least one uppercase letter')
        return v


class PasswordChangeSchema(BaseModel):
    """Schema for password change request"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    
    @validator('new_password')
    def validate_password_strength(cls, v):
        """Validate password has digit and uppercase letter"""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


# ========== Response Schemas ==========

class UserResponseSchema(BaseModel):
    """Schema for user information in responses"""
    id: int
    email: str
    full_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "created_at": "2025-01-01T00:00:00Z"
            }
        }


class TokenResponseSchema(BaseModel):
    """Schema for authentication token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserResponseSchema = Field(..., description="User information")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": 1,
                    "email": "john.doe@example.com",
                    "full_name": "John Doe",
                    "created_at": "2025-01-01T00:00:00Z"
                }
            }
        }


class MessageResponseSchema(BaseModel):
    """Schema for generic message responses"""
    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Operation success status")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully",
                "success": True
            }
        }


# ========== Internal Schemas (Database) ==========

class UserInDBSchema(BaseModel):
    """Schema for user as stored in database (internal use only)"""
    id: int
    email: str
    full_name: str
    password_hash: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool = True
    is_verified: bool = False
    
    class Config:
        from_attributes = True
