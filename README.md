# 🌟 UtopiaHire - AI-Powered Career Platform

> **A comprehensive, production-ready AI-powered career platform with 5 integrated modules for job seekers and professionals in MENA & Sub-Saharan Africa.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.1.1-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-3178C6.svg)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg)](https://www.postgresql.org/)
[![Vite](https://img.shields.io/badge/Vite-7.1.7-646CFF.svg)](https://vitejs.dev/)

---

## 📊 Project at a Glance

- **Total Modules**: 5 comprehensive feature modules
- **API Endpoints**: 39 fully documented REST endpoints
- **Database Tables**: 18 optimized PostgreSQL tables with 50+ indexes
- **Backend Dependencies**: 50+ production-grade Python packages
- **Frontend Dependencies**: 20+ modern React ecosystem packages
- **Documentation**: ~9,700+ lines of comprehensive technical documentation
- **Test Coverage**: 15 dedicated test modules covering all features
- **Lines of Code**: Backend (8 API files + 4 migrations), Frontend (12 source directories)

---

## 🚀 Core Features

### 🔐 Module 1: Authentication & User Management
- **Secure JWT-based authentication** with bcrypt password hashing
- User registration and login with email validation
- Protected routes and role-based access control
- Token expiration and refresh mechanisms
- Rate limiting on authentication endpoints (5/minute)

**API Endpoints (6)**: Register, Login, Get Profile, Update Profile, Change Password, Delete Account

### 💼 Module 2: Job Matching & Recommendations
- **AI-powered job matching algorithm** with compatibility scoring
- Real-time job scraping from multiple sources (Google Jobs, LinkedIn, JSearch)
- Advanced filtering by location, salary, experience level, skills
- Job saving and application tracking
- Beautiful animated job grid interface with smooth transitions
- Intelligent fallback strategy across multiple job APIs

**API Endpoints (10)**: Search Jobs, Save Job, Get Saved Jobs, Remove Saved Job, Get Job Details, Get Recommendations, Update Preferences, Get User Jobs, Delete Job, Batch Operations

**Data Sources**: SerpAPI (Google Jobs), LinkedIn RapidAPI, JSearch RapidAPI

### 🤖 Module 3: AI Interview Simulator
- **Interactive AI-powered interview practice** with real-time feedback
- 500+ curated interview questions across multiple categories
- Difficulty levels: Easy, Medium, Hard
- Real-time answer analysis with AI scoring and feedback
- Interview history tracking with performance metrics
- Question categories: Technical, Behavioral, Situational, General

**API Endpoints (8)**: Start Session, Get Questions, Submit Answer, End Session, Get History, Get Feedback, Get Sessions, Delete Session

**AI Engine**: Groq API (llama-3.3-70b-versatile) for ultra-fast response generation

### 🔍 Module 4: Digital Footprint Scanner
- **GitHub profile analysis** with contribution graphs and activity metrics
- **StackOverflow reputation scanning** and expertise tracking
- Multi-platform digital presence assessment (GitHub, StackOverflow, LinkedIn, Twitter)
- Technical, social, and impact score calculation
- Privacy-aware scanning with configurable settings
- AI-powered career recommendations based on footprint analysis

**API Endpoints (5)**: Scan Footprint, Get Scans, Get Scan Details, Update Scan, Delete Scan

**Supported Platforms**: GitHub (full integration), StackOverflow (API integration), LinkedIn (planned), Twitter (planned)

### 📄 Module 5: Resume Analyzer & Enhancer
- **PDF/DOCX resume parsing** with intelligent text extraction
- **AI-powered content analysis** with comprehensive scoring
- Resume structure analysis (sections, formatting, ATS compatibility)
- Skills extraction and categorization
- Professional resume enhancement with AI suggestions
- **3 professional resume templates** (Classic, Modern, Executive)
- **AI-powered cover letter generation** tailored to job descriptions
- **Job compatibility analysis** with detailed insights and recommendations

**API Endpoints (10)**: Upload Resume, Get Resumes, Analyze Resume, Get Analysis, Enhance Resume, Download Enhanced, Generate Cover Letter, Check Compatibility, Delete Resume, Get Templates

**Document Processing**: PyPDF2 3.0.1, python-docx 1.1.0, reportlab 4.0.7

---

## 🛠️ Technology Stack

### Backend (Python 3.9+)

#### Core Framework & API
- **FastAPI** 0.104.1 - Modern async web framework
- **Uvicorn** 0.24.0 [standard] - ASGI server with auto-reload
- **Pydantic** 2.5.0 - Data validation and settings management
- **pydantic-settings** 2.1.0 - Environment configuration

#### Database & Data Layer
- **PostgreSQL** 15+ with advanced features
- **psycopg2-binary** 2.9.9 - PostgreSQL adapter (sync)
- **asyncpg** 0.29.0 - Async PostgreSQL adapter
- **Database Features**:
  - 18 tables organized in 6 modules
  - 50+ optimized indexes (B-tree, GIN, Unique)
  - JSONB columns for flexible data storage
  - Array columns for multi-value fields
  - Triggers and CHECK constraints
  - CASCADE deletes for referential integrity
  - Connection pooling for performance

#### Authentication & Security
- **python-jose[cryptography]** 3.3.0 - JWT token generation
- **passlib[bcrypt]** 1.7.4 - Password hashing
- **python-multipart** 0.0.6 - Form data handling
- **email-validator** 2.1.0 - Email validation

#### AI & Machine Learning
- **Groq API** - Ultra-fast LLM inference (llama-3.3-70b-versatile)
- **nltk** 3.8.1 - Natural Language Processing and text analysis
- **spaCy** (optional) - Advanced NLP features

#### Document Processing
- **PyPDF2** 3.0.1 - PDF parsing and extraction
- **python-docx** 1.1.0 - Word document handling
- **reportlab** 4.0.7 - PDF generation and templates

#### HTTP & External APIs
- **httpx** 0.25.2 - Async HTTP client
- **requests** 2.31.0 - HTTP library for API calls
- **beautifulsoup4** 4.12.2 - HTML parsing
- **lxml** 4.9.3 - XML/HTML processing

#### Development & Testing
- **pytest** 7.4.3 - Testing framework
- **pytest-asyncio** 0.21.1 - Async test support
- **python-dotenv** 1.0.0 - Environment variable management

#### Additional Features
- **slowapi** 0.1.9 - Rate limiting middleware
- **aiofiles** 23.2.1 - Async file operations
- **python-dateutil** 2.8.2 - Date/time utilities

### Frontend (React 19.1.1 + TypeScript 5.9.3)

#### Core Framework
- **React** 19.1.1 - Latest React with concurrent features
- **react-dom** 19.1.1 - React DOM renderer
- **TypeScript** 5.9.3 - Type-safe JavaScript
- **Vite** 7.1.7 - Lightning-fast build tool and dev server

#### Routing & State Management
- **react-router-dom** 7.9.4 - Client-side routing
- **@tanstack/react-query** 5.90.6 - Server state management and caching
- **React Context API** - Global state management

#### HTTP & API Communication
- **axios** 1.12.2 - Promise-based HTTP client

#### Forms & Validation
- **react-hook-form** 7.65.0 - Performant form library
- **zod** 4.1.12 - TypeScript-first schema validation
- **@hookform/resolvers** 5.2.2 - Validation resolvers

#### UI Components & Design
- **@headlessui/react** 2.2.9 - Unstyled, accessible UI components
- **@heroicons/react** 2.2.0 - Beautiful hand-crafted SVG icons
- **lucide-react** 0.546.0 - Icon library
- **react-icons** 5.5.0 - Popular icon packs

#### Styling & Theming
- **tailwindcss** 3.4.18 - Utility-first CSS framework
- **clsx** 2.1.1 - Conditional className utility
- **tailwind-merge** 3.3.1 - Merge Tailwind classes without conflicts
- **@tailwindcss/forms** 0.5.10 - Form styling plugin

#### Animations & Motion
- **framer-motion** 12.23.24 - Production-ready motion library
- **gsap** 3.13.0 - Professional-grade animation library

#### Data Visualization
- **recharts** 3.2.1 - Composable charting library

#### User Experience
- **react-hot-toast** 2.6.0 - Toast notifications

#### Development Tools
- **ESLint** 9.36.0 - Code linting
- **@vitejs/plugin-react** 4.3.4 - Vite React plugin
- **@types/react** 19.0.13 - React TypeScript types

### Database Schema (PostgreSQL 15+)

#### Tables & Organization (18 Total)

**Users & Authentication (2 tables)**
- `users` - User accounts and profiles
- `platform_credentials` - OAuth and external platform tokens

**Resume Management (4 tables)**
- `resumes` - Uploaded resume files and metadata
- `analyses` - AI-powered resume analysis results
- `improved_resumes` - Enhanced resume versions with AI suggestions
- `skills_database` - Extracted skills and categorization

**Jobs Module (3 tables)**
- `jobs` - Scraped job listings with full details
- `saved_jobs` - User-saved job bookmarks
- `job_keywords` - Extracted keywords for matching

**Interview Module (5 tables)**
- `question_bank` - 500+ interview questions (Technical, Behavioral, etc.)
- `interview_sessions` - Practice session tracking
- `interview_questions` - Questions used in sessions
- `interview_answers` - User responses
- `interview_feedback` - AI-generated feedback and scoring

**Digital Footprint (4 tables)**
- `footprint_scans` - Multi-platform scan results
- `github_contributions` - GitHub activity metrics
- `stackoverflow_activity` - SO reputation and answers
- `platform_profiles` - Aggregated profile data

#### Indexes & Performance (50+ Total)
- **B-tree Indexes (35+)**: Foreign keys, timestamps, status fields
- **GIN Indexes (15+)**: JSONB columns, array fields for fast searches
- **Unique Indexes (8+)**: Email, username, platform handles

#### Advanced Features
- **JSONB Columns**: Parsed resume data, job skills, interview feedback, platform data
- **Array Columns**: Skills lists, categories, tags
- **Triggers**: Updated_at timestamp automation
- **CHECK Constraints**: Data validation at DB level
- **CASCADE Deletes**: Referential integrity maintenance
- **Connection Pooling**: Performance optimization

### External APIs & Services

#### AI & Machine Learning
- **Groq API** (llama-3.3-70b-versatile)
  - Ultra-fast LLM inference (< 1 second responses)
  - Resume analysis and enhancement
  - Cover letter generation
  - Interview answer evaluation
  - Career recommendations

#### Job Data Sources (Multi-API Fallback Strategy)
- **SerpAPI** (Google Jobs) - Primary source, 1000+ jobs/search
- **LinkedIn RapidAPI** - Fallback #1, professional network data
- **JSearch RapidAPI** - Fallback #2, aggregated job boards

#### Developer Platform Integrations
- **GitHub API** v3
  - Profile and repository analysis
  - Contribution graphs and activity
  - Language statistics
  - Commit history
- **StackOverflow API** v2.3
  - Reputation tracking
  - Question/answer history
  - Badge and tag expertise
  - Community engagement metrics

---

## 📋 Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+), macOS (Big Sur+), Windows 10+ (WSL2 recommended)
- **Python**: 3.9 or higher (3.11+ recommended for best performance)
- **Node.js**: 18.x or higher (20.x recommended)
- **PostgreSQL**: 13 or higher (15+ recommended)
- **npm**: 9.x or higher (or yarn/pnpm)
- **Git**: Latest version

### API Keys (Required/Optional)
- ✅ **Required**: Groq API key for AI features
- ⭐ **Recommended**: SerpAPI key for job searching
- ⚙️ **Optional**: GitHub token for footprint scanning
- ⚙️ **Optional**: StackOverflow key for footprint scanning
- ⚙️ **Optional**: RapidAPI key for additional job sources

---

## 🚀 Quick Start Guide

### 1. Clone the Repository

```bash
git clone git@github.com:Talent-Bridge-hub/team-xyz.git
cd team-xyz
```

### 2. Database Setup

#### Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql@15

# Start PostgreSQL service
sudo systemctl start postgresql    # Linux
brew services start postgresql@15  # macOS
```

#### Create Database & User

```bash
# Access PostgreSQL shell
sudo -u postgres psql
```

```sql
-- Execute in PostgreSQL shell
CREATE DATABASE utopiahire;
CREATE USER utopia_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE utopiahire TO utopia_user;
ALTER DATABASE utopiahire OWNER TO utopia_user;
\q
```

#### Verify Database Connection

```bash
psql -h localhost -U utopia_user -d utopiahire -c "SELECT version();"
```

### 3. Backend Setup

#### Option A: Automated Setup (Recommended)

```bash
# Install all backend dependencies automatically
./install_dependencies.sh
```

This script will:
- Install all Python packages from `requirements.txt`
- Download NLTK data (punkt, stopwords, averaged_perceptron_tagger)
- Verify all imports and dependencies
- Display installation summary

#### Option B: Manual Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies (50+ packages)
cd backend
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

#### Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual credentials
nano .env  # or use any text editor
```

**Required Configuration**:
```bash
# Database (REQUIRED)
DATABASE_URL=postgresql://utopia_user:your_password@localhost:5432/utopiahire

# AI Engine (REQUIRED)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Security (REQUIRED - Generate with: openssl rand -hex 32)
SECRET_KEY=your_generated_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Job APIs (RECOMMENDED)
SERPAPI_API_KEY=your_serpapi_key_here
JSEARCH_API_KEY=your_rapidapi_key_here

# Footprint APIs (OPTIONAL)
GITHUB_TOKEN=your_github_token_here
STACKOVERFLOW_KEY=your_stackoverflow_key_here
```

📖 **See [Environment Variables](#-environment-variables) section below for complete configuration options.**

#### Run Database Migrations

```bash
# Run all migrations in order (creates 18 tables + 50+ indexes)
cd /home/firas/Utopia
source venv/bin/activate
export PYTHONPATH="/home/firas/Utopia:$PYTHONPATH"

python backend/migrations/create_resumes_table.py
python backend/migrations/create_jobs_table.py
python backend/migrations/create_interview_tables.py
python backend/migrations/create_footprint_tables.py

# Verify all tables were created
psql -h localhost -U utopia_user -d utopiahire -c "\dt"
# Expected: 18 tables
```

#### Start Backend Server

```bash
# Option A: Using the startup script (Recommended)
cd /home/firas/Utopia/backend
./start.sh

# Option B: Manual startup
cd /home/firas/Utopia/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on: **http://localhost:8000**  
**API Documentation (Swagger)**: http://localhost:8000/docs  
**API Documentation (ReDoc)**: http://localhost:8000/redoc

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd /home/firas/Utopia/frontend

# Install dependencies (20+ packages)
npm install
# Or use yarn: yarn install
# Or use pnpm: pnpm install

# (Optional) Configure frontend environment
cp .env.example .env
nano .env  # Edit if needed
```

**Frontend Environment (Optional)**:
```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=UtopiaHire
```

```bash
# Start development server with hot reload
npm run dev
```

Frontend will run on: **http://localhost:5173**

### 5. Verify Installation

#### Test Backend Endpoints

```bash
# Health check
curl http://localhost:8000/

# API documentation
curl http://localhost:8000/docs
```

#### Test Frontend

Open your browser to: http://localhost:5173

You should see the UtopiaHire landing page with:
- ✅ Smooth animations
- ✅ Navigation menu
- ✅ Module cards (Auth, Jobs, Interview, Footprint, Resume)
- ✅ Registration/Login functionality

---

## 🔑 Environment Variables

### Backend Configuration (`.env` in root directory)

Create a `.env` file in the root directory by copying `.env.example`:

```bash
cp .env.example .env
```

#### Required Variables

```bash
# ============================================
# DATABASE CONFIGURATION (REQUIRED)
# ============================================
DATABASE_URL=postgresql://utopia_user:your_password@localhost:5432/utopiahire

# Alternative format (both supported)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=utopiahire
DB_USER=utopia_user
DB_PASSWORD=your_secure_password

# ============================================
# AI CONFIGURATION (REQUIRED)
# ============================================
# Get from: https://console.groq.com/keys
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile

# ============================================
# SECURITY (REQUIRED)
# ============================================
# Generate with: openssl rand -hex 32
SECRET_KEY=your_32_character_hex_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
```

#### Recommended Variables

```bash
# ============================================
# JOB SCRAPING APIs (RECOMMENDED)
# ============================================
# Get from: https://serpapi.com/manage-api-key
SERPAPI_API_KEY=your_serpapi_key_here

# Get from: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
JSEARCH_API_KEY=your_rapidapi_key_here
```

#### Optional Variables

```bash
# ============================================
# FOOTPRINT SCANNER APIs (OPTIONAL)
# ============================================
# Get from: https://github.com/settings/tokens
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Get from: https://stackapps.com/apps/oauth/register
STACKOVERFLOW_KEY=your_stackoverflow_key_here

# ============================================
# APPLICATION SETTINGS (OPTIONAL)
# ============================================
APP_NAME=UtopiaHire
APP_VERSION=1.0.0
DEBUG=true
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# ============================================
# CORS CONFIGURATION (OPTIONAL)
# ============================================
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173

# ============================================
# RATE LIMITING (OPTIONAL)
# ============================================
RATE_LIMIT_ENABLED=true
RATE_LIMIT_AUTH=5/minute
RATE_LIMIT_RESUME=10/hour
RATE_LIMIT_JOBS=5/hour
RATE_LIMIT_INTERVIEW=20/hour
RATE_LIMIT_FOOTPRINT=10/hour

# ============================================
# FILE UPLOAD SETTINGS (OPTIONAL)
# ============================================
MAX_UPLOAD_SIZE=10485760  # 10 MB in bytes
UPLOAD_DIR=/tmp/utopiahire_uploads
```

### Frontend Configuration (Optional)

Create `frontend/.env`:

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=UtopiaHire
```

---

## 📁 Project Structure

```
Utopia/
├── .env                          # Environment variables (DO NOT COMMIT)
├── .env.example                  # Environment template (Safe to commit)
├── .env.production               # Production environment config
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── requirements.txt              # Python dependencies (50+ packages)
├── install_dependencies.sh       # Automated dependency installer
│
├── backend/                      # FastAPI Backend Application
│   ├── app/                      # Main application code
│   │   ├── main.py               # Application entry point (213 lines)
│   │   │                         # - FastAPI app initialization
│   │   │                         # - Lifespan context manager
│   │   │                         # - CORS middleware
│   │   │                         # - Request timing middleware
│   │   │                         # - Exception handlers
│   │   │                         # - Logging configuration
│   │   ├── api/                  # API endpoints (8 files)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py           # Authentication endpoints (6)
│   │   │   ├── deps.py           # Dependency injection utilities
│   │   │   ├── resume.py         # Resume endpoints (10)
│   │   │   ├── jobs.py           # Job endpoints (10)
│   │   │   ├── interview.py      # Interview endpoints (8)
│   │   │   └── footprint.py      # Footprint endpoints (5)
│   │   ├── core/                 # Core functionality
│   │   │   ├── config.py         # Settings and configuration
│   │   │   ├── database.py       # Database connection manager
│   │   │   └── security.py       # JWT and password utilities
│   │   ├── models/               # Pydantic models
│   │   │   ├── user.py           # User models
│   │   │   ├── resume.py         # Resume models
│   │   │   ├── job.py            # Job models
│   │   │   ├── interview.py      # Interview models
│   │   │   └── footprint.py      # Footprint models
│   │   ├── modules/              # Feature modules
│   │   │   ├── resume/           # Resume processing logic
│   │   │   ├── jobs/             # Job scraping and matching
│   │   │   ├── interview/        # Interview AI logic
│   │   │   └── footprint/        # Footprint scanning logic
│   │   └── shared/               # Shared utilities
│   │       ├── groq_client.py    # Groq API client
│   │       ├── pdf_parser.py     # PDF extraction
│   │       └── validators.py     # Custom validators
│   ├── database/                 # Database scripts and utilities
│   ├── migrations/               # Database migrations (4 files)
│   │   ├── create_resumes_table.py
│   │   ├── create_jobs_table.py
│   │   ├── create_interview_tables.py
│   │   └── create_footprint_tables.py
│   ├── start.sh                  # Backend startup script
│   └── uvicorn.log               # Server logs
│
├── frontend/                     # React TypeScript Frontend
│   ├── src/                      # Source code
│   │   ├── main.tsx              # Application entry point
│   │   ├── App.tsx               # Root component
│   │   ├── index.css             # Global styles
│   │   ├── components/           # Reusable React components
│   │   │   ├── auth/             # Auth components (Login, Register)
│   │   │   ├── resume/           # Resume components
│   │   │   ├── jobs/             # Job listing components
│   │   │   ├── interview/        # Interview simulator UI
│   │   │   ├── footprint/        # Footprint dashboard
│   │   │   ├── layout/           # Layout components (Header, Footer)
│   │   │   └── common/           # Shared components (Button, Card, Modal)
│   │   ├── pages/                # Page components (routes)
│   │   │   ├── Home.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Resume.tsx
│   │   │   ├── Jobs.tsx
│   │   │   ├── Interview.tsx
│   │   │   └── Footprint.tsx
│   │   ├── contexts/             # React contexts
│   │   │   ├── AuthContext.tsx   # Authentication state
│   │   │   └── ThemeContext.tsx  # Theme state
│   │   ├── hooks/                # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useApi.ts
│   │   │   └── useDebounce.ts
│   │   ├── services/             # API service layer
│   │   │   ├── api.ts            # Axios instance
│   │   │   ├── authService.ts    # Auth API calls
│   │   │   ├── resumeService.ts  # Resume API calls
│   │   │   ├── jobService.ts     # Job API calls
│   │   │   ├── interviewService.ts
│   │   │   └── footprintService.ts
│   │   ├── types/                # TypeScript type definitions
│   │   │   ├── user.ts
│   │   │   ├── resume.ts
│   │   │   ├── job.ts
│   │   │   ├── interview.ts
│   │   │   └── footprint.ts
│   │   ├── utils/                # Utility functions
│   │   │   ├── format.ts         # Formatters
│   │   │   ├── validation.ts     # Validators
│   │   │   └── storage.ts        # Local storage
│   │   ├── schemas/              # Zod validation schemas
│   │   └── assets/               # Static assets (images, icons)
│   ├── public/                   # Public static files
│   ├── package.json              # Frontend dependencies (20+ packages)
│   ├── vite.config.ts            # Vite configuration
│   ├── tailwind.config.js        # TailwindCSS configuration
│   ├── tsconfig.json             # TypeScript configuration
│   └── eslint.config.js          # ESLint configuration
│
├── config/                       # Configuration files
│   ├── database.py               # Alternative DB config
│   └── settings.json             # App settings
│
├── data/                         # Application data
│   ├── resumes/                  # Uploaded resume files
│   ├── outputs/                  # Generated documents
│   └── scraped_jobs/             # Cached job data
│
├── docs/                         # Comprehensive Documentation (9 files, ~9,700 lines)
│   ├── README.md                 # Documentation index
│   │
│   ├── BACKEND_API_DOCUMENTATION_PART1.md    # API Overview & Auth (6 endpoints)
│   ├── BACKEND_API_DOCUMENTATION_PART2.md    # Resume (10) & Jobs (10) APIs
│   ├── BACKEND_API_DOCUMENTATION_PART3.md    # Interview (8) & Footprint (5) APIs
│   ├── BACKEND_API_DOCUMENTATION_PART4.md    # Operations, Deployment, Testing
│   │
│   ├── DATABASE_DOCUMENTATION_PART1.md       # Foundation & Core Tables
│   ├── DATABASE_DOCUMENTATION_PART2.md       # Enhancement & Jobs Module
│   ├── DATABASE_DOCUMENTATION_PART3.md       # Interview Module (5 tables)
│   ├── DATABASE_DOCUMENTATION_PART4.md       # Footprint Scanner (8 tables)
│   ├── DATABASE_DOCUMENTATION_PART5.md       # Operations & Best Practices
│   ├── DATABASE_README.md                    # Database documentation index
│   │
│   ├── PROJECT_STRUCTURE_COMPLETE.md         # Complete project structure
│   ├── PROJECT_COMPLETE.md                   # Project overview
│   ├── FRONTEND_UX_ENHANCEMENTS.md          # Frontend improvements
│   ├── FOOTPRINT_MODULE_PART1.md            # Footprint feature docs
│   ├── FOOTPRINT_MODULE_PART2.md            # Footprint advanced features
│   ├── RESUME_MODULE_PART1.md               # Resume feature docs
│   ├── RESUME_MODULE_PART2.md               # Resume advanced features
│   ├── INTERVIEW_MODULE_PART1.md            # Interview feature docs
│   ├── INTERVIEW_MODULE_PART2A.md           # Interview Q&A system
│   └── INTERVIEW_MODULE_PART2B.md           # Interview AI feedback
│
├── scripts/                      # Utility scripts
│   ├── cli/                      # Command-line tools
│   └── populate/                 # Database population scripts
│
├── tests/                        # Test suite (15 test files)
│   ├── test_auth.py              # Authentication tests
│   ├── test_resume.py            # Resume module tests
│   ├── test_jobs.py              # Jobs module tests
│   ├── test_interview_endpoint.py
│   ├── test_footprint.py
│   ├── test_groq_implementations.py
│   ├── test_job_matcher.py
│   ├── test_analyzer.py
│   ├── test_ai_integration.py
│   └── [10 more test files]
│
├── utils/                        # Shared utilities across modules
├── logs/                         # Application logs
│   └── *.log                     # Rotating log files
│
└── venv/                         # Python virtual environment (gitignored)
```

---

## 🧪 Testing

### Run All Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests with coverage
cd /home/firas/Utopia
pytest tests/ -v --cov=backend/app --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Run Specific Test Modules

```bash
# Test authentication
pytest tests/test_auth.py -v

# Test resume module
pytest tests/test_resume.py -v

# Test jobs module
pytest tests/test_jobs.py -v

# Test interview module
pytest tests/test_interview_endpoint.py -v

# Test footprint module
pytest tests/test_footprint.py -v

# Test AI integrations
pytest tests/test_groq_implementations.py -v
```

### Test Coverage Breakdown
- **Authentication**: User registration, login, token validation
- **Resume**: Upload, parsing, analysis, enhancement, templates
- **Jobs**: Search, save, recommendations, compatibility
- **Interview**: Session management, questions, answers, feedback
- **Footprint**: GitHub scanning, StackOverflow analysis, scoring
- **AI Integration**: Groq API calls, response parsing, error handling

---

## 📚 Documentation

### Comprehensive Documentation (~9,700 lines)

All documentation is located in the `docs/` directory:

#### Backend API Documentation (~4,500 lines)
- **[Backend API Documentation - Part 1](docs/BACKEND_API_DOCUMENTATION_PART1.md)** - Overview, Architecture, Authentication API (6 endpoints)
- **[Backend API Documentation - Part 2](docs/BACKEND_API_DOCUMENTATION_PART2.md)** - Resume API (10 endpoints), Jobs API (10 endpoints)
- **[Backend API Documentation - Part 3](docs/BACKEND_API_DOCUMENTATION_PART3.md)** - Interview API (8 endpoints), Footprint API (5 endpoints)
- **[Backend API Documentation - Part 4](docs/BACKEND_API_DOCUMENTATION_PART4.md)** - Operations, Deployment, Testing, Database Schema

#### Database Documentation (~5,200 lines)
- **[Database Documentation - Part 1](docs/DATABASE_DOCUMENTATION_PART1.md)** - Foundation & Core Tables (users, resumes, analyses)
- **[Database Documentation - Part 2](docs/DATABASE_DOCUMENTATION_PART2.md)** - Enhancement & Jobs Module (improved_resumes, skills, jobs)
- **[Database Documentation - Part 3](docs/DATABASE_DOCUMENTATION_PART3.md)** - Interview Module (5 tables, 500+ questions)
- **[Database Documentation - Part 4](docs/DATABASE_DOCUMENTATION_PART4.md)** - Footprint Scanner (8 tables, multi-platform)
- **[Database Documentation - Part 5](docs/DATABASE_DOCUMENTATION_PART5.md)** - Operations (50+ indexes, migrations, best practices)
- **[Database README](docs/DATABASE_README.md)** - Database documentation master index

#### Feature-Specific Documentation
- **[Resume Module Documentation](docs/RESUME_MODULE_PART1.md)** - Resume parsing, analysis, enhancement
- **[Interview Module Documentation](docs/INTERVIEW_MODULE_PART1.md)** - AI interview simulator details
- **[Footprint Module Documentation](docs/FOOTPRINT_MODULE_PART1.md)** - Digital footprint scanner
- **[Frontend UX Enhancements](docs/FRONTEND_UX_ENHANCEMENTS.md)** - UI/UX improvements

#### Project Documentation
- **[Project Structure Complete](docs/PROJECT_STRUCTURE_COMPLETE.md)** - Detailed project organization
- **[Project Complete](docs/PROJECT_COMPLETE.md)** - Project overview and architecture
- **[Documentation Index](docs/README.md)** - Master documentation index

### Interactive API Documentation

Start the backend server and visit:
- **Swagger UI**: http://localhost:8000/docs (interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (beautiful API reference)

---

## 🚢 Deployment

### Production Deployment Checklist

#### 1. Environment Configuration
- [ ] Set `DEBUG=false` in `.env`
- [ ] Generate strong `SECRET_KEY` (use `openssl rand -hex 32`)
- [ ] Configure production database with connection pooling
- [ ] Set up environment-specific CORS origins
- [ ] Configure rate limiting for production traffic
- [ ] Set up log rotation and monitoring

#### 2. Database Setup
- [ ] Create production PostgreSQL database
- [ ] Run all migrations in production environment
- [ ] Set up database backups (pg_dump scheduled jobs)
- [ ] Configure database connection pooling (pgbouncer recommended)
- [ ] Set up read replicas for high availability (if needed)

#### 3. Backend Deployment
- [ ] Install production dependencies (`pip install -r requirements.txt`)
- [ ] Configure Gunicorn or uvicorn workers
- [ ] Set up reverse proxy (Nginx recommended)
- [ ] Configure SSL/TLS certificates (Let's Encrypt)
- [ ] Set up systemd service for backend
- [ ] Configure health check endpoints
- [ ] Set up application monitoring (Sentry, DataDog, etc.)

#### 4. Frontend Deployment
- [ ] Build production assets (`npm run build`)
- [ ] Configure API base URL for production
- [ ] Set up CDN for static assets (Cloudflare, AWS CloudFront)
- [ ] Enable gzip/brotli compression
- [ ] Configure caching headers
- [ ] Set up SSL/TLS for frontend domain

#### 5. Security Hardening
- [ ] Enable HTTPS only (HSTS headers)
- [ ] Configure CORS for production domains only
- [ ] Set up rate limiting at reverse proxy level
- [ ] Enable SQL injection protection (parameterized queries already used)
- [ ] Set up WAF (Web Application Firewall) rules
- [ ] Configure CSP (Content Security Policy) headers
- [ ] Enable security headers (X-Frame-Options, X-Content-Type-Options)

#### 6. Monitoring & Logging
- [ ] Set up centralized logging (ELK stack, Loki, etc.)
- [ ] Configure application performance monitoring
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)
- [ ] Configure error tracking (Sentry)
- [ ] Set up database query monitoring
- [ ] Configure alerts for critical issues

### Deployment Commands

#### Backend (Using systemd)

Create `/etc/systemd/system/utopiahire-backend.service`:

```ini
[Unit]
Description=UtopiaHire Backend API
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/utopiahire/backend
Environment="PATH=/var/www/utopiahire/venv/bin"
Environment="PYTHONPATH=/var/www/utopiahire"
ExecStart=/var/www/utopiahire/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable utopiahire-backend
sudo systemctl start utopiahire-backend
```

#### Frontend (Using Nginx)

Create `/etc/nginx/sites-available/utopiahire`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Frontend static files
    root /var/www/utopiahire/frontend/dist;
    index index.html;
    
    # Frontend routing (SPA)
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API proxy
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/utopiahire /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Cloud Deployment Options

#### AWS
- **Backend**: EC2 + Application Load Balancer
- **Database**: RDS PostgreSQL with Multi-AZ
- **Frontend**: S3 + CloudFront CDN
- **Secrets**: AWS Secrets Manager
- **Monitoring**: CloudWatch

#### DigitalOcean
- **Backend**: App Platform or Droplets
- **Database**: Managed PostgreSQL Database
- **Frontend**: App Platform (static sites)
- **Monitoring**: Integrated monitoring

#### Heroku
- **Backend**: Heroku Python app with Gunicorn
- **Database**: Heroku PostgreSQL add-on
- **Frontend**: Heroku Node.js app or Netlify
- **Monitoring**: Heroku Metrics

#### Docker Deployment

Create `Dockerfile` for backend:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: utopiahire
      POSTGRES_USER: utopia_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: .
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://utopia_user:${DB_PASSWORD}@db:5432/utopiahire
      GROQ_API_KEY: ${GROQ_API_KEY}
      SECRET_KEY: ${SECRET_KEY}
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    depends_on:
      - backend
    ports:
      - "80:80"

volumes:
  postgres_data:
```

---

## 🤝 Contributing

### Development Workflow

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** from `main`
4. **Make your changes** with clear commit messages
5. **Write tests** for new features
6. **Run the test suite** to ensure nothing breaks
7. **Push to your fork** and **submit a pull request**

### Code Style Guidelines

#### Python (Backend)
- Follow **PEP 8** style guide
- Use **type hints** for function parameters and returns
- Write **docstrings** for classes and functions
- Maximum line length: 88 characters (Black formatter)
- Sort imports with `isort`

#### TypeScript/React (Frontend)
- Follow **Airbnb Style Guide** for React
- Use **functional components** with hooks
- Write **TypeScript types** for props and state
- Use **ESLint** and **Prettier** for formatting
- Component files: PascalCase (e.g., `UserProfile.tsx`)
- Utility files: camelCase (e.g., `formatDate.ts`)

### Testing Requirements
- Write tests for all new features
- Maintain or improve code coverage
- Test edge cases and error handling
- Use descriptive test names

### Pull Request Process
1. Update documentation if you change functionality
2. Add your changes to the CHANGELOG (if exists)
3. Ensure all tests pass
4. Request review from maintainers
5. Address review comments promptly

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors & Contributors

- **Development Team** - Initial work and ongoing maintenance
- **Contributors** - Thank you to all contributors who have helped improve UtopiaHire!

See the list of [contributors](https://github.com/Talent-Bridge-hub/team-xyz/contributors) who participated in this project.

---

## 🆘 Support & Help

### Getting Help

- **Documentation**: Check the comprehensive docs in `docs/` directory
- **API Docs**: Visit http://localhost:8000/docs after starting backend
- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/Talent-Bridge-hub/team-xyz/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/Talent-Bridge-hub/team-xyz/discussions)

### Common Issues

#### Backend Won't Start
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in `.env`
- Ensure all migrations are run
- Check logs in `backend/uvicorn.log`

#### Frontend Build Fails
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (should be 18+)
- Verify all dependencies: `npm ls`

#### Database Connection Errors
- Test connection: `psql -h localhost -U utopia_user -d utopiahire`
- Verify DATABASE_URL format in `.env`
- Check PostgreSQL logs: `/var/log/postgresql/postgresql-15-main.log`

#### API Key Errors
- Verify Groq API key is valid: https://console.groq.com/keys
- Check API key format in `.env` (no quotes needed)
- Test API key: `curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/...`

---

## 🎉 Acknowledgments

- **FastAPI** - For the excellent modern Python web framework
- **React** - For the powerful frontend library
- **Groq** - For ultra-fast LLM inference
- **PostgreSQL** - For the robust database system
- **Vite** - For the lightning-fast build tool
- **TailwindCSS** - For the utility-first CSS framework
- **All Open Source Contributors** - For the amazing tools and libraries

---

## 📊 Project Roadmap

### Current Version: 1.0.0

### Planned Features

#### Version 1.1.0 (Next Release)
- [ ] Real-time notifications system
- [ ] Email verification for new users
- [ ] Advanced analytics dashboard
- [ ] Job application tracking
- [ ] Resume version history

#### Version 1.2.0
- [ ] Mobile app (React Native)
- [ ] LinkedIn integration for footprint scanner
- [ ] Twitter/X integration for social presence
- [ ] Advanced AI career path recommendations
- [ ] Salary negotiation assistant

#### Version 2.0.0 (Future)
- [ ] Multi-language support (Arabic, French, Swahili)
- [ ] Company profiles and employer dashboard
- [ ] Video interview practice with AI feedback
- [ ] Peer-to-peer mock interviews
- [ ] Marketplace for career services
- [ ] Integration with ATS systems

---

## 📞 Contact

For questions, suggestions, or collaboration opportunities:

- **Email**: support@utopiahire.com (placeholder)
- **GitHub**: https://github.com/Talent-Bridge-hub/team-xyz
- **Twitter**: @UtopiaHire (placeholder)

---

<div align="center">

**Built with ❤️ for job seekers in MENA & Sub-Saharan Africa**

⭐ Star us on GitHub if you find UtopiaHire helpful!

</div>
