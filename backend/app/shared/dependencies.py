"""
API dependencies for authentication and common utilities
Used across all API endpoints
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.app.core.security import decode_access_token
from backend.app.core.database import get_database, DatabaseWrapper
from backend.app.models.user import UserResponse


# Security scheme for Bearer token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: DatabaseWrapper = Depends(get_database)
) -> UserResponse:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: Bearer token from request header
        db: Database connection
        
    Returns:
        UserResponse: Current user information
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Decode and verify token
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user ID from token
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = db.get_one("users", "id = %s", (int(user_id),))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Map 'name' to 'full_name' for response
    if 'name' in user:
        user['full_name'] = user['name']
    
    return UserResponse(**user)


async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Verify user is active (can be extended with is_active field)
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: Active user information
    """
    # Can add is_active check here if needed
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: DatabaseWrapper = Depends(get_database)
) -> Optional[UserResponse]:
    """
    Get current user if authenticated, None otherwise
    Useful for endpoints that work with or without authentication
    
    Args:
        credentials: Optional Bearer token
        db: Database connection
        
    Returns:
        Optional[UserResponse]: User if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        
        if user_id is None:
            return None
        
        user = db.get_one("users", "id = %s", (int(user_id),))
        if user is None:
            return None
        
        # Map 'name' to 'full_name' for response
        if 'name' in user:
            user['full_name'] = user['name']
        
        return UserResponse(**user)
    except Exception:
        return None
