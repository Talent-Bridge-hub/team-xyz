# UtopiaHire Database Documentation
## Complete Technical Reference

> **Generated:** November 6, 2025  
> **Version:** 1.0.0  
> **Database:** PostgreSQL 14+  
> **Total Documentation:** ~4,850 lines across 5 parts

---

## 📚 Documentation Structure

This comprehensive database documentation is organized into **5 parts**, each under 1000 lines for easy navigation:

### [Part 1: Foundation & Core Tables](./DATABASE_DOCUMENTATION_PART1.md)
**~1000 lines** | Database architecture, connection management, users & resume tables

**Contents:**
- Database Overview & Statistics
- Architecture & Design Principles
- Connection Pool Implementation
- Core Security Features
- **Tables Covered:**
  - `users` - User accounts & authentication
  - `resumes` - Resume uploads & parsed data
  - `analyses` - AI-powered resume analysis

**Key Topics:** PostgreSQL 14+ features, JSONB usage, connection pooling, parameterized queries, ATS scoring

---

### [Part 2: Enhancement & Jobs Module](./DATABASE_DOCUMENTATION_PART2.md)
**~1000 lines** | Resume improvements, skills tracking, job listings

**Contents:**
- Resume Enhancement System
- Skills Database & Keywords
- Job Listings & Matching
- Saved Jobs Feature
- **Tables Covered:**
  - `improved_resumes` - AI-enhanced versions
  - `skills_database` - Comprehensive skills catalog
  - `job_keywords` - Job-specific keywords
  - `jobs` - Job listings (JSONB skills)
  - `saved_jobs` - User bookmarks & application tracking

**Key Topics:** JSONB for flexible data, skill matching algorithms, job recommendations, application pipeline

---

### [Part 3: Interview Module](./DATABASE_DOCUMENTATION_PART3.md)
**~1000 lines** | AI-powered interview simulator with comprehensive feedback

**Contents:**
- Interview System Architecture
- Question Bank (500+ questions)
- Multi-dimensional Scoring
- Detailed Feedback Generation
- **Tables Covered:**
  - `question_bank` - Interview questions library
  - `interview_sessions` - User interview sessions
  - `interview_questions` - Session-question mapping
  - `interview_answers` - Responses with 6-dimension scores
  - `interview_feedback` - Comprehensive session feedback

**Key Topics:** Question categorization (technical/behavioral/situational), scoring algorithms (relevance, completeness, clarity, technical accuracy, communication), JSONB feedback structures, region-specific content (MENA, Africa)

---

### [Part 4: Digital Footprint Scanner](./DATABASE_DOCUMENTATION_PART4.md)
**~950 lines** | Multi-platform professional presence analysis

**Contents:**
- Footprint Module Overview
- Multi-platform Data Aggregation
- Scoring Algorithms
- Privacy & Security Analysis
- **Tables Covered:**
  - `footprint_scans` - Complete digital footprint data

**Key Topics:** GitHub analysis (repos, commits, stars), StackOverflow metrics (reputation, badges), LinkedIn profiling, JSONB for flexible platform data, 4-dimensional scoring (visibility, activity, impact, expertise), privacy risk assessment, career insights

---

### [Part 5: Operations & Best Practices](./DATABASE_DOCUMENTATION_PART5.md)
**~900 lines** | Indexes, migrations, performance optimization, troubleshooting

**Contents:**
- Complete Index Strategy (50+ indexes)
- Migration System (Python-based)
- Database Maintenance Procedures
- Performance Optimization
- Security Best Practices
- Troubleshooting Guide

**Key Topics:** B-tree vs GIN indexes, connection pool optimization, VACUUM/ANALYZE, backup/restore, query optimization, JSONB performance, deadlock prevention, monitoring

---

## 🗄️ Database Overview

### Statistics

| Metric | Value |
|--------|-------|
| **Total Tables** | 18 |
| **Total Indexes** | 50+ |
| **Index Types** | B-tree (35+), GIN (15+), Unique (8+) |
| **JSONB Columns** | 20+ |
| **Modules** | 6 (Auth, Resume, Jobs, Interview, Footprint, Skills) |
| **Foreign Keys** | 25+ |
| **CHECK Constraints** | 30+ |
| **Triggers** | 5+ |

### Technology Stack

- **RDBMS:** PostgreSQL 14+
- **Driver:** psycopg2 (Python)
- **Cursor:** RealDictCursor (returns dicts, not tuples)
- **Connection:** SimpleConnectionPool (1-10 connections)
- **Migration:** Python scripts with execute_query
- **Features Used:** JSONB, GIN indexes, Arrays, Triggers, CHECK constraints

