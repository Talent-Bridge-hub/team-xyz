# CareerStar Backend API Documentation - Part 4
## System Operations, Deployment & Testing
---

## Table of Contents (Part 4)

14. [Health Checks & Monitoring](#health-checks--monitoring)
15. [API Quick Reference](#api-quick-reference)

---

## 14. Health Checks & Monitoring

### GET /health

**Basic health check endpoint**

Simple endpoint for load balancers and monitoring tools.

**Authentication:** Not required

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

---

### GET /api/v1/health

**Detailed system health check**

Comprehensive health information including service status.

**Authentication:** Not required

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-06T12:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": {
      "status": "healthy",
      "response_time_ms": 15,
      "connected": true
    },
    "groq_api": {
      "status": "healthy",
      "configured": true
    },
    "github_api": {
      "status": "healthy",
      "configured": true,
      "rate_limit_remaining": 4500
    },
    "stackoverflow_api": {
      "status": "healthy",
      "configured": true
    },
    "jsearch_api": {
      "status": "healthy",
      "configured": true
    }
  },
  "system": {
    "uptime_seconds": 86400,
    "memory_usage_mb": 256,
    "cpu_usage_percent": 12.5
  }
}
```

**Service Status Codes:**
- `healthy`: Service is operational
- `degraded`: Service is running but with issues
- `unhealthy`: Service is down or unreachable

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

---

### Response Time Monitoring

All API responses include a custom header for performance monitoring:

```
X-Process-Time: 0.142
```

This header indicates the server-side processing time in seconds.


## 15. API Quick Reference

### Complete Endpoint List (39 Endpoints)

#### Authentication API (6 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login user |
| GET | `/api/v1/auth/me` | Get current user |
| PUT | `/api/v1/auth/profile` | Update profile |
| POST | `/api/v1/auth/refresh` | Refresh token |
| DELETE | `/api/v1/auth/account` | Delete account |

#### Resume API (10 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/resumes/upload` | Upload resume |
| POST | `/api/v1/resumes/analyze` | Analyze resume |
| POST | `/api/v1/resumes/enhance` | Enhance resume |
| POST | `/api/v1/resumes/{id}/download-enhanced` | Download enhanced |
| GET | `/api/v1/resumes/list` | List resumes |
| GET | `/api/v1/resumes/{id}/download` | Download original |
| DELETE | `/api/v1/resumes/{id}` | Delete resume |
| GET | `/api/v1/resumes/templates` | List templates |
| GET | `/api/v1/resumes/templates/{id}/download` | Download template |
| POST | `/api/v1/resumes/generate-cover-letter` | Generate cover letter |

#### Jobs API (10 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/jobs/scrape` | Scrape jobs |
| POST | `/api/v1/jobs/match` | Match jobs with resume |
| GET | `/api/v1/jobs/list` | List jobs |
| POST | `/api/v1/jobs/search` | Search jobs |
| POST | `/api/v1/jobs/compatibility` | Analyze compatibility |
| GET | `/api/v1/jobs/{job_id}` | Get job details |
| POST | `/api/v1/jobs/{job_id}/save` | Save job |
| DELETE | `/api/v1/jobs/{job_id}/save` | Unsave job |
| GET | `/api/v1/jobs/saved` | Get saved jobs |
| GET | `/api/v1/jobs/insights` | Market insights |

#### Interview API (8 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/interview/start` | Start interview |
| GET | `/api/v1/interview/{id}/question` | Get next question |
| POST | `/api/v1/interview/answer` | Submit answer |
| POST | `/api/v1/interview/{id}/complete` | Complete session |
| GET | `/api/v1/interview/sessions` | List sessions |
| GET | `/api/v1/interview/{id}` | Get session details |
| GET | `/api/v1/interview/stats/overview` | Get statistics |
| DELETE | `/api/v1/interview/{id}` | Delete session |

#### Footprint API (5 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/footprint/scan` | Scan footprint |
| GET | `/api/v1/footprint/recommendations/{id}` | Get recommendations |
| GET | `/api/v1/footprint/history` | Get scan history |
| GET | `/api/v1/footprint/compare/{id1}/{id2}` | Compare scans |
| GET | `/api/v1/footprint/{id}` | Get scan details |

#### System Endpoints (2 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| GET | `/api/v1/health` | Detailed health check |

---

## Appendix A: Technology Stack

### Backend Framework
- **FastAPI 0.104+**: Modern async web framework
- **Uvicorn**: ASGI server
- **Python 3.10+**: Programming language

### Database
- **PostgreSQL 14+**: Primary database
- **SQLAlchemy**: ORM with async support
- **Alembic**: Database migrations

### Authentication & Security
- **JWT (PyJWT)**: Token-based authentication
- **Passlib**: Password hashing (bcrypt)
- **Python-Multipart**: File uploads

### AI & ML Services
- **Groq API**: AI-powered analysis (llama-3.3-70b-versatile)
- **HuggingFace**: Alternative ML models

### External APIs
- **GitHub REST API v3**: Repository analysis
- **Stack Exchange API 2.3**: StackOverflow data
- **JSearch API**: Job scraping

### File Processing
- **PyPDF2**: PDF parsing
- **python-docx**: Word document processing
- **ReportLab**: PDF generation

### Data Validation
- **Pydantic v2**: Request/response validation
- **Email-Validator**: Email validation

### HTTP Client
- **HTTPX**: Async HTTP client
- **Requests**: Synchronous HTTP client

---


© 2025 CareerStar. All rights reserved.
