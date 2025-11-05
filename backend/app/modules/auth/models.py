"""
Database models and queries for User authentication
Handles direct PostgreSQL database operations for the users table
"""

from typing import Optional, Dict, Any
from datetime import datetime


# ========== Database Schema Documentation ==========
"""
Users Table Schema (PostgreSQL):

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    region VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Note: 'name' field in DB maps to 'full_name' in API responses
"""


# ========== SQL Query Constants ==========

class UserQueries:
    """SQL queries for user operations"""
    
    # Create
    INSERT_USER = """
        INSERT INTO users (email, name, password_hash, created_at)
        VALUES (%s, %s, %s, %s)
        RETURNING id, email, name, created_at
    """
    
    # Read
    SELECT_BY_ID = """
        SELECT id, email, name, password_hash, created_at, updated_at
        FROM users
        WHERE id = %s
    """
    
    SELECT_BY_EMAIL = """
        SELECT id, email, name, password_hash, created_at, updated_at
        FROM users
        WHERE email = %s
    """
    
    SELECT_ALL = """
        SELECT id, email, name, created_at, updated_at
        FROM users
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """
    
    COUNT_USERS = """
        SELECT COUNT(*) as count FROM users
    """
    
    # Update
    UPDATE_PROFILE = """
        UPDATE users
        SET name = %s, email = %s, updated_at = %s
        WHERE id = %s
        RETURNING id, email, name, created_at, updated_at
    """
    
    UPDATE_PASSWORD = """
        UPDATE users
        SET password_hash = %s, updated_at = %s
        WHERE id = %s
    """
    
    UPDATE_USER = """
        UPDATE users
        SET {fields}
        WHERE id = %s
        RETURNING id, email, name, created_at, updated_at
    """
    
    # Delete
    DELETE_USER = """
        DELETE FROM users WHERE id = %s
    """
    
    # Check existence
    CHECK_EMAIL_EXISTS = """
        SELECT EXISTS(SELECT 1 FROM users WHERE email = %s) as exists
    """


# ========== Database Row Converters ==========

def user_row_to_dict(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert database row to dictionary with proper field mapping
    Maps 'name' (DB) to 'full_name' (API)
    """
    if not row:
        return None
    
    return {
        'id': row.get('id'),
        'email': row.get('email'),
        'full_name': row.get('name'),  # Map DB 'name' to API 'full_name'
        'password_hash': row.get('password_hash'),  # DB password_hash column
        'created_at': row.get('created_at'),
        'updated_at': row.get('updated_at')
    }


def user_row_to_response(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert database row to API response format (without password)
    """
    if not row:
        return None
    
    return {
        'id': row.get('id'),
        'email': row.get('email'),
        'full_name': row.get('name'),  # Map DB 'name' to API 'full_name'
        'created_at': row.get('created_at')
    }


def prepare_user_data(full_name: str, email: str, password_hash: str) -> tuple:
    """
    Prepare user data for insertion
    Returns tuple ready for SQL INSERT
    """
    return (email, full_name, password_hash, datetime.utcnow())


def prepare_update_data(user_id: int, **fields) -> tuple:
    """
    Prepare user data for update
    Returns tuple ready for SQL UPDATE
    """
    fields['updated_at'] = datetime.utcnow()
    # Map 'full_name' to 'name' for database
    if 'full_name' in fields:
        fields['name'] = fields.pop('full_name')
    
    return fields
