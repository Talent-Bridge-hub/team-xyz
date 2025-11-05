"""
Authentication Dependencies

FastAPI dependencies for authentication and authorization.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from app.shared.security import verify_token
from app.shared.database import get_database, DatabaseWrapper
from .service import AuthService
from .schemas import UserResponseSchema


# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scheme_name="JWT"
)


async def get_auth_service(
    db: DatabaseWrapper = Depends(get_database)
) -> AuthService:
    """
    Dependency to get auth service instance.
    
    Args:
        db: Database connection
        
    Returns:
        AuthService instance
    """
    return AuthService(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserResponseSchema:
    """
    Dependency to get current authenticated user from JWT token.
    
    Args:
        token: JWT access token from Authorization header
        auth_service: Auth service instance
        
    Returns:
        Current user information
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Verify token and extract payload
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get user_id from token
    user_id: Optional[int] = payload.get("user_id")
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Fetch user from database
    user = await auth_service.get_user_by_id(user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user


async def get_current_active_user(
    current_user: UserResponseSchema = Depends(get_current_user)
) -> UserResponseSchema:
    """
    Dependency to get current active user (user must be active).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    # Note: Add 'is_active' field to UserResponseSchema if you implement user deactivation
    # For now, all authenticated users are considered active
    return current_user


async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[UserResponseSchema]:
    """
    Dependency to get current user if authenticated, None otherwise.
    Useful for optional authentication endpoints.
    
    Args:
        token: Optional JWT access token
        auth_service: Auth service instance
        
    Returns:
        User information if authenticated, None otherwise
    """
    if not token:
        return None
    
    try:
        payload = verify_token(token)
        if payload is None:
            return None
        
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        
        return await auth_service.get_user_by_id(user_id)
    except Exception:
        return None


def require_roles(*required_roles: str):
    """
    Dependency factory to require specific user roles.
    
    Usage:
        @router.get("/admin")
        async def admin_endpoint(user = Depends(require_roles("admin"))):
            pass
    
    Args:
        *required_roles: Role names required to access endpoint
        
    Returns:
        Dependency function
    """
    async def role_checker(
        current_user: UserResponseSchema = Depends(get_current_user)
    ) -> UserResponseSchema:
        """
        Check if current user has required roles.
        
        Note: Implement role system in your database first.
        """
        # TODO: Implement role checking logic
        # For now, allow all authenticated users
        return current_user
    
    return role_checker


def require_permissions(*required_permissions: str):
    """
    Dependency factory to require specific permissions.
    
    Usage:
        @router.delete("/users/{user_id}")
        async def delete_user(
            user_id: int,
            user = Depends(require_permissions("users:delete"))
        ):
            pass
    
    Args:
        *required_permissions: Permission names required
        
    Returns:
        Dependency function
    """
    async def permission_checker(
        current_user: UserResponseSchema = Depends(get_current_user)
    ) -> UserResponseSchema:
        """
        Check if current user has required permissions.
        
        Note: Implement permission system in your database first.
        """
        # TODO: Implement permission checking logic
        # For now, allow all authenticated users
        return current_user
    
    return permission_checker
