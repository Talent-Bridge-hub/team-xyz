# UtopiaHire - AI-Powered Career Platform

> **A comprehensive AI-powered career platform with 5 integrated modules for job seekers and professionals.**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6.svg)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791.svg)](https://www.postgresql.org/)

---

## 🚀 Features

### 🔐 Module 1: Authentication & User Management
- Secure JWT-based authentication
- User registration and login
- Protected routes and role-based access

### 💼 Module 2: Job Matching & Recommendations
- AI-powered job matching algorithm
- Real-time job scraping from multiple APIs
- Advanced filtering (location, salary, experience)
- Beautiful animated job grid interface

### 🤖 Module 3: AI Interview Simulator
- Interactive AI-powered interview practice
- Real-time answer analysis and feedback
- Question bank with multiple categories and difficulty levels
- Interview history and performance tracking

### 🔍 Module 4: Digital Footprint Scanner
- GitHub profile analysis and contribution graphs
- StackOverflow reputation scanning
- Technical, social, and impact score calculation
- AI-powered career recommendations

### 📄 Module 5: Resume Analyzer & Enhancer
- PDF/DOCX resume parsing
- AI-powered content analysis
- Resume enhancement suggestions
- Professional template generation (3 styles)

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.12)
- **Database:** PostgreSQL
- **ORM/Query:** psycopg2
- **Authentication:** JWT tokens with bcrypt
- **AI/ML:** Groq API (llama-3.3-70b-versatile), spaCy NLP

### Frontend
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** TailwindCSS 3
- **Animations:** Framer Motion
- **HTTP Client:** Axios
- **Routing:** React Router v6

### APIs & Services
- **GitHub API** - Profile and repository analysis
- **StackOverflow API** - Developer reputation tracking
- **Groq API** - Ultra-fast AI inference for recommendations and analysis
- **Job APIs** - Real-time job scraping (3 providers)

---

## 📋 Prerequisites

- **Python:** 3.12 or higher
- **Node.js:** 18.x or higher
- **PostgreSQL:** 13 or higher
- **Git:** Latest version

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone git@github.com:Talent-Bridge-hub/team-xyz.git
cd team-xyz
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and API keys

# Run database migrations
python backend/migrations/create_jobs_table.py
python backend/migrations/create_resumes_table.py
python backend/migrations/create_interview_tables.py
python backend/migrations/create_footprint_tables.py

# Start backend server
cd backend
./start.sh
```

Backend will run on: **http://localhost:8000**

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env if needed (default: VITE_API_BASE_URL=http://localhost:8000)

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:5173**

---

## 🔑 Environment Variables

### Root `.env`

```bash
```bash
# Database
DATABASE_URL=postgresql://utopia_user:your_password@localhost/utopiahire

# API Keys
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx

# Security
SECRET_KEY=your-secret-key-here
```
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs (Optional)
STACKOVERFLOW_API_KEY=your_stackoverflow_key
```

### Frontend `.env`

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=UtopiaHire
```

---

## 📁 Project Structure

```
Utopia/
├── backend/              # FastAPI backend application
│   ├── app/              # Main application code
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality (config, database, security)
│   │   └── models/       # Pydantic models
│   ├── database/         # Database scripts
│   └── migrations/       # Database migrations
│
├── frontend/             # React frontend application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── contexts/     # React contexts
│   │   ├── services/     # API service layer
│   │   └── types/        # TypeScript types
│   └── public/           # Static assets
│
├── utils/                # Shared utility scripts
├── config/               # Configuration files
├── data/                 # Application data (resumes, outputs)
├── docs/                 # Documentation
├── scripts/              # Utility scripts
│   ├── populate/         # Database population scripts
│   └── cli/              # CLI tools
├── tests/                # Test scripts
└── logs/                 # Application logs
```

For complete structure details, see [PROJECT_STRUCTURE_COMPLETE.md](PROJECT_STRUCTURE_COMPLETE.md)

---

## 🧪 Running Tests

```bash
# Run all tests
cd tests
python test_add_jobs.py
python test_ai_integration.py
python test_delete.py
python test_enhancement_download.py
python test_hf_token.py
python test_interview_endpoint.py
python test_job_matcher.py
```

---

## 📊 Database Population

```bash
# Quick job population (fast, smaller dataset)
python scripts/populate/quick_populate_jobs.py

# Comprehensive job population (slower, larger dataset)
python scripts/populate/populate_jobs_comprehensive.py

# Daily job updater (scheduled task)
python scripts/populate/daily_job_updater.py
```

---

## 🎯 API Documentation

Once the backend is running, visit:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📚 Module Documentation

Detailed documentation for each module:

- [Module 1: Authentication](backend/AUTH_SYSTEM_COMPLETE.md)
- [Module 2: Job Matcher](backend/MODULE_2_COMPLETE.md)
- [Module 3: AI Interview](backend/MODULE_3_COMPLETE.md)
- [API Architecture](backend/API_ARCHITECTURE.md)

---

## 🔒 Security

- **Authentication:** JWT tokens with secure password hashing (bcrypt)
- **Environment Variables:** Sensitive data stored in `.env` files (not committed)
- **CORS:** Configured for frontend origins only
- **Input Validation:** Pydantic models for request validation
- **SQL Injection Protection:** Parameterized queries throughout

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is proprietary software. All rights reserved.

---

## 👥 Team

**Talent Bridge Hub - Team XYZ**

---

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Contact the development team

---

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Authentication & User Management
- ✅ Job Matching & Recommendations
- ✅ AI Interview Simulator
- ✅ Digital Footprint Scanner
- ✅ Resume Analyzer & Enhancer

### Phase 2 (Planned)
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] Mobile responsive improvements

### Phase 3 (Future)
- [ ] Machine learning model improvements
- [ ] Real-time chat support
- [ ] Integration with more job boards
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)

---

## 📊 Project Stats

- **Backend Files:** 23 Python files
- **Frontend Files:** 43 TypeScript/TSX files
- **Utility Scripts:** 14 files
- **Total Source Files:** ~160 files
- **Lines of Code:** 15,000+
- **Test Coverage:** 7 test scripts

---

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework for Python
- **React** - A JavaScript library for building user interfaces
- **Groq** - Lightning-fast LLM inference platform
- **TailwindCSS** - Utility-first CSS framework
- **PostgreSQL** - Robust relational database

---

**Made with ❤️ by Team XYZ**
