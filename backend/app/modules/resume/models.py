"""
Database models and queries for Resume management
Handles direct PostgreSQL database operations for the resumes table
"""

from typing import Optional, Dict, Any
from datetime import datetime
import json


# ========== Database Schema Documentation ==========
"""
Resumes Table Schema (PostgreSQL):

CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    parsed_text TEXT,
    parsed_data JSONB,
    word_count INTEGER DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_analyzed TIMESTAMP,
    last_score FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_uploaded_at ON resumes(uploaded_at DESC);
"""


# ========== SQL Query Constants ==========

class ResumeQueries:
    """SQL queries for resume operations"""
    
    # Create
    INSERT_RESUME = """
        INSERT INTO resumes (
            user_id, filename, file_path, file_size, file_type,
            parsed_text, parsed_data, word_count, uploaded_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, user_id, filename, file_path, file_size, file_type,
                  parsed_text, parsed_data, word_count, uploaded_at,
                  last_analyzed, last_score
    """
    
    # Read
    SELECT_BY_ID = """
        SELECT id, user_id, filename, file_path, file_size, file_type,
               parsed_text, parsed_data, word_count, uploaded_at,
               last_analyzed, last_score
        FROM resumes
        WHERE id = %s
    """
    
    SELECT_BY_USER = """
        SELECT id, user_id, filename, file_path, file_size, file_type,
               parsed_text, parsed_data, word_count, uploaded_at,
               last_analyzed, last_score
        FROM resumes
        WHERE user_id = %s
        ORDER BY uploaded_at DESC
        LIMIT %s OFFSET %s
    """
    
    SELECT_BY_USER_AND_ID = """
        SELECT id, user_id, filename, file_path, file_size, file_type,
               parsed_text, parsed_data, word_count, uploaded_at,
               last_analyzed, last_score
        FROM resumes
        WHERE id = %s AND user_id = %s
    """
    
    COUNT_BY_USER = """
        SELECT COUNT(*) as count
        FROM resumes
        WHERE user_id = %s
    """
    
    # Update
    UPDATE_ANALYSIS = """
        UPDATE resumes
        SET last_analyzed = %s, last_score = %s
        WHERE id = %s
        RETURNING id, user_id, filename, file_path, file_size, file_type,
                  parsed_text, parsed_data, word_count, uploaded_at,
                  last_analyzed, last_score
    """
    
    UPDATE_RESUME = """
        UPDATE resumes
        SET {fields}
        WHERE id = %s AND user_id = %s
        RETURNING id, user_id, filename, file_path, file_size, file_type,
                  parsed_text, parsed_data, word_count, uploaded_at,
                  last_analyzed, last_score
    """
    
    # Delete
    DELETE_RESUME = """
        DELETE FROM resumes
        WHERE id = %s AND user_id = %s
    """
    
    # Check existence
    CHECK_RESUME_EXISTS = """
        SELECT EXISTS(
            SELECT 1 FROM resumes
            WHERE id = %s AND user_id = %s
        ) as exists
    """


# ========== Database Row Converters ==========

def resume_row_to_dict(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert database row to dictionary
    Handles JSONB parsing for parsed_data field
    """
    if not row:
        return None
    
    # Parse JSONB field if it's a string
    parsed_data = row.get('parsed_data')
    if isinstance(parsed_data, str):
        try:
            parsed_data = json.loads(parsed_data)
        except:
            parsed_data = {}
    
    return {
        'id': row.get('id'),
        'user_id': row.get('user_id'),
        'filename': row.get('filename'),
        'file_path': row.get('file_path'),
        'file_size': row.get('file_size'),
        'file_type': row.get('file_type'),
        'parsed_text': row.get('parsed_text'),
        'parsed_data': parsed_data,
        'word_count': row.get('word_count', 0),
        'uploaded_at': row.get('uploaded_at'),
        'last_analyzed': row.get('last_analyzed'),
        'last_score': row.get('last_score')
    }


def resume_row_to_list_item(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert database row to list item format (minimal fields)
    """
    if not row:
        return None
    
    return {
        'resume_id': row.get('id'),
        'filename': row.get('filename'),
        'uploaded_at': row.get('uploaded_at'),
        'last_analyzed': row.get('last_analyzed'),
        'last_score': row.get('last_score'),
        'word_count': row.get('word_count', 0),
        'file_type': row.get('file_type')
    }


def prepare_resume_data(
    user_id: int,
    filename: str,
    file_path: str,
    file_size: int,
    file_type: str,
    parsed_text: str,
    parsed_data: Dict[str, Any],
    word_count: int
) -> tuple:
    """
    Prepare resume data for insertion
    Returns tuple ready for SQL INSERT
    """
    # Convert parsed_data dict to JSON string for JSONB field
    parsed_data_json = json.dumps(parsed_data) if parsed_data else '{}'
    
    return (
        user_id,
        filename,
        file_path,
        file_size,
        file_type,
        parsed_text,
        parsed_data_json,
        word_count,
        datetime.utcnow()
    )


def prepare_analysis_update(resume_id: int, score: float) -> tuple:
    """
    Prepare data for updating analysis results
    Returns tuple ready for SQL UPDATE
    """
    return (datetime.utcnow(), score, resume_id)

