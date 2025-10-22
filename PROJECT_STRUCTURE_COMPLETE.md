# UtopiaHire - Complete Project Structure

> **Generated:** October 21, 2025  
> **Version:** 1.0  
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
9. [File Count Summary](#file-count-summary)

---

## Project Overview

**UtopiaHire** is a comprehensive AI-powered career platform with 5 core modules:
- **Module 1:** Authentication & User Management
- **Module 2:** Job Matching & Recommendations
- **Module 3:** AI Interview Simulator
- **Module 4:** Digital Footprint Scanner
- **Module 5:** Resume Analyzer & Enhancer

**Tech Stack:**
- **Backend:** Python 3.12, FastAPI, PostgreSQL
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS
- **AI/ML:** HuggingFace (Zephyr-7b-beta, Mistral), spaCy NLP
- **APIs:** GitHub API, StackOverflow API

---

## Root Directory

```
Utopia/
├── .env                                    # Environment variables (API keys, DB credentials)
├── backend.log                             # Backend server logs
├── server.log                              # Additional server logs
├── requirements.txt                        # Python dependencies
├── README.md                               # Main project documentation
├── utopiahire                              # CLI entry point script
│
├── install_dependencies.sh                 # Automated dependency installation
├── status.sh                               # System status checker
├── test_all.sh                             # Run all tests
│
├── daily_job_updater.py                    # Automated job update script
├── populate_jobs_comprehensive.py          # Populate database with jobs
├── quick_populate_jobs.py                  # Quick job population script
│
├── test_add_jobs.py                        # Test job addition
├── test_ai_integration.py                  # Test AI integration
├── test_daily_updater.sh                   # Test daily updater
├── test_delete.py                          # Test delete functionality
├── test_enhancement_download.py            # Test resume enhancement download
├── test_footprint_api.sh                   # Test footprint API
├── test_hf_token.py                        # Test HuggingFace token
├── test_interview_api.sh                   # Test interview API
├── test_interview_endpoint.py              # Test interview endpoint
├── test_job_filters.sh                     # Test job filters
├── test_job_matcher.py                     # Test job matcher
│
└── Documentation Files (48 .md files)
    ├── ADVANCED_SEARCH_ENHANCEMENTS.md
    ├── AI_INTEGRATION_GUIDE.md
    ├── AI_RECOMMENDATIONS_ENHANCEMENT.md
    ├── AUTHENTICATION_FIXED.md
    ├── AUTH_TEST_RESULTS.md
    ├── BACKEND_INTEGRATION_COMPLETE.md
    ├── BILAN_DISPLAY_FIX.md
    ├── CHROMA_GRID_COMPLETE.md
    ├── COMPLETE.md
    ├── COMPLETE_PROJECT_SUMMARY.md
    ├── COMPLETE_SUMMARY.md
    ├── CONVERSATION_SUMMARY.md
    ├── DAILY_JOB_AUTOMATION_GUIDE.md
    ├── DELETE_FEATURE_GUIDE.md
    ├── EDUCATION_SCORING_FIXED.md
    ├── ENDPOINTS_FIXED.md
    ├── ENHANCEMENT_DOWNLOAD_FIX.md
    ├── ENHANCEMENT_FEATURES_STATUS.md
    ├── ENHANCEMENT_FEATURE_COMPLETE.md
    ├── ENHANCEMENT_FIX.md
    ├── FEATURES_WORKING_YES.md
    ├── FILTERS_VERIFICATION_COMPLETE.md
    ├── FINAL_SUMMARY.md
    ├── FIXES_APPLIED.md
    ├── FOOTPRINT_FIX_SUMMARY.md
    ├── FOOTPRINT_MODULE_UI_COMPLETE.md
    ├── FOOTPRINT_THEME_AND_AUTH_FIXES.md
    ├── GITHUB_SKILLS_ENHANCEMENT.md
    ├── HF_TOKEN_FIXED.md
    ├── HOW_TO_POPULATE_JOBS.md
    ├── IMPLEMENTATION_COMPLETE.md
    ├── INTERVIEW_FIXED_AND_READY.md
    ├── INTERVIEW_FIXED_FINAL.md
    ├── INTERVIEW_HISTORY_FIXES.md
    ├── INTERVIEW_QUICKSTART.md
    ├── INTERVIEW_SIMULATOR_IMPLEMENTATION.md
    ├── JOBS_FILTER_TEST_RESULTS.md
    ├── MATCHING_ENHANCEMENTS.md
    ├── MODULE_3_COMPLETE.md
    ├── MODULE_4_COMPLETE.md
    ├── MODULE_4_COMPLETE_OLD.md
    ├── MODULE_4_TESTING_COMPLETE.md
    ├── OVERALL_SCORE_AND_ENHANCEMENT_FIXED.md
    ├── PDF_ENHANCEMENT_FIXES.md
    ├── PROGRESS.md
    ├── PROGRESS_OLD.md
    ├── PROJECT_COMPLETE.md
    ├── QUICKREF.md
    ├── QUICKREF_INTERVIEWER.md
    ├── QUICKREF_JOB_MATCHER.md
    ├── QUICKSTART.md
    ├── QUICK_REFERENCE.txt
    ├── QUICK_TEST_GUIDE.md
    ├── READY_TO_TEST.md
    ├── REQUIREMENTS_ANALYSIS.md
    ├── RESUME_INTERVIEW_FIX.md
    ├── RESUME_MODULE_COMPLETE.md
    ├── RESUME_TESTING_GUIDE.md
    ├── SCORES_FIXED.md
    ├── SESSION_COMPLETE.md
    ├── STATUS.md
    ├── STRICT_SCORING_FIXED.md
    ├── SYSTEM_OVERVIEW.md
    ├── TESTING_READY.md
    ├── VERSION_COMPATIBILITY_REPORT.md
    ├── VIEW_REPORT_BUTTON.md
    ├── VIEW_REPORT_DEBUG.md
    ├── WATCH_LOGS.md
    └── WHERE_ARE_MY_FILES.md
```

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

## Environment Variables

### Root `.env`
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/utopiahire

# API Keys
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
STACKOVERFLOW_API_KEY=optional
```

### Frontend `.env`
```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=UtopiaHire
```

---

## File Count Summary

| Category | Count | Description |
|----------|-------|-------------|
| **Backend Python Files** | 23 | API endpoints, models, core logic |
| **Frontend TypeScript Files** | 42 | Components, pages, services |
| **Utility Scripts** | 14 | Resume parser, job matcher, analyzers |
| **Configuration Files** | 15 | Database, API, build configs |
| **Documentation Files** | 55+ | Markdown documentation |
| **Test Scripts** | 13 | API tests, integration tests |
| **Data Files** | 30+ | Resumes, templates, scraped jobs |
| **SQL Files** | 3 | Database schemas |
| **Total Files** | 195+ | Excluding node_modules, venv, cache |

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

---

## Complete File Tree

```
Utopia/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── deps.py
│   │   │   ├── footprint.py
│   │   │   ├── interview.py
│   │   │   ├── jobs.py
│   │   │   └── resume.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── footprint.py
│   │   │   ├── interview.py
│   │   │   ├── job.py
│   │   │   ├── resume.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── database/
│   │   └── interview_question_bank.sql
│   ├── migrations/
│   │   ├── create_footprint_tables.py
│   │   ├── create_interview_tables.py
│   │   ├── create_jobs_table.py
│   │   └── create_resumes_table.py
│   ├── API_ARCHITECTURE.md
│   ├── AUTH_SYSTEM_COMPLETE.md
│   ├── MODULE_1_COMPLETE.md
│   ├── MODULE_2_COMPLETE.md
│   ├── MODULE_3_COMPLETE.md
│   ├── WEB_PROGRESS_REPORT_1.md
│   ├── WEB_PROGRESS_REPORT_2.md
│   ├── __init__.py
│   ├── requirements.txt
│   ├── start.sh
│   └── test_api.py
│
├── cli/
│   └── utopiahire.py
│
├── config/
│   ├── database.py
│   ├── footprint_schema.sql
│   ├── interview_schema.sql
│   ├── job_apis.py
│   └── schema.sql
│
├── data/
│   ├── outputs/
│   │   ├── sample_resume_analysis_20251014_153141.json
│   │   └── sample_resume_enhanced_20251014_153141.txt
│   ├── resumes/
│   │   ├── templates/
│   │   │   ├── resume_template_Entry-Level_Student_20251015_213500.docx
│   │   │   ├── resume_template_Entry-Level_Student_20251015_213520.docx
│   │   │   ├── resume_template_Entry-Level___Student_20251015_212903.pdf
│   │   │   ├── resume_template_Entry-Level___Student_20251015_212926.pdf
│   │   │   ├── resume_template_Entry-Level___Student_20251015_212935.pdf
│   │   │   ├── resume_template_Entry-Level___Student_20251015_212953.pdf
│   │   │   ├── resume_template_Modern_Skills-Focused_20251015_210443.pdf
│   │   │   ├── resume_template_Modern_Skills-Focused_20251015_212935.pdf
│   │   │   ├── resume_template_Modern_Skills-Focused_20251015_213520.docx
│   │   │   ├── resume_template_Professional_Chronological_20251015_210432.pdf
│   │   │   ├── resume_template_Professional_Chronological_20251015_212935.pdf
│   │   │   ├── resume_template_Professional_Chronological_20251015_213520.docx
│   │   │   ├── resume_template_Professional_Chronological_20251015_213619.docx
│   │   │   ├── resume_template_Professional_Chronological_20251015_213736.docx
│   │   │   ├── resume_template_Professional_Chronological_20251017_084410.docx
│   │   │   └── test_entry.pdf
│   │   ├── 10_20251015_192853_CS & CN & Cyber Challenge.pdf
│   │   ├── 10_20251015_200600_cv-template.pdf
│   │   ├── 10_20251017_213046_cv-template-4.pdf
│   │   ├── 7_20251014_210623_test_resume.docx
│   │   ├── 7_20251014_210725_test_resume.docx
│   │   └── sample_resume.pdf
│   └── scraped_jobs/
│       └── jobs_20251014_165323.json
│
├── docs/
│   ├── API_KEY_SETUP.md
│   ├── FRONTEND_INTEGRATION.md
│   ├── MODULE_2_JOB_MATCHER.md
│   ├── MODULE_3_AI_INTERVIEWER.md
│   ├── MODULE_4_FOOTPRINT_SCANNER.md
│   ├── REAL_JOB_SCRAPING.md
│   └── REAL_JOB_SCRAPING_PLAN.md
│
├── frontend/
│   ├── .vscode/
│   │   ├── extensions.json
│   │   └── settings.json
│   ├── public/
│   │   └── vite.svg
│   ├── src/
│   │   ├── assets/
│   │   │   └── react.svg
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   ├── footprint/
│   │   │   │   ├── ActivityChart.tsx
│   │   │   │   ├── FootprintScanForm.tsx
│   │   │   │   ├── GitHubContributionGraph.tsx
│   │   │   │   ├── RecommendationsList.tsx
│   │   │   │   └── ScoreGauge.tsx
│   │   │   ├── interview/
│   │   │   │   ├── InterviewChat.tsx
│   │   │   │   ├── InterviewHistory.tsx
│   │   │   │   └── InterviewSetup.tsx
│   │   │   ├── jobs/
│   │   │   │   ├── JobCard.tsx
│   │   │   │   ├── JobChromaGrid.css
│   │   │   │   ├── JobChromaGrid.tsx
│   │   │   │   ├── JobDetailModal.tsx
│   │   │   │   ├── JobList.tsx
│   │   │   │   └── JobMatcher.tsx
│   │   │   ├── layout/
│   │   │   │   └── DashboardLayout.tsx
│   │   │   ├── menu/
│   │   │   └── resume/
│   │   │       ├── ResumeAnalysisView.tsx
│   │   │       ├── ResumeEnhancement.tsx
│   │   │       ├── ResumeList.tsx
│   │   │       ├── ResumeTemplatesModal.tsx
│   │   │       └── ResumeUploadForm.tsx
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx
│   │   ├── hooks/
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── LoginPage.tsx
│   │   │   │   └── RegisterPage.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── DashboardHome.tsx
│   │   │   │   ├── DashboardPage.tsx
│   │   │   │   └── index.ts
│   │   │   ├── footprint/
│   │   │   │   ├── FootprintPage.tsx
│   │   │   │   └── index.ts
│   │   │   ├── interview/
│   │   │   │   └── index.tsx
│   │   │   ├── jobs/
│   │   │   │   └── index.tsx
│   │   │   └── resume/
│   │   │       ├── ResumePage.tsx
│   │   │       └── index.ts
│   │   ├── services/
│   │   │   ├── api-client.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── interview.service.ts
│   │   │   ├── jobs.service.ts
│   │   │   └── resume.service.ts
│   │   ├── types/
│   │   │   └── api.ts
│   │   ├── utils/
│   │   ├── App.css
│   │   ├── App.tsx
│   │   ├── index.css
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── .env
│   ├── .gitignore
│   ├── ALL_ERRORS_FIXED.md
│   ├── ERROR_FIXES.md
│   ├── JOBS_UI_COMPLETE.md
│   ├── README.md
│   ├── STATUS_REPORT.md
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
│
├── logs/
│   └── job_updater.log
│
├── models/
│
├── utils/
│   ├── ai_answer_analyzer.py
│   ├── ai_recommendation_generator.py
│   ├── answer_analyzer.py
│   ├── create_sample_resume.py
│   ├── footprint_calculator.py
│   ├── github_analyzer.py
│   ├── interview_simulator.py
│   ├── job_matcher.py
│   ├── job_scraper.py
│   ├── resume_analyzer.py
│   ├── resume_enhancer.py
│   ├── resume_parser.py
│   ├── resume_templates.py
│   ├── resume_templates_pdf_backup.py
│   └── stackoverflow_scanner.py
│
├── .env
├── ADVANCED_SEARCH_ENHANCEMENTS.md
├── AI_INTEGRATION_GUIDE.md
├── AI_RECOMMENDATIONS_ENHANCEMENT.md
├── AUTHENTICATION_FIXED.md
├── AUTH_TEST_RESULTS.md
├── BACKEND_INTEGRATION_COMPLETE.md
├── BILAN_DISPLAY_FIX.md
├── CHROMA_GRID_COMPLETE.md
├── COMPLETE.md
├── COMPLETE_PROJECT_SUMMARY.md
├── COMPLETE_SUMMARY.md
├── CONVERSATION_SUMMARY.md
├── DAILY_JOB_AUTOMATION_GUIDE.md
├── DELETE_FEATURE_GUIDE.md
├── EDUCATION_SCORING_FIXED.md
├── ENDPOINTS_FIXED.md
├── ENHANCEMENT_DOWNLOAD_FIX.md
├── ENHANCEMENT_FEATURES_STATUS.md
├── ENHANCEMENT_FEATURE_COMPLETE.md
├── ENHANCEMENT_FIX.md
├── FEATURES_WORKING_YES.md
├── FILTERS_VERIFICATION_COMPLETE.md
├── FINAL_SUMMARY.md
├── FIXES_APPLIED.md
├── FOOTPRINT_FIX_SUMMARY.md
├── FOOTPRINT_MODULE_UI_COMPLETE.md
├── FOOTPRINT_THEME_AND_AUTH_FIXES.md
├── GITHUB_SKILLS_ENHANCEMENT.md
├── HF_TOKEN_FIXED.md
├── HOW_TO_POPULATE_JOBS.md
├── IMPLEMENTATION_COMPLETE.md
├── INTERVIEW_FIXED_AND_READY.md
├── INTERVIEW_FIXED_FINAL.md
├── INTERVIEW_HISTORY_FIXES.md
├── INTERVIEW_QUICKSTART.md
├── INTERVIEW_SIMULATOR_IMPLEMENTATION.md
├── JOBS_FILTER_TEST_RESULTS.md
├── MATCHING_ENHANCEMENTS.md
├── MODULE_3_COMPLETE.md
├── MODULE_4_COMPLETE.md
├── MODULE_4_COMPLETE_OLD.md
├── MODULE_4_TESTING_COMPLETE.md
├── OVERALL_SCORE_AND_ENHANCEMENT_FIXED.md
├── PDF_ENHANCEMENT_FIXES.md
├── PROGRESS.md
├── PROGRESS_OLD.md
├── PROJECT_COMPLETE.md
├── QUICKREF.md
├── QUICKREF_INTERVIEWER.md
├── QUICKREF_JOB_MATCHER.md
├── QUICKSTART.md
├── QUICK_REFERENCE.txt
├── QUICK_TEST_GUIDE.md
├── README.md
├── READY_TO_TEST.md
├── REQUIREMENTS_ANALYSIS.md
├── RESUME_INTERVIEW_FIX.md
├── RESUME_MODULE_COMPLETE.md
├── RESUME_TESTING_GUIDE.md
├── SCORES_FIXED.md
├── SESSION_COMPLETE.md
├── STATUS.md
├── STRICT_SCORING_FIXED.md
├── SYSTEM_OVERVIEW.md
├── TESTING_READY.md
├── VERSION_COMPATIBILITY_REPORT.md
├── VIEW_REPORT_BUTTON.md
├── VIEW_REPORT_DEBUG.md
├── WATCH_LOGS.md
├── WHERE_ARE_MY_FILES.md
├── backend.log
├── daily_job_updater.py
├── install_dependencies.sh
├── populate_jobs_comprehensive.py
├── quick_populate_jobs.py
├── requirements.txt
├── server.log
├── status.sh
├── test_add_jobs.py
├── test_ai_integration.py
├── test_all.sh
├── test_daily_updater.sh
├── test_delete.py
├── test_enhancement_download.py
├── test_footprint_api.sh
├── test_hf_token.py
├── test_interview_api.sh
├── test_interview_endpoint.py
├── test_job_filters.sh
├── test_job_matcher.py
└── utopiahire
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
# All tests
./test_all.sh

# Specific module tests
./test_footprint_api.sh
./test_interview_api.sh
./test_job_filters.sh
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
**Documentation Generated:** October 21, 2025  
**Total Files Documented:** 195+

For more information, see the main `README.md` file.

---

**End of Project Structure Documentation**