---

## 📋 Complete Table Reference

### Module 1: Users & Authentication (2 tables)
| Table | Purpose | Key Features |
|-------|---------|--------------|
| `users` | User accounts | Bcrypt passwords, soft delete, regions |
| `platform_credentials` | OAuth tokens | Encrypted tokens, expiry tracking |

### Module 2: Resume Management (4 tables)
| Table | Purpose | Key Features |
|-------|---------|--------------|
| `resumes` | Resume uploads | JSONB parsed data, file storage |
| `analyses` | AI analysis | Multi-score system (ATS, keyword, format) |
| `improved_resumes` | Enhanced versions | Change tracking, version control |
| `skills_database` | Skills catalog | Categorized, popularity tracking |

### Module 3: Jobs (2 tables)
| Table | Purpose | Key Features |
|-------|---------|--------------|
| `jobs` | Job listings | JSONB skills, salary ranges, remote flag |
| `saved_jobs` | User bookmarks | Application status tracking |

### Module 4: Interview (5 tables)
| Table | Purpose | Key Features |
|-------|---------|--------------|
| `question_bank` | Question library | 500+ questions, arrays for skills/roles |
| `interview_sessions` | User sessions | Status tracking, timing, scores |
| `interview_questions` | Session questions | Order tracking, time limits |
| `interview_answers` | User responses | 6-dimension scoring, JSONB feedback |
| `interview_feedback` | Final summary | Ratings, resources, recommendations |

### Module 5: Digital Footprint (1 table)
| Table | Purpose | Key Features |
|-------|---------|--------------|
| `footprint_scans` | Platform analysis | Multi-platform JSONB, privacy reports |

### Module 6: Reference Data (2 tables)
| Table | Purpose | Key Features |
|-------|---------|--------------|
| `job_keywords` | Job-specific terms | Frequency tracking, role mapping |
| `skills_database` | Skills reference | Categories, regions, popularity |

---

## 🚀 Quick Start

### Connect to Database
```bash
psql -h localhost -U utopia_user -d utopiahire
```

### View Tables
```sql
\dt
```

### Essential Queries

**Get user with resumes:**
```sql
SELECT 
    u.id, u.name, u.email,
    COUNT(r.id) as resume_count,
    MAX(r.last_score) as best_score
FROM users u
LEFT JOIN resumes r ON u.id = r.user_id
WHERE u.id = 1
GROUP BY u.id;
```

**Find jobs matching user skills:**
```sql
WITH user_skills AS (
    SELECT jsonb_array_elements_text(
        parsed_data->'skills'->'technical'
    ) as skill
    FROM resumes
    WHERE user_id = 1
    ORDER BY uploaded_at DESC
    LIMIT 1
)
SELECT 
    j.id, j.title, j.company,
    COUNT(us.skill) as matching_skills
FROM jobs j,
LATERAL jsonb_array_elements_text(j.required_skills) AS req_skill
JOIN user_skills us ON us.skill = req_skill
GROUP BY j.id, j.title, j.company
HAVING COUNT(us.skill) >= 3
ORDER BY matching_skills DESC
LIMIT 10;
```

**Latest interview performance:**
```sql
SELECT 
    sess.id,
    sess.job_role,
    sess.average_score,
    fb.technical_rating,
    fb.communication_rating
FROM interview_sessions sess
LEFT JOIN interview_feedback fb ON sess.id = fb.session_id
WHERE sess.user_id = 1
  AND sess.status = 'completed'
ORDER BY sess.completed_at DESC
LIMIT 5;
```

---

## 🔧 Common Operations

### Backup Database
```bash
pg_dump -h localhost -U utopia_user -d utopiahire \
    -F c -b -v -f "backup_$(date +%Y%m%d).dump"
```

### Run Migration
```bash
cd /home/firas/Utopia/backend
python migrations/create_resumes_table.py
```

### Check Database Size
```sql
SELECT pg_size_pretty(pg_database_size('utopiahire'));
```

### Find Slow Queries
```sql
SELECT query, calls, mean_time, max_time
FROM pg_stat_statements
WHERE mean_time > 1000
ORDER BY mean_time DESC
LIMIT 10;
```

---

## 📊 Performance Tips

### Index Usage
- ✅ B-tree indexes on foreign keys, timestamps, frequently queried columns
- ✅ GIN indexes on JSONB columns for fast containment queries
- ✅ Unique indexes enforce constraints and improve lookups
- ✅ Partial indexes for commonly filtered subsets

