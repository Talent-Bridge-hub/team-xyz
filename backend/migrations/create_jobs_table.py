"""
Database Migration: Create jobs table
Stores scraped job postings with JSONB fields for flexible data
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import database as db_module


def create_jobs_table():
    """
    Create jobs table with JSONB support for flexible data storage
    """
    
    # Drop existing table if exists (for clean migration)
    drop_query = "DROP TABLE IF EXISTS jobs CASCADE;"
    
    # Create jobs table
    create_query = """
    CREATE TABLE IF NOT EXISTS jobs (
        id SERIAL PRIMARY KEY,
        job_id VARCHAR(255) UNIQUE NOT NULL,
        title VARCHAR(500) NOT NULL,
        company VARCHAR(500) NOT NULL,
        location TEXT NOT NULL,
        region VARCHAR(100),
        job_type VARCHAR(50) DEFAULT 'Full-time',
        experience_level VARCHAR(50),
        description TEXT,
        required_skills JSONB DEFAULT '[]'::jsonb,
        preferred_skills JSONB DEFAULT '[]'::jsonb,
        salary_range JSONB,
        posted_date VARCHAR(50),
        remote BOOLEAN DEFAULT false,
        url TEXT NOT NULL,
        source VARCHAR(100),
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Create indexes for better query performance
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_jobs_job_id ON jobs(job_id);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_region ON jobs(region);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_job_type ON jobs(job_type);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_experience_level ON jobs(experience_level);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_remote ON jobs(remote);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_fetched_at ON jobs(fetched_at DESC);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_required_skills ON jobs USING GIN(required_skills);",
        "CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date DESC);"
    ]
    
    try:
        print("Creating jobs table...")
        
        # Initialize connection pool
        db_module.initialize_connection_pool()
        
        # Drop existing table
        print("  - Dropping existing table if exists...")
        db_module.execute_query(drop_query, fetch=False)
        
        # Create table
        print("  - Creating jobs table...")
        db_module.execute_query(create_query, fetch=False)
        
        # Create indexes
        print("  - Creating indexes...")
        for index_query in indexes:
            db_module.execute_query(index_query, fetch=False)
        
        print("✓ Jobs table created successfully!")
        print("\nTable schema:")
        print("  - job_id: Unique identifier from API")
        print("  - title: Job title")
        print("  - company: Company name")
        print("  - location: Job location")
        print("  - region: Geographic region (MENA, Sub-Saharan Africa, etc.)")
        print("  - job_type: Employment type (Full-time, Part-time, etc.)")
        print("  - experience_level: Required experience (Junior, Mid-level, Senior)")
        print("  - description: Full job description")
        print("  - required_skills: JSONB array of required skills")
        print("  - preferred_skills: JSONB array of preferred skills")
        print("  - salary_range: JSONB object with min, max, currency")
        print("  - posted_date: When job was posted")
        print("  - remote: Whether remote work is available")
        print("  - url: Application URL")
        print("  - source: Where job was scraped from")
        print("  - fetched_at: When job was scraped")
        
        print("\n✓ Created 11 indexes for optimized queries")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating jobs table: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 70)
    print("Database Migration: Create Jobs Table")
    print("=" * 70)
    print()
    
    success = create_jobs_table()
    
    if success:
        print("\n" + "=" * 70)
        print("Migration completed successfully!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("Migration failed!")
        print("=" * 70)
        sys.exit(1)
