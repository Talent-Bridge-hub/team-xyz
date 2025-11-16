# Interview Module Documentation - Part 1

---

## Table of Contents - Part 1

1. [Module Overview](#module-overview)
2. [System Architecture](#system-architecture)
3. [Core Features](#core-features)
4. [Backend API Reference](#backend-api-reference)
5. [Data Models](#data-models)

---

## Module Overview

### Purpose

The **AI Interview Simulator** is a comprehensive practice platform that helps job seekers prepare for real interviews through AI-powered simulations. The module provides:

- **Realistic Interview Experience**: Simulates real interview scenarios with job-specific questions
- **Instant AI Feedback**: Groq AI-powered answer analysis with multi-dimensional scoring
- **Progressive Learning**: Track improvement over time with detailed performance metrics
- **Personalized Recommendations**: Tailored feedback based on job role, difficulty level, and performance

### Benefits

| Benefit | Description |
|---------|-------------|
| **Safe Practice Environment** | Practice without pressure, make mistakes, and learn |
| **Instant Feedback** | Get immediate analysis and suggestions for improvement |
| **Comprehensive Coverage** | Technical, behavioral, and mixed interview types |
| **Progress Tracking** | Monitor improvement across multiple sessions |
| **AI-Powered Analysis** | Advanced answer evaluation using Groq LLaMA 3.3 70B model |
| **Customizable Sessions** | Tailor interviews to specific job roles and difficulty levels |

### Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Backend Framework** | FastAPI | 0.104+ | High-performance REST API |
| **Database** | PostgreSQL | 14+ | Relational data storage with JSONB support |
| **AI Engine** | Groq API | Latest | Fast LLM inference for answer analysis |
| **AI Model** | LLaMA 3.3 70B Versatile | Latest | Advanced language understanding |
| **ORM** | psycopg2 | 2.9+ | PostgreSQL adapter |
| **Session Management** | Python datetime | 3.12+ | Session tracking and timing |
| **Validation** | Pydantic | 2.0+ | Request/response validation |

### Key Statistics

- **5 Database Tables**: Complete interview lifecycle tracking
- **13 API Endpoints**: Full CRUD + session management
- **40+ Pre-loaded Questions**: Curated question bank
- **6 Scoring Dimensions**: Multi-faceted answer evaluation
- **3 Difficulty Levels**: Junior, Mid, Senior
- **4 Interview Types**: Technical, Behavioral, Mixed, Job-Specific
- **10+ Job Roles**: Pre-configured role templates
- **Real-time Analysis**: < 2 second response time with Groq

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ InterviewPage│  │InterviewSetup│  │InterviewChat │         │
│  │  (Container) │  │   (Config)   │  │  (Q&A Flow)  │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
│         └──────────────────┴──────────────────┘                  │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │ API Calls
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND API (FastAPI)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              interview.py (API Endpoints)                 │  │
│  │  • POST /start       • POST /answer                       │  │
│  │  • GET  /question    • POST /complete                     │  │
│  │  • GET  /sessions    • GET  /stats                        │  │
│  └──────────────┬───────────────────────────────────────────┘  │
│                 │                                                │
│  ┌──────────────┴───────────────────────────────────────────┐  │
│  │         interview_simulator.py (Business Logic)          │  │
│  │  • Session Management  • Question Selection              │  │
│  │  • Progress Tracking   • Feedback Generation             │  │
│  └──────────────┬───────────────────────────────────────────┘  │
│                 │                                                │
└─────────────────┼────────────────────────────────────────────────┘
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
┌─────────────┐         ┌─────────────────────┐
│  PostgreSQL │         │  Groq AI Service    │
│  (Database) │         │  (Answer Analysis)  │
│             │         │                     │
│ • Sessions  │         │ • LLaMA 3.3 70B     │
│ • Questions │         │ • Real-time Scoring │
│ • Answers   │         │ • Feedback Gen      │
│ • Feedback  │         └─────────────────────┘
└─────────────┘
```

### Data Flow Diagram

```
Interview Session Flow:
┌─────────────────────────────────────────────────────────────────┐
│ 1. START SESSION                                                │
│    User → InterviewSetup → POST /start → Create Session        │
│    ↓                                                             │
│    Select: Type, Role, Difficulty, Num Questions, Resume        │
│    ↓                                                             │
│    Database: Insert interview_sessions record                   │
│    ↓                                                             │
│    Select Questions: From question_bank based on criteria       │
│    ↓                                                             │
│    Database: Insert interview_questions records                 │
│    ↓                                                             │
│    Response: session_id + first_question                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 2. ANSWER QUESTIONS (Loop)                                      │
│    User Types Answer → POST /answer → Groq AI Analysis         │
│    ↓                                                             │
│    Groq API Call:                                               │
│      - Model: llama-3.3-70b-versatile                           │
│      - Temperature: 0.3 (consistent scoring)                    │
│      - Timeout: 2-3 seconds                                     │
│    ↓                                                             │
│    AI Analysis Returns:                                         │
│      - 6 Scoring Dimensions (0-100)                             │
│      - Strengths, Weaknesses, Missing Points                    │
│      - Actionable Suggestions                                   │
│      - Narrative Feedback                                       │
│      - Sentiment Analysis                                       │
│    ↓                                                             │
│    Database: Insert interview_answers record                    │
│    ↓                                                             │
│    Update Session: questions_answered++, recalc avg_score       │
│    ↓                                                             │
│    Response: Feedback + has_more_questions flag                 │
│    ↓                                                             │
│    If has_more → GET /question → Next Question                  │
│    If complete → Proceed to Completion                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 3. COMPLETE SESSION                                             │
│    All Questions Answered → POST /complete → Generate Report   │
│    ↓                                                             │
│    Calculate Session Statistics:                                │
│      - Average scores across all dimensions                     │
│      - Overall performance rating                               │
│      - Ratings (1-5): Technical, Communication, Confidence      │
│    ↓                                                             │
│    Generate Session Feedback:                                   │
│      - Key Strengths (top 5)                                    │
│      - Areas to Improve (top 5)                                 │
│      - Recommended Resources                                    │
│      - Preparation Tips                                         │
│      - Practice Recommendations                                 │
│    ↓                                                             │
│    Database: Insert interview_feedback record                   │
│    ↓                                                             │
│    Update Session: status='completed', completed_at, duration   │
│    ↓                                                             │
│    Response: Completion Report with all metrics                 │
└─────────────────────────────────────────────────────────────────┘
```

### File Structure

```
Utopia/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── interview.py              # 🔥 Main API endpoints (13 endpoints, 850 lines)
│   │   └── models/
│   │       └── interview.py              # 🔥 Pydantic models (40+ models, 600 lines)
│   ├── database/
│   │   └── interview_question_bank.sql   # 📦 Pre-populated questions (40+ questions)
│   └── migrations/
│       └── create_interview_tables.py    # 🗄️ Database migrations
│
├── config/
│   └── interview_schema.sql              # 🗄️ Complete database schema (5 tables)
│
├── utils/
│   ├── interview_simulator.py            # 🧠 Core business logic (800 lines)
│   └── groq_answer_analyzer.py           # 🤖 AI answer analysis (400 lines)
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   └── interview/
    │   │       └── index.tsx              # 📄 Main interview page (150 lines)
    │   ├── components/
    │   │   └── interview/
    │   │       ├── InterviewSetup.tsx     # ⚙️ Session configuration (400 lines)
    │   │       ├── InterviewChat.tsx      # 💬 Q&A chat interface (550 lines)
    │   │       └── InterviewHistory.tsx   # 📊 Past sessions view (850 lines)
    │   └── services/
    │       └── interview.service.ts       # 🔌 API client (350 lines)
    │
    └── Total: ~4,990 lines of code
```

---

## Core Features

### 1. Session Configuration

#### Supported Session Types

| Type | Description | Question Mix | Use Case |
|------|-------------|--------------|----------|
| **Technical** | Programming & problem-solving | 100% technical | Software engineering roles |
| **Behavioral** | Soft skills & experience | 100% behavioral/situational | All roles |
| **Mixed** | Balanced combination | 60% technical + 40% behavioral | Most common |
| **Job-Specific** | Role-tailored questions | Customized per role | Specialized positions |

#### Difficulty Levels

| Level | Experience | Question Complexity | Example Questions |
|-------|-----------|---------------------|-------------------|
| **Junior** | 0-2 years | Fundamentals, basic concepts | "What is REST API?", "Explain var vs let" |
| **Mid** | 2-5 years | Intermediate, applied knowledge | "Optimize slow query", "Async vs Sync" |
| **Senior** | 5+ years | Advanced, system design | "Design Twitter scale", "Event-driven arch" |

#### Supported Job Roles

**Pre-configured Roles:**
- Software Engineer
- Frontend Developer
- Backend Developer
- Full Stack Developer
- Data Scientist
- Data Analyst
- Product Manager
- DevOps Engineer
- Mobile Developer
- UI/UX Designer
- *Custom Role (user-defined)*

### 2. AI-Powered Answer Analysis

#### Groq AI Integration

```python
# Configuration
MODEL: llama-3.3-70b-versatile
TEMPERATURE: 0.3  # Low for consistent scoring
MAX_TOKENS: 2000
TIMEOUT: 5 seconds
```

#### Scoring Dimensions (0-100 scale)

| Dimension | Weight | Description | Example Factors |
|-----------|--------|-------------|-----------------|
| **Overall** | 100% | Aggregate performance | Average of all dimensions |
| **Relevance** | 20% | Addresses the question | On-topic, focused answer |
| **Completeness** | 25% | Covers all key points | Mentions expected topics |
| **Clarity** | 15% | Easy to understand | Structure, flow, examples |
| **Technical Accuracy** | 25% | Factually correct | No errors, up-to-date info |
| **Communication** | 15% | Expression quality | Grammar, confidence, tone |

#### Feedback Components

1. **Strengths** (3-5 items)
   - What the candidate did well
   - Positive aspects of the answer
   - Areas demonstrating competence

2. **Weaknesses** (2-4 items)
   - Areas needing improvement
   - Common mistakes made
   - Gaps in knowledge

3. **Missing Points** (1-3 items)
   - Key concepts not mentioned
   - Expected topics omitted
   - Critical details overlooked

4. **Suggestions** (3-5 items)
   - Actionable improvement steps
   - Specific recommendations
   - Practice exercises

5. **Narrative Feedback** (2-3 sentences)
   - Holistic evaluation summary
   - Overall impression
   - Encouragement + guidance

6. **Sentiment Analysis**
   - `positive`: Confident, strong answer
   - `neutral`: Adequate, room for improvement
   - `negative`: Significant gaps, needs work

### 3. Question Bank

#### Question Categories

| Category | Count | Topics Covered |
|----------|-------|----------------|
| **Programming Fundamentals** | 8 | Variables, types, OOP, data structures |
| **Web Development** | 6 | REST APIs, HTTP, frontend/backend |
| **Database** | 5 | SQL, NoSQL, optimization, queries |
| **System Design** | 4 | Architecture, scalability, microservices |
| **Tools & Workflows** | 3 | Git, CI/CD, DevOps |
| **Behavioral** | 8 | Learning, teamwork, conflict, leadership |
| **Situational** | 6 | Problem-solving, decision-making, pressure |

#### Question Attributes

```sql
CREATE TABLE interview_question_bank (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,              -- The question
    question_type VARCHAR(50) NOT NULL,       -- technical/behavioral/situational
    category VARCHAR(100),                    -- programming, system_design, etc.
    difficulty_level VARCHAR(20) NOT NULL,    -- junior/mid/senior
    job_roles TEXT[],                         -- Applicable roles
    key_points JSONB,                         -- Expected answer points
    sample_answer TEXT,                       -- Reference answer
    tags TEXT[]                               -- Searchable tags
);
```

#### Sample Questions

**Junior Technical:**
```
"Explain the difference between var, let, and const in JavaScript."
Expected Points: var scope, let block-scope, const immutability
```

**Mid Technical:**
```
"How would you optimize a slow database query?"
Expected Points: indexes, EXPLAIN, query plan, caching
```

**Senior Technical:**
```
"Design a system like Twitter that handles millions of users."
Expected Points: load balancing, sharding, caching, message queues, CDN
```

**Behavioral:**
```
"Tell me about a time you had to learn a new technology quickly."
STAR Method: Situation, Task, Action, Result
```

### 4. Session Management

#### Session Lifecycle

```
┌─────────────┐
│   CREATED   │  ← Start session
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ IN_PROGRESS │  ← Answering questions
└──────┬──────┘
       │
       ├──→ (Timeout) ──→ ABANDONED
       │
       ▼
┌─────────────┐
│  COMPLETED  │  ← All questions answered
└─────────────┘
```

#### Session States

| State | Description | Allowed Actions |
|-------|-------------|-----------------|
| `in_progress` | Active interview | Answer questions, get next question |
| `completed` | Finished | View report, delete session |
| `abandoned` | Timed out/cancelled | View partial results, restart |

#### Session Metadata

- **Timestamps**: `started_at`, `completed_at`
- **Duration**: Auto-calculated in seconds
- **Progress**: `questions_answered / total_questions`
- **Average Score**: Real-time calculation
- **User Context**: `user_id`, `resume_id` (optional)

### 5. Performance Tracking

#### Session Statistics

```typescript
{
  total_sessions: 42,
  total_questions_answered: 210,
  average_overall_score: 78.5,
  average_session_duration_minutes: 25.3,
  performance_distribution: {
    excellent: 10,
    good: 20,
    average: 8,
    needs_improvement: 4
  },
  favorite_job_role: "Software Engineer",
  improvement_trend: "improving"  // improving/stable/declining
}
```

#### Performance Ratings (1-5 scale)

| Rating | Description | Score Range |
|--------|-------------|-------------|
| **5 ⭐⭐⭐⭐⭐** | Exceptional | 90-100 |
| **4 ⭐⭐⭐⭐** | Strong | 80-89 |
| **3 ⭐⭐⭐** | Good | 70-79 |
| **2 ⭐⭐** | Fair | 60-69 |
| **1 ⭐** | Needs Work | 0-59 |

#### Improvement Tracking

- **Trend Analysis**: Compare last 3 vs previous 3 sessions
- **Score Evolution**: Line chart of overall scores over time
- **Weak Areas**: Track improvement in specific dimensions
- **Practice Frequency**: Sessions per week/month

---

## Backend API Reference

### Base URL
```
http://localhost:8000/api/v1/interview
```

### Authentication
All endpoints require JWT authentication via Bearer token in the `Authorization` header.

```http
Authorization: Bearer <jwt_token>
```

---

### 1. Start Interview Session

**Endpoint:** `POST /start`

**Description:** Create a new interview session and receive the first question.

**Request Body:**
```json
{
  "session_type": "mixed",
  "job_role": "Software Engineer",
  "difficulty_level": "mid",
  "num_questions": 5,
  "resume_id": 10  // Optional
}
```

**Request Schema:**
```typescript
{
  session_type: 'technical' | 'behavioral' | 'mixed' | 'job-specific',
  job_role: string,            // Required, min 3 chars
  difficulty_level: 'junior' | 'mid' | 'senior',
  num_questions: number,       // Min: 1, Max: 20
  resume_id?: number           // Optional, for personalized questions
}
```

**Response (200 OK):**
```json
{
  "session_id": 42,
  "session_type": "mixed",
  "job_role": "Software Engineer",
  "difficulty_level": "mid",
  "total_questions": 5,
  "first_question": {
    "question_id": 15,
    "question_number": 1,
    "total_questions": 5,
    "question_text": "What is the difference between SQL and NoSQL databases?",
    "question_type": "technical",
    "category": "database",
    "difficulty": "mid"
  },
  "message": "Interview session started! You have 5 questions to answer. Good luck!"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (e.g., num_questions > 20)
- `401 Unauthorized`: Missing/invalid auth token
- `500 Internal Server Error`: Database error

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/interview/start \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_type": "mixed",
    "job_role": "Backend Developer",
    "difficulty_level": "senior",
    "num_questions": 10
  }'
```

---

### 2. Get Next Question

**Endpoint:** `GET /{session_id}/question`

**Description:** Retrieve the next unanswered question in the session.

**Path Parameters:**
- `session_id` (integer): Interview session ID

**Response (200 OK):**
```json
{
  "question_id": 23,
  "question_number": 3,
  "total_questions": 5,
  "question_text": "Explain dependency injection and why it is useful.",
  "question_type": "technical",
  "category": "design_patterns",
  "difficulty": "mid"
}
```

**Error Responses:**
- `404 Not Found`: Session not found or no more questions
- `400 Bad Request`: Session already completed
- `401 Unauthorized`: Session doesn't belong to user

**Example cURL:**
```bash
curl -X GET http://localhost:8000/api/v1/interview/42/question \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 3. Submit Answer

**Endpoint:** `POST /answer`

**Description:** Submit an answer to a question and receive AI-powered feedback.

**Request Body:**
```json
{
  "session_id": 42,
  "question_id": 15,
  "answer": "SQL databases are relational and use structured schemas with tables and rows. They ensure ACID properties and are good for complex queries. NoSQL databases are non-relational, schema-less, and better for unstructured data and horizontal scaling. Examples: MySQL (SQL), MongoDB (NoSQL).",
  "time_taken_seconds": 120
}
```

**Request Schema:**
```typescript
{
  session_id: number,
  question_id: number,
  answer: string,              // Min: 10 characters
  time_taken_seconds?: number  // Optional, auto-calculated if not provided
}
```

**Response (200 OK):**
```json
{
  "answer_id": 156,
  "question_number": 1,
  "question_text": "What is the difference between SQL and NoSQL databases?",
  "your_answer": "SQL databases are relational...",
  "time_taken_seconds": 120,
  "scores": {
    "overall": 82,
    "relevance": 90,
    "completeness": 85,
    "clarity": 88,
    "technical_accuracy": 80,
    "communication": 87
  },
  "feedback": {
    "strengths": [
      "Clear explanation of fundamental differences",
      "Provided concrete examples (MySQL, MongoDB)",
      "Mentioned ACID properties and use cases"
    ],
    "weaknesses": [
      "Could elaborate more on horizontal vs vertical scaling",
      "Missing CAP theorem mention"
    ],
    "missing_points": [
      "NoSQL types (document, key-value, graph, columnar)",
      "Trade-offs between consistency and availability"
    ],
    "suggestions": [
      "Research different NoSQL database types and their specific use cases",
      "Study CAP theorem for distributed systems",
      "Practice explaining with real-world scenarios (e.g., social media vs banking)"
    ],
    "narrative": "Strong foundational answer that covers the main differences. You demonstrated good understanding of both paradigms. To improve, dive deeper into the trade-offs and provide more nuanced explanations of when to use each type."
  },
  "sentiment": "positive",
  "has_more_questions": true
}
```

**Error Responses:**
- `400 Bad Request`: Answer too short (<10 chars) or question already answered
- `404 Not Found`: Question not in session
- `401 Unauthorized`: Session doesn't belong to user
- `500 Internal Server Error`: AI analysis failed

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/interview/answer \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 42,
    "question_id": 15,
    "answer": "SQL databases are relational...",
    "time_taken_seconds": 120
  }'
```

---

### 4. Complete Session

**Endpoint:** `POST /{session_id}/complete`

**Description:** Finalize the interview session and generate comprehensive performance report.

**Path Parameters:**
- `session_id` (integer): Interview session ID

**Response (200 OK):**
```json
{
  "session_id": 42,
  "completed": true,
  "questions_answered": 5,
  "total_time_seconds": 1200,
  "average_scores": {
    "overall": 78.5,
    "relevance": 82.0,
    "completeness": 75.0,
    "clarity": 80.0,
    "technical_accuracy": 77.5,
    "communication": 78.0
  },
  "performance": "good",
  "ratings": {
    "technical": 4,
    "communication": 4,
    "confidence": 3
  },
  "feedback": {
    "strengths": [
      "Consistently strong performance across questions",
      "Excellent technical knowledge and accuracy",
      "Clear and confident communication style",
      "Well-structured and organized responses",
      "Good time management per question"
    ],
    "areas_to_improve": [
      "Provide more comprehensive answers covering all key points",
      "Work on confident and clear communication",
      "Focus more directly on what the question asks"
    ],
    "recommended_resources": [
      "LeetCode for technical practice",
      "Cracking the Coding Interview book",
      "System Design Interview resources",
      "STAR Method Guide for behavioral questions"
    ],
    "preparation_tips": "You're on the right track! Focus on the areas mentioned below.\n\nPractice answering questions out loud to build confidence.\n\nUse the STAR method (Situation, Task, Action, Result) for structured answers.",
    "practice_recommendations": "Practice 3-4 times per week. Mix technical and behavioral questions."
  },
  "message": "Interview completed! You answered 5 questions with an average score of 78.5%"
}
```

**Error Responses:**
- `404 Not Found`: Session not found
- `400 Bad Request`: Session already completed
- `401 Unauthorized`: Session doesn't belong to user

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/interview/42/complete \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 5. List User Sessions

**Endpoint:** `GET /sessions`

**Description:** Retrieve paginated list of user's interview sessions.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Max records to return (default: 20, max: 100)
- `session_type` (string, optional): Filter by type (technical/behavioral/mixed/job-specific)
- `session_status` (string, optional): Filter by status (in_progress/completed)

**Response (200 OK):**
```json
{
  "sessions": [
    {
      "id": 42,
      "session_type": "mixed",
      "job_role": "Software Engineer",
      "difficulty_level": "mid",
      "total_questions": 5,
      "questions_answered": 5,
      "status": "completed",
      "average_score": 78.5,
      "duration_seconds": 1200,
      "started_at": "2025-11-06T10:30:00Z",
      "completed_at": "2025-11-06T10:50:00Z",
      "overall_performance": "good",
      "technical_rating": 4,
      "communication_rating": 4,
      "confidence_rating": 3
    },
    {
      "id": 41,
      "session_type": "technical",
      "job_role": "Backend Developer",
      "difficulty_level": "senior",
      "total_questions": 10,
      "questions_answered": 7,
      "status": "in_progress",
      "average_score": null,
      "duration_seconds": null,
      "started_at": "2025-11-05T14:15:00Z",
      "completed_at": null,
      "overall_performance": null,
      "technical_rating": null,
      "communication_rating": null,
      "confidence_rating": null
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 20
}
```

**Example cURL:**
```bash
# Get all completed sessions
curl -X GET "http://localhost:8000/api/v1/interview/sessions?session_status=completed&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Get in-progress technical sessions
curl -X GET "http://localhost:8000/api/v1/interview/sessions?session_type=technical&session_status=in_progress" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 6. Get Session Details

**Endpoint:** `GET /{session_id}`

**Description:** Retrieve detailed information about a specific session including all Q&A pairs.

**Path Parameters:**
- `session_id` (integer): Interview session ID

**Response (200 OK):**
```json
{
  "session_id": 42,
  "session_type": "mixed",
  "job_role": "Software Engineer",
  "difficulty_level": "mid",
  "status": "completed",
  "started_at": "2025-11-06T10:30:00Z",
  "completed_at": "2025-11-06T10:50:00Z",
  "total_questions": 5,
  "questions_answered": 5,
  "duration_seconds": 1200,
  "average_scores": {
    "overall": 78.5,
    "relevance": 82.0,
    "completeness": 75.0,
    "clarity": 80.0,
    "technical_accuracy": 77.5,
    "communication": 78.0
  },
  "questions_and_answers": [
    {
      "question_number": 1,
      "question_text": "What is the difference between SQL and NoSQL databases?",
      "question_type": "technical",
      "user_answer": "SQL databases are relational...",
      "time_taken_seconds": 120,
      "scores": {
        "overall": 82,
        "relevance": 90,
        "completeness": 85,
        "clarity": 88,
        "technical_accuracy": 80,
        "communication": 87
      },
      "feedback": {
        "strengths": ["Clear explanation...", "Provided examples..."],
        "weaknesses": ["Could elaborate more..."],
        "missing_points": ["NoSQL types..."],
        "suggestions": ["Research different NoSQL types..."],
        "narrative": "Strong foundational answer..."
      },
      "sentiment": "positive"
    }
    // ... more Q&A pairs
  ],
  "feedback": {
    "strengths": ["Consistently strong performance...", "Excellent technical knowledge..."],
    "areas_to_improve": ["Provide more comprehensive answers..."],
    "recommended_resources": ["LeetCode for technical practice...", "STAR Method Guide..."],
    "preparation_tips": "You're on the right track!...",
    "practice_recommendations": "Practice 3-4 times per week..."
  }
}
```

**Error Responses:**
- `404 Not Found`: Session not found
- `401 Unauthorized`: Session doesn't belong to user

**Example cURL:**
```bash
curl -X GET http://localhost:8000/api/v1/interview/42 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 7. Get User Statistics

**Endpoint:** `GET /stats/overview`

**Description:** Retrieve user's overall interview statistics and performance overview.

**Response (200 OK):**
```json
{
  "total_sessions": 15,
  "total_questions_answered": 75,
  "average_overall_score": 78.5,
  "average_session_duration_minutes": 20.5,
  "performance_distribution": {
    "excellent": 3,
    "good": 8,
    "average": 3,
    "needs_improvement": 1
  },
  "favorite_job_role": "Software Engineer",
  "improvement_trend": "improving"
}
```

**Example cURL:**
```bash
curl -X GET http://localhost:8000/api/v1/interview/stats/overview \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 8. Delete Session

**Endpoint:** `DELETE /{session_id}`

**Description:** Permanently delete an interview session and all related data.

**Path Parameters:**
- `session_id` (integer): Interview session ID

**Response (200 OK):**
```json
{
  "message": "Interview session deleted successfully"
}
```

**Error Responses:**
- `404 Not Found`: Session not found
- `401 Unauthorized`: Session doesn't belong to user

**Example cURL:**
```bash
curl -X DELETE http://localhost:8000/api/v1/interview/42 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Data Models

### Request Models

#### InterviewStartRequest
```python
class InterviewStartRequest(BaseModel):
    session_type: SessionType = Field(
        default=SessionType.MIXED,
        description="Type of interview session"
    )
    job_role: str = Field(
        default="Software Engineer",
        description="Target job role"
    )
    difficulty_level: DifficultyLevel = Field(
        default=DifficultyLevel.MID,
        description="Interview difficulty level"
    )
    num_questions: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of questions (1-20)"
    )
    resume_id: Optional[int] = Field(
        None,
        description="Optional resume ID to tailor questions"
    )
```

#### AnswerSubmitRequest
```python
class AnswerSubmitRequest(BaseModel):
    session_id: int = Field(..., description="Interview session ID")
    question_id: int = Field(..., description="Question ID from question bank")
    answer: str = Field(
        ..., 
        min_length=10, 
        description="The candidate's answer (min 10 chars)"
    )
    time_taken_seconds: Optional[int] = Field(
        None, 
        description="Time taken to answer in seconds"
    )
```

### Response Models

#### QuestionResponse
```python
class QuestionResponse(BaseModel):
    question_number: int = Field(..., description="Question number in session")
    total_questions: int = Field(..., description="Total questions in session")
    question_id: int = Field(..., description="Question ID from database")
    question_text: str = Field(..., description="The question text")
    question_type: str = Field(..., description="Type of question")
    category: Optional[str] = Field(None, description="Question category")
    difficulty: str = Field(..., description="Difficulty level")
```

#### AnswerScores
```python
class AnswerScores(BaseModel):
    overall: float = Field(..., ge=0, le=100, description="Overall score (0-100)")
    relevance: float = Field(..., ge=0, le=100, description="Relevance to question")
    completeness: float = Field(..., ge=0, le=100, description="Answer completeness")
    clarity: float = Field(..., ge=0, le=100, description="Communication clarity")
    technical_accuracy: float = Field(..., ge=0, le=100, description="Technical correctness")
    communication: float = Field(..., ge=0, le=100, description="Communication quality")
```

#### AnswerFeedback
```python
class AnswerFeedback(BaseModel):
    strengths: List[str] = Field(..., description="What was done well")
    weaknesses: List[str] = Field(..., description="Areas that need improvement")
    missing_points: List[str] = Field(..., description="Key points that were missed")
    suggestions: List[str] = Field(..., description="Actionable improvement suggestions")
    narrative: str = Field(..., description="Narrative feedback summary")
```

#### AnswerResponse
```python
class AnswerResponse(BaseModel):
    answer_id: int = Field(..., description="Answer record ID")
    question_number: int = Field(..., description="Question number answered")
    question_text: str = Field(..., description="The question that was answered")
    your_answer: str = Field(..., description="The submitted answer")
    time_taken_seconds: int = Field(..., description="Time taken to answer")
    scores: AnswerScores = Field(..., description="Scoring breakdown")
    feedback: AnswerFeedback = Field(..., description="Detailed feedback")
    sentiment: str = Field(..., description="Detected sentiment")
    has_more_questions: bool = Field(..., description="Whether there are more questions")
```

#### SessionCompletionResponse
```python
class SessionCompletionResponse(BaseModel):
    session_id: int = Field(..., description="Session ID")
    completed: bool = Field(True, description="Whether session is completed")
    questions_answered: int = Field(..., description="Number of questions answered")
    total_time_seconds: int = Field(..., description="Total time for session")
    average_scores: SessionAverageScores = Field(..., description="Average scores")
    performance: str = Field(..., description="Overall performance rating")
    ratings: SessionRatings = Field(..., description="Performance ratings")
    feedback: SessionFeedbackDetail = Field(..., description="Detailed feedback")
    message: str = Field(..., description="Completion message")
```

---

**[Continue to Part 2 →](INTERVIEW_MODULE_PART2.md)**

---

## Quick Reference

### API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/start` | Start new interview session |
| GET | `/{id}/question` | Get next question |
| POST | `/answer` | Submit answer |
| POST | `/{id}/complete` | Complete session |
| GET | `/sessions` | List all sessions |
| GET | `/{id}` | Get session details |
| GET | `/stats/overview` | Get user statistics |
| DELETE | `/{id}` | Delete session |

### Key Metrics

- **Average Response Time**: < 2 seconds (with Groq AI)
- **Database Tables**: 5 tables
- **Pre-loaded Questions**: 40+ questions
- **Supported Job Roles**: 10+ roles
- **Interview Types**: 4 types
- **Difficulty Levels**: 3 levels
- **Scoring Dimensions**: 6 dimensions

---

*End of Part 1*
