# UtopiaHire Backend API Documentation - Part 1
## Complete API Reference Guide

---

## Table of Contents (Part 1)

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Authentication System](#authentication-system)
4. [Common Patterns](#common-patterns)
5. [Error Handling](#error-handling)
6. [Authentication API](#authentication-api)

---

## 1. Overview

### Platform Description

**CareerStar** is an AI-powered career platform designed for developers and tech professionals in MENA and Sub-Saharan Africa. The backend provides RESTful APIs for:

- **User Authentication & Management**
- **Resume Analysis & Enhancement**
- **Job Matching & Recommendations**
- **AI Interview Simulation**
- **Digital Footprint Scanning**

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI 0.104+ | High-performance async API framework |
| **Database** | PostgreSQL 14+ | Relational database with JSONB support |
| **Authentication** | JWT (HS256) | Stateless token-based authentication |
| **Validation** | Pydantic v2 | Request/response data validation |
| **AI/ML** | Groq API, HuggingFace | AI-powered analysis and recommendations |
| **External APIs** | GitHub API v3, Stack Exchange API 2.3, JSearch API | Data aggregation |
| **CORS** | FastAPI CORSMiddleware | Cross-origin resource sharing |
| **Server** | Uvicorn | ASGI server |

### Key Features

1. **Secure Authentication**: JWT-based with bcrypt password hashing
2. **AI-Powered Analysis**: Resume scoring, interview feedback, job matching
3. **Real-time Job Scraping**: Integration with multiple job APIs
4. **Digital Footprint**: GitHub and StackOverflow analysis
5. **Comprehensive Error Handling**: Detailed error responses
6. **Rate Limiting**: Protection against API abuse
7. **Request Validation**: Automatic Pydantic validation

---

## 2. Architecture

### System Design

```
┌──────────────┐
│   Frontend   │ (React + TypeScript)
│  (Port 5173) │
└──────┬───────┘
       │ HTTP/REST
       │ JSON
       ▼
┌──────────────────────────────────────┐
│        FastAPI Backend               │
│         (Port 8000)                  │
├──────────────────────────────────────┤
│  ┌────────────────────────────────┐  │
│  │     API Router Layer           │  │
│  │  - Auth, Resume, Jobs,         │  │
│  │  - Interview, Footprint        │  │
│  └────────────┬───────────────────┘  │
│               │                       │
│  ┌────────────▼───────────────────┐  │
│  │    Business Logic Layer        │  │
│  │  - Validators, Analyzers,      │  │
│  │  - Matchers, Simulators        │  │
│  └────────────┬───────────────────┘  │
│               │                       │
│  ┌────────────▼───────────────────┐  │
│  │      Database Layer            │  │
│  │  - PostgreSQL Connection Pool  │  │
│  │  - Query Execution             │  │
│  └────────────┬───────────────────┘  │
└───────────────┼───────────────────────┘
                │
     ┌──────────┴──────────┐
     │                     │
┌────▼────────┐   ┌────────▼─────────┐
│ PostgreSQL  │   │ External APIs    │
│  Database   │   │ - GitHub         │
│             │   │ - StackOverflow  │
│             │   │ - JSearch        │
│             │   │ - Groq AI        │
└─────────────┘   └──────────────────┘
```

### Module Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── api/                       # API endpoint routers
│   │   ├── auth.py               # Authentication endpoints
│   │   ├── resume.py             # Resume management endpoints
│   │   ├── jobs.py               # Job matching endpoints
│   │   ├── interview.py          # Interview simulator endpoints
│   │   ├── footprint.py          # Footprint scanner endpoints
│   │   └── deps.py               # Shared dependencies
│   ├── core/                      # Core functionality
│   │   ├── config.py             # Configuration settings
│   │   ├── database.py           # Database connection
│   │   └── security.py           # JWT & password handling
│   └── models/                    # Pydantic data models
│       ├── user.py               # User models
│       ├── resume.py             # Resume models
│       ├── job.py                # Job models
│       ├── interview.py          # Interview models
│       └── footprint.py          # Footprint models
├── utils/                         # Utility modules
│   ├── resume_parser.py          # PDF/DOCX parsing
│   ├── resume_analyzer.py        # Resume analysis
│   ├── job_matcher.py            # Job matching algorithm
│   ├── interview_simulator.py    # Interview logic
│   ├── github_analyzer.py        # GitHub API integration
│   └── groq_*.py                 # AI integrations
└── migrations/                    # Database migrations
```

### Database Schema Overview

**Core Tables:**

1. **users** - User accounts and authentication
2. **resumes** - Uploaded resume files and parsed data
3. **jobs** - Job postings from external APIs
4. **interview_sessions** - Interview session metadata
5. **interview_questions** - Session-specific questions
6. **interview_answers** - User answers with scores
7. **footprint_scans** - Digital footprint analysis results
8. **saved_jobs** - User-saved job bookmarks

**Key Relationships:**

```
users (1) ──< (N) resumes
users (1) ──< (N) interview_sessions
users (1) ──< (N) footprint_scans
users (1) ──< (N) saved_jobs
interview_sessions (1) ──< (N) interview_questions
interview_questions (1) ──< (1) interview_answers
```

---

## 3. Authentication System

### JWT Token Structure

**Algorithm:** HS256  
**Token Type:** Bearer  
**Expiration:** 24 hours (configurable)

**Token Payload:**
```json
{
  "sub": "123",           // User ID
  "email": "user@example.com",
  "exp": 1730886400,      // Expiration timestamp
  "iat": 1730800000       // Issued at timestamp
}
```

### Authentication Flow

```
┌──────────┐                          ┌──────────┐
│  Client  │                          │  Server  │
└────┬─────┘                          └────┬─────┘
     │                                     │
     │  POST /api/v1/auth/register         │
     │  { email, password, full_name }     │
     ├────────────────────────────────────>│
     │                                     │
     │  1. Validate input                  │
     │  2. Hash password (bcrypt)          │
     │  3. Insert user in DB               │
     │  4. Generate JWT token              │
     │                                     │
     │  200 OK                             │
     │  { access_token, user }             │
     │<────────────────────────────────────┤
     │                                     │
     │  Store token in localStorage        │
     │                                     │
     │  POST /api/v1/resumes/upload        │
     │  Authorization: Bearer <token>      │
     ├────────────────────────────────────>│
     │                                     │
     │  1. Extract token from header       │
     │  2. Verify signature                │
     │  3. Decode payload                  │
     │  4. Fetch user from DB              │
     │  5. Validate user exists            │
     │  6. Execute protected operation     │
     │                                     │
     │  200 OK                             │
     │  { ... response data ... }          │
     │<────────────────────────────────────┤
     │                                     │
```

### Password Security

- **Hashing Algorithm:** bcrypt with salt
- **Rounds:** 12 (configurable)
- **Validation:** Minimum 8 characters, at least 1 digit and 1 uppercase letter

### Token Refresh Strategy

- **Current:** No refresh tokens (re-login required after expiration)
- **Recommended:** Implement refresh token endpoint for production

---

## 4. Common Patterns

### Request/Response Format

**Standard Success Response:**
```json
{
  "data": { ... },
  "message": "Operation successful",
  "timestamp": "2025-11-06T10:30:00Z"
}
```

**Standard Error Response:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { ... }
  }
}
```

### Pagination Pattern

All list endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Response Structure:**
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "total_pages": 8
}
```

### File Upload Pattern

**Content-Type:** `multipart/form-data`  
**Max Size:** 10MB  
**Allowed Types:** PDF, DOCX, DOC

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/v1/resumes/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@resume.pdf"
```

### Authentication Header

All protected endpoints require:

```
Authorization: Bearer <jwt_token>
```

---

## 5. Error Handling

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| **200** | OK | Successful GET, PUT, DELETE |
| **201** | Created | Successful POST (resource created) |
| **400** | Bad Request | Invalid input, validation errors |
| **401** | Unauthorized | Missing or invalid authentication |
| **403** | Forbidden | Valid auth but insufficient permissions |
| **404** | Not Found | Resource doesn't exist |
| **422** | Unprocessable Entity | Validation errors (Pydantic) |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Internal Server Error | Unexpected server errors |
| **503** | Service Unavailable | External API failures |

### Error Response Examples

**Validation Error (400):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "loc": ["body", "email"],
        "msg": "value is not a valid email address",
        "type": "value_error.email"
      }
    ]
  }
}
```

**Authentication Error (401):**
```json
{
  "detail": "Invalid authentication credentials"
}
```

**Not Found Error (404):**
```json
{
  "detail": "Resume with ID 123 not found"
}
```

**Rate Limit Error (429):**
```json
{
  "error": "Rate limit exceeded. Try again in 60 seconds."
}
```

**Server Error (500):**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "details": "Database connection timeout"
  }
}
```

