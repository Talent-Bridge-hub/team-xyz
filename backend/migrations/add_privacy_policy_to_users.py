"""
Migration script to add privacy policy acceptance fields to users table
Run this script to update the database schema
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from config import database as db

def migrate():
    """Add privacy policy fields to users table"""
    
    print("Starting migration: Adding privacy policy fields to users table...")
    
    try:
        # Add password_hash column if it doesn't exist (for auth)
        db.execute_query("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);
        """, fetch=False)
        print("✓ Added password_hash column (if not exists)")
        
        # Add privacy policy acceptance column
        db.execute_query("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS accepted_privacy_policy BOOLEAN DEFAULT FALSE;
        """, fetch=False)
        print("✓ Added accepted_privacy_policy column")
        
        # Add privacy policy acceptance timestamp
        db.execute_query("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS privacy_policy_accepted_at TIMESTAMP;
        """, fetch=False)
        print("✓ Added privacy_policy_accepted_at column")
        
        # Update existing users to have accepted_privacy_policy = TRUE
        # (assuming existing users implicitly accepted when they registered)
        db.execute_query("""
            UPDATE users 
            SET accepted_privacy_policy = TRUE,
                privacy_policy_accepted_at = created_at
            WHERE accepted_privacy_policy IS NULL OR accepted_privacy_policy = FALSE;
        """, fetch=False)
        print("✓ Updated existing users to have accepted privacy policy")
        
        # Create index on privacy policy acceptance for analytics
        db.execute_query("""
            CREATE INDEX IF NOT EXISTS idx_users_privacy_accepted 
            ON users(accepted_privacy_policy, privacy_policy_accepted_at);
        """, fetch=False)
        print("✓ Created index on privacy policy fields")
        
        print("\n✅ Migration completed successfully!")
        print("Users table now includes privacy policy acceptance tracking.")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise


def rollback():
    """Rollback the migration (remove privacy policy fields)"""
    
    print("Rolling back migration: Removing privacy policy fields...")
    
    try:
        # Drop index
        db.execute_query("""
            DROP INDEX IF EXISTS idx_users_privacy_accepted;
        """, fetch=False)
        print("✓ Dropped privacy policy index")
        
        # Drop columns
        db.execute_query("""
            ALTER TABLE users 
            DROP COLUMN IF EXISTS accepted_privacy_policy,
            DROP COLUMN IF EXISTS privacy_policy_accepted_at;
        """, fetch=False)
        print("✓ Dropped privacy policy columns")
        
        print("\n✅ Rollback completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Rollback failed: {e}")
        raise


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate users table to add privacy policy fields')
    parser.add_argument('--rollback', action='store_true', help='Rollback the migration')
    args = parser.parse_args()
    
    # Initialize database connection
    db.initialize_connection_pool()
    
    if args.rollback:
        rollback()
    else:
        migrate()
