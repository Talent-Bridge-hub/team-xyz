# CareerStar Database Documentation - Part 1
## Overview, Architecture & Core Tables
 
---

## Table of Contents (Part 1)

1. [Database Overview](#database-overview)
2. [Architecture & Design](#architecture--design)
3. [Connection Management](#connection-management)
4. [Core Tables: Users & Authentication](#core-tables-users--authentication)
5. [Resume Management Tables](#resume-management-tables)

---

## 1. Database Overview

### Platform Database System

**CareerStar** uses PostgreSQL 14+ as its primary database management system, providing:
- **ACID Compliance**: Ensures data integrity and consistency
- **JSONB Support**: Flexible data storage for complex structures
- **Advanced Indexing**: GIN, B-tree, and partial indexes for optimal performance
- **Full-Text Search**: Built-in text search capabilities
- **Concurrent Access**: Multi-user support with row-level locking

### Database Configuration

**Connection Details:**
```
Host: localhost (configurable)
Port: 5432
Database: utopiahire
User: utopia_user
Password: (environment variable)
```

**Environment Variables:**
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=utopiahire
DB_USER=utopia_user
DB_PASSWORD=utopia_secure_2025
```

### Key Statistics

| Metric | Value |
|--------|-------|
| **Total Tables** | 18 |
| **Total Indexes** | 50+ |
| **Primary Data Types** | TEXT, INTEGER, JSONB, TIMESTAMP, BOOLEAN |
| **Total Modules** | 6 (Auth, Resume, Jobs, Interview, Footprint, Core) |
| **Estimated Size** | ~500MB (with sample data) |

---

## 2. Architecture & Design

### Database Schema Organization

The database is organized into **6 logical modules**:

```
┌─────────────────────────────────────────────────────────────┐
│                    CareerStar DATABASE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Module 1   │  │   Module 2   │  │   Module 3   │     │
│  │    Users     │  │   Resumes    │  │     Jobs     │     │
│  │     (2)      │  │     (4)      │  │     (2)      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Module 4   │  │   Module 5   │  │   Module 6   │     │
│  │  Interview   │  │  Footprint   │  │    Skills    │     │
│  │     (5)      │  │     (1)      │  │     (2)      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘

Numbers in parentheses indicate table count per module
```

### Entity Relationship Diagram

```
┌─────────────┐
│    users    │
│   (Core)    │
└──────┬──────┘
       │
       ├──────────────┬──────────────┬──────────────┬──────────────┐
       │              │              │              │              │
       ▼              ▼              ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ resumes  │   │saved_jobs│   │interview │   │footprint │   │  other   │
│          │   │          │   │sessions  │   │  scans   │   │  tables  │
└────┬─────┘   └──────────┘   └────┬─────┘   └──────────┘   └──────────┘
     │                              │
     ├──────────┬──────────┐        ├──────────┬──────────┐
     │          │          │        │          │          │
     ▼          ▼          ▼        ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│analyses │ │enhanced │ │ jobs    │ │questions│ │ answers │ │feedback │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

### Design Principles

**1. Normalization (3NF)**
- Minimal data redundancy
- Clear relationships between entities
- Efficient updates and deletions

**2. JSONB for Flexibility**
- Store complex nested data structures
- Easy schema evolution
- Fast querying with GIN indexes

**3. Cascading Deletes**
- `ON DELETE CASCADE` for dependent data
- Maintains referential integrity
- Automatic cleanup

**4. Timestamp Tracking**
- `created_at` for record creation
- `updated_at` for modifications (auto-updated via triggers)
- Audit trail for important operations

**5. Performance Optimization**
- Strategic indexing on frequently queried columns
- GIN indexes for JSONB and array columns
- Partial indexes for specific query patterns

---

## 3. Connection Management

### Connection Pool Architecture

**File:** `/config/database.py`

The database uses **connection pooling** for efficient resource management:

```python
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,      # Minimum connections maintained
    maxconn=10,     # Maximum concurrent connections
    host='localhost',
    port=5432,
    database='utopiahire',
    user='utopia_user',
    password='utopia_secure_2025'
)
```

**Benefits:**
- ✅ Reuses existing connections (faster than creating new ones)
- ✅ Limits concurrent connections (prevents database overload)
- ✅ Automatic connection management
- ✅ Thread-safe operations

### Connection Lifecycle

```mermaid
graph LR
    A[Request Arrives] --> B[Get Connection from Pool]
    B --> C[Execute Query]
    C --> D[Commit/Rollback]
    D --> E[Release Connection to Pool]
    E --> F[Connection Ready for Reuse]
```

### Core Database Functions

**1. Initialize Connection Pool:**
```python
def initialize_connection_pool(min_connections=1, max_connections=10):
    """Initialize database connection pool"""
    global connection_pool
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        min_connections, max_connections, **DB_CONFIG
    )
```

**2. Execute Query (Parameterized):**
```python
def execute_query(query: str, params: tuple = None, fetch: bool = True):
    """
    Execute SQL query with parameters (prevents SQL injection)
    
    Args:
        query: SQL with %s placeholders
        params: Tuple of values to safely insert
        fetch: Return results (True) or just execute (False)
    
    Returns:
        List of dictionaries (if fetch=True)
    """
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, params)
    
    if fetch:
        results = cursor.fetchall()
        connection.commit()
        return [dict(row) for row in results]
    else:
        connection.commit()
        return None
```

**3. Insert Data:**
```python
def insert_one(table: str, data: Dict[str, Any]) -> int:
    """
    Insert single row and return ID
    
    Example:
        user_id = insert_one('users', {
            'name': 'John Doe',
            'email': 'john@example.com'
        })
    """
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"
    result = execute_query(query, tuple(data.values()))
    return result[0]['id']
```

**4. Update Data:**
```python
def update_one(table: str, data: Dict, where: Dict) -> bool:
    """
    Update single row
    
    Example:
        update_one('users', {'name': 'Jane'}, {'id': 1})
    """
    set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
    where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    params = tuple(list(data.values()) + list(where.values()))
    execute_query(query, params, fetch=False)
    return True
```

**5. Retrieve Data:**
```python
def get_one(table: str, where: Dict) -> Optional[Dict]:
    """Get single row"""
    where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
    query = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"
    results = execute_query(query, tuple(where.values()))
    return results[0] if results else None

def get_many(table: str, where: Dict = None, limit: int = 100) -> List[Dict]:
    """Get multiple rows"""
    query = f"SELECT * FROM {table}"
    params = None
    
    if where:
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        query += f" WHERE {where_clause}"
        params = tuple(where.values())
    
    query += f" LIMIT {limit}"
    return execute_query(query, params) or []
```

### SQL Injection Prevention

**❌ NEVER DO THIS:**
```python
# VULNERABLE TO SQL INJECTION!
email = user_input
query = f"SELECT * FROM users WHERE email = '{email}'"
execute_query(query)
```

**✅ ALWAYS DO THIS:**
```python
# SAFE: Uses parameterized queries
email = user_input
query = "SELECT * FROM users WHERE email = %s"
execute_query(query, (email,))
```

---

## 4. Core Tables: Users & Authentication

### 4.1 Users Table

**Purpose:** Central user account storage for authentication and profile management

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    region VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-incrementing unique identifier |
| `name` | VARCHAR(255) | NOT NULL | User's full name |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | Email address (used for login) |
| `hashed_password` | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `region` | VARCHAR(100) | NULL | Geographic region (Tunisia, Nigeria, etc.) |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account status (soft delete support) |
| `created_at` | TIMESTAMP | AUTO | Account creation timestamp |
| `updated_at` | TIMESTAMP | AUTO | Last modification timestamp |

**Indexes:**
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

**Triggers:**
```sql
-- Auto-update updated_at on row modification
CREATE TRIGGER update_users_updated_at 
BEFORE UPDATE ON users
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();
```

**Security Features:**

1. **Password Hashing (Bcrypt):**
   ```python
   from passlib.context import CryptContext
   
   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
   hashed_password = pwd_context.hash(plain_password)
   ```

2. **Email Uniqueness:**
   - UNIQUE constraint prevents duplicate accounts
   - Case-insensitive comparison in application layer

3. **Soft Delete:**
   - `is_active` flag allows account deactivation without data loss
   - Maintains referential integrity

**Example Queries:**

```sql
-- Register new user
INSERT INTO users (name, email, hashed_password, region)
VALUES ('John Doe', 'john@example.com', '$2b$12$...', 'Tunisia')
RETURNING id, name, email, created_at;

-- Login (verify user exists)
SELECT id, name, email, hashed_password, is_active
FROM users
WHERE email = 'john@example.com' AND is_active = true;

-- Update profile
UPDATE users
SET name = 'Jane Doe', updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- Soft delete (deactivate account)
UPDATE users
SET is_active = false, updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- Get user count by region
SELECT region, COUNT(*) as user_count
FROM users
WHERE is_active = true
GROUP BY region
ORDER BY user_count DESC;
```

**Relationships:**
- **One-to-Many:** users → resumes
- **One-to-Many:** users → interview_sessions
- **One-to-Many:** users → footprint_scans
- **One-to-Many:** users → saved_jobs

---

## 5. Resume Management Tables

### 5.1 Resumes Table

**Purpose:** Store uploaded resume files and parsed content

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    raw_text TEXT,
    parsed_data JSONB,
    file_size INTEGER,
    word_count INTEGER DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_analyzed TIMESTAMP,
    last_score FLOAT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique resume identifier |
| `user_id` | INTEGER | FK → users(id), CASCADE | Resume owner |
| `filename` | VARCHAR(255) | NOT NULL | Original file name |
| `file_path` | TEXT | NOT NULL | Server storage path |
| `file_type` | VARCHAR(10) | NOT NULL | File extension (pdf, docx, doc) |
| `raw_text` | TEXT | NULL | Extracted plain text from file |
| `parsed_data` | JSONB | NULL | Structured resume data (see below) |
| `file_size` | INTEGER | NULL | File size in bytes |
| `word_count` | INTEGER | DEFAULT 0 | Total word count |
| `uploaded_at` | TIMESTAMP | AUTO | Upload timestamp |
| `last_analyzed` | TIMESTAMP | NULL | Last analysis date |
| `last_score` | FLOAT | NULL | Most recent ATS score (0-100) |
| `updated_at` | TIMESTAMP | AUTO | Last modification |

**Parsed Data Structure (JSONB):**
```json
{
  "personal_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+216 12 345 678",
    "location": "Tunis, Tunisia",
    "linkedin": "linkedin.com/in/johndoe"
  },
  "summary": "Experienced software engineer with 5+ years...",
  "skills": {
    "technical": ["Python", "JavaScript", "SQL", "Docker"],
    "soft": ["Leadership", "Communication", "Problem Solving"],
    "languages": ["English", "Arabic", "French"]
  },
  "experience": [
    {
      "title": "Senior Software Engineer",
      "company": "TechCorp",
      "location": "Tunis, Tunisia",
      "start_date": "2020-01",
      "end_date": "present",
      "description": "Led development of microservices architecture...",
      "achievements": [
        "Reduced API response time by 40%",
        "Mentored 5 junior developers"
      ]
    }
  ],
  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "University of Tunis",
      "location": "Tunis, Tunisia",
      "graduation_year": "2018",
      "gpa": "3.8/4.0"
    }
  ],
  "certifications": [
    {
      "name": "AWS Certified Solutions Architect",
      "issuer": "Amazon Web Services",
      "date": "2022-06",
      "expiry": "2025-06"
    }
  ],
  "projects": [
    {
      "name": "E-commerce Platform",
      "description": "Built scalable platform serving 100K+ users",
      "technologies": ["React", "Node.js", "PostgreSQL"],
      "url": "github.com/johndoe/ecommerce"
    }
  ]
}
```

**Indexes:**
```sql
CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_uploaded_at ON resumes(uploaded_at DESC);
CREATE INDEX idx_resumes_last_score ON resumes(last_score);
CREATE INDEX idx_resumes_parsed_data ON resumes USING GIN(parsed_data);
```

**File Storage:**
- **Location:** `/home/firas/Utopia/data/resumes/`
- **Naming:** `{user_id}_{timestamp}_{filename}`
- **Max Size:** 10MB (configurable)
- **Allowed Types:** PDF, DOCX, DOC

**Example Queries:**

```sql
-- Upload resume
INSERT INTO resumes (user_id, filename, file_path, file_type, file_size)
VALUES (1, 'resume.pdf', '/data/resumes/1_20251106_resume.pdf', 'pdf', 245678)
RETURNING id;

-- Update with parsed data
UPDATE resumes
SET 
    raw_text = 'Extracted text here...',
    parsed_data = '{"personal_info": {...}}'::jsonb,
    word_count = 450,
    updated_at = CURRENT_TIMESTAMP
WHERE id = 1;

-- Get user's resumes
SELECT id, filename, file_type, last_score, uploaded_at
FROM resumes
WHERE user_id = 1
ORDER BY uploaded_at DESC;

-- Search by skill (JSONB query)
SELECT r.id, r.filename, u.name as user_name
FROM resumes r
JOIN users u ON r.user_id = u.id
WHERE r.parsed_data @> '{"skills": {"technical": ["Python"]}}'::jsonb;

-- Get resumes needing analysis (no score or old)
SELECT id, filename, uploaded_at
FROM resumes
WHERE last_analyzed IS NULL 
   OR last_analyzed < NOW() - INTERVAL '30 days'
ORDER BY uploaded_at DESC
LIMIT 20;
```

---

### 5.2 Analyses Table

**Purpose:** Store AI-powered resume analysis results

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    ats_score INTEGER CHECK (ats_score >= 0 AND ats_score <= 100),
    formatting_score INTEGER CHECK (formatting_score >= 0 AND formatting_score <= 100),
    keyword_score INTEGER CHECK (keyword_score >= 0 AND keyword_score <= 100),
    overall_score INTEGER CHECK (overall_score >= 0 AND overall_score <= 100),
    suggestions JSONB,
    strengths JSONB,
    weaknesses JSONB,
    missing_sections JSONB,
    model_used VARCHAR(100),
    analysis_time_seconds FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Analysis identifier |
| `resume_id` | INTEGER | FK → resumes(id), CASCADE | Resume being analyzed |
| `ats_score` | INTEGER | 0-100 | ATS compatibility score |
| `formatting_score` | INTEGER | 0-100 | Visual formatting quality |
| `keyword_score` | INTEGER | 0-100 | Keyword matching score |
| `overall_score` | INTEGER | 0-100 | Composite score |
| `suggestions` | JSONB | NULL | Improvement recommendations |
| `strengths` | JSONB | NULL | Positive aspects found |
| `weaknesses` | JSONB | NULL | Areas needing improvement |
| `missing_sections` | JSONB | NULL | Recommended additions |
| `model_used` | VARCHAR(100) | NULL | AI model name (Groq, spaCy) |
| `analysis_time_seconds` | FLOAT | NULL | Processing duration |
| `created_at` | TIMESTAMP | AUTO | Analysis timestamp |

**Score Calculation:**
```
Overall Score = (ATS Score × 0.4) + (Keyword Score × 0.4) + (Formatting Score × 0.2)
```

**Suggestions Structure (JSONB):**
```json
{
  "suggestions": [
    {
      "category": "format",
      "priority": "high",
      "issue": "Multiple fonts used",
      "recommendation": "Use a single professional font throughout",
      "impact": "Better ATS readability"
    },
    {
      "category": "content",
      "priority": "medium",
      "issue": "Missing quantifiable achievements",
      "recommendation": "Add metrics to accomplishments (e.g., 'Increased sales by 30%')",
      "impact": "Demonstrates concrete value"
    }
  ],
  "strengths": [
    "Clear work history progression",
    "Strong technical skills section",
    "Well-formatted contact information"
  ],
  "weaknesses": [
    "Lacks summary section",
    "No certifications listed",
    "Experience descriptions too brief"
  ],
  "missing_sections": [
    "Professional Summary",
    "Certifications",
    "Projects Portfolio"
  ]
}
```

**Indexes:**
```sql
CREATE INDEX idx_analyses_resume_id ON analyses(resume_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at DESC);
```

**Example Queries:**

```sql
-- Save analysis results
INSERT INTO analyses (
    resume_id, ats_score, formatting_score, keyword_score,
    overall_score, suggestions, strengths, weaknesses,
    model_used, analysis_time_seconds
)
VALUES (
    1, 85, 90, 75, 83,
    '{"suggestions": [...]}'::jsonb,
    '["Clear structure", "Strong skills"]'::jsonb,
    '["Missing summary"]'::jsonb,
    'Groq-llama-3.3-70b',
    2.5
)
RETURNING id;

-- Get latest analysis for resume
SELECT *
FROM analyses
WHERE resume_id = 1
ORDER BY created_at DESC
LIMIT 1;

-- Get average scores by date
SELECT 
    DATE(created_at) as analysis_date,
    AVG(overall_score) as avg_score,
    COUNT(*) as num_analyses
FROM analyses
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY analysis_date DESC;

-- Find resumes with low scores
SELECT 
    r.id, r.filename, a.overall_score,
    a.suggestions->>'category' as main_issue
FROM resumes r
JOIN analyses a ON r.id = a.resume_id
WHERE a.overall_score < 70
ORDER BY a.overall_score ASC;
```

---

**End of Part 1**

**Next:** [Part 2 - Resume Enhancement, Skills Database & Jobs Tables](./DATABASE_DOCUMENTATION_PART2.md)

---

**Documentation Navigation:**
- **Part 1** (Current): Overview, Architecture, Users, Resumes, Analyses
- **Part 2**: Resume Enhancements, Skills Database, Jobs Tables
- **Part 3**: Interview Module Tables
- **Part 4**: Footprint Scanner Tables
- **Part 5**: Indexes, Triggers, Migrations & Best Practices
