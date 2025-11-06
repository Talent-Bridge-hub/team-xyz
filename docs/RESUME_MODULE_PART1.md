# Resume Module Documentation - Part 1
## Overview, Architecture, Features & Backend API

> **Generated:** November 6, 2025  
> **Module:** Resume Analyzer & Enhancer (Module 5)  
> **Version:** 1.0  
> **Status:** Production Ready

---

## Table of Contents - Part 1

1. [Module Overview](#1-module-overview)
2. [System Architecture](#2-system-architecture)
3. [Core Features](#3-core-features)
4. [Backend API Reference](#4-backend-api-reference)
5. [API Models & Request/Response Formats](#5-api-models--requestresponse-formats)

---

## 1. Module Overview

### 1.1 Purpose

The Resume Module is a comprehensive AI-powered career tool that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) and improve their chances of landing interviews. It provides:

- **Resume Parsing**: Extract structured data from PDF/DOCX files
- **ATS Analysis**: Score resumes on multiple criteria (format, keywords, content)
- **AI Enhancement**: Improve bullet points with action verbs and quantification
- **Cover Letter Generation**: Create personalized cover letters using Groq AI
- **Template Library**: Professional DOCX templates ready for customization

### 1.2 Key Benefits

✅ **For Job Seekers:**
- Instant ATS compatibility scores (0-100)
- Actionable improvement suggestions
- AI-powered content enhancement
- Professional cover letter generation
- Free downloadable templates

✅ **Regional Focus:**
- Optimized for MENA (Middle East & North Africa) markets
- Sub-Saharan Africa job market support
- Bilingual keyword optimization (English, French, Arabic)
- Regional skill recommendations

### 1.3 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI (Python 3.12) | REST API server |
| **AI Engine** | Groq API (llama-3.3-70b-versatile) | Cover letter generation |
| **NLP** | NLTK, spaCy | Text processing |
| **PDF Parsing** | PyPDF2 | PDF text extraction |
| **DOCX Parsing** | python-docx | Word document processing |
| **PDF Generation** | ReportLab | Enhanced resume PDFs |
| **Database** | PostgreSQL + JSONB | Resume storage |
| **Frontend** | React 18 + TypeScript | User interface |

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TS)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ Upload Form │  │ Analysis View│  │ Enhancement UI   │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ Resume List │  │ Templates    │  │ Cover Letter Gen │   │
│  └─────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │ HTTPS/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND API (FastAPI)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Resume Router (850+ lines)              │   │
│  │  11 Endpoints: Upload, Analyze, Enhance, Download   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────┐
│   Parser     │  │    Analyzer      │  │  Enhancer    │
│  (474 lines) │  │   (912 lines)    │  │ (623 lines)  │
└──────────────┘  └──────────────────┘  └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                    ┌──────────────┐
                    │  PostgreSQL  │
                    │   Database   │
                    └──────────────┘
```

### 2.2 Data Flow

**Upload & Analysis Flow:**
```
User uploads PDF/DOCX
    ↓
ResumeParser extracts text + structured data
    ↓
Store in PostgreSQL (resumes table)
    ↓
ResumeAnalyzer calculates scores
    ↓
Store analysis (analyses table)
    ↓
Return results to frontend
```

**Enhancement Flow:**
```
User requests enhancement
    ↓
Load resume data from DB
    ↓
ResumeEnhancer applies improvements
    ↓
Generate enhanced PDF/DOCX
    ↓
Store enhancement (improved_resumes table)
    ↓
Return download link
```

**Cover Letter Flow:**
```
User provides job details
    ↓
Load resume data
    ↓
CoverLetterGenerator (Groq API)
    ↓
Generate personalized letter
    ↓
Return text + suggestions
```

### 2.3 File Structure

```
Utopia/
├── backend/app/api/
│   └── resume.py                   # 850+ lines - All API endpoints
│
├── utils/
│   ├── resume_parser.py            # 474 lines - PDF/DOCX parsing
│   ├── resume_analyzer.py          # 912 lines - ATS analysis
│   ├── resume_enhancer.py          # 623 lines - Content improvement
│   ├── cover_letter_generator.py   # 397 lines - AI cover letters
│   └── resume_templates.py         # 410 lines - DOCX templates
│
├── frontend/src/
│   ├── components/resume/
│   │   ├── ResumeUploadForm.tsx
│   │   ├── ResumeAnalysisView.tsx
│   │   ├── ResumeEnhancement.tsx
│   │   ├── ResumeList.tsx
│   │   ├── ResumeTemplatesModal.tsx
│   │   └── CoverLetterGenerator.tsx
│   │
│   └── services/
│       └── resume.service.ts       # 212 lines - API client
│
└── data/resumes/                   # Resume storage
    ├── templates/                  # Generated templates
    └── enhanced/                   # Enhanced versions
```

---

## 3. Core Features

### 3.1 Feature Matrix

| Feature | Status | AI-Powered | ATS-Friendly | Description |
|---------|--------|------------|--------------|-------------|
| **Resume Upload** | ✅ Stable | ❌ | ✅ | PDF/DOCX file upload (max 10MB) |
| **Resume Parsing** | ✅ Stable | ❌ | ✅ | Extract text, sections, contact info |
| **ATS Analysis** | ✅ Stable | ❌ | ✅ | Score resume (0-100) on multiple criteria |
| **Content Enhancement** | ✅ Stable | ⚠️ Rule-based | ✅ | Improve bullet points, action verbs |
| **Cover Letter Generation** | ✅ Stable | ✅ Groq AI | ✅ | Personalized AI-generated letters |
| **Template Download** | ✅ Stable | ❌ | ✅ | 3 professional DOCX templates |
| **Enhanced Resume Download** | ✅ Stable | ⚠️ Rule-based | ✅ | Generate improved PDF/DOCX |
| **Resume List & Management** | ✅ Stable | ❌ | N/A | List, view, delete resumes |

### 3.2 ATS Analysis Criteria

The analyzer evaluates resumes on **4 main dimensions**:

#### 3.2.1 ATS Compatibility Score (0-100)
- ✅ Email address present
- ✅ Phone number present
- ✅ Clear section headers
- ✅ Appropriate length (150-1000 words)
- ✅ Education section present
- ✅ Experience/Skills sections present
- ✅ Minimal special characters

#### 3.2.2 Formatting Score (0-100)
- ✅ Consistent structure (4+ sections)
- ✅ Appropriate section lengths
- ✅ Bullet points usage
- ✅ Proper density (not too dense)
- ✅ Section header capitalization

#### 3.2.3 Keyword Score (0-100)
- ✅ Regional keywords (MENA/Africa focus)
- ✅ Action verbs (10+ recommended)
- ✅ Technical skills (10+ recommended)
- ✅ Industry-relevant terms

**Sample Keywords (40+ tracked):**
- **Technical:** python, java, javascript, sql, react, node.js, django, flask, data analysis, machine learning, ai, cloud, aws, azure
- **Business:** project management, agile, scrum, team leadership, problem solving, communication, collaboration, strategic planning
- **Regional:** bilingual, french, arabic, english, multicultural, remote work, startup, fintech, e-commerce, mobile development

#### 3.2.4 Content Quality Score (0-100)
- ✅ Experience section with bullet points
- ✅ Education details
- ✅ Skills list (5+ skills)
- ✅ Professional summary (20+ words)
- ✅ Complete contact information

### 3.3 Enhancement Capabilities

The enhancer applies **rule-based improvements**:

#### 3.3.1 Action Verb Upgrades
```
Weak → Strong Replacements:
- "helped" → "assisted", "supported", "facilitated", "contributed to"
- "worked on" → "developed", "implemented", "executed", "delivered"
- "did" → "performed", "executed", "accomplished", "completed"
- "made" → "created", "developed", "designed", "built"
- "was responsible for" → "managed", "oversaw", "directed", "coordinated"
- "used" → "utilized", "leveraged", "employed", "applied"
- "got" → "achieved", "obtained", "secured", "earned"
- "tried" → "initiated", "pioneered", "launched", "spearheaded"
```

#### 3.3.2 Tone Improvements
```
Casual → Professional:
- "good" → "excellent"
- "nice" → "professional"
- "pretty" → "highly"
- "really" → "significantly"
- "very" → "exceptionally"
- "lots of" → "extensive"
- "a lot" → "substantial"
- "many" → "numerous"
```

#### 3.3.3 Quantification Suggestions
- Add placeholders like `[+X%]` for achievements
- Suggest metrics: "by X%", "for X+ clients", "across X projects", "within X months"
- Encourage numerical impact statements

### 3.4 Cover Letter Generation (AI)

**AI Model:** Groq API - llama-3.3-70b-versatile

**Capabilities:**
- Personalized content based on resume + job description
- Multiple tone options: professional, enthusiastic, formal, conversational
- Length options: short (250 words), medium (350 words), long (500 words)
- Automatic keyword matching from job description
- Structured sections: greeting, opening, body, closing, signature

**Example Request:**
```json
{
  "resume_id": 123,
  "job_title": "Full Stack Developer",
  "company": "Tech Innovators Inc",
  "job_description": "We are seeking a Full Stack Developer...",
  "tone": "professional",
  "length": "medium",
  "highlights": ["Led team of 5 engineers", "Built scalable microservices"]
}
```

---

## 4. Backend API Reference

### 4.1 API Endpoints Overview

**Base URL:** `http://localhost:8000/api/resume`

| # | Method | Endpoint | Auth Required | Description |
|---|--------|----------|---------------|-------------|
| 1 | POST | `/upload` | ✅ | Upload resume file |
| 2 | POST | `/analyze` | ✅ | Analyze resume |
| 3 | POST | `/enhance` | ✅ | Get enhancement suggestions |
| 4 | GET | `/list` | ✅ | List user's resumes |
| 5 | DELETE | `/{resume_id}` | ✅ | Delete resume |
| 6 | GET | `/{resume_id}/download` | ✅ | Download original |
| 7 | POST | `/{resume_id}/download-enhanced` | ✅ | Download enhanced |
| 8 | GET | `/templates` | ❌ | List templates |
| 9 | GET | `/templates/{template_id}/download` | ❌ | Download template |
| 10 | POST | `/generate-cover-letter` | ✅ | Generate cover letter |

### 4.2 Endpoint Details

---

#### 4.2.1 POST `/upload` - Upload Resume

**Purpose:** Upload and parse a resume file (PDF or DOCX)

**Authentication:** Required (JWT Bearer token)

**Request:**
```http
POST /api/resume/upload
Content-Type: multipart/form-data
Authorization: Bearer <JWT_TOKEN>

file: <resume.pdf or resume.docx>
```

**Success Response (201 Created):**
```json
{
  "resume_id": 123,
  "filename": "john_doe_resume.pdf",
  "file_size": 245678,
  "file_type": "pdf",
  "parsed_text_length": 3456,
  "word_count": 567,
  "uploaded_at": "2025-11-06T10:30:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid file type or file too large
- `401 Unauthorized`: Missing or invalid JWT token
- `500 Internal Server Error`: Parsing failed

**Validation Rules:**
- Allowed extensions: `.pdf`, `.docx`, `.doc`
- Max file size: 10 MB
- Min file size: > 0 bytes

---

#### 4.2.2 POST `/analyze` - Analyze Resume

**Purpose:** Perform comprehensive ATS analysis on uploaded resume

**Authentication:** Required

**Request:**
```json
{
  "resume_id": 123,
  "job_title": "Software Engineer",
  "job_description": "Optional job description for targeted analysis"
}
```

**Success Response (200 OK):**
```json
{
  "resume_id": 123,
  "overall_score": 78,
  "skill_match_score": 82.5,
  "experience_score": 75.0,
  "education_score": 70.0,
  "grade": "B",
  "ats_score": {
    "overall_score": 85,
    "keyword_score": 70,
    "format_score": 90,
    "content_score": 75,
    "matched_keywords": [],
    "missing_keywords": [],
    "strengths": [
      "✓ Excellent ATS compatibility",
      "✓ Well-formatted and easy to read"
    ],
    "weaknesses": [
      "⚠ Limited skills section - add more relevant skills"
    ]
  },
  "section_scores": [
    {
      "section_name": "Experience",
      "score": 75.0,
      "feedback": "Experience section present",
      "issues": [],
      "suggestions": []
    }
  ],
  "strengths": [
    "✓ Complete contact information",
    "✓ Detailed achievement descriptions"
  ],
  "weaknesses": [
    "⚠ Limited skills section - add more relevant skills"
  ],
  "critical_issues": [],
  "recommendations": [
    "[HIGH] Contact: Add your phone number for direct contact",
    "[MEDIUM] Content: Add more bullet points to experience section"
  ],
  "improvement_suggestions": [
    "Add more relevant technical and soft skills keywords",
    "Use consistent formatting with clear section headers"
  ],
  "word_count": 567,
  "action_verb_count": 10,
  "quantified_achievements": 5,
  "spelling_errors": 0,
  "formatting_issues": 0,
  "analyzed_at": "2025-11-06T10:35:00Z",
  "analysis_duration_ms": 1234
}
```

**Score Calculation:**
- `overall_score` = Skills (35%) + Experience (40%) + Education (25%)
- Each component scored 0-100
- Grade assigned: A (90+), B (80+), C (70+), D (60+), F (<60)

---

#### 4.2.3 POST `/enhance` - Get Enhancement Suggestions

**Purpose:** Get AI-powered improvement suggestions

**Authentication:** Required

**Request:**
```json
{
  "resume_id": 123,
  "enhancement_type": "full",
  "target_job": "Full Stack Developer"
}
```

**Enhancement Types:**
- `full`: Complete enhancement (default)
- `grammar`: Grammar and spelling only
- `action_verbs`: Action verb improvements
- `quantify`: Add quantification
- `ats_optimize`: ATS optimization

**Success Response (200 OK):**
```json
{
  "resume_id": 123,
  "enhancement_type": "full",
  "suggestions": [
    {
      "section": "Professional Summary",
      "original_text": "Good software engineer with experience...",
      "enhanced_text": "Results-driven software engineer with 5+ years experience...",
      "improvement_type": "full",
      "impact": "high",
      "explanation": "Enhanced professional summary with stronger language and better structure"
    },
    {
      "section": "Experience",
      "original_text": "Worked on web applications",
      "enhanced_text": "Developed scalable web applications serving 100K+ users",
      "improvement_type": "full",
      "impact": "high",
      "explanation": "Added action verb and quantification"
    }
  ],
  "total_suggestions": 12,
  "high_impact_count": 5,
  "medium_impact_count": 4,
  "low_impact_count": 3,
  "estimated_score_improvement": 15.5,
  "enhanced_at": "2025-11-06T10:40:00Z"
}
```

---

#### 4.2.4 GET `/list` - List User's Resumes

**Purpose:** Get paginated list of user's uploaded resumes

**Authentication:** Required

**Request:**
```http
GET /api/resume/list?page=1&page_size=10
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 10, max: 50)

**Success Response (200 OK):**
```json
{
  "resumes": [
    {
      "resume_id": 123,
      "filename": "john_doe_resume.pdf",
      "uploaded_at": "2025-11-06T10:30:00Z",
      "last_analyzed": "2025-11-06T10:35:00Z",
      "last_score": 78,
      "word_count": 567,
      "file_type": "pdf"
    },
    {
      "resume_id": 122,
      "filename": "jane_smith_resume.docx",
      "uploaded_at": "2025-11-05T14:20:00Z",
      "last_analyzed": null,
      "last_score": null,
      "word_count": 432,
      "file_type": "docx"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 10
}
```

---

#### 4.2.5 DELETE `/{resume_id}` - Delete Resume

**Purpose:** Delete a resume and its associated file

**Authentication:** Required

**Request:**
```http
DELETE /api/resume/123
Authorization: Bearer <JWT_TOKEN>
```

**Success Response (200 OK):**
```json
{
  "message": "Resume deleted successfully",
  "success": true,
  "resume_id": 123
}
```

**Error Responses:**
- `404 Not Found`: Resume not found or access denied

---

#### 4.2.6 GET `/{resume_id}/download` - Download Original

**Purpose:** Download the original uploaded resume file

**Authentication:** Required

**Request:**
```http
GET /api/resume/123/download
Authorization: Bearer <JWT_TOKEN>
```

**Success Response (200 OK):**
```http
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="john_doe_resume.pdf"

<binary file content>
```

---

#### 4.2.7 POST `/{resume_id}/download-enhanced` - Download Enhanced

**Purpose:** Generate and download enhanced resume with improvements applied

**Authentication:** Required

**Request:**
```json
{
  "enhancement_type": "full",
  "target_job": "Software Engineer",
  "selected_improvements": [1, 3, 5]
}
```

**Success Response (200 OK):**
```http
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="john_doe_resume_enhanced_20251106_103000.pdf"

<binary enhanced PDF content>
```

---

#### 4.2.8 GET `/templates` - List Templates

**Purpose:** Get list of available resume templates

**Authentication:** Not required (public endpoint)

**Request:**
```http
GET /api/resume/templates
```

**Success Response (200 OK):**
```json
{
  "templates": [
    {
      "id": "professional_chronological",
      "name": "Professional Chronological",
      "description": "Traditional format highlighting work experience. Best for professionals with 3+ years of experience.",
      "best_for": "Experienced Professionals",
      "ats_friendly": true,
      "sections": ["Contact", "Professional Summary", "Experience", "Skills", "Education", "Certifications"]
    },
    {
      "id": "modern_skills_focused",
      "name": "Modern Skills-Focused",
      "description": "Emphasizes technical skills and projects. Ideal for developers and tech professionals.",
      "best_for": "Tech & Engineering Roles",
      "ats_friendly": true,
      "sections": ["Contact", "Skills", "Technical Projects", "Experience", "Education"]
    },
    {
      "id": "entry_level_student",
      "name": "Entry-Level Student",
      "description": "Perfect for students, recent graduates, and career changers with limited work experience.",
      "best_for": "Students & New Graduates",
      "ats_friendly": true,
      "sections": ["Contact", "Education", "Skills", "Projects", "Internships/Experience", "Activities"]
    }
  ],
  "total": 3,
  "message": "Available resume templates"
}
```

---

#### 4.2.9 GET `/templates/{template_id}/download` - Download Template

**Purpose:** Download a resume template DOCX file (editable Word document)

**Authentication:** Not required (public endpoint)

**Request:**
```http
GET /api/resume/templates/professional_chronological/download
```

**Valid Template IDs:**
- `professional_chronological`
- `modern_skills_focused`
- `entry_level_student`

**Success Response (200 OK):**
```http
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="resume_template_Professional_Chronological_20251106_103000.docx"

<binary DOCX content>
```

**Error Responses:**
- `404 Not Found`: Template ID not found

---

#### 4.2.10 POST `/generate-cover-letter` - Generate Cover Letter

**Purpose:** Generate personalized cover letter using Groq AI

**Authentication:** Required

**Request:**
```json
{
  "resume_id": 123,
  "job_title": "Full Stack Developer",
  "company": "Tech Innovators Inc",
  "job_description": "We are seeking a Full Stack Developer with 3+ years experience in React and Node.js...",
  "tone": "professional",
  "length": "medium",
  "highlights": [
    "Led team of 5 engineers",
    "Built scalable microservices architecture"
  ]
}
```

**Request Parameters:**
- `resume_id` (required): Resume to base letter on
- `job_title` (required): Target position
- `company` (required): Company name
- `job_description` (required): Full job posting
- `tone` (optional): "professional" (default), "enthusiastic", "formal", "conversational"
- `length` (optional): "short" (250 words), "medium" (350 words, default), "long" (500 words)
- `highlights` (optional): Specific achievements to emphasize

**Success Response (200 OK):**
```json
{
  "cover_letter": "[Full cover letter text with header, greeting, body, and closing]",
  "word_count": 385,
  "sections": {
    "header": "John Doe\njohn.doe@example.com | +1-555-123-4567",
    "greeting": "Dear Hiring Manager,",
    "opening": "I am writing to express my strong interest...",
    "body": "With 5+ years of experience in full-stack development...",
    "closing": "I would welcome the opportunity to discuss...",
    "signature": "Sincerely,\nJohn Doe"
  },
  "suggestions": [
    "Consider adding specific metrics or KPIs to quantify your achievements",
    "Proofread carefully for typos and grammatical errors",
    "Research the company and mention specific initiatives"
  ],
  "metadata": {
    "job_title": "Full Stack Developer",
    "company": "Tech Innovators Inc",
    "tone": "professional",
    "length": "medium",
    "generated_at": "2025-11-06T10:45:00Z"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Resume not found or invalid parameters
- `500 Internal Server Error`: Groq API error

---

## 5. API Models & Request/Response Formats

### 5.1 Core Data Models

```python
# Pydantic models used in backend/app/models/resume.py

class ResumeUploadResponse(BaseModel):
    resume_id: int
    filename: str
    file_size: int
    file_type: str
    parsed_text_length: int
    word_count: int
    uploaded_at: datetime

class ATSScore(BaseModel):
    overall_score: int  # 0-100
    keyword_score: int  # 0-100
    format_score: int   # 0-100
    content_score: int  # 0-100
    matched_keywords: List[str]
    missing_keywords: List[str]
    strengths: List[str]
    weaknesses: List[str]

class SectionScore(BaseModel):
    section_name: str
    score: float
    feedback: str
    issues: List[str]
    suggestions: List[str]

class ResumeAnalysisResponse(BaseModel):
    resume_id: int
    overall_score: int
    skill_match_score: float
    experience_score: float
    education_score: float
    grade: str
    ats_score: ATSScore
    section_scores: List[SectionScore]
    strengths: List[str]
    weaknesses: List[str]
    critical_issues: List[str]
    recommendations: List[str]
    improvement_suggestions: List[str]
    word_count: int
    action_verb_count: int
    quantified_achievements: int
    spelling_errors: int
    formatting_issues: int
    analyzed_at: datetime
    analysis_duration_ms: int

class EnhancementSuggestion(BaseModel):
    section: str
    original_text: str
    enhanced_text: str
    improvement_type: str
    impact: str  # 'high', 'medium', 'low'
    explanation: str

class ResumeEnhancementResponse(BaseModel):
    resume_id: int
    enhancement_type: str
    suggestions: List[EnhancementSuggestion]
    total_suggestions: int
    high_impact_count: int
    medium_impact_count: int
    low_impact_count: int
    estimated_score_improvement: float
    enhanced_at: datetime

class CoverLetterRequest(BaseModel):
    resume_id: int
    job_title: str
    company: str
    job_description: str
    tone: Optional[str] = "professional"
    length: Optional[str] = "medium"
    highlights: Optional[List[str]] = None

class CoverLetterResponse(BaseModel):
    cover_letter: str
    word_count: int
    sections: Dict[str, str]
    suggestions: List[str]
    metadata: Dict[str, Any]
```

---

## Continue to Part 2

**Part 2 covers:**
- Database schema and tables
- Utility modules deep dive
- Frontend components
- Integration guide
- Configuration and deployment

---

**Generated by:** UtopiaHire Documentation Team  
**Last Updated:** November 6, 2025  
**Next Review:** December 2025