---

## 6. Authentication API

**Base Path:** `/api/v1/auth`  
**Tag:** `Authentication`

### Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Create new user account | ❌ |
| POST | `/login` | Login with credentials | ❌ |
| GET | `/me` | Get current user info | ✅ |
| PUT | `/profile` | Update user profile | ✅ |
| POST | `/refresh` | Refresh JWT token | ✅ |
| DELETE | `/account` | Delete user account | ✅ |

---

### POST /api/v1/auth/register

**Register a new user account**

Creates a new user with hashed password and returns JWT token.

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe"
}
```

**Validation Rules:**
- `email`: Valid email format, unique in database
- `password`: Minimum 8 characters, contains digit and uppercase letter
- `full_name`: Non-empty string

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "created_at": "2025-11-06T10:00:00Z"
  }
}
```

**Error Responses:**

**400 - Email Already Registered:**
```json
{
  "detail": "Email already registered"
}
```

**400 - Password Too Weak:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "loc": ["body", "password"],
        "msg": "Password must be at least 8 characters",
        "type": "value_error"
      }
    ]
  }
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe"
  }'
```

**Example Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsImV4cCI6MTczMDg4NjQwMH0.xYz...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "created_at": "2025-11-06T10:00:00.123456Z"
  }
}
```

---

### POST /api/v1/auth/login

