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
from .models import (
    UserQueries,
    user_row_to_dict,
    user_row_to_response,
    prepare_user_data
)
from app.shared.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)
from app.shared.database import DatabaseWrapper
from app.core.config import settings


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
        result = self.db.execute_query(
            UserQueries.CHECK_EMAIL_EXISTS,
            (user_data.email,)
        )
        
        if result and result[0].get('exists'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and prepare data
        password_hash = get_password_hash(user_data.password)
        user_tuple = prepare_user_data(user_data.full_name, user_data.email, password_hash)
        
        # Create user in database
        result = self.db.execute_query(UserQueries.INSERT_USER, user_tuple)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        user_row = result[0]
        
        # Generate access token
        access_token = create_access_token(
            data={"sub": user_row["email"], "user_id": user_row["id"]}
        )
        
        # Build response
        user_response = UserResponseSchema(
            id=user_row["id"],
            email=user_row["email"],
            full_name=user_row.get("name", ""),
            created_at=user_row["created_at"]
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
        result = self.db.execute_query(
            UserQueries.SELECT_BY_EMAIL,
            (credentials.email,)
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user_row = result[0]
        user_dict = user_row_to_dict(user_row)
        
        # Verify password
        if not verify_password(credentials.password, user_dict["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Generate access token
        access_token = create_access_token(
            data={"sub": user_dict["email"], "user_id": user_dict["id"]}
        )
        
        # Build response
        user_response = UserResponseSchema(
            id=user_dict["id"],
            email=user_dict["email"],
            full_name=user_dict["full_name"],
            created_at=user_dict["created_at"]
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
        result = self.db.execute_query(UserQueries.SELECT_BY_ID, (user_id,))
        
        if not result:
            return None
        
        user_dict = user_row_to_dict(result[0])
        
        return UserResponseSchema(
            id=user_dict["id"],
            email=user_dict["email"],
            full_name=user_dict["full_name"],
            created_at=user_dict["created_at"]
        )
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email (internal use).
        
        Args:
            email: User email
            
        Returns:
            User data dictionary or None if not found
        """
        result = self.db.execute_query(UserQueries.SELECT_BY_EMAIL, (email,))
        
        if not result:
            return None
        
        return user_row_to_dict(result[0])
    
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
        result = self.db.execute_query(UserQueries.SELECT_BY_ID, (user_id,))
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_dict = user_row_to_dict(result[0])
        
        # Prepare update fields
        update_fields = {}
        
        if update_data.full_name:
            update_fields["name"] = update_data.full_name
        
        if update_data.email:
            # Check if new email already exists
            check_result = self.db.execute_query(
                "SELECT id FROM users WHERE email = %s AND id != %s",
                (update_data.email, user_id)
            )
            if check_result:
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
            if not verify_password(update_data.current_password, user_dict["password_hash"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Current password is incorrect"
                )
            
            # Hash new password
            update_fields["password"] = get_password_hash(update_data.new_password)
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        # Build dynamic UPDATE query
        update_fields["updated_at"] = datetime.utcnow()
        set_clause = ", ".join([f"{k} = %s" for k in update_fields.keys()])
        query = UserQueries.UPDATE_USER.format(fields=set_clause)
        params = tuple(list(update_fields.values()) + [user_id])
        
        # Update user
        result = self.db.execute_query(query, params)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user"
            )
        
        updated_user = user_row_to_dict(result[0])
        
        return UserResponseSchema(
            id=updated_user["id"],
            email=updated_user["email"],
            full_name=updated_user["full_name"],
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
        result = self.db.execute_query(UserQueries.SELECT_BY_ID, (user_id,))
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_dict = user_row_to_dict(result[0])
        
        # Verify current password
        if not verify_password(current_password, user_dict["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Hash and update new password
        new_password_hash = get_password_hash(new_password)
        
        self.db.execute_query(
            UserQueries.UPDATE_PASSWORD,
            (new_password_hash, datetime.utcnow(), user_id)
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
        result = self.db.execute_query(UserQueries.SELECT_BY_ID, (user_id,))
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Delete user
        self.db.execute_query(UserQueries.DELETE_USER, (user_id,))
        
        return True
