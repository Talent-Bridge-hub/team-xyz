"""
Database connection and utilities
Wraps the existing config/database.py functions for FastAPI
"""

import sys
from typing import Optional, Dict, List, Any
from pathlib import Path

# Add parent directory to path to import existing modules
backend_dir = Path(__file__).resolve().parent.parent.parent
project_root = backend_dir.parent
sys.path.insert(0, str(project_root))

from config import database as db_module


class DatabaseWrapper:
    """
    Simple wrapper around config.database module functions
    Provides a consistent interface for FastAPI endpoints
    """
    
    def __init__(self):
        """Initialize database connection pool"""
        db_module.initialize_connection_pool()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results"""
        results = db_module.execute_query(query, params, fetch=True)
        return results if results else []
    
    def insert_one(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """Insert a single row and return the ID"""
        return db_module.insert_one(table, data)
    
    def update_one(self, table: str, data: Dict[str, Any], condition: str, params: tuple = None) -> bool:
        """
        Update a single row
        Note: config.database uses Dict for where, we adapt condition string
        """
        try:
            # Build SET clause
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
            
            # Combine data values and condition params
            all_params = tuple(list(data.values()) + list(params if params else []))
            db_module.execute_query(query, all_params, fetch=False)
            return True
        except Exception:
            return False
    
    def get_one(self, table: str, condition: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        """Get a single row matching condition"""
        query = f"SELECT * FROM {table} WHERE {condition} LIMIT 1"
        results = db_module.execute_query(query, params, fetch=True)
        return results[0] if results else None
    
    def delete_one(self, table: str, condition: str, params: tuple = None) -> bool:
        """Delete a single row"""
        try:
            query = f"DELETE FROM {table} WHERE {condition}"
            db_module.execute_query(query, params, fetch=False)
            return True
        except Exception:
            return False
    
    def get_many(self, table: str, condition: str = None, params: tuple = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get multiple rows matching optional condition"""
        where_clause = f"WHERE {condition}" if condition else ""
        query = f"SELECT * FROM {table} {where_clause} ORDER BY id DESC LIMIT {limit}"
        results = db_module.execute_query(query, params, fetch=True)
        return results if results else []
    
    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """Alias for insert_one"""
        return self.insert_one(table, data)
    
    def update(self, table: str, data: Dict[str, Any], condition: str, params: tuple = None) -> bool:
        """Alias for update_one"""
        return self.update_one(table, data, condition, params)


# Global database instance
_db_instance: Optional[DatabaseWrapper] = None


def get_database() -> DatabaseWrapper:
    """
    Dependency function for FastAPI endpoints
    Returns the database wrapper instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseWrapper()
    return _db_instance


class DatabaseManager:
    """Database manager for backwards compatibility with main.py"""
    
    def __init__(self):
        self._db: Optional[DatabaseWrapper] = None
    
    def get_db(self) -> DatabaseWrapper:
        """Get database instance"""
        if self._db is None:
            self._db = DatabaseWrapper()
        return self._db
    
    def close(self):
        """Close database connections"""
        # The connection pool is managed by config.database
        # No explicit close needed here
        pass


# Create global database manager instance
db_manager = DatabaseManager()