**Login with email and password**

Authenticates user and returns JWT token. Uses OAuth2 password flow.

**Request Body (Form Data):**
```
username=john.doe@example.com
password=SecurePass123
```

**Note:** OAuth2 spec requires field name `username` (use email as value)

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "created_at": "2025-11-06T10:00:00Z"
  }
}
```

**Error Responses:**

**401 - Invalid Credentials:**
```json
{
  "detail": "Incorrect email or password"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john.doe@example.com&password=SecurePass123"
```

**Frontend Integration (JavaScript):**
```javascript
const login = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append('username', email);  // OAuth2 requires 'username'
  formData.append('password', password);
  
  const response = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData
  });
  
  if (!response.ok) {
    throw new Error('Login failed');
  }
  
  const data = await response.json();
  
  // Store token
  localStorage.setItem('access_token', data.access_token);
  
  return data;
};
```

---

### GET /api/v1/auth/me

**Get current authenticated user information**

Returns profile information for the authenticated user.

**Authentication:** Required (Bearer token)

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "full_name": "John Doe",
  "created_at": "2025-11-06T10:00:00Z"
}
```

**Error Responses:**

**401 - Unauthorized:**
```json
{
  "detail": "Invalid authentication credentials"
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### PUT /api/v1/auth/profile

**Update user profile**

Updates user information. Can update email, full name, or password.

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "full_name": "John Updated Doe",
  "email": "john.new@example.com",
  "current_password": "SecurePass123",
  "new_password": "NewSecurePass456"
}
```

**Note:** All fields are optional. To change password, both `current_password` and `new_password` are required.

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "john.new@example.com",
  "full_name": "John Updated Doe",
  "created_at": "2025-11-06T10:00:00Z",
  "updated_at": "2025-11-06T12:30:00Z"
}
```

**Error Responses:**

**400 - Email Already in Use:**
```json
{
  "detail": "Email already in use"
}
```

**400 - Missing Current Password:**
```json
{
  "detail": "Current password required to set new password"
}
```

**401 - Incorrect Current Password:**
```json
{
  "detail": "Current password is incorrect"
}
```

**Example Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/auth/profile" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Updated Doe",
    "current_password": "SecurePass123",
    "new_password": "NewSecurePass456"
  }'
```

---

### POST /api/v1/auth/refresh

**Refresh JWT access token**

Issues a new JWT token with extended expiry. Requires valid (non-expired) token.

**Authentication:** Required (Bearer token)

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "email": "john.doe@example.com",
    "full_name": "John Doe",
    "created_at": "2025-11-06T10:00:00Z"
  }
}
```

**Error Responses:**

**401 - Token Expired:**
```json
{
  "detail": "Invalid authentication credentials"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Authorization: Bearer <current_token>"
```

---

### DELETE /api/v1/auth/account

**Delete user account**

Permanently deletes the user account and all associated data.

**⚠️ WARNING:** This is a destructive operation and cannot be undone.

**Authentication:** Required (Bearer token)

**Response (200 OK):**
```json
{
  "message": "Account successfully deleted",
  "success": true
}
```

**Error Responses:**

**401 - Unauthorized:**
```json
{
  "detail": "Invalid authentication credentials"
}
```

**500 - Deletion Failed:**
```json
{
  "detail": "Failed to delete account"
}
```

**Example Request:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/auth/account" \
  -H "Authorization: Bearer <token>"
```

---

## Security Best Practices

### Token Storage

**Frontend (Browser):**
- ✅ **Recommended:** `localStorage` or `sessionStorage`
- ❌ **Avoid:** Cookies (unless httpOnly + secure flags set)

**Example:**
```javascript
// Store token
localStorage.setItem('access_token', token);

// Retrieve token
const token = localStorage.getItem('access_token');

// Remove token (logout)
localStorage.removeItem('access_token');
```

### Token Usage

**HTTP Header:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Axios Example:**
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'
});

// Add token to all requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Password Requirements

- Minimum 8 characters
- At least 1 digit
- At least 1 uppercase letter
- Recommended: Special characters

**Validation Regex:**
```python
import re

def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    return True
```

---

**End of Part 1**

Continue to [Part 2](#) for Resume API, Jobs API, and Interview API documentation.
