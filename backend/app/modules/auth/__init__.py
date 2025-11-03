"""
Authentication Module

Handles user registration, login, JWT authentication, and profile management.

Features:
- User registration with email validation
- Secure login with JWT tokens
- Password hashing with bcrypt
- Profile management
- Protected route dependencies
"""

from .router import router
from .service import AuthService
from .schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserUpdateSchema,
    UserResponseSchema,
    TokenResponseSchema,
    MessageResponseSchema
)
from .dependencies import (
    get_current_user,
    get_current_active_user,
    get_optional_current_user,
    require_roles,
    require_permissions
)

__all__ = [
    # Router
    "router",
    
    # Service
    "AuthService",
    
    # Schemas
    "UserRegisterSchema",
    "UserLoginSchema",
    "UserUpdateSchema",
    "UserResponseSchema",
    "TokenResponseSchema",
    "MessageResponseSchema",
    
    # Dependencies
    "get_current_user",
    "get_current_active_user",
    "get_optional_current_user",
    "require_roles",
    "require_permissions",
]
