# UtopiaHire Web Interface - API Architecture

**Version:** 1.0  
**Date:** October 14, 2025  
**Status:** Design Phase

---

## Overview

FastAPI-based REST API providing access to all 4 UtopiaHire modules through a modern web interface. Built for performance, security, and developer experience.

---

## Technology Stack

### Backend
- **Framework:** FastAPI 0.104+
- **Database:** PostgreSQL 16 (existing)
- **Authentication:** JWT tokens (python-jose)
- **File Upload:** python-multipart
- **Validation:** Pydantic v2
- **Async:** asyncio + aiofiles
- **CORS:** FastAPI CORS middleware

### Frontend (Next Phase)
- **Framework:** React 18 + Vite
- **Styling:** Tailwind CSS 3
- **Charts:** Chart.js + react-chartjs-2
- **HTTP Client:** axios
- **State:** React Context API
- **Routing:** React Router 6

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Settings and environment
│   │   ├── security.py         # JWT and password hashing
│   │   └── database.py         # Database connection pool
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Common dependencies
│   │   ├── resume.py           # Module 1 endpoints
│   │   ├── jobs.py             # Module 2 endpoints
│   │   ├── interview.py        # Module 3 endpoints
│   │   ├── footprint.py        # Module 4 endpoints
│   │   └── auth.py             # Authentication endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User models
│   │   ├── resume.py           # Resume request/response models
│   │   ├── job.py              # Job models
│   │   ├── interview.py        # Interview models
│   │   └── footprint.py        # Footprint models
│   └── services/
│       ├── __init__.py
│       ├── resume_service.py   # Business logic for Module 1
│       ├── job_service.py      # Business logic for Module 2
│       ├── interview_service.py # Business logic for Module 3
│       └── footprint_service.py # Business logic for Module 4
├── requirements.txt
└── Dockerfile
```

---

## API Endpoints

### Base URL: `http://localhost:8000/api/v1`

### 1. Authentication (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Create new user account | No |
| POST | `/auth/login` | Login and get JWT token | No |
| POST | `/auth/refresh` | Refresh JWT token | Yes |
| GET | `/auth/me` | Get current user info | Yes |
| PUT | `/auth/profile` | Update user profile | Yes |

**Request Examples:**

```json
// POST /auth/register
{
  "email": "developer@example.com",
  "password": "SecurePass123!",
  "full_name": "John Developer"
}

// POST /auth/login
{
  "email": "developer@example.com",
  "password": "SecurePass123!"
}

// Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "developer@example.com",
    "full_name": "John Developer"
  }
}
```

---

### 2. Resume Reviewer (`/resume`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/resume/upload` | Upload resume file | Yes |
| POST | `/resume/analyze` | Analyze resume (ATS score) | Yes |
| POST | `/resume/enhance` | Get enhancement suggestions | Yes |
| POST | `/resume/full` | Full analysis + enhancement | Yes |
| GET | `/resume/history` | Get user's resume history | Yes |
| DELETE | `/resume/{id}` | Delete resume | Yes |

**Request Examples:**

```python
# POST /resume/upload (multipart/form-data)
# Files: file (PDF/DOCX)

# POST /resume/analyze
{
  "resume_id": 123,
  "target_role": "Software Engineer"  # optional
}

# Response
{
  "resume_id": 123,
  "ats_score": 85,
  "sections_found": ["contact", "experience", "education", "skills"],
  "missing_sections": ["projects"],
  "keyword_analysis": {
    "found": ["Python", "JavaScript", "React"],
    "missing": ["Docker", "Kubernetes"]
  },
  "recommendations": [
    "Add a Projects section to showcase your work",
    "Include Docker and Kubernetes in your skills"
  ]
}
```

---

### 3. Job Matcher (`/jobs`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/jobs/scrape` | Scrape jobs from APIs | Yes |
| POST | `/jobs/match` | Match resume to jobs | Yes |
| GET | `/jobs/list` | List all scraped jobs | Yes |
| GET | `/jobs/{id}` | Get single job details | Yes |
| GET | `/jobs/market` | Get market insights | Yes |
| POST | `/jobs/save` | Save job to favorites | Yes |

