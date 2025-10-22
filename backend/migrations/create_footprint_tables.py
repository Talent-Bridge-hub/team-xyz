"""
Database Migration: Create footprint_scans table
Stores digital footprint analysis results from GitHub, StackOverflow, etc.
"""

import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(backend_dir)
sys.path.insert(0, project_root)

from config import database as db_module


def create_footprint_tables():
    """
    Create footprint scanning tables
    """
    
    # Drop existing table if exists
    drop_query = "DROP TABLE IF EXISTS footprint_scans CASCADE;"
    
    # Create footprint_scans table
    create_query = """
    CREATE TABLE IF NOT EXISTS footprint_scans (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        
        -- Scan metadata
        scan_type VARCHAR(50) DEFAULT 'full',
        platforms_scanned TEXT[] DEFAULT '{}',
        
        -- GitHub data (stored as JSONB for flexibility)
        github_username VARCHAR(200),
        github_data JSONB,
        github_score INTEGER,
        
        -- StackOverflow data
        stackoverflow_user_id INTEGER,
        stackoverflow_name VARCHAR(200),
        stackoverflow_data JSONB,
        stackoverflow_score INTEGER,
        
        -- LinkedIn data (future expansion)
        linkedin_url TEXT,
        linkedin_data JSONB,
        
        -- Overall scores
        overall_visibility_score INTEGER CHECK (overall_visibility_score >= 0 AND overall_visibility_score <= 100),
        professional_score INTEGER CHECK (professional_score >= 0 AND professional_score <= 100),
        
        -- Dimension scores
        visibility_score INTEGER DEFAULT 0 CHECK (visibility_score >= 0 AND visibility_score <= 100),
        activity_score INTEGER DEFAULT 0 CHECK (activity_score >= 0 AND activity_score <= 100),
        impact_score INTEGER DEFAULT 0 CHECK (impact_score >= 0 AND impact_score <= 100),
        expertise_score INTEGER DEFAULT 0 CHECK (expertise_score >= 0 AND expertise_score <= 100),
        
        -- Privacy analysis
        privacy_report JSONB,
        privacy_risk_level VARCHAR(50),
        
        -- Recommendations
        recommendations JSONB,
        career_insights JSONB,
        
        -- Timestamps
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """
    
    # Indexes for better query performance
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_footprint_user_id ON footprint_scans(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_footprint_scanned_at ON footprint_scans(scanned_at DESC);",
        "CREATE INDEX IF NOT EXISTS idx_footprint_github_username ON footprint_scans(github_username);",
        "CREATE INDEX IF NOT EXISTS idx_footprint_stackoverflow_id ON footprint_scans(stackoverflow_user_id);",
        "CREATE INDEX IF NOT EXISTS idx_footprint_visibility ON footprint_scans(overall_visibility_score DESC);",
        "CREATE INDEX IF NOT EXISTS idx_footprint_platforms ON footprint_scans USING GIN(platforms_scanned);",
    ]
    
    try:
        print("Creating footprint tables...")
        
        # Initialize connection pool
        db_module.initialize_connection_pool()
        
        # Drop existing table
        print("  - Dropping existing table if exists...")
        db_module.execute_query(drop_query, fetch=False)
        
        # Create table
        print("  - Creating footprint_scans table...")
        db_module.execute_query(create_query, fetch=False)
        
        # Create indexes
        print("  - Creating indexes...")
        for index_query in indexes:
            db_module.execute_query(index_query, fetch=False)
        
        print("✓ Footprint tables created successfully!")
        print("\nTable created:")
        print("  - footprint_scans: Stores digital footprint analysis")
        print("\n✓ Created 6 indexes for optimized queries")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating footprint tables: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 70)
    print("Database Migration: Create Footprint Tables")
    print("=" * 70)
    print()
    
    success = create_footprint_tables()
    
    if success:
        print("\n" + "=" * 70)
        print("Migration completed successfully!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("Migration failed!")
        print("=" * 70)
        sys.exit(1)
