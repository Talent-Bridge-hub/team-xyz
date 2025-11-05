"""
Authentication API endpoints
User registration, login, token refresh, profile management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .service import AuthService
from .schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserUpdateSchema,
    UserResponseSchema,
    TokenResponseSchema,
    MessageResponseSchema
)
from .dependencies import get_current_user, get_current_active_user
from app.shared.database import get_database, DatabaseWrapper


router = APIRouter()


def get_auth_service(db: DatabaseWrapper = Depends(get_database)) -> AuthService:
    """Dependency to get auth service instance."""
    return AuthService(db)


@router.post("/register", response_model=TokenResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegisterSchema,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters, must contain digit and uppercase
    - **full_name**: User's full name
    
    Returns JWT access token and user information
    """
    return await auth_service.register_user(user_data)


@router.post("/login", response_model=TokenResponseSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login with email and password
    
    - **username**: User's email address (OAuth2 spec uses 'username')
    - **password**: User's password
    
    Returns JWT access token and user information
    """
    # Convert form data to schema (OAuth2 uses 'username' field)
    credentials = UserLoginSchema(email=form_data.username, password=form_data.password)
    return await auth_service.login_user(credentials)


@router.get("/me", response_model=UserResponseSchema)
async def get_current_user_info(
    current_user: UserResponseSchema = Depends(get_current_active_user)
):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    """
    return current_user


@router.put("/profile", response_model=UserResponseSchema)
async def update_profile(
    update_data: UserUpdateSchema,
    current_user: UserResponseSchema = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Update user profile
    
    - **full_name**: Update full name (optional)
    - **email**: Update email address (optional)
    - **phone**: Update phone number (optional)
    - **location**: Update location (optional)
    - **new_password**: Change password (requires current_password)
    
    Requires valid JWT token in Authorization header
    """
    return await auth_service.update_profile(current_user.id, update_data)


@router.post("/refresh", response_model=TokenResponseSchema)
async def refresh_token(
    current_user: UserResponseSchema = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Refresh JWT access token
    
    Requires valid (non-expired) JWT token in Authorization header
    Returns new JWT token with extended expiry
    """
    return await auth_service.refresh_token(current_user)


@router.delete("/account", response_model=MessageResponseSchema)
async def delete_account(
    current_user: UserResponseSchema = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Delete user account (soft delete - marks as inactive)
    
    Requires valid JWT token in Authorization header
    This is a destructive operation and cannot be undone
    """
    return await auth_service.delete_account(current_user.id)