**Request Examples:**

```json
// POST /jobs/scrape
{
  "query": "Python Developer",
  "location": "Remote",
  "apis": ["serpapi", "jsearch"],  // optional, default: all
  "max_results": 50  // optional, default: 30
}

// Response
{
  "jobs_scraped": 47,
  "success_rate": 0.94,
  "sources": {
    "serpapi": 25,
    "jsearch": 22
  },
  "duration_seconds": 12.5
}

// POST /jobs/match
{
  "resume_id": 123,
  "job_query": "Software Engineer",
  "location": "USA"
}

// Response
{
  "matches": [
    {
      "job_id": 456,
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "Remote",
      "match_score": 92,
      "matching_skills": ["Python", "FastAPI", "PostgreSQL"],
      "missing_skills": ["Kubernetes"],
      "salary_range": "$120k - $150k",
      "apply_url": "https://..."
    }
  ],
  "total_jobs": 47,
  "avg_match_score": 78
}
```

---

### 4. Interview Simulator (`/interview`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/interview/start` | Start new interview session | Yes |
| GET | `/interview/questions` | Get questions for session | Yes |
| POST | `/interview/submit` | Submit answer for analysis | Yes |
| GET | `/interview/feedback` | Get AI feedback for answer | Yes |
| GET | `/interview/history` | Get past interview sessions | Yes |
| GET | `/interview/stats` | Get performance statistics | Yes |

**Request Examples:**

```json
// POST /interview/start
{
  "role": "Software Engineer",
  "difficulty": "medium",  // easy, medium, hard
  "num_questions": 5  // optional, default: 5
}

// Response
{
  "session_id": 789,
  "role": "Software Engineer",
  "num_questions": 5,
  "started_at": "2025-10-14T10:30:00Z"
}

// POST /interview/submit
{
  "session_id": 789,
  "question_id": 12,
  "answer": "I would use a hash map to solve this problem..."
}

// Response
{
  "question_id": 12,
  "scores": {
    "relevance": 85,
    "completeness": 78,
    "clarity": 90,
    "technical_accuracy": 82,
    "communication": 88
  },
  "overall_score": 85,
  "strengths": ["Clear explanation", "Good example usage"],
  "improvements": ["Could mention time complexity"],
  "ai_feedback": "Your answer demonstrates solid understanding..."
}
```

---

### 5. Footprint Scanner (`/footprint`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/footprint/scan` | Scan GitHub/SO profiles | Yes |
| GET | `/footprint/view` | View current footprint | Yes |
| GET | `/footprint/trends` | Get historical trends | Yes |
| GET | `/footprint/insights` | Get personalized insights | Yes |
| PUT | `/footprint/profiles` | Update profile links | Yes |

**Request Examples:**

```json
// POST /footprint/scan
{
  "github_username": "octocat",  // optional
  "stackoverflow_id": 22656  // optional
}

// Response
{
  "scan_id": 999,
  "overall_score": 64,
  "performance_level": "AVERAGE",
  "percentile": 43,
  "platforms": {
    "github": {
      "score": 43,
      "username": "octocat",
      "repositories": 8,
      "total_stars": 19841,
      "followers": 3938
    },
    "stackoverflow": {
      "score": 97,
      "reputation": 1518237,
      "gold_badges": 892,
      "silver_badges": 9304
    }
  },
  "dimensions": {
    "visibility": 100,
    "activity": 50,
    "impact": 97,
    "expertise": 72
  },
  "insights": {
    "strengths": [
      "World-class Stack Overflow presence",
      "Massive repository impact"
    ],
    "recommendations": [
      "Increase recent GitHub activity"
    ]
  },
  "scanned_at": "2025-10-14T10:30:00Z"
}

// GET /footprint/trends?limit=10
// Response
{
  "trends": [
    {
      "date": "2025-10-14",
      "overall_score": 64,
      "github_score": 43,
      "stackoverflow_score": 97,
      "change": 0
    },
    {
      "date": "2025-10-07",
      "overall_score": 64,
      "github_score": 43,
      "stackoverflow_score": 97,
      "change": 0
    }
  ],
  "total_scans": 2
}
```