### Query Optimization
- ✅ Always use parameterized queries (prevents SQL injection)
- ✅ Add LIMIT to queries on large tables
- ✅ Use EXPLAIN ANALYZE to check query plans
- ✅ Leverage JSONB operators (@>, ?, ?&) with GIN indexes

### Connection Pooling
- ✅ Reuses connections (10x faster than creating new ones)
- ✅ Min: 1 connection, Max: 10 connections
- ✅ Always release connections after use

---

## 🔒 Security Features

### Authentication
- Bcrypt password hashing (never store plain text)
- Email uniqueness constraints
- Soft delete (is_active flag)

### Data Protection
- Parameterized queries prevent SQL injection
- ON DELETE CASCADE maintains referential integrity
- Encrypted API tokens in platform_credentials

### Privacy
- Privacy risk assessment in footprint scans
- Configurable profile visibility
- Audit logging for sensitive operations

---

## 📖 Documentation Navigation

| Part | Focus | Lines | Link |
|------|-------|-------|------|
| **Part 1** | Overview, Users, Resumes | ~1000 | [Read Part 1](./DATABASE_DOCUMENTATION_PART1.md) |
| **Part 2** | Enhancements, Skills, Jobs | ~1000 | [Read Part 2](./DATABASE_DOCUMENTATION_PART2.md) |
| **Part 3** | Interview Module | ~1000 | [Read Part 3](./DATABASE_DOCUMENTATION_PART3.md) |
| **Part 4** | Footprint Scanner | ~950 | [Read Part 4](./DATABASE_DOCUMENTATION_PART4.md) |
| **Part 5** | Operations & Best Practices | ~900 | [Read Part 5](./DATABASE_DOCUMENTATION_PART5.md) |

---

## 🎯 Key Concepts

### JSONB Usage
**UtopiaHire** extensively uses JSONB for flexible data storage:
- Resume parsed data (skills, experience, education)
- Job requirements and salary ranges
- Interview feedback and scoring details
- Digital footprint platform data
- Privacy reports and recommendations

**Benefits:**
- Schema flexibility without migrations
- Fast querying with GIN indexes
- Native JSON operators (@>, ?, ->, ->>)

### Scoring Systems

**Resume Analysis (0-100):**
- ATS Score: Applicant Tracking System compatibility
- Keyword Score: Relevance to job requirements
- Formatting Score: Visual presentation quality
- Overall Score: Weighted composite

**Interview Evaluation (0-100 per dimension):**
- Relevance: Answer addresses the question
- Completeness: Covers key points
- Clarity: Communication quality
- Technical Accuracy: Correctness of information
- Communication: Overall articulation
- Overall: Weighted composite

**Digital Footprint (0-100):**
- Visibility: Online discoverability
- Activity: Recent contributions
- Impact: Influence and reach
- Expertise: Demonstrated knowledge

---

## 💡 Best Practices

### Schema Design
1. Use appropriate data types (INTEGER for IDs, not VARCHAR)
2. Add CHECK constraints for validation
3. Include created_at and updated_at timestamps
4. Use ON DELETE CASCADE for dependent data
5. Index all foreign keys

### Query Writing
1. Always use parameterized queries
2. Add LIMIT to prevent huge result sets
3. Use JOINs instead of N+1 queries
4. Leverage JSONB operators with GIN indexes
5. Test with EXPLAIN ANALYZE

### Maintenance
1. Run VACUUM ANALYZE weekly
2. Monitor index usage and remove unused
3. Back up daily (automated)
4. Check slow query logs
5. Reindex monthly

---

## 🆘 Need Help?

### Common Issues
- **Slow queries?** → Check Part 5, Performance Optimization
- **JSONB queries not using index?** → Verify GIN index exists and query uses correct operators
- **Connection pool exhausted?** → Check for connection leaks, ensure release_connection() is called
- **Migration failed?** → Check migration logs, verify table dependencies

### Resources
- **API Documentation:** See `/docs/API_DOCUMENTATION_PART*.md`
- **GitHub:** Repository contains all schemas and migrations
- **PostgreSQL Docs:** https://www.postgresql.org/docs/14/

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-06 | Initial comprehensive documentation (5 parts, ~4,850 lines) |

---

## 📫 Contact & Support

For questions or issues:
- **Documentation Issues:** Check corresponding part for detailed information
- **Schema Questions:** Refer to Part 1 (Architecture)
- **Performance Issues:** See Part 5 (Optimization)
- **Security Concerns:** Review Part 5 (Best Practices)

---

**UtopiaHire Database Documentation** - Complete technical reference for the PostgreSQL 14+ database powering the UtopiaHire platform.
