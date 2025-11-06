# UtopiaHire Backend API Documentation - Part 2
## Resume & Jobs API Reference

> **Generated:** November 6, 2025  
> **Version:** 1.0.0  
> **Base URL:** `http://localhost:8000/api/v1`

---

## Table of Contents (Part 2)

7. [Resume API](#resume-api)
8. [Jobs API](#jobs-api)

---

## 7. Resume API

**Base Path:** `/api/v1/resumes`  
**Tag:** `Resume`  
**Authentication:** Required for all endpoints

### Endpoints Overview

| Method | Endpoint | Description | File Upload |
|--------|----------|-------------|-------------|
| POST | `/upload` | Upload resume file | ✅ |
| POST | `/analyze` | Analyze resume for ATS | ❌ |
| POST | `/enhance` | Get AI enhancement suggestions | ❌ |
| POST | `/{resume_id}/download-enhanced` | Generate enhanced resume | ❌ |
| GET | `/list` | List user's resumes | ❌ |
| GET | `/{resume_id}/download` | Download original resume | ❌ |
| DELETE | `/{resume_id}` | Delete resume | ❌ |
| GET | `/templates` | List resume templates | ❌ |
| GET | `/templates/{template_id}/download` | Download template | ❌ |
| POST | `/generate-cover-letter` | Generate AI cover letter | ❌ |

---

### POST /api/v1/resumes/upload

**Upload and parse a resume file**

Accepts PDF or DOCX files, parses content, and stores in database.

**Authentication:** Required

**Content-Type:** `multipart/form-data`

**Request Body:**
- `file`: Resume file (PDF/DOCX, max 10MB)

**Response (201 Created):**
```json
{
  "resume_id": 1,
  "filename": "john_doe_resume.pdf",
  "file_size": 245632,
  "file_type": "pdf",
  "parsed_text_length": 1234,
  "word_count": 456,
  "uploaded_at": "2025-11-06T10:00:00Z"
}
```

**Error Responses:**

**400 - Invalid File Type:**
```json
{
  "detail": "Invalid file type. Allowed: .pdf, .docx, .doc"
}
```

**400 - File Too Large:**
```json
{
  "detail": "File too large. Maximum size: 10.0MB"
}
```

**400 - Empty File:**
```json
{
  "detail": "Empty file uploaded"
}
```

**Example Request (cURL):**
```bash
curl -X POST "http://localhost:8000/api/v1/resumes/upload" \
  -H "Authorization: Bearer <token>" \
  -F "file=@/path/to/resume.pdf"
```

**Example Request (JavaScript):**
```javascript
const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/v1/resumes/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  return response.json();
};
```

---

### POST /api/v1/resumes/analyze

**Analyze resume for ATS compatibility and quality**

Performs comprehensive analysis including ATS scoring, keyword matching, and content quality assessment.

**Authentication:** Required

**Request Body:**
```json
{
  "resume_id": 1,
  "job_title": "Senior Software Engineer",
  "job_description": "We are looking for..."
}
```

**Fields:**
- `resume_id` (required): ID of uploaded resume
- `job_title` (optional): Target job title for optimization
- `job_description` (optional): Job description to match against

**Response (200 OK):**
```json
{
  "resume_id": 1,
  "overall_score": 82.5,
  "skill_match_score": 85.0,
  "experience_score": 80.0,
  "education_score": 78.0,
  "grade": "B+",
  "ats_score": {
    "overall_score": 82,
    "keyword_score": 80,
    "format_score": 90,
    "content_score": 75,
    "matched_keywords": ["Python", "Django", "PostgreSQL", "REST API"],
    "missing_keywords": ["Kubernetes", "Docker", "CI/CD"],
    "strengths": [
      "Clear section headers",
      "Good use of action verbs",
      "Quantified achievements"
    ],
    "weaknesses": [
      "Missing some technical keywords",
      "Could add more metrics"
    ]
  },
  "section_scores": [
    {
      "section_name": "Experience",
      "score": 85.0,
      "feedback": "Strong experience section with clear achievements",
      "issues": [],
      "suggestions": ["Add more quantified results"]
    },
    {
      "section_name": "Skills",
      "score": 80.0,
      "feedback": "Good skill coverage",
      "issues": [],
      "suggestions": ["Consider adding cloud technologies"]
    }
  ],
  "strengths": [
    "Clear professional summary",
    "Well-structured experience section",
    "Quantified achievements"
  ],
  "weaknesses": [
    "Missing some in-demand skills",
    "Could improve formatting"
  ],
  "critical_issues": [],
  "recommendations": [
    "[HIGH] Skills: Add cloud technologies (Docker, Kubernetes) (Impact: Improves ATS matching)",
    "[MEDIUM] Experience: Add more quantified achievements (Impact: Demonstrates impact)",
    "[LOW] Format: Optimize for ATS scanning (Impact: Better parsing)"
  ],
  "improvement_suggestions": [
    "[HIGH] Skills: Add cloud technologies (Docker, Kubernetes) (Impact: Improves ATS matching)",
    "[MEDIUM] Experience: Add more quantified achievements (Impact: Demonstrates impact)"
  ],
  "word_count": 456,
  "action_verb_count": 12,
  "quantified_achievements": 8,
  "spelling_errors": 0,
  "formatting_issues": 0,
  "analyzed_at": "2025-11-06T10:30:00Z",
  "analysis_duration_ms": 1250
}
```

**Error Responses:**

**404 - Resume Not Found:**
```json
{
  "detail": "Resume not found or access denied"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/resumes/analyze" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_title": "Senior Software Engineer"
  }'
```

---

### POST /api/v1/resumes/enhance

**Get AI-powered enhancement suggestions**

Generates specific improvement recommendations using AI analysis.

**Authentication:** Required

**Request Body:**
```json
{
  "resume_id": 1,
  "enhancement_type": "full",
  "target_job": "Senior Backend Developer"
}
```

**Fields:**
- `resume_id` (required): ID of resume
- `enhancement_type` (required): Type of enhancement
  - `full`: Complete enhancement
  - `grammar`: Grammar and writing improvements
  - `action_verbs`: Strengthen action verbs
  - `quantify`: Add more metrics
  - `ats_optimize`: Optimize for ATS systems
- `target_job` (optional): Target job for tailored suggestions

**Response (200 OK):**
```json
{
  "resume_id": 1,
  "enhancement_type": "full",
  "suggestions": [
    {
      "section": "Professional Summary",
      "original_text": "Experienced developer with Python skills",
      "enhanced_text": "Results-driven Senior Backend Developer with 5+ years of expertise in Python, Django, and scalable microservices architecture",
      "improvement_type": "full",
      "impact": "high",
      "explanation": "Enhanced summary with quantified experience and specific technical expertise"
    },
    {
      "section": "Experience",
      "original_text": "Worked on backend systems",
      "enhanced_text": "Architected and implemented high-performance backend systems serving 100K+ daily users, improving response time by 40%",
      "improvement_type": "full",
      "impact": "high",
      "explanation": "Added quantifiable metrics and specific impact"
    },
    {
      "section": "Skills",
      "original_text": "Python, databases",
      "enhanced_text": "Python (Django, FastAPI) | PostgreSQL, MongoDB | Docker, Kubernetes | REST APIs, GraphQL",
      "improvement_type": "full",
      "impact": "medium",
      "explanation": "Expanded skills with specific technologies and better organization"
    }
  ],
  "total_suggestions": 3,
  "high_impact_count": 2,
  "medium_impact_count": 1,
  "low_impact_count": 0,
  "estimated_score_improvement": 12.5,
  "enhanced_at": "2025-11-06T10:45:00Z"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/resumes/enhance" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "enhancement_type": "full",
    "target_job": "Senior Backend Developer"
  }'
```

---

### POST /api/v1/resumes/{resume_id}/download-enhanced

**Generate and download enhanced resume**

Applies AI improvements and generates an enhanced PDF file.

**Authentication:** Required

**Path Parameters:**
- `resume_id`: ID of resume to enhance

**Request Body:**
```json
{
  "enhancement_type": "full",
  "target_job": "Senior Backend Developer",
  "selected_improvements": [1, 3, 5]
}
```

**Fields:**
- `enhancement_type` (required): Type of enhancement
- `target_job` (optional): Target job
- `selected_improvements` (optional): Specific improvement IDs to apply

**Response (200 OK):**
- **Content-Type:** `application/octet-stream`
- **File:** Enhanced resume PDF

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/resumes/1/download-enhanced" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"enhancement_type": "full"}' \
  -o enhanced_resume.pdf
```

---

### GET /api/v1/resumes/list

**List user's uploaded resumes**

Returns paginated list of all resumes uploaded by the user.

**Authentication:** Required

**Query Parameters:**
- `page` (optional, default: 1): Page number
- `page_size` (optional, default: 10, max: 50): Items per page

**Response (200 OK):**
```json
{
  "resumes": [
    {
      "resume_id": 1,
      "filename": "john_doe_resume.pdf",
      "uploaded_at": "2025-11-06T10:00:00Z",
      "last_analyzed": "2025-11-06T10:30:00Z",
      "last_score": 82.5,
      "word_count": 456,
      "file_type": "pdf"
    },
    {
      "resume_id": 2,
      "filename": "john_doe_resume_v2.docx",
      "uploaded_at": "2025-11-05T14:20:00Z",
      "last_analyzed": null,
      "last_score": null,
      "word_count": 520,
      "file_type": "docx"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 10
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/resumes/list?page=1&page_size=10" \
  -H "Authorization: Bearer <token>"
```

---

### DELETE /api/v1/resumes/{resume_id}

**Delete a resume**

Permanently deletes resume from database and disk.

**Authentication:** Required

**Path Parameters:**
- `resume_id`: ID of resume to delete

**Response (200 OK):**
```json
{
  "message": "Resume deleted successfully",
  "success": true,
  "resume_id": 1
}
```

**Error Responses:**

**404 - Resume Not Found:**
```json
{
  "detail": "Resume not found or access denied"
}
```

**Example Request:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/resumes/1" \
  -H "Authorization: Bearer <token>"
```

---

### POST /api/v1/resumes/generate-cover-letter

**Generate AI-powered personalized cover letter**

Creates a tailored cover letter based on resume and job description using Groq AI.

**Authentication:** Required

**Request Body:**
```json
{
  "resume_id": 1,
  "job_title": "Senior Backend Developer",
  "company": "TechCorp Inc.",
  "job_description": "We are seeking an experienced backend developer...",
  "tone": "professional",
  "length": "medium",
  "highlights": ["5+ years Python experience", "Led team of 5 developers"]
}
```

**Fields:**
- `resume_id` (required): Resume to base letter on
- `job_title` (required): Target job title
- `company` (required): Company name
- `job_description` (required): Full job description
- `tone` (optional, default: "professional"): Writing tone
  - `professional`, `enthusiastic`, `formal`, `conversational`
- `length` (optional, default: "medium"): Letter length
  - `short` (250 words), `medium` (400 words), `long` (600 words)
- `highlights` (optional): Specific achievements to emphasize

**Response (200 OK):**
```json
{
  "cover_letter": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the Senior Backend Developer position at TechCorp Inc...",
  "word_count": 387,
  "sections": {
    "opening": "I am writing to express my strong interest...",
    "body": "With over 5 years of experience in Python development...",
    "closing": "I look forward to discussing how my experience..."
  },
  "suggestions": [
    "Consider mentioning specific TechCorp projects",
    "Add more detail about leadership experience"
  ],
  "metadata": {
    "tone": "professional",
    "length": "medium",
    "reading_time_minutes": 2
  }
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/resumes/generate-cover-letter" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_title": "Senior Backend Developer",
    "company": "TechCorp Inc.",
    "job_description": "We are seeking...",
    "tone": "professional",
    "length": "medium"
  }'
```

---

## 8. Jobs API

**Base Path:** `/api/v1/jobs`  
**Tag:** `Jobs`  
**Authentication:** Required for most endpoints

### Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/scrape` | Scrape jobs from external APIs | ✅ |
| POST | `/match` | Match jobs with resume | ✅ |
| GET | `/list` | List available jobs | ✅ |
| POST | `/search` | Advanced job search | ✅ |
| GET | `/insights` | Get market insights | ✅ |
| GET | `/{job_id}` | Get job details | ✅ |
| POST | `/{job_id}/save` | Save/bookmark job | ✅ |
| DELETE | `/{job_id}/save` | Remove saved job | ✅ |
| GET | `/saved` | List saved jobs | ✅ |
| POST | `/compatibility` | Analyze job compatibility (AI) | ✅ |

---

### POST /api/v1/jobs/scrape

**Scrape jobs from external APIs**

Fetches real job postings from JSearch API and stores in database.

**Authentication:** Required

**Request Body:**
```json
{
  "queries": ["Software Engineer", "Backend Developer", "Python Developer"],
  "locations": ["Tunisia", "Morocco", "Remote"],
  "num_results_per_query": 15
}
```

**Fields:**
- `queries` (required): List of job titles to search
- `locations` (required): List of locations
- `num_results_per_query` (optional, default: 10, max: 50): Results per query

**Response (200 OK):**
```json
{
  "jobs_scraped": 45,
  "jobs_stored": 42,
  "queries_processed": 3,
  "locations_processed": 3,
  "api_used": "JSearch",
  "scraping_duration_ms": 5240,
  "message": "Successfully scraped 45 jobs and stored 42 in database"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/scrape" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["Software Engineer", "Backend Developer"],
    "locations": ["Tunisia", "Remote"],
    "num_results_per_query": 15
  }'
```

---

### POST /api/v1/jobs/match

**Match jobs with resume**

Uses AI-powered matching algorithm to find relevant jobs based on uploaded resume.

**Authentication:** Required

**Request Body:**
```json
{
  "resume_id": 1,
  "limit": 20,
  "min_score": 60,
  "fetch_fresh_jobs": true,
  "queries": ["Backend Developer", "Software Engineer"],
  "locations": ["Tunisia"]
}
```

**Fields:**
- `resume_id` (required): Resume to match against
- `limit` (optional, default: 10): Max matches to return
- `min_score` (optional, default: 50): Minimum match score (0-100)
- `fetch_fresh_jobs` (optional, default: true): Scrape fresh jobs before matching
- `queries` (optional): Custom job queries (auto-extracted if not provided)
- `locations` (optional): Custom locations (uses resume location if not provided)

**Response (200 OK):**
```json
{
  "resume_id": 1,
  "matches": [
    {
      "job": {
        "id": "job_12345",
        "title": "Senior Backend Developer",
        "company": "TechCorp",
        "location": "Tunis, Tunisia",
        "region": "MENA",
        "type": "Full-time",
        "experience_level": "Mid-level",
        "description": "We are looking for...",
        "required_skills": ["Python", "Django", "PostgreSQL", "REST API", "Docker"],
        "preferred_skills": ["Kubernetes", "AWS", "CI/CD"],
        "salary_range": {
          "min": 30000,
          "max": 50000,
          "currency": "USD",
          "text": "$30,000 - $50,000/year"
        },
        "posted_date": "2025-11-05",
        "remote": false,
        "url": "https://example.com/jobs/12345",
        "source": "JSearch",
        "fetched_at": "2025-11-06T09:00:00Z"
      },
      "match_score": {
        "overall_score": 85.5,
        "skill_score": 90.0,
        "location_score": 100.0,
        "experience_score": 75.0,
        "breakdown": {
          "matched_skills": ["Python", "Django", "PostgreSQL", "REST API"],
          "missing_skills": ["Docker"]
        }
      },
      "matched_at": "2025-11-06T10:00:00Z"
    }
  ],
  "total_matches": 15,
  "matches_found": 15,
  "jobs_searched": 500,
  "total_jobs_searched": 500,
  "average_score": 72.3,
  "avg_match_score": 72.3,
  "best_match_score": 85.5,
  "processing_time_ms": 2341.25,
  "matched_at": "2025-11-06T10:00:00Z",
  "message": "Found 15 job matches with average score 72.3"
}
```

**Scoring Algorithm:**

**Overall Score = (Skill Score × 0.6) + (Location Score × 0.2) + (Experience Score × 0.2)**

- **Skill Score (60%)**: Percentage of required skills matched
- **Location Score (20%)**: Location match (100 if same region, 50 if remote, 0 otherwise)
- **Experience Score (20%)**: Experience level match (100 if exact, 75 if close, 50 if acceptable)

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/match" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "limit": 20,
    "min_score": 70,
    "fetch_fresh_jobs": true
  }'
```

---

### GET /api/v1/jobs/list

**List available jobs with filters**

Returns paginated list of jobs with optional filtering.

**Authentication:** Required

**Query Parameters:**
- `page` (optional, default: 1): Page number
- `page_size` (optional, default: 20, max: 100): Items per page
- `location` (optional): Filter by location or region
- `job_type` (optional): Filter by type (Full-time, Part-time, Contract, Internship)
- `remote_only` (optional, default: false): Show only remote jobs
- `experience_level` (optional): Filter by level (Junior, Mid-Level, Senior, Lead, Executive)

**Response (200 OK):**
```json
{
  "jobs": [
    {
      "id": "job_12345",
      "title": "Senior Backend Developer",
      "company": "TechCorp",
      "location": "Tunis, Tunisia",
      "remote": false,
      "job_type": "Full-time",
      "experience_level": "Mid-level",
      "salary_range": {
        "min": 30000,
        "max": 50000,
        "currency": "USD",
        "text": "$30,000 - $50,000/year"
      },
      "posted_date": "2025-11-05",
      "url": "https://example.com/jobs/12345",
      "required_skills": ["Python", "Django", "PostgreSQL", "REST API", "Docker"]
    }
  ],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "total_pages": 8
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/list?page=1&location=Tunisia&job_type=Full-time&remote_only=false" \
  -H "Authorization: Bearer <token>"
```

---

### POST /api/v1/jobs/search

**Advanced job search with multiple filters**

Searches jobs with keyword matching and complex filters.

**Authentication:** Required

**Request Body:**
```json
{
  "keywords": "Python backend",
  "location": "Tunisia",
  "job_type": "full_time",
  "experience_level": "mid_level",
  "remote_only": false,
  "min_salary": 25000,
  "max_salary": 60000,
  "required_skills": ["Python", "Django"],
  "page": 1,
  "page_size": 20
}
```

**Fields (all optional):**
- `keywords`: Search in title and description
- `location`: Location filter
- `job_type`: Employment type (full_time, part_time, contract, internship, temporary)
- `experience_level`: Experience level (junior, mid_level, senior, lead, executive)
- `remote_only`: Show only remote jobs
- `min_salary`, `max_salary`: Salary range
- `required_skills`: Must-have skills
- `page`, `page_size`: Pagination

**Response:** Same as `/list` endpoint

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/search" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Python Django",
    "location": "Tunisia",
    "job_type": "full_time",
    "min_salary": 30000,
    "required_skills": ["Python", "Django"]
  }'
```

---

### POST /api/v1/jobs/compatibility

**Analyze job compatibility with AI (NEW - Groq-powered)**

Uses Groq AI (llama-3.3-70b-versatile) to provide detailed compatibility analysis between resume and job.

**Authentication:** Required

**Request Body:**
```json
{
  "resume_id": 1,
  "job_description": "We are seeking a Senior Backend Developer with 5+ years of Python experience...",
  "job_title": "Senior Backend Developer",
  "company": "TechCorp Inc.",
  "required_skills": ["Python", "Django", "PostgreSQL", "Docker", "Kubernetes"]
}
```

**Fields:**
- `resume_id` (required): Resume to analyze
- `job_description` (required): Full job description
- `job_title` (optional): Job title
- `company` (optional): Company name
- `required_skills` (optional): List of required skills

**Response (200 OK):**
```json
{
  "resume_id": 1,
  "job_title": "Senior Backend Developer",
  "company": "TechCorp Inc.",
  "overall_match_score": 82,
  "skill_match_score": 85,
  "experience_match_score": 80,
  "education_match_score": 78,
  "matched_skills": [
    "Python (5 years experience)",
    "Django (3 years experience)",
    "PostgreSQL (4 years experience)",
    "REST APIs (5 years experience)"
  ],
  "missing_skills": [
    "Kubernetes (mentioned in job but not in resume)",
    "Docker (limited experience shown)"
  ],
  "strengths": [
    "Strong Python background with 5+ years",
    "Extensive Django framework experience",
    "Led backend team of 5 developers",
    "Implemented scalable microservices architecture"
  ],
  "gaps": [
    "Limited container orchestration experience",
    "Could emphasize DevOps skills more",
    "Cloud platform experience not highlighted"
  ],
  "recommendations": [
    "Highlight any Docker/Kubernetes projects you've worked on",
    "Add specific metrics about system scalability",
    "Emphasize cloud platform experience if applicable",
    "Include more details about team leadership"
  ],
  "ai_summary": "Strong candidate with excellent Python and Django background. Experience aligns well with senior-level requirements. Main areas for improvement: container orchestration and cloud platforms.",
  "ai_detailed_analysis": "The candidate demonstrates strong technical capabilities in Python development with 5+ years of experience, which exceeds the job requirement. Django expertise is evident through multiple projects. However, the resume could better showcase container orchestration skills (Docker/Kubernetes) which are increasingly important for backend roles. Leadership experience is present but could be quantified more. Overall match is strong with room for resume optimization.",
  "analyzed_at": "2025-11-06T11:00:00Z"
}
```

**Scoring Formula:**
- **Overall Score = (Skills × 0.50) + (Experience × 0.35) + (Education × 0.15)**

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/compatibility" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description": "We are seeking a Senior Backend Developer...",
    "job_title": "Senior Backend Developer",
    "company": "TechCorp Inc.",
    "required_skills": ["Python", "Django", "PostgreSQL"]
  }'
```

---

**End of Part 2**

Continue to [Part 3](#) for Interview API and Footprint API documentation.
