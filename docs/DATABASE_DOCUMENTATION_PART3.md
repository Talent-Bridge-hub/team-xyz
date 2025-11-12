# UtopiaHire Database Documentation - Part 3
## Interview Module Tables
---

## Table of Contents (Part 3)

1. [Interview Module Overview](#interview-module-overview)
2. [Question Bank Table](#question-bank-table)
3. [Interview Sessions Table](#interview-sessions-table)
4. [Interview Questions Table](#interview-questions-table)
5. [Interview Answers Table](#interview-answers-table)
6. [Interview Feedback Table](#interview-feedback-table)

---

## 1. Interview Module Overview

### Purpose & Architecture

The **Interview Module** provides an AI-powered interview simulation system that:
- ✅ Generates customized interview questions based on job role and difficulty
- ✅ Evaluates answers across 6 dimensions (relevance, completeness, clarity, technical accuracy, communication, overall)
- ✅ Provides detailed feedback and improvement suggestions
- ✅ Tracks user progress across multiple sessions
- ✅ Supports technical, behavioral, and situational questions
- ✅ Offers region-specific content (MENA, Africa, Global)

### Module Structure

```
┌────────────────────────────────────────────────────┐
│           INTERVIEW MODULE                          │
├────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────┐         ┌─────────────────┐  │
│  │ question_bank   │         │interview_sessions│ │
│  │  (500+ Qs)      │◄────────┤   (User owned)   │ │
│  └─────────────────┘         └────────┬─────────┘  │
│           │                           │             │
│           │                           │             │
│           ▼                           ▼             │
│  ┌─────────────────┐         ┌─────────────────┐  │
│  │interview_questions│       │interview_answers │  │
│  │ (Session Qs)     │────────┤  (User responses)│  │
│  └─────────────────┘         └─────────────────┘  │
│                                       │             │
│                                       ▼             │
│                            ┌─────────────────┐     │
│                            │interview_feedback│    │
│                            │ (Final summary)  │    │
│                            └─────────────────┘     │
│                                                     │
└────────────────────────────────────────────────────┘
```

### Data Flow

```
1. User starts interview → Create interview_session
2. System selects questions → Populate interview_questions from question_bank
3. User answers questions → Store in interview_answers
4. AI analyzes each answer → Update scores in interview_answers
5. Session completes → Generate interview_feedback
```

---

## 2. Question Bank Table

**Purpose:** Comprehensive repository of interview questions with metadata

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS question_bank (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    difficulty_level VARCHAR(20) NOT NULL,
    category VARCHAR(100),
    required_skills TEXT[],
    job_roles TEXT[],
    region VARCHAR(50) DEFAULT 'Global',
    sample_answer TEXT,
    key_points JSONB,
    common_mistakes JSONB,
    follow_up_questions TEXT[],
    difficulty_score INTEGER CHECK (difficulty_score >= 1 AND difficulty_score <= 10),
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Question identifier |
| `question_text` | TEXT | NOT NULL | The actual question |
| `question_type` | VARCHAR(50) | NOT NULL | technical/behavioral/situational |
| `difficulty_level` | VARCHAR(20) | NOT NULL | junior/mid/senior |
| `category` | VARCHAR(100) | NULL | Specific topic (e.g., "System Design") |
| `required_skills` | TEXT[] | NULL | Skills needed to answer |
| `job_roles` | TEXT[] | NULL | Relevant job positions |
| `region` | VARCHAR(50) | DEFAULT 'Global' | Geographic relevance |
| `sample_answer` | TEXT | NULL | Model answer |
| `key_points` | JSONB | NULL | Critical points to mention |
| `common_mistakes` | JSONB | NULL | Typical errors to avoid |
| `follow_up_questions` | TEXT[] | NULL | Related follow-ups |
| `difficulty_score` | INTEGER | 1-10 CHECK | Numeric difficulty rating |
| `usage_count` | INTEGER | DEFAULT 0 | Times used in interviews |
| `created_at` | TIMESTAMP | AUTO | Creation timestamp |
| `updated_at` | TIMESTAMP | AUTO | Last update timestamp |

**Question Types:**

| Type | Description | Examples |
|------|-------------|----------|
| **technical** | Technical knowledge & skills | "Explain REST vs GraphQL", "What is a closure?" |
| **behavioral** | Past experiences & soft skills | "Describe a time you faced a tight deadline" |
| **situational** | Hypothetical scenarios | "How would you handle a production bug?" |
| **coding** | Live coding challenges | "Implement a binary search algorithm" |
| **system_design** | Architecture questions | "Design a URL shortener service" |

**Difficulty Levels:**
- **junior** (1-3): Entry-level, basic concepts
- **mid** (4-7): Intermediate, requires experience
- **senior** (8-10): Advanced, leadership & architecture

**Key Points Structure (JSONB):**
```json
{
  "must_mention": [
    "Stateless architecture of REST",
    "Single endpoint in GraphQL",
    "REST uses multiple endpoints",
    "GraphQL allows flexible queries"
  ],
  "bonus_points": [
    "REST caching advantages",
    "GraphQL N+1 query problem",
    "Use cases for each",
    "Performance considerations"
  ],
  "evaluation_criteria": {
    "completeness": "Covers core differences",
    "depth": "Explains advantages/disadvantages",
    "clarity": "Easy to understand explanation",
    "examples": "Provides concrete examples"
  }
}
```

**Common Mistakes Structure (JSONB):**
```json
{
  "mistakes": [
    {
      "mistake": "Confusing REST with HTTP",
      "correction": "REST is an architectural style, HTTP is a protocol"
    },
    {
      "mistake": "Claiming one is always better than the other",
      "correction": "Both have valid use cases depending on requirements"
    },
    {
      "mistake": "Not mentioning specific examples",
      "correction": "Use concrete examples to illustrate points"
    }
  ],
  "red_flags": [
    "Cannot explain basic differences",
    "Provides incorrect information",
    "Shows no practical experience"
  ]
}
```

**Indexes:**
```sql
CREATE INDEX idx_question_bank_type ON question_bank(question_type);
CREATE INDEX idx_question_bank_difficulty ON question_bank(difficulty_level);
CREATE INDEX idx_question_bank_skills ON question_bank USING GIN(required_skills);
CREATE INDEX idx_question_bank_roles ON question_bank USING GIN(job_roles);
CREATE INDEX idx_question_bank_region ON question_bank(region);
```

**Sample Questions:**

```sql
-- Technical Question (Mid-level)
INSERT INTO question_bank (
    question_text, question_type, difficulty_level, category,
    required_skills, job_roles, sample_answer, key_points,
    difficulty_score
) VALUES (
    'Explain the difference between REST and GraphQL. When would you use each?',
    'technical',
    'mid',
    'API Design',
    ARRAY['REST', 'GraphQL', 'API Design'],
    ARRAY['Backend Developer', 'Full Stack Developer'],
    'REST (Representational State Transfer) is an architectural style using multiple endpoints (e.g., /users, /posts). GraphQL uses a single endpoint with flexible queries. REST is simpler, better for caching, ideal for CRUD operations. GraphQL is better when clients need different data shapes, reduces over-fetching/under-fetching. Use REST for simple APIs, public APIs, mobile apps needing caching. Use GraphQL for complex data relationships, multiple client types, rapid iteration.',
    '{
      "must_mention": [
        "REST uses multiple endpoints",
        "GraphQL uses single endpoint",
        "GraphQL allows flexible queries",
        "REST is simpler for basic operations"
      ],
      "bonus_points": [
        "Caching advantages of REST",
        "Over-fetching/under-fetching in REST",
        "N+1 query problem in GraphQL",
        "Type safety in GraphQL"
      ]
    }'::jsonb,
    5
);

-- Behavioral Question (Senior-level)
INSERT INTO question_bank (
    question_text, question_type, difficulty_level, category,
    job_roles, sample_answer, key_points, difficulty_score
) VALUES (
    'Tell me about a time you had to make a critical architecture decision with incomplete information.',
    'behavioral',
    'senior',
    'Leadership & Decision Making',
    ARRAY['Senior Engineer', 'Tech Lead', 'Software Architect'],
    'At my previous role, we needed to choose a database for a new microservice with uncertain scale requirements. I gathered what data we had: current user base, growth projections, and similar services performance. I proposed PostgreSQL with a migration plan to distributed database if needed, rather than over-engineering upfront. I documented assumptions, set up monitoring to validate them, and established triggers for re-evaluation. This approach balanced risk with pragmatism. The system scaled successfully for 2 years before needing optimization.',
    '{
      "must_mention": [
        "Specific situation with incomplete data",
        "Process used to gather available information",
        "Decision made and rationale",
        "Outcome of the decision"
      ],
      "bonus_points": [
        "Risk mitigation strategies",
        "How assumptions were documented",
        "Monitoring/validation approach",
        "Learning or adjustments made"
      ]
    }'::jsonb,
    8
);

-- Situational Question (MENA-specific)
INSERT INTO question_bank (
    question_text, question_type, difficulty_level, category,
    required_skills, job_roles, region, sample_answer,
    key_points, difficulty_score
) VALUES (
    'How would you approach building a multilingual application for MENA markets supporting Arabic and French?',
    'situational',
    'mid',
    'Internationalization',
    ARRAY['i18n', 'Arabic', 'Frontend Development'],
    ARRAY['Frontend Developer', 'Full Stack Developer'],
    'MENA',
    'I would implement i18n from the start: 1) Use i18n library (e.g., react-i18next). 2) Support RTL (right-to-left) for Arabic with CSS logical properties. 3) Store translations in JSON files organized by locale. 4) Consider cultural differences (date formats, number formatting). 5) Test with native speakers for both languages. 6) Handle text expansion (Arabic text often longer). 7) Use Unicode UTF-8 encoding. 8) Consider dialect variations in Arabic (Egyptian, Levantine, Gulf).',
    '{
      "must_mention": [
        "RTL (right-to-left) support for Arabic",
        "i18n library or framework",
        "Separate translation files",
        "Cultural considerations"
      ],
      "bonus_points": [
        "Specific tools (react-i18next, vue-i18n)",
        "CSS logical properties",
        "Arabic dialect awareness",
        "Date/number formatting differences",
        "Text expansion handling",
        "Font considerations for Arabic"
      ]
    }'::jsonb,
    6
);
```

**Example Queries:**

```sql
-- Get questions for specific interview configuration
SELECT id, question_text, difficulty_level, category
FROM question_bank
WHERE question_type = 'technical'
  AND difficulty_level = 'mid'
  AND 'Python' = ANY(required_skills)
  AND region IN ('Global', 'Tunisia')
ORDER BY RANDOM()
LIMIT 5;

-- Find questions by job role
SELECT id, question_text, question_type, difficulty_level
FROM question_bank
WHERE 'Senior Engineer' = ANY(job_roles)
ORDER BY usage_count ASC, difficulty_score DESC
LIMIT 10;

-- Get mixed interview questions (70% technical, 30% behavioral)
(
  SELECT id, question_text, question_type
  FROM question_bank
  WHERE question_type = 'technical' 
    AND difficulty_level = 'senior'
  ORDER BY RANDOM()
  LIMIT 7
)
UNION ALL
(
  SELECT id, question_text, question_type
  FROM question_bank
  WHERE question_type = 'behavioral'
    AND difficulty_level = 'senior'
  ORDER BY RANDOM()
  LIMIT 3
);

-- Increment usage count
UPDATE question_bank
SET usage_count = usage_count + 1
WHERE id = ANY(ARRAY[1, 5, 12, 18, 25]);

-- Search questions by keyword
SELECT id, question_text, category, difficulty_level
FROM question_bank
WHERE question_text ILIKE '%microservices%'
   OR category ILIKE '%microservices%'
ORDER BY difficulty_score DESC;
```

---

## 3. Interview Sessions Table

**Purpose:** Track individual interview sessions for users

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS interview_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE SET NULL,
    session_type VARCHAR(50) NOT NULL,
    job_role VARCHAR(100),
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('junior', 'mid', 'senior')),
    total_questions INTEGER DEFAULT 0,
    questions_answered INTEGER DEFAULT 0,
    average_score FLOAT,
    status VARCHAR(20) CHECK (status IN ('in_progress', 'completed', 'abandoned')),
    duration_seconds INTEGER,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    notes TEXT
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Session identifier |
| `user_id` | INTEGER | FK → users(id), CASCADE | Session owner |
| `resume_id` | INTEGER | FK → resumes(id), SET NULL | Associated resume (optional) |
| `session_type` | VARCHAR(50) | NOT NULL | Interview type (see below) |
| `job_role` | VARCHAR(100) | NULL | Target job role |
| `difficulty_level` | VARCHAR(20) | CHECK | junior/mid/senior |
| `total_questions` | INTEGER | DEFAULT 0 | Questions in session |
| `questions_answered` | INTEGER | DEFAULT 0 | Questions completed |
| `average_score` | FLOAT | NULL | Average overall score (0-100) |
| `status` | VARCHAR(20) | CHECK | in_progress/completed/abandoned |
| `duration_seconds` | INTEGER | NULL | Total time spent |
| `started_at` | TIMESTAMP | AUTO | Session start time |
| `completed_at` | TIMESTAMP | NULL | Session completion time |
| `notes` | TEXT | NULL | User/admin notes |

**Session Types:**
- **technical** - Pure technical questions
- **behavioral** - Behavioral & situational questions
- **mixed** - Combination of technical & behavioral
- **job-specific** - Questions tailored to specific job posting

**Status Flow:**
```
in_progress → completed
            ↘ abandoned
```

**Indexes:**
```sql
CREATE INDEX idx_interview_sessions_user_id ON interview_sessions(user_id);
CREATE INDEX idx_interview_sessions_status ON interview_sessions(status);
CREATE INDEX idx_interview_sessions_started_at ON interview_sessions(started_at DESC);
```

**Example Queries:**

```sql
-- Start new interview session
INSERT INTO interview_sessions (
    user_id, resume_id, session_type, job_role,
    difficulty_level, total_questions, status
)
VALUES (
    1, 5, 'mixed', 'Senior Backend Developer', 'senior', 10, 'in_progress'
)
RETURNING id;

-- Update session progress
UPDATE interview_sessions
SET 
    questions_answered = questions_answered + 1,
    average_score = (
        SELECT AVG(overall_score)
        FROM interview_answers
        WHERE session_id = 42
    )
WHERE id = 42;

-- Complete session
UPDATE interview_sessions
SET 
    status = 'completed',
    completed_at = CURRENT_TIMESTAMP,
    duration_seconds = EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - started_at))
WHERE id = 42;

-- Get user's interview history
SELECT 
    id, session_type, job_role, difficulty_level,
    total_questions, questions_answered, average_score,
    status, started_at, completed_at
FROM interview_sessions
WHERE user_id = 1
ORDER BY started_at DESC;

-- Get incomplete sessions (reminders)
SELECT id, session_type, job_role, started_at,
       EXTRACT(HOUR FROM NOW() - started_at) as hours_ago
FROM interview_sessions
WHERE user_id = 1 
  AND status = 'in_progress'
  AND started_at < NOW() - INTERVAL '24 hours'
ORDER BY started_at ASC;

-- Performance analytics
SELECT 
    user_id,
    COUNT(*) as total_sessions,
    AVG(average_score) as overall_avg_score,
    AVG(duration_seconds)/60 as avg_duration_minutes,
    COUNT(*) FILTER (WHERE status = 'completed') as completed_count,
    COUNT(*) FILTER (WHERE status = 'abandoned') as abandoned_count
FROM interview_sessions
WHERE created_at >= NOW() - INTERVAL '90 days'
GROUP BY user_id
HAVING COUNT(*) >= 3
ORDER BY overall_avg_score DESC;
```

---

## 4. Interview Questions Table

**Purpose:** Link specific questions to interview sessions (junction table)

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS interview_questions (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES interview_sessions(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES question_bank(id) ON DELETE CASCADE,
    question_order INTEGER NOT NULL,
    asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_limit_seconds INTEGER,
    UNIQUE(session_id, question_order)
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Record identifier |
| `session_id` | INTEGER | FK → interview_sessions(id), CASCADE | Parent session |
| `question_id` | INTEGER | FK → question_bank(id), CASCADE | Selected question |
| `question_order` | INTEGER | NOT NULL | Question number in session (1, 2, 3...) |
| `asked_at` | TIMESTAMP | AUTO | When question was presented |
| `time_limit_seconds` | INTEGER | NULL | Optional time limit |

**Purpose:**
- Associates questions from question_bank with specific sessions
- Maintains question order within session
- Tracks timing information

**Indexes:**
```sql
CREATE INDEX idx_interview_questions_session_id ON interview_questions(session_id);
CREATE INDEX idx_interview_questions_question_id ON interview_questions(question_id);
CREATE UNIQUE INDEX idx_interview_questions_session_order 
  ON interview_questions(session_id, question_order);
```

**Example Queries:**

```sql
-- Add questions to session
INSERT INTO interview_questions (session_id, question_id, question_order, time_limit_seconds)
VALUES 
    (42, 15, 1, 300),  -- 5 minutes
    (42, 28, 2, 300),
    (42, 103, 3, 600), -- 10 minutes for harder question
    (42, 45, 4, 300);

-- Get questions for session with details
SELECT 
    iq.id, iq.question_order, iq.time_limit_seconds,
    qb.question_text, qb.question_type, qb.difficulty_level,
    qb.category, qb.key_points
FROM interview_questions iq
JOIN question_bank qb ON iq.question_id = qb.id
WHERE iq.session_id = 42
ORDER BY iq.question_order;

-- Get next unanswered question
SELECT 
    iq.id as interview_question_id,
    iq.question_order,
    qb.question_text,
    qb.question_type,
    qb.sample_answer
FROM interview_questions iq
JOIN question_bank qb ON iq.question_id = qb.id
LEFT JOIN interview_answers ia ON iq.id = ia.interview_question_id
WHERE iq.session_id = 42 
  AND ia.id IS NULL
ORDER BY iq.question_order
LIMIT 1;

-- Session progress check
SELECT 
    COUNT(*) as total_questions,
    COUNT(ia.id) as answered_questions,
    COUNT(*) - COUNT(ia.id) as remaining_questions
FROM interview_questions iq
LEFT JOIN interview_answers ia ON iq.id = ia.interview_question_id
WHERE iq.session_id = 42;
```

---

## 5. Interview Answers Table

**Purpose:** Store user answers with AI-generated scores and feedback

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS interview_answers (
    id SERIAL PRIMARY KEY,
    interview_question_id INTEGER REFERENCES interview_questions(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES interview_sessions(id) ON DELETE CASCADE,
    user_answer TEXT,
    time_taken_seconds INTEGER,
    relevance_score INTEGER CHECK (relevance_score >= 0 AND relevance_score <= 100),
    completeness_score INTEGER CHECK (completeness_score >= 0 AND completeness_score <= 100),
    clarity_score INTEGER CHECK (clarity_score >= 0 AND clarity_score <= 100),
    technical_accuracy_score INTEGER CHECK (technical_accuracy_score >= 0 AND technical_accuracy_score <= 100),
    communication_score INTEGER CHECK (communication_score >= 0 AND communication_score <= 100),
    overall_score INTEGER CHECK (overall_score >= 0 AND overall_score <= 100),
    strengths JSONB,
    weaknesses JSONB,
    missing_points JSONB,
    suggestions JSONB,
    ai_feedback TEXT,
    word_count INTEGER,
    sentiment VARCHAR(20),
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Answer identifier |
| `interview_question_id` | INTEGER | FK → interview_questions(id), CASCADE | Question answered |
| `session_id` | INTEGER | FK → interview_sessions(id), CASCADE | Parent session |
| `user_answer` | TEXT | NULL | User's response text |
| `time_taken_seconds` | INTEGER | NULL | Answer duration |
| `relevance_score` | INTEGER | 0-100 CHECK | Answer relevance to question |
| `completeness_score` | INTEGER | 0-100 CHECK | Coverage of key points |
| `clarity_score` | INTEGER | 0-100 CHECK | Communication clarity |
| `technical_accuracy_score` | INTEGER | 0-100 CHECK | Technical correctness |
| `communication_score` | INTEGER | 0-100 CHECK | Overall communication quality |
| `overall_score` | INTEGER | 0-100 CHECK | Composite score |
| `strengths` | JSONB | NULL | Positive aspects |
| `weaknesses` | JSONB | NULL | Areas needing improvement |
| `missing_points` | JSONB | NULL | Key points not mentioned |
| `suggestions` | JSONB | NULL | Improvement recommendations |
| `ai_feedback` | TEXT | NULL | Detailed AI-generated feedback |
| `word_count` | INTEGER | NULL | Total words in answer |
| `sentiment` | VARCHAR(20) | NULL | positive/neutral/negative |
| `analyzed_at` | TIMESTAMP | AUTO | Analysis timestamp |

**Score Calculation:**
```
Overall Score = (
    Relevance × 0.25 +
    Completeness × 0.25 +
    Technical Accuracy × 0.25 +
    Clarity × 0.15 +
    Communication × 0.10
)
```

**Feedback Structure (JSONB):**
```json
{
  "strengths": [
    "Clear explanation of core concepts",
    "Good use of concrete examples",
    "Demonstrated practical experience",
    "Well-structured answer"
  ],
  "weaknesses": [
    "Missing discussion of edge cases",
    "Could elaborate on performance implications",
    "Example could be more detailed"
  ],
  "missing_points": [
    "Did not mention caching strategies",
    "Overlooked security considerations",
    "Failed to discuss scalability aspects"
  ],
  "suggestions": [
    "Add specific metrics or numbers to strengthen claims",
    "Discuss trade-offs between different approaches",
    "Include edge cases in explanations",
    "Structure answer with introduction, body, conclusion"
  ]
}
```

**Indexes:**
```sql
CREATE INDEX idx_interview_answers_question_id ON interview_answers(interview_question_id);
CREATE INDEX idx_interview_answers_session_id ON interview_answers(session_id);
CREATE INDEX idx_interview_answers_overall_score ON interview_answers(overall_score DESC);
```

**Example Queries:**

```sql
-- Save user answer (initially without scores)
INSERT INTO interview_answers (
    interview_question_id, session_id, user_answer,
    time_taken_seconds, word_count
)
VALUES (
    105, 42,
    'REST and GraphQL are both API architectures. REST uses multiple endpoints...',
    180, 85
)
RETURNING id;

-- Update with AI analysis scores
UPDATE interview_answers
SET 
    relevance_score = 85,
    completeness_score = 78,
    clarity_score = 90,
    technical_accuracy_score = 82,
    communication_score = 88,
    overall_score = 83,
    strengths = '["Clear explanation", "Good examples"]'::jsonb,
    weaknesses = '["Missing edge cases"]'::jsonb,
    missing_points = '["Caching strategies", "Security"]'::jsonb,
    suggestions = '["Add metrics", "Discuss trade-offs"]'::jsonb,
    ai_feedback = 'Strong answer demonstrating good understanding...',
    sentiment = 'positive'
WHERE id = 250;

-- Get answer with full context
SELECT 
    ia.user_answer,
    ia.overall_score,
    ia.time_taken_seconds,
    ia.strengths,
    ia.weaknesses,
    ia.suggestions,
    qb.question_text,
    qb.sample_answer,
    qb.key_points
FROM interview_answers ia
JOIN interview_questions iq ON ia.interview_question_id = iq.id
JOIN question_bank qb ON iq.question_id = qb.id
WHERE ia.id = 250;

-- Session answer summary
SELECT 
    AVG(overall_score) as avg_score,
    AVG(time_taken_seconds) as avg_time,
    AVG(word_count) as avg_words,
    COUNT(*) as total_answers
FROM interview_answers
WHERE session_id = 42;

-- Find weakest areas for user
SELECT 
    UNNEST(ARRAY[
        'relevance', 'completeness', 'clarity',
        'technical_accuracy', 'communication'
    ]) as dimension,
    UNNEST(ARRAY[
        AVG(relevance_score),
        AVG(completeness_score),
        AVG(clarity_score),
        AVG(technical_accuracy_score),
        AVG(communication_score)
    ]) as avg_score
FROM interview_answers ia
JOIN interview_sessions sess ON ia.session_id = sess.id
WHERE sess.user_id = 1
ORDER BY avg_score ASC
LIMIT 3;
```

---

## 6. Interview Feedback Table

**Purpose:** Comprehensive feedback summary for completed interview sessions

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS interview_feedback (
    id SERIAL PRIMARY KEY,
    session_id INTEGER UNIQUE REFERENCES interview_sessions(id) ON DELETE CASCADE,
    overall_performance TEXT,
    technical_rating INTEGER CHECK (technical_rating >= 1 AND technical_rating <= 5),
    communication_rating INTEGER CHECK (communication_rating >= 1 AND communication_rating <= 5),
    confidence_rating INTEGER CHECK (confidence_rating >= 1 AND confidence_rating <= 5),
    key_strengths JSONB,
    areas_to_improve JSONB,
    recommended_resources JSONB,
    preparation_tips TEXT,
    practice_recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Feedback identifier |
| `session_id` | INTEGER | UNIQUE FK → interview_sessions(id), CASCADE | Associated session |
| `overall_performance` | TEXT | NULL | High-level performance summary |
| `technical_rating` | INTEGER | 1-5 CHECK | Technical skills rating |
| `communication_rating` | INTEGER | 1-5 CHECK | Communication skills rating |
| `confidence_rating` | INTEGER | 1-5 CHECK | Confidence level rating |
| `key_strengths` | JSONB | NULL | Notable strengths |
| `areas_to_improve` | JSONB | NULL | Improvement opportunities |
| `recommended_resources` | JSONB | NULL | Learning resources |
| `preparation_tips` | TEXT | NULL | Interview prep advice |
| `practice_recommendations` | TEXT | NULL | Practice suggestions |
| `created_at` | TIMESTAMP | AUTO | Feedback generation time |

**Rating Scale (1-5):**
- **1** - Poor: Needs significant improvement
- **2** - Below Average: Some knowledge but major gaps
- **3** - Average: Meets basic expectations
- **4** - Good: Strong performance
- **5** - Excellent: Outstanding, exceeds expectations

**Feedback Structure (JSONB):**
```json
{
  "key_strengths": [
    {
      "area": "Technical Knowledge",
      "description": "Strong understanding of core concepts",
      "examples": ["Excellent explanation of microservices", "Clear grasp of database optimization"]
    },
    {
      "area": "Communication",
      "description": "Articulated ideas clearly with good examples",
      "examples": ["Used STAR method effectively", "Provided concrete metrics"]
    }
  ],
  "areas_to_improve": [
    {
      "area": "System Design",
      "priority": "high",
      "description": "Need to strengthen knowledge of scalability patterns",
      "specific_gaps": ["Load balancing strategies", "Caching architectures", "Database sharding"],
      "action_items": [
        "Study system design interview books",
        "Practice designing real-world systems",
        "Review case studies of large-scale systems"
      ]
    },
    {
      "area": "Answer Structure",
      "priority": "medium",
      "description": "Answers could be more concise and organized",
      "specific_gaps": ["Too verbose at times", "Not always answering the question directly"],
      "action_items": [
        "Practice STAR method (Situation, Task, Action, Result)",
        "Prepare answer frameworks",
        "Time management practice"
      ]
    }
  ],
  "recommended_resources": [
    {
      "type": "book",
      "title": "Designing Data-Intensive Applications",
      "author": "Martin Kleppmann",
      "relevance": "Excellent for system design and scalability"
    },
    {
      "type": "online_course",
      "title": "System Design Interview Prep",
      "platform": "Educative.io",
      "url": "https://educative.io/courses/grokking-system-design",
      "relevance": "Comprehensive system design patterns"
    },
    {
      "type": "practice_platform",
      "name": "LeetCode",
      "url": "https://leetcode.com",
      "focus": "Practice behavioral questions and system design"
    }
  ]
}
```

**Indexes:**
```sql
CREATE UNIQUE INDEX idx_interview_feedback_session_id ON interview_feedback(session_id);
```

**Example Queries:**

```sql
-- Generate feedback for completed session
INSERT INTO interview_feedback (
    session_id, overall_performance,
    technical_rating, communication_rating, confidence_rating,
    key_strengths, areas_to_improve, recommended_resources,
    preparation_tips, practice_recommendations
)
VALUES (
    42,
    'Strong performance overall with good technical knowledge. Areas for improvement include system design and answer conciseness.',
    4, 4, 3,
    '{"key_strengths": [...]}'::jsonb,
    '{"areas_to_improve": [...]}'::jsonb,
    '{"recommended_resources": [...]}'::jsonb,
    'Practice more system design questions. Use STAR method for behavioral questions. Focus on concise, structured answers.',
    'Complete 5 system design problems. Practice 10 behavioral questions. Mock interviews with peers.'
);

-- Get feedback for session
SELECT 
    ifb.*,
    sess.average_score,
    sess.duration_seconds,
    sess.job_role
FROM interview_feedback ifb
JOIN interview_sessions sess ON ifb.session_id = sess.id
WHERE sess.id = 42;

-- User progress tracking
SELECT 
    sess.started_at,
    sess.session_type,
    sess.average_score,
    ifb.technical_rating,
    ifb.communication_rating,
    ifb.confidence_rating
FROM interview_sessions sess
LEFT JOIN interview_feedback ifb ON sess.id = ifb.session_id
WHERE sess.user_id = 1 
  AND sess.status = 'completed'
ORDER BY sess.started_at ASC;

-- Identify common improvement areas across users
SELECT 
    improvement_area->>'area' as area,
    improvement_area->>'priority' as priority,
    COUNT(*) as frequency
FROM interview_feedback,
LATERAL jsonb_array_elements(areas_to_improve) AS improvement_area
GROUP BY improvement_area->>'area', improvement_area->>'priority'
ORDER BY frequency DESC;
```

---

**End of Part 3**

**Next:** [Part 4 - Footprint Scanner Tables](./DATABASE_DOCUMENTATION_PART4.md)

---

**Documentation Navigation:**
- [Part 1](./DATABASE_DOCUMENTATION_PART1.md): Overview, Architecture, Users, Resumes
- [Part 2](./DATABASE_DOCUMENTATION_PART2.md): Resume Enhancements, Skills, Jobs
- **Part 3** (Current): Interview Module Tables
- **Part 4**: Footprint Scanner Tables  
- **Part 5**: Indexes, Migrations & Best Practices
