# UtopiaHire - Complete Project Structure

> **Generated:** November 4, 2025  
> **Version:** 3.0 (Updated with Job Compatibility Feature)  
> **Description:** Complete file and folder structure of the UtopiaHire platform

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Root Directory](#root-directory)
3. [Backend Structure](#backend-structure)
4. [Frontend Structure](#frontend-structure)
5. [Utilities](#utilities)
6. [Configuration](#configuration)
7. [Data & Assets](#data--assets)
8. [Documentation](#documentation)
9. [Tests](#tests)
10. [File Count Summary](#file-count-summary)

---

## Project Overview

**UtopiaHire** is a comprehensive AI-powered career platform with 6 core modules:
- **Module 1:** Authentication & User Management
- **Module 2:** Job Matching & Recommendations
- **Module 3:** AI Interview Simulator
- **Module 4:** Digital Footprint Scanner
- **Module 5:** Resume Analyzer & Enhancer
- **Module 6:** Job Compatibility Analyzer (NEW)

**Tech Stack:**
- **Backend:** Python 3.12, FastAPI, PostgreSQL
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS
- **AI/ML:** Groq API (llama-3.3-70b-versatile), HuggingFace (Zephyr-7b-beta, Mistral), spaCy NLP
- **APIs:** GitHub API, StackOverflow API, Groq API

---

## Root Directory

```
Utopia/
├── .env                                    # Environment variables (API keys, DB credentials)
├── .gitignore                              # Git ignore rules (includes tests/ folder)
├── README.md                               # Main project README
├── requirements.txt                        # Python dependencies
├── install_dependencies.sh                 # Automated dependency installation
│
├── daily_job_updater.py                    # Automated job update script
├── populate_jobs_comprehensive.py          # Populate database with jobs
├── quick_populate_jobs.py                  # Quick job population script
│
├── backend/                                # Backend API server
├── frontend/                               # React frontend application
├── utils/                                  # Utility scripts
├── config/                                 # Configuration files
├── data/                                   # Data storage
├── logs/                                   # Log files
│
├── tests/                                  # All test files (ignored by git)
│   ├── test_add_jobs.py
│   ├── test_ai_integration.py
│   ├── test_analyzer.py
│   ├── test_api.py
│   ├── test_auth.py
│   ├── test_delete.py
│   ├── test_enhancement_download.py
│   ├── test_footprint.py
│   ├── test_groq_interview.py
│   ├── test_groq_recommendations.py
│   ├── test_hf_token.py
│   ├── test_interview_endpoint.py
│   ├── test_job_compatibility.py           # NEW - Test job compatibility analyzer
│   ├── test_job_matcher.py
│   ├── test_jobs.py
│   └── test_resume.py
│
└── docs/                                   # Documentation (13+ markdown files)
    ├── AI_MIGRATION_COMPLETE.md
    ├── ALL_ERRORS_FIXED.md
    ├── ARCHITECTURE.md
    ├── DEPLOYMENT.md
    ├── ERROR_FIXES.md
    ├── FOOTPRINT_MODULE_DOCUMENTATION.md
    ├── JOBS_UI_COMPLETE.md
    ├── JOB_COMPATIBILITY_FEATURE.md        # NEW - Job compatibility docs
    ├── MIGRATION_GUIDE.md
    ├── PROJECT_COMPLETE.md
    ├── PROJECT_STRUCTURE_COMPLETE.md       # This file
    ├── STATUS_REPORT.md
    └── WEB_PROGRESS_REPORT_2.md
```

**Note:** All test files have been moved to `tests/` folder (ignored by git). All documentation is now in `docs/` folder.

---

## Backend Structure

```
backend/
├── __init__.py                             # Backend package initializer
├── requirements.txt                        # Backend-specific dependencies
├── start.sh                                # Backend startup script
├── test_api.py                             # Backend API tests
│
├── app/                                    # Main application directory
│   ├── __init__.py
│   ├── main.py                             # FastAPI application entry point
│   │
│   ├── api/                                # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py                         # Authentication endpoints (login, register)
│   │   ├── deps.py                         # Dependency injection utilities
│   │   ├── footprint.py                    # Footprint scanner endpoints
│   │   ├── interview.py                    # Interview simulator endpoints
│   │   ├── jobs.py                         # Job matching endpoints
│   │   └── resume.py                       # Resume analyzer endpoints
│   │
│   ├── core/                               # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                       # Configuration settings
│   │   ├── database.py                     # Database connection pool
│   │   └── security.py                     # JWT tokens, password hashing
│   │
│   └── models/                             # Pydantic models
│       ├── __init__.py
│       ├── footprint.py                    # Footprint data models
│       ├── interview.py                    # Interview data models
│       ├── job.py                          # Job data models
│       ├── resume.py                       # Resume data models
│       └── user.py                         # User data models
│
├── database/                               # Database scripts
│   └── interview_question_bank.sql         # Pre-populated interview questions
│
├── migrations/                             # Database migrations
│   ├── create_footprint_tables.py          # Footprint schema migration
│   ├── create_interview_tables.py          # Interview schema migration
│   ├── create_jobs_table.py                # Jobs schema migration
│   └── create_resumes_table.py             # Resumes schema migration
│
└── Documentation/
    ├── API_ARCHITECTURE.md                 # API design documentation
    ├── AUTH_SYSTEM_COMPLETE.md             # Authentication system docs
    ├── MODULE_1_COMPLETE.md                # Module 1 documentation
    ├── MODULE_2_COMPLETE.md                # Module 2 documentation
    ├── MODULE_3_COMPLETE.md                # Module 3 documentation
    ├── WEB_PROGRESS_REPORT_1.md            # Progress report 1
    └── WEB_PROGRESS_REPORT_2.md            # Progress report 2
```

### Backend API Endpoints Summary

| Module | Endpoint | Method | Description |
|--------|----------|--------|-------------|
| **Auth** | `/api/auth/register` | POST | User registration |
| **Auth** | `/api/auth/login` | POST | User login (JWT token) |
| **Resume** | `/api/resume/upload` | POST | Upload resume file |
| **Resume** | `/api/resume/analyze/{id}` | GET | Get resume analysis |
| **Resume** | `/api/resume/enhance` | POST | Enhance resume content |
| **Resume** | `/api/resume/download-template` | GET | Download resume template |
| **Jobs** | `/api/jobs/match` | POST | Match jobs to resume |
| **Jobs** | `/api/v1/jobs/compatibility` | POST | Analyze job compatibility (NEW) |
| **Jobs** | `/api/jobs/` | GET | List all jobs (with filters) |
| **Jobs** | `/api/jobs/{id}` | GET | Get job details |
| **Jobs** | `/api/jobs/{id}` | DELETE | Delete job posting |
| **Interview** | `/api/interview/start` | POST | Start interview session |
| **Interview** | `/api/interview/{id}/answer` | POST | Submit answer |
| **Interview** | `/api/interview/{id}/complete` | POST | Complete interview |
| **Interview** | `/api/interview/history` | GET | Get interview history |
| **Footprint** | `/api/footprint/scan` | POST | Scan digital footprint |
| **Footprint** | `/api/footprint/recommendations` | GET | Get AI recommendations |
| **Footprint** | `/api/footprint/history` | GET | Get scan history |

---

## Frontend Structure

```
frontend/
├── .env                                    # Frontend environment variables
├── .gitignore                              # Git ignore rules
├── index.html                              # HTML entry point
├── package.json                            # Node.js dependencies
├── package-lock.json                       # Locked dependency versions
├── README.md                               # Frontend documentation
│
├── Configuration Files/
│   ├── eslint.config.js                    # ESLint configuration
│   ├── postcss.config.js                   # PostCSS configuration
│   ├── tailwind.config.js                  # TailwindCSS configuration
│   ├── tsconfig.json                       # TypeScript base config
│   ├── tsconfig.app.json                   # TypeScript app config
│   ├── tsconfig.node.json                  # TypeScript node config
│   └── vite.config.ts                      # Vite bundler config
│
├── .vscode/                                # VS Code settings
│   ├── extensions.json                     # Recommended extensions
│   └── settings.json                       # Workspace settings
│
├── public/                                 # Static assets
│   └── vite.svg                            # Vite logo
│
├── src/                                    # Source code
│   ├── main.tsx                            # Application entry point
│   ├── App.tsx                             # Root component
│   ├── App.css                             # Global app styles
│   ├── index.css                           # Global CSS (Tailwind imports)
│   ├── vite-env.d.ts                       # Vite type definitions
│   │
│   ├── assets/                             # Images and icons
│   │   └── react.svg                       # React logo
│   │
│   ├── components/                         # React components
│   │   ├── auth/                           # Auth components (empty - reserved)
│   │   │
│   │   ├── common/                         # Shared components
│   │   │   └── ProtectedRoute.tsx          # Route authentication wrapper
│   │   │
│   │   ├── footprint/                      # Footprint scanner components
│   │   │   ├── ActivityChart.tsx           # GitHub activity chart
│   │   │   ├── FootprintScanForm.tsx       # Scan input form
│   │   │   ├── GitHubContributionGraph.tsx # Contribution heatmap
│   │   │   ├── RecommendationsList.tsx     # AI recommendations display
│   │   │   └── ScoreGauge.tsx              # Score visualization gauge
│   │   │
│   │   ├── interview/                      # Interview simulator components
│   │   │   ├── InterviewChat.tsx           # Chat interface
│   │   │   ├── InterviewHistory.tsx        # Past interviews list
│   │   │   └── InterviewSetup.tsx          # Interview configuration
│   │   │
│   │   ├── jobs/                           # Job matching components
│   │   │   ├── JobCard.tsx                 # Individual job card
│   │   │   ├── JobChromaGrid.css           # Chroma grid styles
│   │   │   ├── JobChromaGrid.tsx           # Animated job grid
│   │   │   ├── JobDetailModal.tsx          # Job details popup
│   │   │   ├── JobList.tsx                 # Jobs list view
│   │   │   └── JobMatcher.tsx              # Job matching interface
│   │   │
│   │   ├── layout/                         # Layout components
│   │   │   └── DashboardLayout.tsx         # Main dashboard layout
│   │   │
│   │   ├── menu/                           # Navigation menu (empty)
│   │   │
│   │   └── resume/                         # Resume module components
│   │       ├── ResumeAnalysisView.tsx      # Analysis results display
│   │       ├── ResumeEnhancement.tsx       # Enhancement interface
│   │       ├── ResumeList.tsx              # Uploaded resumes list
│   │       ├── ResumeTemplatesModal.tsx    # Template selector modal
│   │       └── ResumeUploadForm.tsx        # File upload form
│   │
│   ├── contexts/                           # React contexts
│   │   └── AuthContext.tsx                 # Authentication context provider
│   │
│   ├── hooks/                              # Custom React hooks (empty)
│   │
│   ├── i18n/                               # Internationalization
│   │   └── I18nContext.tsx                 # i18n context provider
│   │
│   ├── pages/                              # Page components
│   │   ├── auth/                           # Authentication pages
│   │   │   ├── LoginPage.tsx               # Login page
│   │   │   └── RegisterPage.tsx            # Registration page
│   │   │
│   │   ├── dashboard/                      # Dashboard pages
│   │   │   ├── DashboardHome.tsx           # Dashboard home
│   │   │   ├── DashboardPage.tsx           # Dashboard wrapper
│   │   │   └── index.ts                    # Dashboard exports
│   │   │
│   │   ├── footprint/                      # Footprint scanner page
│   │   │   ├── FootprintPage.tsx           # Main footprint page
│   │   │   └── index.ts                    # Footprint exports
│   │   │
│   │   ├── interview/                      # Interview simulator page
│   │   │   └── index.tsx                   # Interview page
│   │   │
│   │   ├── jobs/                           # Job matching page
│   │   │   └── index.tsx                   # Jobs page
│   │   │
│   │   └── resume/                         # Resume analyzer page
│   │       ├── ResumePage.tsx              # Main resume page
│   │       └── index.ts                    # Resume exports
│   │
│   ├── schemas/                            # Validation schemas (empty - reserved)
│   │
│   ├── services/                           # API service layer
│   │   ├── api-client.ts                   # Axios API client
│   │   ├── auth.service.ts                 # Authentication service
│   │   ├── interview.service.ts            # Interview API calls
│   │   ├── jobs.service.ts                 # Jobs API calls
│   │   └── resume.service.ts               # Resume API calls
│   │
│   ├── types/                              # TypeScript types
│   │   └── api.ts                          # API type definitions
│   │
│   └── utils/                              # Utility functions (empty)
│
└── Documentation/
    ├── ALL_ERRORS_FIXED.md                 # Error fixes documentation
    ├── ERROR_FIXES.md                      # Additional error fixes
    ├── JOBS_UI_COMPLETE.md                 # Jobs UI completion report
    └── STATUS_REPORT.md                    # Status report
```

### Frontend Routes

| Route | Component | Description | Protected |
|-------|-----------|-------------|-----------|
| `/` | `DashboardHome` | Landing page | ❌ |
| `/login` | `LoginPage` | User login | ❌ |
| `/register` | `RegisterPage` | User registration | ❌ |
| `/dashboard` | `DashboardPage` | Main dashboard | ✅ |
| `/resume` | `ResumePage` | Resume analyzer | ✅ |
| `/jobs` | `JobsPage` | Job matcher | ✅ |
| `/interview` | `InterviewPage` | Interview simulator | ✅ |
| `/footprint` | `FootprintPage` | Footprint scanner | ✅ |

---

## Utilities

```
utils/
├── ai_answer_analyzer.py                   # AI-powered answer analysis
├── ai_recommendation_generator.py          # AI career recommendations
├── answer_analyzer.py                      # Interview answer analyzer
├── create_sample_resume.py                 # Generate sample resumes
├── footprint_calculator.py                 # Calculate footprint scores
├── github_analyzer.py                      # GitHub profile analyzer
├── interview_simulator.py                  # Interview simulation engine
├── job_compatibility_analyzer.py           # AI job compatibility analyzer (NEW)
├── job_matcher.py                          # Job matching algorithm
├── job_scraper.py                          # Job scraping utilities
├── resume_analyzer.py                      # Resume content analyzer
├── resume_enhancer.py                      # AI resume enhancement
├── resume_parser.py                        # Resume parsing (PDF/DOCX)
├── resume_templates.py                     # Resume template generator
├── resume_templates_pdf_backup.py          # PDF template backup
└── stackoverflow_scanner.py                # StackOverflow profile scanner
```

### Utility Functions Overview

| File | Key Classes/Functions | Description |
|------|----------------------|-------------|
| `ai_answer_analyzer.py` | `AIAnswerAnalyzer` | Analyzes interview answers using HuggingFace AI |
| `ai_recommendation_generator.py` | `AIRecommendationGenerator` | Generates personalized career recommendations |
| `answer_analyzer.py` | `AnswerAnalyzer` | Evaluates interview answers (relevance, depth) |
| `footprint_calculator.py` | `FootprintCalculator` | Calculates technical, social, impact scores |
| `github_analyzer.py` | `GitHubAnalyzer` | Fetches GitHub stats, repos, README |
| `interview_simulator.py` | `InterviewSimulator` | Manages interview sessions and questions |
| `job_compatibility_analyzer.py` | `JobCompatibilityAnalyzer` | AI job/resume compatibility using Groq API (NEW) |
| `job_matcher.py` | `JobMatcher` | Matches resumes to job postings |
| `job_scraper.py` | `JobScraper` | Scrapes jobs from external APIs |
| `resume_analyzer.py` | `ResumeAnalyzer` | Extracts skills, experience, education |
| `resume_enhancer.py` | `ResumeEnhancer` | AI-powered resume improvement |
| `resume_parser.py` | `ResumeParser` | Parses PDF/DOCX files |
| `resume_templates.py` | `ResumeTemplateGenerator` | Generates DOCX/PDF templates |
| `stackoverflow_scanner.py` | `StackOverflowScanner` | Fetches SO reputation and activity |

---

## Configuration

```
config/
├── database.py                             # Database configuration
├── footprint_schema.sql                    # Footprint table schemas
├── interview_schema.sql                    # Interview table schemas
├── job_apis.py                             # Job API configurations
└── schema.sql                              # Main database schema
```

### Database Schemas

**Tables:**
1. `users` - User accounts (id, email, hashed_password, created_at)
2. `resumes` - Uploaded resumes (id, user_id, filename, analysis_result)
3. `jobs` - Job postings (id, title, company, description, requirements)
4. `interviews` - Interview sessions (id, user_id, job_id, status, score)
5. `footprint_scans` - Footprint scan results (id, user_id, github_data, scores)
6. `interview_questions` - Question bank (id, category, difficulty, question_text)

---

## Data & Assets

```
data/
├── outputs/                                # Generated outputs
│   ├── sample_resume_analysis_20251014_153141.json
│   └── sample_resume_enhanced_20251014_153141.txt
│
├── resumes/                                # Uploaded resumes
│   ├── templates/                          # Generated templates
│   │   ├── resume_template_Entry-Level_Student_20251015_213500.docx
│   │   ├── resume_template_Entry-Level_Student_20251015_213520.docx
│   │   ├── resume_template_Entry-Level___Student_20251015_212903.pdf
│   │   ├── resume_template_Entry-Level___Student_20251015_212926.pdf
│   │   ├── resume_template_Entry-Level___Student_20251015_212935.pdf
│   │   ├── resume_template_Entry-Level___Student_20251015_212953.pdf
│   │   ├── resume_template_Modern_Skills-Focused_20251015_210443.pdf
│   │   ├── resume_template_Modern_Skills-Focused_20251015_212935.pdf
│   │   ├── resume_template_Modern_Skills-Focused_20251015_213520.docx
│   │   ├── resume_template_Professional_Chronological_20251015_210432.pdf
│   │   ├── resume_template_Professional_Chronological_20251015_212935.pdf
│   │   ├── resume_template_Professional_Chronological_20251015_213520.docx
│   │   ├── resume_template_Professional_Chronological_20251015_213619.docx
│   │   ├── resume_template_Professional_Chronological_20251015_213736.docx
│   │   ├── resume_template_Professional_Chronological_20251017_084410.docx
│   │   └── test_entry.pdf
│   │
│   ├── 10_20251015_192853_CS & CN & Cyber Challenge.pdf
│   ├── 10_20251015_200600_cv-template.pdf
│   ├── 10_20251017_213046_cv-template-4.pdf
│   ├── 7_20251014_210623_test_resume.docx
│   ├── 7_20251014_210725_test_resume.docx
│   └── sample_resume.pdf
│
└── scraped_jobs/                           # Scraped job data
    └── jobs_20251014_165323.json
```

---

## Documentation

```
docs/
├── API_KEY_SETUP.md                        # API key configuration guide
├── FRONTEND_INTEGRATION.md                 # Frontend integration guide
├── MODULE_2_JOB_MATCHER.md                 # Job matcher documentation
├── MODULE_3_AI_INTERVIEWER.md              # AI interviewer documentation
├── MODULE_4_FOOTPRINT_SCANNER.md           # Footprint scanner documentation
├── REAL_JOB_SCRAPING.md                    # Job scraping guide
└── REAL_JOB_SCRAPING_PLAN.md               # Job scraping plan
```

---

## CLI

```
cli/
└── utopiahire.py                           # Command-line interface tool
```

**CLI Commands:**
```bash
# Analyze resume
./utopiahire analyze-resume path/to/resume.pdf

# Match jobs
./utopiahire match-jobs --resume-id 123

# Start interview
./utopiahire interview --job-id 456

# Scan footprint
./utopiahire scan-footprint --github username
```

---

## Logs

```
logs/
└── job_updater.log                         # Daily job updater logs
```

---

## Models

```
models/                                     # Empty directory (models in backend/app/models/)
```

---

## Tests

All test files are now organized in the `tests/` folder and excluded from git tracking:

```
tests/
├── test_add_jobs.py                        # Test job addition functionality
├── test_ai_integration.py                  # Test AI integration
├── test_analyzer.py                        # Test resume analyzer
├── test_api.py                             # Test backend API endpoints
├── test_auth.py                            # Test authentication system
├── test_delete.py                          # Test delete operations
├── test_enhancement_download.py            # Test resume enhancement download
├── test_footprint.py                       # Test footprint scanner
├── test_groq_interview.py                  # Test Groq interview integration
├── test_groq_recommendations.py            # Test Groq recommendations
├── test_hf_token.py                        # Test HuggingFace token
├── test_interview_endpoint.py              # Test interview endpoints
├── test_job_compatibility.py               # Test job compatibility analyzer (NEW)
├── test_job_matcher.py                     # Test job matcher
├── test_jobs.py                            # Test jobs API
└── test_resume.py                          # Test resume API
```

**Running Tests:**
```bash
# Run all tests
pytest tests/ -v

# Run specific test
python tests/test_job_compatibility.py
```

---

## Environment Variables

### Root `.env`
```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=utopiahire
DB_USER=utopia_user
DB_PASSWORD=utopia_secure_2025

# AI/ML API Keys
GROQ_API_KEY=gsk_xxxxxxxxxxxxx              # NEW - For job compatibility analysis
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx              # For footprint scanner

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
APP_NAME=UtopiaHire
APP_VERSION=1.0.0
DEBUG=true
LOG_LEVEL=INFO

# External APIs (Optional)
STACKOVERFLOW_API_KEY=optional
```

### Frontend `.env`
```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=UtopiaHire
```

---

## File Count Summary (Updated - November 4, 2025)

| Category | Count | Description |
|----------|-------|-------------|
| **Backend Python Files** | 23 | API endpoints, models, core logic, migrations |
| **Frontend TypeScript/TSX Files** | 44 | Components, pages, services (including JobCompatibilityAnalyzer) |
| **Utility Scripts** | 15 | Resume parser, job matcher, AI analyzers (including job_compatibility_analyzer) |
| **Configuration Files** | 13 | Database, API, build configs (Vite, Tailwind, TypeScript) |
| **Documentation Files** | 20 | Markdown files (1 README, 13 in docs/, 6 in backend/frontend) |
| **Test Scripts** | 16 | Python test scripts in tests/ folder (ignored by git) |
| **Data Files** | 20+ | Resumes, templates, scraped jobs |
| **SQL Files** | 4 | Database schemas |
| **Shell Scripts** | 1 | install_dependencies.sh |
| **CSS Files** | 3 | App.css, index.css, JobChromaGrid.css |
| **HTML Files** | 1 | index.html |
| **Total Source Files** | ~180 | Excluding node_modules, venv, __pycache__, .git, tests/ |

---

## Key Technologies by Directory

### Backend (`/backend`)
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **psycopg2** - PostgreSQL adapter
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing

### Frontend (`/frontend`)
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Framer Motion** - Animations
- **Axios** - HTTP client

### Utils (`/utils`)
- **Groq API** - llama-3.3-70b-versatile for job compatibility (NEW)
- **spaCy** - NLP processing
- **HuggingFace** - AI models
- **PyPDF2** - PDF parsing
- **python-docx** - DOCX parsing
- **ReportLab** - PDF generation

---

## Directory Permissions

```bash
# Data directories (user writable)
chmod 755 data/
chmod 755 data/resumes/
chmod 755 data/outputs/
chmod 755 logs/

# Scripts (executable)
chmod +x install_dependencies.sh
chmod +x status.sh
chmod +x test_all.sh
chmod +x utopiahire
chmod +x backend/start.sh

# Configuration (readable only)
chmod 600 .env
chmod 600 frontend/.env
```

---

## Build Artifacts (Excluded from Git)

```
# Not tracked in version control
venv/                                       # Python virtual environment
node_modules/                               # Node.js dependencies
__pycache__/                                # Python bytecode cache
*.pyc                                       # Compiled Python files
.git/                                       # Git repository
dist/                                       # Build output
build/                                      # Build artifacts
.vscode/                                    # VS Code settings (sometimes)
```

---

## Quick Navigation Guide

| Task | Directory | File |
|------|-----------|------|
| Add new API endpoint | `backend/app/api/` | Create new `.py` file |
| Modify database schema | `config/` | Edit `.sql` files |
| Create new frontend component | `frontend/src/components/` | Add `.tsx` file |
| Add new page | `frontend/src/pages/` | Add new folder with `index.tsx` |
| Update AI logic | `utils/` | Modify analyzer/generator files |
| Configure environment | Root or `frontend/` | Edit `.env` files |
| Add tests | Root directory | Create `test_*.py` or `test_*.sh` |
| Update documentation | `docs/` or root | Edit/create `.md` files |

---

## Module File Mapping

### Module 1: Authentication
- **Backend:** `backend/app/api/auth.py`, `backend/app/core/security.py`
- **Frontend:** `frontend/src/pages/auth/`, `frontend/src/contexts/AuthContext.tsx`
- **Database:** `config/schema.sql` (users table)

### Module 2: Job Matcher
- **Backend:** `backend/app/api/jobs.py`, `backend/app/models/job.py`
- **Frontend:** `frontend/src/pages/jobs/`, `frontend/src/components/jobs/`
- **Utils:** `utils/job_matcher.py`, `utils/job_scraper.py`
- **Database:** `config/schema.sql` (jobs table)

### Module 3: AI Interview Simulator
- **Backend:** `backend/app/api/interview.py`, `backend/app/models/interview.py`
- **Frontend:** `frontend/src/pages/interview/`, `frontend/src/components/interview/`
- **Utils:** `utils/interview_simulator.py`, `utils/ai_answer_analyzer.py`
- **Database:** `config/interview_schema.sql`

### Module 4: Digital Footprint Scanner
- **Backend:** `backend/app/api/footprint.py`, `backend/app/models/footprint.py`
- **Frontend:** `frontend/src/pages/footprint/`, `frontend/src/components/footprint/`
- **Utils:** `utils/github_analyzer.py`, `utils/stackoverflow_scanner.py`, `utils/footprint_calculator.py`, `utils/ai_recommendation_generator.py`
- **Database:** `config/footprint_schema.sql`

### Module 5: Resume Analyzer
- **Backend:** `backend/app/api/resume.py`, `backend/app/models/resume.py`
- **Frontend:** `frontend/src/pages/resume/`, `frontend/src/components/resume/`
- **Utils:** `utils/resume_parser.py`, `utils/resume_analyzer.py`, `utils/resume_enhancer.py`, `utils/resume_templates.py`
- **Database:** `config/schema.sql` (resumes table)

### Module 6: Job Compatibility Analyzer (NEW - November 4, 2025)
- **Backend:** `backend/app/api/jobs.py` (compatibility endpoint), `backend/app/models/job.py` (JobCompatibilityRequest/Response)
- **Frontend:** `frontend/src/components/jobs/JobCompatibilityAnalyzer.tsx`
- **Utils:** `utils/job_compatibility_analyzer.py` (447 lines)
- **AI:** Groq API (llama-3.3-70b-versatile model)
- **Features:** 
  - AI-powered compatibility analysis
  - Skill matching with fuzzy logic
  - Experience relevance evaluation
  - Education assessment
  - Personalized recommendations
  - AI-generated detailed feedback
- **Scoring:** Overall = Skills(50%) + Experience(35%) + Education(15%)

---

## Complete File Tree

```
Utopia/
├── .env                                    # Environment variables (API keys, DB)
├── .env.production                         # Production environment config
├── .git/                                   # Git repository
├── .gitignore                              # Git ignore rules
├── .pytest_cache/                          # Pytest cache directory
├── README.md                               # Main project README
├── install_dependencies.sh                 # Dependency installation script
├── requirements.txt                        # Python dependencies
│
├── backend/                                # Backend API server
│   ├── __init__.py                         # Backend package initializer
│   ├── __pycache__/                        # Python bytecode cache
│   ├── start.sh                            # Backend startup script
│   ├── uvicorn.log                         # Uvicorn server logs
│   │
│   ├── app/                                # Main application
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── main.py                         # FastAPI entry point
│   │   │
│   │   ├── api/                            # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__/
│   │   │   ├── auth.py                     # Authentication (login, register)
│   │   │   ├── deps.py                     # Dependency injection
│   │   │   ├── footprint.py                # Footprint scanner endpoints
│   │   │   ├── interview.py                # Interview simulator endpoints
│   │   │   ├── jobs.py                     # Job matching/compatibility endpoints
│   │   │   └── resume.py                   # Resume analyzer/cover letter endpoints
│   │   │
│   │   ├── core/                           # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__/
│   │   │   ├── config.py                   # Configuration settings
│   │   │   ├── config.py.bak               # Config backup
│   │   │   ├── database.py                 # Database connection
│   │   │   ├── events.py                   # Application events
│   │   │   └── security.py                 # JWT, password hashing
│   │   │
│   │   ├── models/                         # Pydantic data models
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__/
│   │   │   ├── footprint.py                # Footprint models
│   │   │   ├── interview.py                # Interview models
│   │   │   ├── job.py                      # Job models
│   │   │   ├── resume.py                   # Resume/CoverLetter models
│   │   │   └── user.py                     # User models
│   │   │
│   │   ├── modules/                        # Modular features
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__/
│   │   │   │
│   │   │   ├── auth/                       # Auth module
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── dependencies.py
│   │   │   │   ├── models.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   │
│   │   │   ├── footprint/                  # Footprint module
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   └── router.py
│   │   │   │
│   │   │   ├── interview/                  # Interview module
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   └── router.py
│   │   │   │
│   │   │   ├── jobs/                       # Jobs module
│   │   │   │   ├── __init__.py
│   │   │   │   ├── matcher.py
│   │   │   │   ├── models.py
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── scraper.py
│   │   │   │   └── service.py
│   │   │   │
│   │   │   └── resume/                     # Resume module
│   │   │       ├── __init__.py
│   │   │       ├── __pycache__/
│   │   │       ├── models.py
│   │   │       ├── router.py
│   │   │       ├── schemas.py
│   │   │       ├── service.py
│   │   │       └── utils.py
│   │   │
│   │   └── shared/                         # Shared utilities
│   │       ├── __init__.py
│   │       ├── __pycache__/
│   │       ├── database.py
│   │       ├── dependencies.py
│   │       └── security.py
│   │
│   ├── database/                           # Database scripts
│   │   └── interview_question_bank.sql     # Interview questions seed data
│   │
│   └── migrations/                         # Database migrations
│       ├── create_footprint_tables.py
│       ├── create_interview_tables.py
│       ├── create_jobs_table.py
│       └── create_resumes_table.py
│
├── config/                                 # Configuration files
│   ├── __pycache__/
│   ├── database.py                         # Database config
│   ├── footprint_schema.sql                # Footprint SQL schema
│   ├── interview_schema.sql                # Interview SQL schema
│   ├── job_apis.py                         # Job API configurations
│   └── schema.sql                          # Main database schema
│
├── data/                                   # Data storage
│   ├── outputs/                            # Generated outputs
│   ├── resumes/                            # Uploaded resumes
│   └── scraped_jobs/                       # Scraped job data
│
├── docs/                                   # Documentation
│   ├── FRONTEND_UX_ENHANCEMENTS.md         # UX enhancement plan
│   ├── PROJECT_COMPLETE.md                 # Project completion status
│   ├── PROJECT_STRUCTURE_COMPLETE.md       # This file
│   └── PROJECT_STRUCTURE_COMPLETE_v2.md.bak # Backup
│
├── frontend/                               # React frontend
│   ├── .gitignore
│   ├── .vscode/                            # VS Code settings
│   ├── README.md
│   ├── eslint.config.js                    # ESLint config
│   ├── index.html                          # HTML entry point
│   ├── node_modules/                       # Node dependencies
│   ├── package-lock.json
│   ├── package.json                        # NPM dependencies
│   ├── postcss.config.js                   # PostCSS config
│   ├── tailwind.config.js                  # Tailwind CSS config
│   ├── tsconfig.app.json                   # TS app config
│   ├── tsconfig.json                       # TS base config
│   ├── tsconfig.node.json                  # TS node config
│   ├── vite.config.ts                      # Vite bundler config
│   │
│   ├── public/                             # Static assets
│   │   └── vite.svg
│   │
│   └── src/                                # Source code
│       ├── App.css                         # App styles
│       ├── App.tsx                         # Root component
│       ├── index.css                       # Global CSS (Tailwind)
│       ├── main.tsx                        # Entry point
│       ├── vite-env.d.ts                   # Vite types
│       │
│       ├── assets/                         # Images/icons
│       │   └── react.svg
│       │
│       ├── components/                     # React components
│       │   ├── auth/                       # Auth components (empty)
│       │   │
│       │   ├── common/                     # Shared components
│       │   │   ├── LoadingComponents.tsx   # Loading spinners/states
│       │   │   ├── ProtectedRoute.tsx      # Route authentication
│       │   │   ├── Skeleton.tsx            # Skeleton loaders
│       │   │   └── ThemeToggle.tsx         # Dark mode toggle
│       │   │
│       │   ├── footprint/                  # Footprint components
│       │   │   ├── ActivityChart.tsx       # Activity visualization
│       │   │   ├── FootprintScanForm.tsx   # Scan input form
│       │   │   ├── GitHubContributionGraph.tsx # Contribution heatmap
│       │   │   ├── RecommendationsList.tsx # AI recommendations
│       │   │   └── ScoreGauge.tsx          # Score gauge
│       │   │
│       │   ├── interview/                  # Interview components
│       │   │   ├── InterviewChat.tsx       # Chat interface
│       │   │   ├── InterviewHistory.tsx    # Interview history
│       │   │   ├── InterviewSetup.old.tsx  # Old setup (backup)
│       │   │   └── InterviewSetup.tsx      # Interview config
│       │   │
│       │   ├── jobs/                       # Job components
│       │   │   ├── JobCard.tsx             # Job card
│       │   │   ├── JobChromaGrid.css       # Chroma grid styles
│       │   │   ├── JobChromaGrid.tsx       # Animated job grid
│       │   │   ├── JobCompatibilityAnalyzer.tsx # AI compatibility (NEW)
│       │   │   ├── JobCompatibilityAnalyzer.tsx.bak # Backup
│       │   │   ├── JobDetailModal.tsx      # Job details modal
│       │   │   ├── JobList.tsx             # Jobs list
│       │   │   └── JobMatcher.tsx          # Job matcher
│       │   │
│       │   ├── layout/                     # Layout components
│       │   │   └── DashboardLayout.tsx     # Dashboard layout
│       │   │
│       │   ├── menu/                       # Menu components (empty)
│       │   │
│       │   └── resume/                     # Resume components
│       │       ├── CoverLetterGenerator.tsx # AI cover letter (NEW)
│       │       ├── ResumeAnalysisView.tsx  # Analysis display
│       │       ├── ResumeEnhancement.tsx   # Enhancement UI
│       │       ├── ResumeList.tsx          # Resume list
│       │       ├── ResumeTemplatesModal.tsx # Template selector
│       │       └── ResumeUploadForm.tsx    # Upload form
│       │
│       ├── contexts/                       # React contexts
│       │   ├── AuthContext.tsx             # Auth provider
│       │   ├── ThemeContext.tsx            # Theme provider
│       │   └── ToastContext.tsx            # Toast notifications
│       │
│       ├── hooks/                          # Custom hooks (empty)
│       │
│       ├── pages/                          # Page components
│       │   ├── auth/                       # Auth pages
│       │   │   ├── LoginPage.tsx
│       │   │   └── RegisterPage.tsx
│       │   │
│       │   ├── dashboard/                  # Dashboard pages
│       │   │   ├── DashboardHome.old.tsx   # Old home (backup)
│       │   │   ├── DashboardHome.tsx       # Dashboard home
│       │   │   ├── DashboardPage.tsx       # Dashboard wrapper
│       │   │   └── index.ts                # Exports
│       │   │
│       │   ├── footprint/                  # Footprint pages
│       │   │   ├── FootprintPage.tsx
│       │   │   └── index.ts
│       │   │
│       │   ├── interview/                  # Interview pages
│       │   │   └── index.tsx
│       │   │
│       │   ├── jobs/                       # Jobs pages
│       │   │   └── index.tsx
│       │   │
│       │   └── resume/                     # Resume pages
│       │       ├── ResumePage.tsx
│       │       └── index.ts
│       │
│       ├── schemas/                        # Validation schemas (empty)
│       │
│       ├── services/                       # API services
│       │   ├── api-client.ts               # Axios client
│       │   ├── auth.service.ts             # Auth API
│       │   ├── interview.service.ts        # Interview API
│       │   ├── jobs.service.ts             # Jobs API
│       │   └── resume.service.ts           # Resume API
│       │
│       ├── types/                          # TypeScript types
│       │   └── api.ts                      # API types
│       │
│       └── utils/                          # Utility functions (empty)
│
├── logs/                                   # Application logs
│   └── job_updater.log
│
├── scripts/                                # Utility scripts
│   ├── cli/                                # CLI tools
│   │   └── utopiahire.py                   # CLI interface
│   │
│   └── populate/                           # Data population
│       ├── daily_job_updater.py            # Daily job updater
│       ├── populate_jobs_comprehensive.py  # Comprehensive job population
│       └── quick_populate_jobs.py          # Quick job population
│
├── tests/                                  # Test files
│   ├── __pycache__/
│   ├── test_add_jobs.py                    # Job addition tests
│   ├── test_ai_integration.py              # AI integration tests
│   ├── test_analyzer.py                    # Analyzer tests
│   ├── test_api.py                         # API tests
│   ├── test_auth.py                        # Auth tests
│   ├── test_delete.py                      # Delete operation tests
│   ├── test_enhancement_download.py        # Resume enhancement tests
│   ├── test_footprint.py                   # Footprint tests
│   ├── test_groq_interview.py              # Groq interview tests
│   ├── test_groq_recommendations.py        # Groq recommendation tests
│   ├── test_hf_token.py                    # HuggingFace token tests
│   ├── test_interview_endpoint.py          # Interview endpoint tests
│   ├── test_job_compatibility.py           # Job compatibility tests
│   ├── test_job_matcher.py                 # Job matcher tests
│   ├── test_jobs.py                        # Jobs API tests
│   └── test_resume.py                      # Resume API tests
│
├── utils/                                  # Utility modules
│   ├── __pycache__/
│   ├── cover_letter_generator.py           # AI cover letter generator (NEW)
│   ├── footprint_calculator.py             # Footprint score calculator
│   ├── github_analyzer.py                  # GitHub profile analyzer
│   ├── groq_answer_analyzer.py             # Groq answer analysis
│   ├── groq_recommendation_generator.py    # Groq recommendations
│   ├── interview_simulator.py              # Interview simulation
│   ├── job_compatibility_analyzer.py       # AI job compatibility
│   ├── job_matcher.py                      # Job matching algorithm
│   ├── job_scraper.py                      # Job scraping
│   ├── resume_analyzer.py                  # Resume analysis
│   ├── resume_enhancer.py                  # Resume enhancement
│   ├── resume_parser.py                    # PDF/DOCX parsing
│   ├── resume_templates.py                 # Template generation
│   └── stackoverflow_scanner.py            # StackOverflow scanner
│
└── venv/                                   # Python virtual environment
```

---

## Usage Examples

### Starting the Application

```bash
# Backend
cd backend
./start.sh

# Frontend
cd frontend
npm run dev
```

### Running Tests

```bash
# Individual test scripts (run with Python)
python3 test_add_jobs.py
python3 test_ai_integration.py
python3 test_delete.py
python3 test_enhancement_download.py
python3 test_hf_token.py
python3 test_interview_endpoint.py
python3 test_job_matcher.py
```

### Populating Data

```bash
# Quick job population
python3 quick_populate_jobs.py

# Comprehensive job population
python3 populate_jobs_comprehensive.py

# Daily job updates
python3 daily_job_updater.py
```

---

## Additional Resources

- **Main README:** `/README.md`
- **API Documentation:** `/backend/API_ARCHITECTURE.md`
- **Quick Start Guide:** `/QUICKSTART.md`
- **Testing Guide:** `/QUICK_TEST_GUIDE.md`
- **System Overview:** `/SYSTEM_OVERVIEW.md`

---

## Contact & Support

**Project:** UtopiaHire - AI-Powered Career Platform  
**Documentation Generated:** November 4, 2025  
**Version:** 3.0 (Updated with Job Compatibility Feature)  
**Total Files Documented:** ~180 source files

**Key Updates in v3.0:**
- Added Module 6: Job Compatibility Analyzer with Groq AI
- Reorganized all tests to `tests/` folder (16 tests)
- Consolidated all documentation in `docs/` folder (13+ docs)
- Updated environment variables (added GROQ_API_KEY)
- Enhanced frontend with JobCompatibilityAnalyzer component

For more information, see:
- Main `README.md`
- `docs/JOB_COMPATIBILITY_FEATURE.md` for new feature details
- `docs/DEPLOYMENT.md` for deployment instructions

---

## Update History

### Version 3.0 - November 4, 2025

#### ✅ New Features Added:

1. **Job Compatibility Analyzer (Module 6):**
   - New backend endpoint: `/api/v1/jobs/compatibility`
   - New utility: `utils/job_compatibility_analyzer.py` (447 lines)
   - New frontend component: `JobCompatibilityAnalyzer.tsx` (463 lines)
   - New test: `tests/test_job_compatibility.py`
   - AI-powered analysis using Groq API (llama-3.3-70b-versatile)
   - Features: skill matching, experience evaluation, AI recommendations
   - Scoring: Overall = Skills(50%) + Experience(35%) + Education(15%)

2. **Project Reorganization:**
   - All test files moved to `tests/` folder (16 test files total)
   - All documentation moved to `docs/` folder (13+ markdown files)
   - Updated `.gitignore` to exclude `tests/` from version control

3. **Documentation Updates:**
   - New documentation: `JOB_COMPATIBILITY_FEATURE.md`
   - Consolidated all docs in `docs/` folder
   - Updated PROJECT_STRUCTURE_COMPLETE.md (this file)

#### 📊 Updated Project Statistics (November 4, 2025):
- **Backend:** 23 Python files (API, models, migrations)
- **Frontend:** 44 TypeScript/TSX files (including JobCompatibilityAnalyzer)
- **Utils:** 15 utility scripts (including job_compatibility_analyzer)
- **Config:** 13 configuration files
- **Tests:** 16 Python test scripts (in tests/ folder, ignored by git)
- **Docs:** 20 markdown files (1 README, 13 in docs/, 6 in backend/frontend)
- **Total Source Files:** ~180 files

---

### Version 2.0 - November 3, 2025

#### ✅ Corrections Made:

1. **Added Missing Directories:**
   - `frontend/src/i18n/` with `I18nContext.tsx`
   - `frontend/src/components/auth/` (empty - reserved for future use)
   - `frontend/src/schemas/` (empty - reserved for future use)

2. **Removed Non-Existent Files:**
   - Removed references to 48+ markdown files
   - Removed: `backend.log`, `server.log`, `utopiahire` CLI script
   - Removed test scripts: `test_all.sh`, etc.

3. **Updated File Counts:**
   - Documentation: 55+ → 9 (accurate count)
   - Test Scripts: 13 → 7 (Python scripts only)
   - Frontend TypeScript Files: 42 → 43 (added I18nContext.tsx)
   - Total Files: 195+ → ~160 (accurate count)

#### 📊 Project Statistics (November 3, 2025):
- **Backend:** 23 Python files
- **Frontend:** 43 TypeScript/TSX files
- **Utils:** 14 utility scripts
- **Tests:** 7 Python test scripts
- **Docs:** 9 markdown files
- **Total Source Files:** ~160 files

---

**End of Project Structure Documentation**
