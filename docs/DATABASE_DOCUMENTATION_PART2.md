# UtopiaHire Database Documentation - Part 2
## Resume Enhancement, Skills Database & Jobs Module

> **Version:** 1.0.0  
> **Database:** PostgreSQL 14+

---

## Table of Contents (Part 2)

1. [Resume Enhancement Tables](#resume-enhancement-tables)
2. [Skills Database Tables](#skills-database-tables)
3. [Jobs Module Tables](#jobs-module-tables)
4. [Saved Jobs Feature](#saved-jobs-feature)

---

## 1. Resume Enhancement Tables

### 1.1 Improved Resumes Table

**Purpose:** Store AI-enhanced versions of original resumes with tracked improvements

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS improved_resumes (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    analysis_id INTEGER REFERENCES analyses(id) ON DELETE SET NULL,
    enhanced_text TEXT,
    enhanced_data JSONB,
    changes_made JSONB,
    improvement_percentage FLOAT,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique improvement identifier |
| `resume_id` | INTEGER | FK → resumes(id), CASCADE | Original resume reference |
| `analysis_id` | INTEGER | FK → analyses(id), SET NULL | Analysis that triggered improvement |
| `enhanced_text` | TEXT | NULL | Improved plain text version |
| `enhanced_data` | JSONB | NULL | Structured enhanced data |
| `changes_made` | JSONB | NULL | Detailed changelog |
| `improvement_percentage` | FLOAT | NULL | Estimated improvement (0-100) |
| `version` | INTEGER | DEFAULT 1 | Enhancement version number |
| `created_at` | TIMESTAMP | AUTO | Creation timestamp |

**Enhanced Data Structure (JSONB):**
```json
{
  "personal_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+216 12 345 678",
    "location": "Tunis, Tunisia",
    "linkedin": "linkedin.com/in/johndoe",
    "improvements": ["Standardized phone format", "Added LinkedIn URL"]
  },
  "professional_summary": {
    "original": "Software engineer with experience...",
    "enhanced": "Results-driven Senior Software Engineer with 5+ years of expertise in building scalable microservices, reducing API response times by 40%, and mentoring cross-functional teams. Proven track record of delivering high-impact solutions in fast-paced environments.",
    "improvements": [
      "Added quantifiable achievements",
      "Incorporated power words",
      "Highlighted leadership skills"
    ]
  },
  "experience": [
    {
      "title": "Senior Software Engineer",
      "company": "TechCorp",
      "location": "Tunis, Tunisia",
      "dates": "Jan 2020 - Present",
      "original_description": "Working on backend services",
      "enhanced_description": "Architected and deployed microservices infrastructure serving 100K+ daily users, achieving 99.9% uptime. Led a team of 5 engineers in migrating monolithic application to containerized architecture, reducing deployment time by 60%.",
      "improvements": [
        "Added specific metrics (100K+ users, 99.9% uptime)",
        "Emphasized leadership role",
        "Highlighted technical achievements",
        "Used action verbs (Architected, Led, Migrated)"
      ],
      "keywords_added": ["microservices", "containerized", "uptime", "deployment"]
    }
  ],
  "skills": {
    "original": ["Python", "JavaScript", "SQL"],
    "enhanced": {
      "technical_skills": ["Python", "JavaScript", "TypeScript", "SQL", "PostgreSQL", "Docker", "Kubernetes"],
      "frameworks": ["Django", "FastAPI", "React", "Node.js"],
      "tools": ["Git", "Jenkins", "AWS", "Terraform"],
      "methodologies": ["Agile", "Scrum", "CI/CD", "TDD"]
    },
    "improvements": [
      "Categorized skills by type",
      "Added missing technologies",
      "Included frameworks and tools",
      "Added methodologies"
    ]
  },
  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "University of Tunis",
      "graduation": "2018",
      "gpa": "3.8/4.0",
      "original": "BSc Computer Science, 2018",
      "enhanced": "Bachelor of Science in Computer Science | GPA: 3.8/4.0 | 2018",
      "improvements": ["Expanded degree name", "Added GPA", "Standardized format"]
    }
  ],
  "new_sections_added": ["Professional Summary", "Certifications", "Projects"],
  "formatting_improvements": [
    "Consistent date formats",
    "Action verb bullets",
    "Quantified achievements",
    "ATS-friendly layout"
  ]
}
```

**Changes Made Structure (JSONB):**
```json
{
  "summary": {
    "total_changes": 45,
    "sections_modified": 6,
    "sections_added": 3,
    "keywords_added": 18,
    "metrics_added": 12
  },
  "detailed_changes": [
    {
      "section": "Professional Summary",
      "type": "addition",
      "original": null,
      "enhanced": "Results-driven Senior Software Engineer...",
      "reason": "Missing professional summary (critical for ATS)",
      "impact": "high"
    },
    {
      "section": "Work Experience",
      "type": "modification",
      "original": "Working on backend services",
      "enhanced": "Architected and deployed microservices infrastructure...",
      "reason": "Vague description without metrics",
      "impact": "high",
      "keywords_added": ["microservices", "deployed", "infrastructure"],
      "metrics_added": ["100K+ users", "99.9% uptime", "60% reduction"]
    },
    {
      "section": "Skills",
      "type": "expansion",
      "original": ["Python", "JavaScript", "SQL"],
      "enhanced": {
        "technical": ["Python", "JavaScript", "TypeScript", "SQL", "PostgreSQL"],
        "frameworks": ["Django", "FastAPI", "React"],
        "tools": ["Docker", "Kubernetes", "AWS"]
      },
      "reason": "Skills list too basic, missing categorization",
      "impact": "medium",
      "keywords_added": ["TypeScript", "PostgreSQL", "Django", "FastAPI", "Docker", "Kubernetes", "AWS"]
    }
  ],
  "ats_improvements": [
    "Added standard section headers",
    "Removed graphics and tables",
    "Simplified formatting",
    "Added missing contact information"
  ],
  "keyword_optimization": {
    "job_title_matches": ["Senior Software Engineer", "Backend Developer"],
    "technical_keywords": ["Python", "microservices", "Docker", "AWS", "PostgreSQL"],
    "soft_skills": ["leadership", "mentoring", "collaboration"],
    "industry_buzzwords": ["scalable", "high-performance", "cloud-native"]
  }
}
```

**Indexes:**
```sql
CREATE INDEX idx_improved_resumes_resume_id ON improved_resumes(resume_id);
CREATE INDEX idx_improved_resumes_version ON improved_resumes(resume_id, version);
```

**Example Queries:**

```sql
-- Save enhanced resume
INSERT INTO improved_resumes (
    resume_id, analysis_id, enhanced_text, enhanced_data,
    changes_made, improvement_percentage, version
)
VALUES (
    1, 5, 'Enhanced resume text...',
    '{"professional_summary": {...}}'::jsonb,
    '{"summary": {"total_changes": 45}}'::jsonb,
    35.5, 1
)
RETURNING id;

-- Get latest enhancement for resume
SELECT *
FROM improved_resumes
WHERE resume_id = 1
ORDER BY version DESC
LIMIT 1;

-- Get all versions with improvement tracking
SELECT 
    ir.version,
    ir.improvement_percentage,
    ir.changes_made->>'total_changes' as total_changes,
    a.overall_score as original_score,
    a.overall_score + ir.improvement_percentage as projected_score,
    ir.created_at
FROM improved_resumes ir
LEFT JOIN analyses a ON ir.analysis_id = a.id
WHERE ir.resume_id = 1
ORDER BY ir.version DESC;

-- Compare original vs enhanced
SELECT 
    r.filename,
    r.parsed_data->'skills' as original_skills,
    ir.enhanced_data->'skills' as enhanced_skills,
    ir.changes_made->'detailed_changes' as changes
FROM resumes r
JOIN improved_resumes ir ON r.id = ir.resume_id
WHERE r.id = 1 AND ir.version = 1;

-- Get most impactful changes
SELECT 
    ir.resume_id,
    jsonb_array_elements(ir.changes_made->'detailed_changes') as change
FROM improved_resumes ir
WHERE (jsonb_array_elements(ir.changes_made->'detailed_changes')->>'impact') = 'high';
```

**Version Control:**
- Multiple enhancement versions tracked per resume
- Each version builds on previous feedback
- Version comparison available via API
- Users can revert to previous versions

---

## 2. Skills Database Tables

### 2.1 Skills Database Table

**Purpose:** Comprehensive database of technical and soft skills with regional relevance

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS skills_database (
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    popularity INTEGER DEFAULT 0,
    region VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Skill identifier |
| `skill_name` | VARCHAR(100) | UNIQUE, NOT NULL | Standardized skill name |
| `category` | VARCHAR(50) | NOT NULL | Skill category (see below) |
| `popularity` | INTEGER | DEFAULT 0 | Usage count/frequency |
| `region` | VARCHAR(50) | NULL | Geographic relevance |
| `created_at` | TIMESTAMP | AUTO | Entry creation date |

**Skill Categories:**

| Category | Description | Examples |
|----------|-------------|----------|
| **programming_language** | Programming languages | Python, JavaScript, Java, C++ |
| **framework** | Software frameworks | React, Django, Spring Boot, Vue.js |
| **database** | Database systems | PostgreSQL, MongoDB, MySQL, Redis |
| **cloud** | Cloud platforms & services | AWS, Azure, Google Cloud, Docker |
| **devops** | DevOps tools | Kubernetes, Jenkins, Terraform, CI/CD |
| **web_dev** | Web development | HTML, CSS, REST API, GraphQL |
| **mobile** | Mobile development | React Native, Flutter, iOS, Android |
| **data_science** | Data & analytics | Machine Learning, TensorFlow, Pandas |
| **soft_skill** | Soft skills | Leadership, Communication, Problem Solving |
| **tool** | Development tools | Git, VS Code, Jira, Figma |

**Sample Data:**
```sql
INSERT INTO skills_database (skill_name, category, popularity, region) VALUES
('Python', 'programming_language', 1500, 'Global'),
('JavaScript', 'programming_language', 1800, 'Global'),
('React', 'framework', 1200, 'Global'),
('Django', 'framework', 800, 'Global'),
('PostgreSQL', 'database', 600, 'Global'),
('Docker', 'cloud', 900, 'Global'),
('Kubernetes', 'devops', 700, 'Global'),
('AWS', 'cloud', 1100, 'Global'),
('Machine Learning', 'data_science', 850, 'Global'),
('Leadership', 'soft_skill', 500, 'Global'),
('Communication', 'soft_skill', 650, 'Global'),
('Arabic', 'language', 300, 'MENA'),
('French', 'language', 450, 'Tunisia');
```

**Indexes:**
```sql
CREATE INDEX idx_skills_category ON skills_database(category);
CREATE INDEX idx_skills_popularity ON skills_database(popularity DESC);
CREATE INDEX idx_skills_region ON skills_database(region);
```

**Example Queries:**

```sql
-- Get top skills by category
SELECT skill_name, popularity
FROM skills_database
WHERE category = 'programming_language'
ORDER BY popularity DESC
LIMIT 10;

-- Search skills by partial name
SELECT skill_name, category
FROM skills_database
WHERE skill_name ILIKE '%script%'
ORDER BY popularity DESC;

-- Get region-specific skills
SELECT skill_name, category, popularity
FROM skills_database
WHERE region IN ('Global', 'Tunisia', 'MENA')
ORDER BY popularity DESC;

-- Increment skill popularity (when used in resume)
UPDATE skills_database
SET popularity = popularity + 1
WHERE skill_name = 'Python';

-- Get trending skills (added recently, high popularity)
SELECT skill_name, category, popularity, created_at
FROM skills_database
WHERE created_at >= NOW() - INTERVAL '6 months'
ORDER BY popularity DESC
LIMIT 20;

-- Skill coverage analysis
SELECT 
    category,
    COUNT(*) as skill_count,
    SUM(popularity) as total_usage
FROM skills_database
GROUP BY category
ORDER BY total_usage DESC;
```

---

### 2.2 Job Keywords Table

**Purpose:** Track job-specific keywords and phrases for resume optimization

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS job_keywords (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(200) NOT NULL,
    job_role VARCHAR(100) NOT NULL,
    frequency INTEGER DEFAULT 1,
    region VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Keyword identifier |
| `keyword` | VARCHAR(200) | NOT NULL | Keyword phrase |
| `job_role` | VARCHAR(100) | NOT NULL | Associated job role |
| `frequency` | INTEGER | DEFAULT 1 | Occurrence frequency |
| `region` | VARCHAR(50) | NULL | Geographic relevance |
| `created_at` | TIMESTAMP | AUTO | Entry creation date |

**Sample Data:**
```sql
INSERT INTO job_keywords (keyword, job_role, frequency, region) VALUES
('microservices architecture', 'Senior Software Engineer', 450, 'Global'),
('agile methodology', 'Software Engineer', 380, 'Global'),
('RESTful API', 'Backend Developer', 520, 'Global'),
('CI/CD pipeline', 'DevOps Engineer', 410, 'Global'),
('machine learning models', 'Data Scientist', 390, 'Global'),
('cloud infrastructure', 'Cloud Architect', 360, 'Global'),
('team collaboration', 'Software Engineer', 290, 'Global'),
('problem solving', 'Software Engineer', 310, 'Global'),
('data analysis', 'Data Analyst', 340, 'Global'),
('responsive design', 'Frontend Developer', 280, 'Global');
```

**Indexes:**
```sql
CREATE INDEX idx_keywords_job_role ON job_keywords(job_role);
CREATE INDEX idx_keywords_frequency ON job_keywords(frequency DESC);
```

**Example Queries:**

```sql
-- Get top keywords for specific job role
SELECT keyword, frequency
FROM job_keywords
WHERE job_role = 'Senior Software Engineer'
ORDER BY frequency DESC
LIMIT 20;

-- Keyword matching (resume optimization)
SELECT jk.keyword, jk.frequency
FROM job_keywords jk
WHERE jk.job_role = 'Backend Developer'
  AND NOT EXISTS (
    SELECT 1 FROM resumes r
    WHERE r.id = 1 
      AND r.raw_text ILIKE '%' || jk.keyword || '%'
  )
ORDER BY jk.frequency DESC;

-- Update keyword frequency
UPDATE job_keywords
SET frequency = frequency + 1
WHERE keyword = 'microservices architecture' 
  AND job_role = 'Senior Software Engineer';

-- Cross-role keyword analysis
SELECT 
    keyword,
    COUNT(DISTINCT job_role) as role_count,
    SUM(frequency) as total_frequency
FROM job_keywords
GROUP BY keyword
HAVING COUNT(DISTINCT job_role) > 1
ORDER BY total_frequency DESC;
```

---

## 3. Jobs Module Tables

### 3.1 Jobs Table

**Purpose:** Store job listings fetched from various sources with JSONB for flexible data

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    region VARCHAR(100),
    job_type VARCHAR(50) DEFAULT 'Full-time',
    experience_level VARCHAR(50),
    description TEXT,
    required_skills JSONB DEFAULT '[]',
    preferred_skills JSONB DEFAULT '[]',
    salary_range JSONB,
    posted_date DATE,
    remote BOOLEAN DEFAULT FALSE,
    url TEXT,
    source VARCHAR(100),
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Internal job identifier |
| `job_id` | VARCHAR(255) | UNIQUE, NOT NULL | External job ID (from source) |
| `title` | VARCHAR(255) | NOT NULL | Job title |
| `company` | VARCHAR(255) | NOT NULL | Company name |
| `location` | VARCHAR(255) | NULL | Job location (city, country) |
| `region` | VARCHAR(100) | NULL | Geographic region (MENA, Africa, Europe) |
| `job_type` | VARCHAR(50) | DEFAULT 'Full-time' | Employment type |
| `experience_level` | VARCHAR(50) | NULL | Required experience level |
| `description` | TEXT | NULL | Full job description |
| `required_skills` | JSONB | DEFAULT '[]' | Must-have skills (array) |
| `preferred_skills` | JSONB | DEFAULT '[]' | Nice-to-have skills (array) |
| `salary_range` | JSONB | NULL | Salary information (object) |
| `posted_date` | DATE | NULL | Original posting date |
| `remote` | BOOLEAN | DEFAULT FALSE | Remote work availability |
| `url` | TEXT | NULL | Original job posting URL |
| `source` | VARCHAR(100) | NULL | Job board source (LinkedIn, Indeed) |
| `fetched_at` | TIMESTAMP | AUTO | Data fetch timestamp |
| `created_at` | TIMESTAMP | AUTO | Database insertion timestamp |
| `updated_at` | TIMESTAMP | AUTO | Last update timestamp |

**Job Types:**
- Full-time
- Part-time
- Contract
- Internship
- Freelance
- Temporary

**Experience Levels:**
- Entry Level / Junior (0-2 years)
- Mid Level (2-5 years)
- Senior (5-10 years)
- Lead / Principal (10+ years)
- Manager / Director

**JSONB Structures:**

**Required/Preferred Skills (Array):**
```json
[
  "Python",
  "FastAPI",
  "PostgreSQL",
  "Docker",
  "AWS",
  "CI/CD",
  "RESTful APIs",
  "Microservices"
]
```

**Salary Range (Object):**
```json
{
  "min": 50000,
  "max": 80000,
  "currency": "USD",
  "period": "yearly",
  "negotiable": true,
  "benefits": [
    "Health insurance",
    "401k matching",
    "Remote work",
    "Professional development budget"
  ]
}
```

**Indexes:**
```sql
CREATE INDEX idx_jobs_job_id ON jobs(job_id);
CREATE INDEX idx_jobs_title ON jobs(title);
CREATE INDEX idx_jobs_company ON jobs(company);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_region ON jobs(region);
CREATE INDEX idx_jobs_job_type ON jobs(job_type);
CREATE INDEX idx_jobs_experience_level ON jobs(experience_level);
CREATE INDEX idx_jobs_remote ON jobs(remote);
CREATE INDEX idx_jobs_fetched_at ON jobs(fetched_at DESC);
CREATE INDEX idx_jobs_required_skills ON jobs USING GIN(required_skills);
CREATE INDEX idx_jobs_posted_date ON jobs(posted_date DESC);
```

**Example Queries:**

```sql
-- Insert new job
INSERT INTO jobs (
    job_id, title, company, location, region,
    job_type, experience_level, description,
    required_skills, preferred_skills, salary_range,
    posted_date, remote, url, source
)
VALUES (
    'LINKEDIN-12345',
    'Senior Python Developer',
    'TechCorp Tunisia',
    'Tunis, Tunisia',
    'Tunisia',
    'Full-time',
    'Senior',
    'We are seeking an experienced Python developer...',
    '["Python", "Django", "PostgreSQL", "Docker"]'::jsonb,
    '["Kubernetes", "AWS", "CI/CD"]'::jsonb,
    '{"min": 3000, "max": 5000, "currency": "TND", "period": "monthly"}'::jsonb,
    '2025-11-01',
    true,
    'https://linkedin.com/jobs/12345',
    'LinkedIn'
)
RETURNING id;

-- Search jobs by title
SELECT id, title, company, location, remote, posted_date
FROM jobs
WHERE title ILIKE '%python%' OR title ILIKE '%developer%'
ORDER BY posted_date DESC
LIMIT 20;

-- Filter by skills (JSONB containment)
SELECT 
    j.id, j.title, j.company, j.location,
    j.required_skills, j.remote
FROM jobs j
WHERE j.required_skills @> '["Python"]'::jsonb
  AND j.remote = true
ORDER BY j.posted_date DESC;

-- Jobs matching user's resume skills
SELECT 
    j.id, j.title, j.company, j.location,
    j.required_skills,
    -- Calculate match percentage
    (
        SELECT COUNT(*)
        FROM jsonb_array_elements_text(j.required_skills) AS required_skill
        WHERE required_skill = ANY(
            SELECT jsonb_array_elements_text(r.parsed_data->'skills'->'technical')
            FROM resumes r
            WHERE r.id = 1
        )
    ) * 100.0 / jsonb_array_length(j.required_skills) as match_percentage
FROM jobs j
WHERE jsonb_array_length(j.required_skills) > 0
ORDER BY match_percentage DESC
LIMIT 20;

-- Get jobs by region and experience
SELECT id, title, company, location, experience_level
FROM jobs
WHERE region = 'Tunisia'
  AND experience_level IN ('Mid Level', 'Senior')
  AND posted_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY posted_date DESC;

-- Remote jobs with salary info
SELECT 
    id, title, company, location,
    salary_range->>'min' as min_salary,
    salary_range->>'max' as max_salary,
    salary_range->>'currency' as currency
FROM jobs
WHERE remote = true
  AND salary_range IS NOT NULL
ORDER BY (salary_range->>'max')::numeric DESC;

-- Job statistics by company
SELECT 
    company,
    COUNT(*) as total_jobs,
    SUM(CASE WHEN remote THEN 1 ELSE 0 END) as remote_jobs,
    AVG(jsonb_array_length(required_skills)) as avg_skills_required
FROM jobs
GROUP BY company
HAVING COUNT(*) > 5
ORDER BY total_jobs DESC;

-- Trending skills in job market
SELECT 
    skill,
    COUNT(*) as job_count
FROM jobs,
LATERAL jsonb_array_elements_text(required_skills) AS skill
WHERE posted_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY skill
ORDER BY job_count DESC
LIMIT 20;
```

---

## 4. Saved Jobs Feature

### 4.1 Saved Jobs Table

**Purpose:** Allow users to bookmark/save jobs for later review

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS saved_jobs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    notes TEXT,
    status VARCHAR(50) DEFAULT 'saved',
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, job_id)
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Saved job identifier |
| `user_id` | INTEGER | FK → users(id), CASCADE | User who saved the job |
| `job_id` | INTEGER | FK → jobs(id), CASCADE | Saved job reference |
| `notes` | TEXT | NULL | User's personal notes |
| `status` | VARCHAR(50) | DEFAULT 'saved' | Application status |
| `saved_at` | TIMESTAMP | AUTO | Save timestamp |

**Status Values:**
- `saved` - Bookmarked for later
- `applied` - Application submitted
- `interview_scheduled` - Interview pending
- `rejected` - Application rejected
- `offer_received` - Job offer received
- `archived` - No longer interested

**Indexes:**
```sql
CREATE INDEX idx_saved_jobs_user_id ON saved_jobs(user_id);
CREATE INDEX idx_saved_jobs_job_id ON saved_jobs(job_id);
CREATE INDEX idx_saved_jobs_status ON saved_jobs(status);
CREATE UNIQUE INDEX idx_saved_jobs_user_job ON saved_jobs(user_id, job_id);
```

**Example Queries:**

```sql
-- Save a job
INSERT INTO saved_jobs (user_id, job_id, notes, status)
VALUES (1, 42, 'Great fit for my skills. Apply by Friday.', 'saved')
ON CONFLICT (user_id, job_id) DO NOTHING
RETURNING id;

-- Get user's saved jobs with details
SELECT 
    sj.id, sj.status, sj.notes, sj.saved_at,
    j.title, j.company, j.location, j.remote,
    j.required_skills, j.salary_range, j.url
FROM saved_jobs sj
JOIN jobs j ON sj.job_id = j.id
WHERE sj.user_id = 1
ORDER BY sj.saved_at DESC;

-- Update application status
UPDATE saved_jobs
SET status = 'applied', notes = 'Applied on 2025-11-06 via LinkedIn'
WHERE user_id = 1 AND job_id = 42;

-- Remove saved job
DELETE FROM saved_jobs
WHERE user_id = 1 AND job_id = 42;

-- Get saved jobs by status
SELECT 
    sj.id, j.title, j.company, sj.saved_at, sj.notes
FROM saved_jobs sj
JOIN jobs j ON sj.job_id = j.id
WHERE sj.user_id = 1 AND sj.status = 'applied'
ORDER BY sj.saved_at DESC;

-- Application pipeline overview
SELECT 
    status,
    COUNT(*) as count,
    array_agg(j.title ORDER BY sj.saved_at DESC) as job_titles
FROM saved_jobs sj
JOIN jobs j ON sj.job_id = j.id
WHERE sj.user_id = 1
GROUP BY status
ORDER BY 
    CASE status
        WHEN 'offer_received' THEN 1
        WHEN 'interview_scheduled' THEN 2
        WHEN 'applied' THEN 3
        WHEN 'saved' THEN 4
        WHEN 'rejected' THEN 5
        WHEN 'archived' THEN 6
    END;

-- Jobs saved but not applied (reminders)
SELECT 
    j.id, j.title, j.company, j.location,
    sj.saved_at,
    EXTRACT(DAY FROM NOW() - sj.saved_at) as days_saved
FROM saved_jobs sj
JOIN jobs j ON sj.job_id = j.id
WHERE sj.user_id = 1 
  AND sj.status = 'saved'
  AND sj.saved_at < NOW() - INTERVAL '7 days'
ORDER BY sj.saved_at ASC;
```

**User Experience Features:**

**1. Quick Save Button:**
```sql
-- One-click save
INSERT INTO saved_jobs (user_id, job_id)
VALUES (1, 42)
ON CONFLICT (user_id, job_id) DO NOTHING;
```

**2. Job Recommendations Based on Saved Jobs:**
```sql
-- Find similar jobs based on saved job skills
WITH saved_skills AS (
    SELECT DISTINCT skill
    FROM saved_jobs sj
    JOIN jobs j ON sj.job_id = j.id,
    LATERAL jsonb_array_elements_text(j.required_skills) AS skill
    WHERE sj.user_id = 1
)
SELECT 
    j.id, j.title, j.company,
    COUNT(DISTINCT ss.skill) as matching_skills
FROM jobs j,
LATERAL jsonb_array_elements_text(j.required_skills) AS required_skill
JOIN saved_skills ss ON ss.skill = required_skill
WHERE j.id NOT IN (
    SELECT job_id FROM saved_jobs WHERE user_id = 1
)
GROUP BY j.id, j.title, j.company
HAVING COUNT(DISTINCT ss.skill) >= 3
ORDER BY matching_skills DESC
LIMIT 10;
```

**3. Application Tracking Statistics:**
```sql
-- User's job application metrics
SELECT 
    COUNT(*) FILTER (WHERE status = 'saved') as saved,
    COUNT(*) FILTER (WHERE status = 'applied') as applied,
    COUNT(*) FILTER (WHERE status = 'interview_scheduled') as interviews,
    COUNT(*) FILTER (WHERE status = 'offer_received') as offers,
    COUNT(*) FILTER (WHERE status = 'rejected') as rejected,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE status = 'interview_scheduled') / 
        NULLIF(COUNT(*) FILTER (WHERE status = 'applied'), 0), 
        2
    ) as interview_rate
FROM saved_jobs
WHERE user_id = 1;
```

---

**Integration Example: Job Matching Algorithm**

```sql
-- Comprehensive job matching for user
WITH user_skills AS (
    SELECT jsonb_array_elements_text(
        r.parsed_data->'skills'->'technical'
    ) as skill
    FROM resumes r
    WHERE r.user_id = 1
    ORDER BY r.uploaded_at DESC
    LIMIT 1
),
user_experience AS (
    SELECT 
        COALESCE(
            jsonb_array_length(r.parsed_data->'experience'),
            0
        ) as years
    FROM resumes r
    WHERE r.user_id = 1
    ORDER BY r.uploaded_at DESC
    LIMIT 1
)
SELECT 
    j.id,
    j.title,
    j.company,
    j.location,
    j.remote,
    j.salary_range,
    j.url,
    -- Skill match score
    (
        SELECT COUNT(*)
        FROM jsonb_array_elements_text(j.required_skills) AS req_skill
        WHERE req_skill IN (SELECT skill FROM user_skills)
    ) * 100.0 / NULLIF(jsonb_array_length(j.required_skills), 0) as skill_match_percentage,
    -- Experience match
    CASE 
        WHEN j.experience_level = 'Entry Level' AND ue.years <= 2 THEN true
        WHEN j.experience_level = 'Mid Level' AND ue.years BETWEEN 2 AND 5 THEN true
        WHEN j.experience_level = 'Senior' AND ue.years >= 5 THEN true
        ELSE false
    END as experience_match
FROM jobs j
CROSS JOIN user_experience ue
WHERE j.posted_date >= CURRENT_DATE - INTERVAL '30 days'
  AND NOT EXISTS (
    SELECT 1 FROM saved_jobs sj 
    WHERE sj.user_id = 1 AND sj.job_id = j.id
  )
ORDER BY 
    skill_match_percentage DESC,
    j.posted_date DESC
LIMIT 50;
```

---

**End of Part 2**

**Next:** [Part 3 - Interview Module Tables](./DATABASE_DOCUMENTATION_PART3.md)

---

**Documentation Navigation:**
- [Part 1](./DATABASE_DOCUMENTATION_PART1.md): Overview, Architecture, Users, Resumes
- **Part 2** (Current): Resume Enhancements, Skills, Jobs
- **Part 3**: Interview Module Tables
- **Part 4**: Footprint Scanner Tables
- **Part 5**: Indexes, Migrations & Best Practices
