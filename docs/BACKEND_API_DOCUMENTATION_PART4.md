# UtopiaHire Backend API Documentation - Part 4
## System Operations, Deployment & Testing

> **Generated:** November 6, 2025  
> **Version:** 1.0.0  
> **Base URL:** `http://localhost:8000/api/v1`

---

## Table of Contents (Part 4)

14. [Health Checks & Monitoring](#health-checks--monitoring)
15. [Database Schema](#database-schema)
16. [Environment Configuration](#environment-configuration)
17. [Deployment Guide](#deployment-guide)
18. [Testing](#testing)
19. [Troubleshooting](#troubleshooting)
20. [API Quick Reference](#api-quick-reference)

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

---

## 15. Database Schema

### Overview

**Database:** PostgreSQL 14+  
**ORM:** SQLAlchemy with async support  
**Migrations:** Alembic

### Core Tables

#### users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

#### resumes
```sql
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    file_type VARCHAR(50),
    parsed_text TEXT,
    parsed_data JSONB,
    last_analyzed_at TIMESTAMP,
    last_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resumes_user_id ON resumes(user_id);
CREATE INDEX idx_resumes_created_at ON resumes(created_at);
CREATE INDEX idx_resumes_parsed_data ON resumes USING GIN(parsed_data);
```

#### resume_analyses
```sql
CREATE TABLE resume_analyses (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    ats_score JSONB NOT NULL,
    section_scores JSONB,
    strengths JSONB,
    weaknesses JSONB,
    recommendations JSONB,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resume_analyses_resume_id ON resume_analyses(resume_id);
CREATE INDEX idx_resume_analyses_user_id ON resume_analyses(user_id);
```

#### resume_enhancements
```sql
CREATE TABLE resume_enhancements (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    enhancement_type VARCHAR(50),
    suggestions JSONB NOT NULL,
    applied_suggestions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resume_enhancements_resume_id ON resume_enhancements(resume_id);
```

#### jobs
```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    location VARCHAR(255),
    job_type VARCHAR(50),
    experience_level VARCHAR(50),
    description TEXT,
    requirements JSONB,
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(10),
    remote_allowed BOOLEAN DEFAULT FALSE,
    skills JSONB,
    source VARCHAR(100),
    source_job_id VARCHAR(255),
    apply_url VARCHAR(500),
    posted_date TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_job_type ON jobs(job_type);
CREATE INDEX idx_jobs_experience_level ON jobs(experience_level);
CREATE INDEX idx_jobs_skills ON jobs USING GIN(skills);
CREATE INDEX idx_jobs_posted_date ON jobs(posted_date);
CREATE INDEX idx_jobs_source_job_id ON jobs(source, source_job_id);
```

#### saved_jobs
```sql
CREATE TABLE saved_jobs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, job_id)
);

CREATE INDEX idx_saved_jobs_user_id ON saved_jobs(user_id);
CREATE INDEX idx_saved_jobs_job_id ON saved_jobs(job_id);
```

#### interview_sessions
```sql
CREATE TABLE interview_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_type VARCHAR(50) NOT NULL,
    job_role VARCHAR(255),
    difficulty_level VARCHAR(50),
    total_questions INTEGER,
    questions_answered INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'in_progress',
    average_score FLOAT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    overall_performance VARCHAR(50),
    technical_rating INTEGER,
    communication_rating INTEGER,
    confidence_rating INTEGER,
    feedback JSONB
);

CREATE INDEX idx_interview_sessions_user_id ON interview_sessions(user_id);
CREATE INDEX idx_interview_sessions_status ON interview_sessions(status);
```

#### interview_questions
```sql
CREATE TABLE interview_questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50),
    category VARCHAR(100),
    difficulty VARCHAR(50),
    ideal_answer TEXT,
    keywords JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_interview_questions_type ON interview_questions(question_type);
CREATE INDEX idx_interview_questions_difficulty ON interview_questions(difficulty);
```

#### interview_answers
```sql
CREATE TABLE interview_answers (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES interview_sessions(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES interview_questions(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    time_taken_seconds INTEGER,
    scores JSONB NOT NULL,
    feedback JSONB,
    sentiment VARCHAR(50),
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_interview_answers_session_id ON interview_answers(session_id);
CREATE INDEX idx_interview_answers_user_id ON interview_answers(user_id);
```

#### footprint_scans
```sql
CREATE TABLE footprint_scans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    github_username VARCHAR(255),
    stackoverflow_id INTEGER,
    github_analysis JSONB,
    stackoverflow_analysis JSONB,
    privacy_report JSONB,
    overall_visibility_score FLOAT,
    professional_score FLOAT,
    visibility_score FLOAT,
    activity_score FLOAT,
    impact_score FLOAT,
    expertise_score FLOAT,
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_footprint_scans_user_id ON footprint_scans(user_id);
CREATE INDEX idx_footprint_scans_scanned_at ON footprint_scans(scanned_at);
```

---

## 16. Environment Configuration

### Required Environment Variables

Create a `.env` file in the project root:

```bash
# Application Settings
PROJECT_NAME="UtopiaHire API"
VERSION="1.0.0"
API_V1_PREFIX="/api/v1"
DEBUG=false

# Server Configuration
HOST="0.0.0.0"
PORT=8000

# Database Configuration
DATABASE_URL="postgresql://user:password@localhost:5432/utopiahire"
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10

# Security
SECRET_KEY="your-super-secret-key-here-min-32-chars"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS Configuration (comma-separated)
BACKEND_CORS_ORIGINS="http://localhost:3000,http://localhost:8080"

# External API Keys
GROQ_API_KEY="your-groq-api-key"
GROQ_MODEL="llama-3.3-70b-versatile"

GITHUB_TOKEN="your-github-personal-access-token"

STACKOVERFLOW_KEY="your-stackoverflow-api-key"

JSEARCH_API_KEY="your-jsearch-api-key"
JSEARCH_API_HOST="jsearch.p.rapidapi.com"

# File Upload Configuration
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR="/home/firas/Utopia/data/resumes"
ALLOWED_EXTENSIONS=".pdf,.doc,.docx"

# Rate Limiting (requests per time window)
RATE_LIMIT_AUTH=5/minute
RATE_LIMIT_RESUME=10/hour
RATE_LIMIT_JOBS_SCRAPE=5/hour
RATE_LIMIT_JOBS_MATCH=20/hour
RATE_LIMIT_INTERVIEW=20/hour
RATE_LIMIT_FOOTPRINT=10/hour

# External Service URLs
JSEARCH_API_URL="https://jsearch.p.rapidapi.com/search"

# Logging
LOG_LEVEL="INFO"
LOG_FORMAT="json"
```

### Configuration Validation

The application validates all configuration on startup:

```python
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    # All settings with type validation
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
        return v
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters")
        return v
    
    class Config:
        env_file = ".env"
```

---

## 17. Deployment Guide

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Git
- Domain name (for production)
- SSL certificate (for HTTPS)

### Local Development Setup

**1. Clone Repository:**
```bash
git clone https://github.com/your-org/utopiahire-backend.git
cd utopiahire-backend
```

**2. Create Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Setup Database:**
```bash
# Create database
createdb utopiahire

# Run migrations
alembic upgrade head
```

**5. Configure Environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

**6. Run Development Server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**7. Access API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### Production Deployment (Ubuntu 22.04)

**1. Install System Dependencies:**
```bash
sudo apt update
sudo apt install -y python3.10 python3-pip python3-venv postgresql nginx certbot
```

**2. Setup PostgreSQL:**
```bash
sudo -u postgres psql
CREATE DATABASE utopiahire;
CREATE USER utopiahire_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE utopiahire TO utopiahire_user;
\q
```

**3. Clone and Setup Application:**
```bash
cd /var/www
sudo git clone https://github.com/your-org/utopiahire-backend.git
sudo chown -R $USER:$USER utopiahire-backend
cd utopiahire-backend

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**4. Configure Environment:**
```bash
nano .env
# Set production values
# DEBUG=false
# DATABASE_URL=postgresql://utopiahire_user:secure_password@localhost/utopiahire
```

**5. Run Database Migrations:**
```bash
alembic upgrade head
```

**6. Create Systemd Service:**
```bash
sudo nano /etc/systemd/system/utopiahire.service
```

```ini
[Unit]
Description=UtopiaHire FastAPI Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/utopiahire-backend
Environment="PATH=/var/www/utopiahire-backend/venv/bin"
ExecStart=/var/www/utopiahire-backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

[Install]
WantedBy=multi-user.target
```

**7. Start Service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable utopiahire
sudo systemctl start utopiahire
sudo systemctl status utopiahire
```

**8. Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/utopiahire
```

```nginx
server {
    listen 80;
    server_name api.utopiahire.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Increase upload size for resume uploads
    client_max_body_size 10M;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/utopiahire /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**9. Setup SSL with Let's Encrypt:**
```bash
sudo certbot --nginx -d api.utopiahire.com
```

**10. Setup Firewall:**
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow 22
sudo ufw enable
```

---

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create upload directory
RUN mkdir -p /app/data/resumes

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: utopiahire
      POSTGRES_USER: utopiahire_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: .
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://utopiahire_user:secure_password@db:5432/utopiahire
      SECRET_KEY: ${SECRET_KEY}
      GROQ_API_KEY: ${GROQ_API_KEY}
      GITHUB_TOKEN: ${GITHUB_TOKEN}
      STACKOVERFLOW_KEY: ${STACKOVERFLOW_KEY}
      JSEARCH_API_KEY: ${JSEARCH_API_KEY}
    volumes:
      - ./data:/app/data
    ports:
      - "8000:8000"

volumes:
  postgres_data:
```

**Build and Run:**
```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

---

## 18. Testing

### Running Tests

**Install Test Dependencies:**
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

**Run All Tests:**
```bash
pytest
```

**Run with Coverage:**
```bash
pytest --cov=app --cov-report=html
```

**Run Specific Test File:**
```bash
pytest tests/test_auth.py
```

### Test Examples

**Authentication Tests (`tests/test_auth.py`):**
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "SecurePass123!",
                "name": "Test User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["user"]["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Register first
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "SecurePass123!",
                "name": "Test User"
            }
        )
        
        # Login
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": "test@example.com",
                "password": "SecurePass123!"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
```

**Resume Tests (`tests/test_resume.py`):**
```python
@pytest.mark.asyncio
async def test_upload_resume():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Login first
        login_response = await client.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "SecurePass123!"}
        )
        token = login_response.json()["access_token"]
        
        # Upload resume
        with open("tests/fixtures/sample_resume.pdf", "rb") as f:
            response = await client.post(
                "/api/v1/resumes/upload",
                files={"file": ("resume.pdf", f, "application/pdf")},
                headers={"Authorization": f"Bearer {token}"}
            )
        
        assert response.status_code == 201
        data = response.json()
        assert "resume_id" in data
        assert data["file_name"] == "resume.pdf"
```

**cURL Testing:**
```bash
# Register user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=SecurePass123!"

# Get current user (replace TOKEN)
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer TOKEN"
```

---

## 19. Troubleshooting

### Common Issues

#### Issue 1: Database Connection Error

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection string in .env
# DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Test connection
psql -U utopiahire_user -d utopiahire -h localhost
```

#### Issue 2: JWT Token Expired

**Error:**
```json
{
  "detail": "Could not validate credentials"
}
```

**Solutions:**
- Refresh token using `/auth/refresh` endpoint
- Increase `ACCESS_TOKEN_EXPIRE_MINUTES` in .env
- Clear browser localStorage and login again

#### Issue 3: File Upload Too Large

**Error:**
```json
{
  "detail": "File size exceeds maximum allowed (10MB)"
}
```

**Solutions:**
- Check file size before upload
- Increase `MAX_UPLOAD_SIZE` in .env
- Configure Nginx `client_max_body_size`

#### Issue 4: Rate Limit Exceeded

**Error:**
```json
{
  "error": "Rate limit exceeded. Try again in 3600 seconds."
}
```

**Solutions:**
- Wait for rate limit window to reset
- Check `X-RateLimit-Reset` header
- Request rate limit increase for production

#### Issue 5: External API Errors

**Groq API Error:**
```json
{
  "detail": "AI service temporarily unavailable"
}
```

**Solutions:**
- Check `GROQ_API_KEY` is valid
- Verify API quota not exceeded
- Fallback to rule-based analysis if available

**GitHub API Error:**
```json
{
  "detail": "GitHub API rate limit exceeded"
}
```

**Solutions:**
- Wait for rate limit reset (check `X-RateLimit-Reset` header)
- Use authenticated requests with `GITHUB_TOKEN`
- GitHub allows 5000 req/hr with authentication vs 60 req/hr without

---

## 20. API Quick Reference

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

### HTTP Status Codes Reference

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request successful, no response body |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

---

### Common Response Headers

```
Content-Type: application/json
X-Process-Time: 0.142
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1730804400
Access-Control-Allow-Origin: *
```

---

### Authentication Header Format

All authenticated endpoints require:

```
Authorization: Bearer <JWT_TOKEN>
```

---

### Pagination Parameters

Standard pagination for list endpoints:

```
?page=1&page_size=20
```

Response includes:
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "total_pages": 8
}
```

---

### Error Response Format

All errors follow this structure:

```json
{
  "detail": "Error message here",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2025-11-06T12:00:00Z"
}
```

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

## Appendix B: API Versioning

**Current Version:** v1  
**Base Path:** `/api/v1`

### Version Strategy

- **Major versions** (v1, v2): Breaking changes
- **Minor versions**: New features (backward compatible)
- **Patch versions**: Bug fixes

### Deprecation Policy

1. New version released with deprecation notice
2. Old version supported for 6 months
3. Final deprecation warning 1 month before removal
4. Old version removed

---

## Appendix C: Support & Resources

### Documentation
- API Documentation: `/docs` (Swagger UI)
- Alternative Docs: `/redoc` (ReDoc)
- OpenAPI Schema: `/openapi.json`

### Contact
- Email: support@utopiahire.com
- GitHub Issues: https://github.com/your-org/utopiahire-backend/issues
- Discord: https://discord.gg/utopiahire

### Additional Resources
- GitHub Repository: https://github.com/your-org/utopiahire-backend
- Frontend Repository: https://github.com/your-org/utopiahire-frontend
- Changelog: `/CHANGELOG.md`
- Contributing Guide: `/CONTRIBUTING.md`

---

**End of Complete UtopiaHire Backend API Documentation**

**Version:** 1.0.0  
**Last Updated:** November 6, 2025  
**Total Endpoints:** 39  
**API Status:** ✅ Production Ready  
**Documentation Parts:** 1-4 (Complete)

© 2025 UtopiaHire. All rights reserved.