---

### 6. Health Check (`/health`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | API health status | No |
| GET | `/health/db` | Database connection | No |

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-14T10:30:00Z",
  "database": "connected",
  "services": {
    "resume_parser": true,
    "job_scraper": true,
    "interview_analyzer": true,
    "footprint_scanner": true
  }
}
```

---

## Authentication Flow

### JWT Token-Based Authentication

1. **Registration:** User creates account → Receives JWT token
2. **Login:** User logs in → Receives JWT token
3. **API Requests:** Include token in `Authorization: Bearer <token>` header
4. **Token Refresh:** Before expiry, refresh token to get new one
5. **Token Expiry:** 24 hours (configurable)

### Security Features
- Passwords hashed with bcrypt
- JWT signed with HS256 algorithm
- HTTPS only in production
- CORS configured for frontend domain
- Rate limiting on auth endpoints
- SQL injection prevention via parameterized queries

---

## Error Handling

### Standard Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | External API down |

---

## Rate Limiting

### Limits per User

| Endpoint Category | Rate Limit |
|------------------|------------|
| Authentication | 5 requests/minute |
| Resume Analysis | 10 requests/hour |
| Job Scraping | 5 requests/hour |
| Interview Sessions | 20 requests/hour |
| Footprint Scanning | 10 requests/hour |

---

## File Upload

### Resume Upload Specifications

- **Max File Size:** 10 MB
- **Allowed Types:** PDF, DOCX, DOC
- **Storage:** Temporary (processed and deleted)
- **Virus Scanning:** Planned for production

---

## Database Connection

### Connection Pool
- **Min Connections:** 5
- **Max Connections:** 20
- **Timeout:** 30 seconds
- **Retry Logic:** 3 attempts with exponential backoff

### Existing Tables Used
- `users` (Module 1)
- `resumes`, `resume_analysis` (Module 1)
- `jobs`, `job_matches` (Module 2)
- `interview_questions`, `interview_sessions`, `interview_answers` (Module 3)
- `user_profiles`, `github_data`, `stackoverflow_data`, `footprint_scores`, `footprint_history` (Module 4)

---

## Deployment

### Development
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```bash
docker build -t utopiahire-api .
docker run -p 8000:8000 utopiahire-api
```

---

## Testing Strategy

### Unit Tests
- Test each endpoint independently
- Mock database and external APIs
- Validate request/response schemas

### Integration Tests
- Test full workflow for each module
- Use test database
- Validate authentication flow

### Load Tests
- Test with 100 concurrent users
- Validate rate limiting
- Check database connection pool

---

## Future Enhancements

### Phase 2 (Weeks 3-4)
- [ ] WebSocket support for real-time interview feedback
- [ ] Background job processing (Celery + Redis)
- [ ] File storage (S3 for resumes)
- [ ] Email notifications
- [ ] Admin dashboard

### Phase 3 (Month 2)
- [ ] GraphQL API
- [ ] API versioning (v2)
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] OAuth2 integration (Google, LinkedIn)

---

## Performance Goals

| Metric | Target | Current |
|--------|--------|---------|
| API Response Time | < 200ms | TBD |
| Resume Analysis | < 3 seconds | ~2 seconds (CLI) |
| Job Scraping | < 15 seconds | ~10 seconds (CLI) |
| Interview Analysis | < 2 seconds | ~1 second (CLI) |
| Footprint Scan | < 10 seconds | ~5 seconds (CLI) |
| Concurrent Users | 100+ | TBD |
| Uptime | 99.9% | TBD |

---

## Documentation

### Auto-Generated API Docs
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## Contact & Support

**Developer:** Firas  
**Project:** UtopiaHire  
**Competition:** IEEE TSYP13 (2025)  
**Repository:** /home/firas/Utopia

---

**Last Updated:** October 14, 2025  
**Status:** ✅ Architecture Complete, Ready for Implementation
