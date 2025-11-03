"""
Authentication Service Layer

Business logic for user authentication, registration, and profile management.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

from .schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserUpdateSchema,
    UserResponseSchema,
    TokenResponseSchema,
    UserInDBSchema
)
from shared.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)
from shared.database import DatabaseWrapper
from core.config import settings


class AuthService:
    """
    Service class for authentication operations.
    
    Handles:
    - User registration
    - User login
    - Token generation and validation
    - Profile management
    - Password management
    """
    
    def __init__(self, db: DatabaseWrapper):
        """
        Initialize auth service with database connection.
        
        Args:
            db: Database wrapper instance
        """
        self.db = db
    
    async def register_user(self, user_data: UserRegisterSchema) -> TokenResponseSchema:
        """
        Register a new user and return access token.
        
        Args:
            user_data: User registration data
            
        Returns:
            Token response with user information
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user already exists
        existing_user = self.db.get_one(
            "users",
            "email = %s",
            (user_data.email,)
        )
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        password_hash = get_password_hash(user_data.password)
        
        # Create user in database
        user_id = self.db.insert_one(
            "users",
            email=user_data.email,
            password_hash=password_hash,
            name=user_data.full_name,  # DB column is 'name'
            created_at=datetime.utcnow()
        )
        
        # Fetch created user
        user = self.db.get_one("users", "id = %s", (user_id,))
        
        # Generate access token
        access_token = create_access_token(
            data={"sub": user["email"], "user_id": user["id"]}
        )
        
        # Build response
        user_response = UserResponseSchema(
            id=user["id"],
            email=user["email"],
            full_name=user.get("name", user.get("full_name", "")),
            created_at=user["created_at"]
        )
        
        return TokenResponseSchema(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response
        )
    
    async def login_user(self, credentials: UserLoginSchema) -> TokenResponseSchema:
        """
        Authenticate user and return access token.
        
        Args:
            credentials: User login credentials
            
        Returns:
            Token response with user information
            
        Raises:
            HTTPException: If credentials are invalid
        """
        # Find user by email
        user = self.db.get_one(
            "users",
            "email = %s",
            (credentials.email,)
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verify password
        if not verify_password(credentials.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Generate access token
        access_token = create_access_token(
            data={"sub": user["email"], "user_id": user["id"]}
        )
        
        # Build response
        user_response = UserResponseSchema(
            id=user["id"],
            email=user["email"],
            full_name=user.get("name", user.get("full_name", "")),
            created_at=user["created_at"]
        )
        
        return TokenResponseSchema(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user_response
        )
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserResponseSchema]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User information or None if not found
        """
        user = self.db.get_one("users", "id = %s", (user_id,))
        
        if not user:
            return None
        
        return UserResponseSchema(
            id=user["id"],
            email=user["email"],
            full_name=user.get("name", user.get("full_name", "")),
            created_at=user["created_at"]
        )
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email (internal use).
        
        Args:
            email: User email
            
        Returns:
            User data dictionary or None if not found
        """
        return self.db.get_one("users", "email = %s", (email,))
    
    async def update_user_profile(
        self,
        user_id: int,
        update_data: UserUpdateSchema
    ) -> UserResponseSchema:
        """
        Update user profile information.
        
        Args:
            user_id: User ID
            update_data: Updated user data
            
        Returns:
            Updated user information
            
        Raises:
            HTTPException: If user not found or validation fails
        """
        # Get current user
        user = self.db.get_one("users", "id = %s", (user_id,))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Prepare update fields
        update_fields = {}
        
        if update_data.full_name:
            update_fields["name"] = update_data.full_name
        
        if update_data.email:
            # Check if new email already exists
            existing = self.db.get_one(
                "users",
                "email = %s AND id != %s",
                (update_data.email, user_id)
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
            update_fields["email"] = update_data.email
        
        # Handle password change
        if update_data.new_password:
            if not update_data.current_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password required for password change"
                )
            
            # Verify current password
            if not verify_password(update_data.current_password, user["password_hash"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect"
                )
            
            # Hash new password
            update_fields["password_hash"] = get_password_hash(update_data.new_password)
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Add updated timestamp
        update_fields["updated_at"] = datetime.utcnow()
        
        # Update user
        self.db.update_one(
            "users",
            update_fields,
            "id = %s",
            (user_id,)
        )
        
        # Fetch updated user
        updated_user = self.db.get_one("users", "id = %s", (user_id,))
        
        return UserResponseSchema(
            id=updated_user["id"],
            email=updated_user["email"],
            full_name=updated_user.get("name", updated_user.get("full_name", "")),
            created_at=updated_user["created_at"]
        )
    
    async def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            True if successful
            
        Raises:
            HTTPException: If current password is incorrect
        """
        user = self.db.get_one("users", "id = %s", (user_id,))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not verify_password(current_password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Hash and update new password
        new_password_hash = get_password_hash(new_password)
        
        self.db.update_one(
            "users",
            {"password_hash": new_password_hash, "updated_at": datetime.utcnow()},
            "id = %s",
            (user_id,)
        )
        
        return True
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete user account.
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful
            
        Raises:
            HTTPException: If user not found
        """
        user = self.db.get_one("users", "id = %s", (user_id,))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Delete user
        self.db.delete_one("users", "id = %s", (user_id,))
        
        return True
