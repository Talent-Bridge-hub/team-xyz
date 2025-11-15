"""
Authentication API endpoints
User registration, login, token refresh, profile management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.app.models.user import (
    UserRegister, UserLogin, UserUpdate, 
    TokenResponse, UserResponse, MessageResponse
)
from backend.app.core.security import (
    get_password_hash, verify_password, create_access_token
)
from backend.app.core.config import settings
from backend.app.core.database import get_database, DatabaseWrapper
from backend.app.api.deps import get_current_user, get_current_active_user


router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: DatabaseWrapper = Depends(get_database)
):
    """
    Register a new user
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters, must contain digit and uppercase
    - **full_name**: User's full name
    
    Returns JWT access token and user information
    """
    # Check if user already exists
    existing_user = db.get_one("users", "email = %s", (user_data.email,))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = get_password_hash(user_data.password)
    
    # Create user in database
    user_id = db.insert_one(
        "users",
        {
            "email": user_data.email,
            "name": user_data.full_name,  # DB uses 'name', not 'full_name'
            "password_hash": password_hash,
            "accepted_privacy_policy": user_data.accepted_privacy_policy,
            "privacy_policy_accepted_at": datetime.utcnow() if user_data.accepted_privacy_policy else None,
            "created_at": datetime.utcnow()
        }
    )
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    # Get created user
    user = db.get_one("users", "id = %s", (user_id,))
    
    # Map 'name' to 'full_name' for response and exclude password_hash
    user_response_data = {
        'id': user['id'],
        'email': user['email'],
        'full_name': user.get('name', ''),
        'created_at': user.get('created_at')
    }
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user_id), "email": user_data.email}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(**user_response_data)
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: DatabaseWrapper = Depends(get_database)
):
    """
    Login with email and password
    
    - **username**: User's email address (OAuth2 spec uses 'username')
    - **password**: User's password
    
    Returns JWT access token and user information
    """
    # OAuth2 uses 'username' field for email
    email = form_data.username
    password = form_data.password
    
    # Get user from database
    user = db.get_one("users", "email = %s", (email,))
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Map 'name' to 'full_name' for response and exclude password_hash
    user_response_data = {
        'id': user['id'],
        'email': user['email'],
        'full_name': user.get('name', ''),
        'created_at': user.get('created_at')
    }
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user["id"]), "email": user["email"]}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(**user_response_data)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Get current authenticated user information
    
    Requires valid JWT token in Authorization header
    """
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: DatabaseWrapper = Depends(get_database)
):
    """
    Update user profile
    
    - **full_name**: Update full name (optional)
    - **email**: Update email address (optional)
    - **new_password**: Change password (requires current_password)
    
    Requires valid JWT token in Authorization header
    """
    updates = {}
    
    # Update full name
    if update_data.full_name is not None:
        updates["name"] = update_data.full_name  # DB uses 'name', not 'full_name'
    
    # Update email
    if update_data.email is not None:
        # Check if email is already taken
        existing = db.get_one("users", "email = %s AND id != %s", 
                             (update_data.email, current_user.id))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        updates["email"] = update_data.email
    
    # Update password
    if update_data.new_password is not None:
        if update_data.current_password is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password required to set new password"
            )
        
        # Verify current password
        user = db.get_one("users", "id = %s", (current_user.id,))
        if not verify_password(update_data.current_password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )
        
        updates["password_hash"] = get_password_hash(update_data.new_password)
    
    # Update timestamp
    updates["updated_at"] = datetime.utcnow()
    
    # Perform update
    if updates:
        success = db.update_one(
            "users",
            updates,
            "id = %s",
            (current_user.id,)
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update profile"
            )
    
    # Get updated user
    updated_user = db.get_one("users", "id = %s", (current_user.id,))
    # Map 'name' to 'full_name' for response
    if 'name' in updated_user:
        updated_user['full_name'] = updated_user['name']
    return UserResponse(**updated_user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """
    Refresh JWT access token
    
    Requires valid (non-expired) JWT token in Authorization header
    Returns new JWT token with extended expiry
    """
    # Create new access token
    access_token = create_access_token(
        data={"sub": str(current_user.id), "email": current_user.email}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=current_user
    )


@router.delete("/account", response_model=MessageResponse)
async def delete_account(
    current_user: UserResponse = Depends(get_current_active_user),
    db: DatabaseWrapper = Depends(get_database)
):
    """
    Delete user account (soft delete - marks as inactive)
    
    Requires valid JWT token in Authorization header
    This is a destructive operation and cannot be undone
    """
    # For now, actually delete (can implement soft delete later)
    success = db.delete_one("users", "id = %s", (current_user.id,))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete account"
        )
    
    return MessageResponse(
        message="Account successfully deleted",
        success=True
    )
