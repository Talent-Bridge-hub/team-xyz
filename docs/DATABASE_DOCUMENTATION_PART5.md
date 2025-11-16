# CareerStar Database Documentation - Part 5
## Indexes, Migrations & Best Practices

## Table of Contents (Part 5)

1. [Index Strategy](#index-strategy)
2. [Migration System](#migration-system)
3. [Database Maintenance](#database-maintenance)
4. [Performance Optimization](#performance-optimization)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## 1. Index Strategy

### 1.1 Index Overview

**CareerStar** uses strategic indexing across all tables to optimize query performance:

| Index Type | Count | Purpose |
|-----------|-------|---------|
| **B-tree** (Default) | 35+ | Standard lookups, sorting, range queries |
| **GIN** (JSONB/Arrays) | 15+ | Full-text search, JSONB queries, array containment |
| **Unique** | 8+ | Enforce uniqueness constraints |
| **Composite** | 5+ | Multi-column queries |
| **Partial** | 3+ | Conditional indexing |

### 1.2 Complete Index Listing

#### **Users & Authentication**
```sql
-- Users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
CREATE INDEX idx_users_region ON users(region);
```

#### **Resume Module**
```sql
-- Resumes table
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_uploaded_at ON resumes(uploaded_at DESC);
CREATE INDEX idx_resumes_last_score ON resumes(last_score);
CREATE INDEX idx_resumes_parsed_data ON resumes USING GIN(parsed_data);

-- Analyses table
CREATE INDEX idx_analyses_resume_id ON analyses(resume_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX idx_analyses_overall_score ON analyses(overall_score DESC);

-- Improved resumes table
CREATE INDEX idx_improved_resumes_resume_id ON improved_resumes(resume_id);
CREATE INDEX idx_improved_resumes_version ON improved_resumes(resume_id, version);
CREATE INDEX idx_improved_resumes_analysis_id ON improved_resumes(analysis_id);
```

#### **Skills & Keywords**
```sql
-- Skills database
CREATE INDEX idx_skills_category ON skills_database(category);
CREATE INDEX idx_skills_popularity ON skills_database(popularity DESC);
CREATE INDEX idx_skills_region ON skills_database(region);
CREATE UNIQUE INDEX idx_skills_name ON skills_database(skill_name);

-- Job keywords
CREATE INDEX idx_keywords_job_role ON job_keywords(job_role);
CREATE INDEX idx_keywords_frequency ON job_keywords(frequency DESC);
CREATE INDEX idx_keywords_region ON job_keywords(region);
```

#### **Jobs Module**
```sql
-- Jobs table
CREATE INDEX idx_jobs_job_id ON jobs(job_id);
CREATE INDEX idx_jobs_title ON jobs(title);
CREATE INDEX idx_jobs_company ON jobs(company);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_region ON jobs(region);
CREATE INDEX idx_jobs_job_type ON jobs(job_type);
CREATE INDEX idx_jobs_experience_level ON jobs(experience_level);
CREATE INDEX idx_jobs_remote ON jobs(remote);
CREATE INDEX idx_jobs_fetched_at ON jobs(fetched_at DESC);
CREATE INDEX idx_jobs_posted_date ON jobs(posted_date DESC);
CREATE INDEX idx_jobs_required_skills ON jobs USING GIN(required_skills);
CREATE INDEX idx_jobs_preferred_skills ON jobs USING GIN(preferred_skills);

-- Saved jobs
CREATE INDEX idx_saved_jobs_user_id ON saved_jobs(user_id);
CREATE INDEX idx_saved_jobs_job_id ON saved_jobs(job_id);
CREATE INDEX idx_saved_jobs_status ON saved_jobs(status);
CREATE UNIQUE INDEX idx_saved_jobs_user_job ON saved_jobs(user_id, job_id);
```

#### **Interview Module**
```sql
-- Question bank
CREATE INDEX idx_question_bank_type ON question_bank(question_type);
CREATE INDEX idx_question_bank_difficulty ON question_bank(difficulty_level);
CREATE INDEX idx_question_bank_category ON question_bank(category);
CREATE INDEX idx_question_bank_region ON question_bank(region);
CREATE INDEX idx_question_bank_skills ON question_bank USING GIN(required_skills);
CREATE INDEX idx_question_bank_roles ON question_bank USING GIN(job_roles);
CREATE INDEX idx_question_bank_usage ON question_bank(usage_count DESC);

-- Interview sessions
CREATE INDEX idx_interview_sessions_user_id ON interview_sessions(user_id);
CREATE INDEX idx_interview_sessions_resume_id ON interview_sessions(resume_id);
CREATE INDEX idx_interview_sessions_status ON interview_sessions(status);
CREATE INDEX idx_interview_sessions_started_at ON interview_sessions(started_at DESC);

-- Interview questions
CREATE INDEX idx_interview_questions_session_id ON interview_questions(session_id);
CREATE INDEX idx_interview_questions_question_id ON interview_questions(question_id);
CREATE UNIQUE INDEX idx_interview_questions_session_order 
  ON interview_questions(session_id, question_order);

-- Interview answers
CREATE INDEX idx_interview_answers_question_id ON interview_answers(interview_question_id);
CREATE INDEX idx_interview_answers_session_id ON interview_answers(session_id);
CREATE INDEX idx_interview_answers_overall_score ON interview_answers(overall_score DESC);

-- Interview feedback
CREATE UNIQUE INDEX idx_interview_feedback_session_id ON interview_feedback(session_id);
```

#### **Footprint Module**
```sql
-- Footprint scans
CREATE INDEX idx_footprint_user_id ON footprint_scans(user_id);
CREATE INDEX idx_footprint_scanned_at ON footprint_scans(scanned_at DESC);
CREATE INDEX idx_footprint_github_username ON footprint_scans(github_username);
CREATE INDEX idx_footprint_stackoverflow_id ON footprint_scans(stackoverflow_user_id);
CREATE INDEX idx_footprint_visibility ON footprint_scans(overall_visibility_score DESC);
CREATE INDEX idx_footprint_platforms ON footprint_scans USING GIN(platforms_scanned);
```

### 1.3 Index Maintenance

**Check Index Usage:**
```sql
-- Find unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Analyze Index Performance:**
```sql
-- Get index statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched,
    idx_scan::float / NULLIF(idx_tup_read, 0) as selectivity
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

**Rebuild Bloated Indexes:**
```sql
-- Reindex specific table
REINDEX TABLE resumes;

-- Reindex entire database (during maintenance window)
REINDEX DATABASE utopiahire;
```

---

## 2. Migration System

### 2.1 Migration Architecture

**CareerStar** uses **Python-based migrations** with custom execute_query functions:

```
/backend/migrations/
├── create_resumes_table.py
├── create_jobs_table.py
├── create_interview_tables.py
├── create_footprint_tables.py
└── README.md
```

### 2.2 Migration Template

```python
#!/usr/bin/env python3
"""
Migration: Create [TABLE_NAME] table
Date: 2025-11-06
Author: UtopiaHire Team
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.database import initialize_connection_pool, execute_query

def migrate():
    """Execute migration"""
    print("🔄 Starting migration: create_table_name")
    
    # Initialize connection
    initialize_connection_pool()
    
    # Drop existing table (if needed)
    drop_sql = """
    DROP TABLE IF EXISTS table_name CASCADE;
    """
    
    # Create table
    create_sql = """
    CREATE TABLE IF NOT EXISTS table_name (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        column_name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Create indexes
    indexes_sql = """
    CREATE INDEX idx_table_user_id ON table_name(user_id);
    CREATE INDEX idx_table_created_at ON table_name(created_at DESC);
    """
    
    try:
        # Execute migration
        print("  📋 Dropping existing table...")
        execute_query(drop_sql, fetch=False)
        
        print("  ✅ Creating table...")
        execute_query(create_sql, fetch=False)
        
        print("  📇 Creating indexes...")
        execute_query(indexes_sql, fetch=False)
        
        print("✅ Migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)
```

### 2.3 Running Migrations

**Execute Single Migration:**
```bash
cd /home/firas/Utopia/backend
python migrations/create_resumes_table.py
```

**Execute All Migrations:**
```bash
cd /home/firas/Utopia/backend
for migration in migrations/create_*.py; do
    echo "Running $migration..."
    python "$migration"
    if [ $? -ne 0 ]; then
        echo "Migration failed: $migration"
        exit 1
    fi
done
```

**Migration with Data Seeding:**
```python
def seed_sample_data():
    """Seed initial data"""
    seed_sql = """
    INSERT INTO question_bank (question_text, question_type, difficulty_level, category)
    VALUES 
        ('Explain REST vs GraphQL', 'technical', 'mid', 'API Design'),
        ('Describe a tight deadline situation', 'behavioral', 'mid', 'Time Management'),
        ('How would you debug a production issue?', 'situational', 'senior', 'Problem Solving')
    ON CONFLICT DO NOTHING;
    """
    
    execute_query(seed_sql, fetch=False)
    print("  🌱 Sample data seeded successfully")

def migrate():
    # ... create tables ...
    seed_sample_data()
    # ...
```

---

## 3. Database Maintenance

### 3.1 Regular Maintenance Tasks

**Daily:**
```sql
-- Update table statistics for query planner
ANALYZE;
```

**Weekly:**
```sql
-- Vacuum to reclaim storage and update statistics
VACUUM ANALYZE;
```

**Monthly:**
```sql
-- Full vacuum (requires maintenance window)
VACUUM FULL;

-- Reindex all tables
REINDEX DATABASE utopiahire;
```

### 3.2 Backup & Restore

**Backup Database:**
```bash
# Full database dump
pg_dump -h localhost -U utopia_user -d utopiahire \
    -F c -b -v -f "/backup/utopiahire_$(date +%Y%m%d).dump"

# Schema only
pg_dump -h localhost -U utopia_user -d utopiahire \
    --schema-only -f "/backup/schema_$(date +%Y%m%d).sql"

# Data only
pg_dump -h localhost -U utopia_user -d utopiahire \
    --data-only -f "/backup/data_$(date +%Y%m%d).sql"
```

**Restore Database:**
```bash
# Restore from custom format dump
pg_restore -h localhost -U utopia_user -d utopiahire \
    -v "/backup/utopiahire_20251106.dump"

# Restore from SQL file
psql -h localhost -U utopia_user -d utopiahire \
    -f "/backup/schema_20251106.sql"
```

**Automated Backup Script:**
```bash
#!/bin/bash
# /home/firas/Utopia/scripts/backup_database.sh

BACKUP_DIR="/backup/utopiahire"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="utopiahire"
DB_USER="utopia_user"

mkdir -p "$BACKUP_DIR"

# Create backup
pg_dump -h localhost -U "$DB_USER" -d "$DB_NAME" \
    -F c -b -v -f "$BACKUP_DIR/backup_$DATE.dump"

# Keep only last 7 days
find "$BACKUP_DIR" -name "backup_*.dump" -mtime +7 -delete

echo "✅ Backup completed: backup_$DATE.dump"
```

**Schedule with Cron:**
```bash
# Daily backup at 2 AM
0 2 * * * /home/firas/Utopia/scripts/backup_database.sh >> /var/log/db_backup.log 2>&1
```

### 3.3 Monitoring

**Database Size:**
```sql
SELECT 
    pg_database.datname as database_name,
    pg_size_pretty(pg_database_size(pg_database.datname)) as size
FROM pg_database
WHERE datname = 'utopiahire';
```

**Table Sizes:**
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - 
                   pg_relation_size(schemaname||'.'||tablename)) as indexes_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**Connection Statistics:**
```sql
SELECT 
    datname,
    numbackends as active_connections,
    xact_commit as transactions_committed,
    xact_rollback as transactions_rolled_back,
    blks_read as blocks_read,
    blks_hit as blocks_hit,
    tup_returned as tuples_returned,
    tup_fetched as tuples_fetched,
    tup_inserted as tuples_inserted,
    tup_updated as tuples_updated,
    tup_deleted as tuples_deleted
FROM pg_stat_database
WHERE datname = 'utopiahire';
```

**Slow Queries:**
```sql
-- Enable query logging (postgresql.conf)
-- log_min_duration_statement = 1000  # Log queries > 1 second

-- View current active queries
SELECT 
    pid,
    now() - query_start as duration,
    state,
    query
FROM pg_stat_activity
WHERE state != 'idle'
  AND query NOT LIKE '%pg_stat_activity%'
ORDER BY duration DESC;
```

---

## 4. Performance Optimization

### 4.1 Query Optimization

**Use EXPLAIN ANALYZE:**
```sql
EXPLAIN ANALYZE
SELECT r.id, r.filename, u.name
FROM resumes r
JOIN users u ON r.user_id = u.id
WHERE r.uploaded_at >= NOW() - INTERVAL '30 days'
ORDER BY r.uploaded_at DESC
LIMIT 20;
```

**Optimize JSONB Queries:**
```sql
-- ❌ SLOW: Full JSONB scan
SELECT * FROM resumes
WHERE parsed_data::text LIKE '%Python%';

-- ✅ FAST: GIN index lookup
SELECT * FROM resumes
WHERE parsed_data @> '{"skills": {"technical": ["Python"]}}'::jsonb;

-- ✅ FAST: JSON path query
SELECT * FROM resumes
WHERE parsed_data->'skills'->'technical' ? 'Python';
```

**Batch Operations:**
```sql
-- ❌ SLOW: Multiple individual inserts
INSERT INTO jobs (title, company) VALUES ('Developer', 'TechCorp');
INSERT INTO jobs (title, company) VALUES ('Engineer', 'StartupXYZ');
-- ... 100 more times

-- ✅ FAST: Single batch insert
INSERT INTO jobs (title, company) VALUES
    ('Developer', 'TechCorp'),
    ('Engineer', 'StartupXYZ'),
    -- ... all 100 rows
    ('Analyst', 'DataCo');
```

**Connection Pooling Benefits:**
```python
# Without pooling: ~50ms per query (connection overhead)
# With pooling: ~5ms per query (10x faster)

# Connection pool reuses existing connections
connection = get_connection()  # Fast (from pool)
execute_query("SELECT ...", connection)
release_connection(connection)  # Returns to pool
```

### 4.2 Index Optimization

**Choose Right Index Type:**
```sql
-- B-tree: Default, good for equality & range queries
CREATE INDEX idx_users_created_at ON users(created_at);

-- GIN: For JSONB, arrays, full-text search
CREATE INDEX idx_resumes_parsed_data ON resumes USING GIN(parsed_data);

-- Partial: Index only relevant rows
CREATE INDEX idx_active_sessions ON interview_sessions(user_id)
WHERE status = 'in_progress';

-- Composite: Multi-column queries
CREATE INDEX idx_jobs_region_type ON jobs(region, job_type);
```

**Index Selectivity:**
```sql
-- Check column selectivity (unique values / total rows)
SELECT 
    COUNT(DISTINCT region)::float / COUNT(*) as selectivity
FROM jobs;

-- High selectivity (> 0.1): Good for indexing
-- Low selectivity (< 0.01): Consider partial index or skip
```

### 4.3 JSONB Best Practices

**Structure JSONB Efficiently:**
```json
// ✅ GOOD: Flat, predictable structure
{
  "skills": ["Python", "JavaScript"],
  "years_experience": 5
}

// ❌ BAD: Deep nesting, inconsistent
{
  "data": {
    "profile": {
      "skills": {
        "list": ["Python"]
      }
    }
  }
}
```

**Index JSONB Paths:**
```sql
-- Index specific path
CREATE INDEX idx_resumes_skills 
ON resumes USING GIN((parsed_data->'skills'));

-- Index entire JSONB
CREATE INDEX idx_resumes_parsed_data 
ON resumes USING GIN(parsed_data);
```

---

## 5. Best Practices

### 5.1 Schema Design

**✅ DO:**
- Use appropriate data types (INTEGER for IDs, not VARCHAR)
- Add CHECK constraints for data validation
- Use ON DELETE CASCADE for dependent data
- Include created_at and updated_at timestamps
- Use JSONB for flexible/nested data
- Add indexes on foreign keys

**❌ DON'T:**
- Store large BLOBs in database (use file storage)
- Use TEXT for short strings (use VARCHAR with limit)
- Over-normalize (reasonable denormalization is OK)
- Create indexes on low-selectivity columns
- Use FLOAT for monetary values (use NUMERIC)

### 5.2 Query Best Practices

**Parameterized Queries:**
```python
# ✅ SAFE: Parameterized
email = user_input
query = "SELECT * FROM users WHERE email = %s"
execute_query(query, (email,))

# ❌ VULNERABLE: SQL injection risk
query = f"SELECT * FROM users WHERE email = '{user_input}'"
execute_query(query)
```

**Limit Result Sets:**
```sql
-- ✅ Always use LIMIT for large tables
SELECT * FROM jobs WHERE region = 'Tunisia' LIMIT 100;

-- ❌ Can return millions of rows
SELECT * FROM jobs WHERE region = 'Tunisia';
```

**Use JOINs Wisely:**
```sql
-- ✅ EFFICIENT: Single JOIN
SELECT r.id, r.filename, u.name
FROM resumes r
JOIN users u ON r.user_id = u.id
WHERE r.uploaded_at >= NOW() - INTERVAL '30 days';

-- ❌ INEFFICIENT: N+1 query problem
-- SELECT * FROM resumes;
-- For each resume: SELECT * FROM users WHERE id = ?
```

### 5.3 Transaction Management

**Use Transactions:**
```python
def transfer_resume_ownership(old_user_id, new_user_id, resume_id):
    """Transfer resume with transaction"""
    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        # Start transaction (implicit with psycopg2)
        cursor.execute(
            "UPDATE resumes SET user_id = %s WHERE id = %s AND user_id = %s",
            (new_user_id, resume_id, old_user_id)
        )
        
        cursor.execute(
            "INSERT INTO audit_log (action, user_id, details) VALUES (%s, %s, %s)",
            ('transfer_resume', old_user_id, f'Resume {resume_id} to user {new_user_id}')
        )
        
        connection.commit()
        print("✅ Transfer completed")
        
    except Exception as e:
        connection.rollback()
        print(f"❌ Transfer failed: {e}")
        raise
    finally:
        release_connection(connection)
```

### 5.4 Security Best Practices

**Password Hashing:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash(plain_password)

# Verify password
is_valid = pwd_context.verify(plain_password, hashed)
```

**Row-Level Security (Future Enhancement):**
```sql
-- Enable RLS
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own resumes
CREATE POLICY user_resumes_policy ON resumes
    FOR SELECT
    USING (user_id = current_setting('app.current_user_id')::integer);
```

---

## 6. Troubleshooting

### 6.1 Common Issues

**Connection Pool Exhausted:**
```python
# Symptom: "Too many connections" error
# Solution: Increase pool size or fix connection leaks

# Check for leaks
connection = get_connection()
# ... do work ...
release_connection(connection)  # ⚠️ Don't forget!

# Or use context manager
with get_connection() as conn:
    # Automatically released
    execute_query("SELECT ...", conn)
```

**Slow Queries:**
```sql
-- Find slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    max_time
FROM pg_stat_statements
WHERE mean_time > 1000  -- > 1 second
ORDER BY mean_time DESC
LIMIT 10;

-- Enable pg_stat_statements (postgresql.conf)
-- shared_preload_libraries = 'pg_stat_statements'
```

**JSONB Query Performance:**
```sql
-- ❌ SLOW: No index
SELECT * FROM resumes
WHERE parsed_data->'skills'->'technical' @> '["Python"]';

-- ✅ FAST: Create GIN index
CREATE INDEX idx_resumes_skills 
ON resumes USING GIN((parsed_data->'skills'->'technical'));
```

**Deadlocks:**
```sql
-- View deadlock information
SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';

-- Prevention: Always lock tables in same order
BEGIN;
LOCK TABLE users IN SHARE MODE;
LOCK TABLE resumes IN SHARE MODE;
-- ... do work ...
COMMIT;
```

### 6.2 Performance Troubleshooting

**Check Table Bloat:**
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    n_dead_tup as dead_tuples,
    n_live_tup as live_tuples,
    ROUND(100 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_percentage
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_dead_tup DESC;

-- Solution: VACUUM FULL tablename;
```

**Analyze Query Plans:**
```sql
-- Get query plan with costs
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT * FROM resumes
WHERE user_id = 1
ORDER BY uploaded_at DESC
LIMIT 10;

-- Look for:
-- - Seq Scan (bad on large tables)
-- - Index Scan (good)
-- - High cost numbers
-- - Rows estimate vs actual
```

### 6.3 Data Integrity Issues

**Find Orphaned Records:**
```sql
-- Resumes without users (shouldn't happen with FK)
SELECT r.id, r.user_id
FROM resumes r
LEFT JOIN users u ON r.user_id = u.id
WHERE u.id IS NULL;

-- Fix: Delete orphaned records
DELETE FROM resumes
WHERE user_id NOT IN (SELECT id FROM users);
```

**Validate JSONB Structure:**
```sql
-- Find invalid JSONB structures
SELECT id, parsed_data
FROM resumes
WHERE NOT (parsed_data ? 'skills')
   OR jsonb_typeof(parsed_data->'skills') != 'object';
```

### 6.4 Maintenance Commands

**Vacuum & Analyze:**
```sql
-- Regular maintenance
VACUUM ANALYZE resumes;

-- Aggressive cleanup (requires lock)
VACUUM FULL resumes;

-- Auto-vacuum settings (postgresql.conf)
autovacuum = on
autovacuum_max_workers = 3
autovacuum_naptime = 1min
```

**Reindex:**
```sql
-- Rebuild single index
REINDEX INDEX idx_resumes_user_id;

-- Rebuild all table indexes
REINDEX TABLE resumes;

-- Rebuild all indexes (maintenance window)
REINDEX DATABASE utopiahire;
```

---

## 7. Quick Reference

### Essential Commands

| Task | Command |
|------|---------|
| **Connect** | `psql -h localhost -U utopia_user -d utopiahire` |
| **List tables** | `\dt` |
| **Describe table** | `\d resumes` |
| **List indexes** | `\di` |
| **Database size** | `SELECT pg_size_pretty(pg_database_size('utopiahire'));` |
| **Active queries** | `SELECT * FROM pg_stat_activity;` |
| **Kill query** | `SELECT pg_cancel_backend(pid);` |
| **Backup** | `pg_dump -U utopia_user utopiahire > backup.sql` |
| **Restore** | `psql -U utopia_user utopiahire < backup.sql` |

---

**End of Part 5**

---

