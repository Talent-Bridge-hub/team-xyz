"""
Database migration to add resumes table
Run this script to create the resumes table
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from config.database import execute_query

def create_resumes_table():
    """Create the resumes table if it doesn't exist"""
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS resumes (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        filename VARCHAR(255) NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        file_type VARCHAR(10) NOT NULL,
        parsed_text TEXT,
        parsed_data JSONB,
        word_count INTEGER DEFAULT 0,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_analyzed TIMESTAMP,
        last_score FLOAT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """
    
    # Create indexes for better performance
    create_indexes_query = """
    CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
    CREATE INDEX IF NOT EXISTS idx_resumes_uploaded_at ON resumes(uploaded_at DESC);
    CREATE INDEX IF NOT EXISTS idx_resumes_last_score ON resumes(last_score);
    """
    
    try:
        print("Creating resumes table...")
        execute_query(create_table_query, fetch=False)
        print("✅ Resumes table created successfully")
        
        print("Creating indexes...")
        execute_query(create_indexes_query, fetch=False)
        print("✅ Indexes created successfully")
        
        print("\n🎉 Database migration completed!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = create_resumes_table()
    sys.exit(0 if success else 1)
