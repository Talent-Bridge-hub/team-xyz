# 🚀 CareerStar - Complete Setup Guide

This guide will help you set up the CareerStar project from scratch, whether you're a new team member or setting up on a new machine.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Clone Repository](#1-clone-repository)
3. [Install Dependencies](#2-install-dependencies)
4. [Configure Environment](#3-configure-environment)
5. [Set Up Database](#4-set-up-database)
6. [Start Application](#5-start-application)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

| Software | Minimum Version | Check Command | Install Guide |
|----------|----------------|---------------|---------------|
| **Python** | 3.9+ | `python3 --version` | [python.org](https://python.org) |
| **Node.js** | 16+ | `node --version` | [nodejs.org](https://nodejs.org) |
| **PostgreSQL** | 13+ | `psql --version` | See below |
| **Git** | 2.0+ | `git --version` | [git-scm.com](https://git-scm.com) |

### Installing PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Fedora/RHEL:**
```bash
sudo dnf install postgresql-server
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

## 1. Clone Repository

```bash
# Clone the project
git clone https://github.com/Talent-Bridge-hub/team-xyz.git

# Navigate to project directory
cd team-xyz
```

**Verify:**
```bash
ls -la
# You should see: backend/, frontend/, config/, etc.
```

---

## 2. Install Dependencies

Run the automated installation script:

```bash
./install_dependencies.sh
```

### What This Script Does:

✅ **Python Backend:**
- Creates virtual environment (`venv/`)
- Upgrades pip
- Installs all packages from `requirements.txt`
- Downloads NLTK data (punkt, stopwords, taggers)
- Verifies all imports

✅ **Frontend:**
- Installs npm packages
- Sets up React + Vite environment

### Expected Output:
```
========================================
🌟 CareerStar - Dependency Installation
========================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Python Backend Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Activating virtual environment...
⬆️  Upgrading pip...
📥 Installing Python packages...
✅ Python packages installed successfully

📥 Downloading NLTK data...
  ✅ punkt
  ✅ punkt_tab
  ✅ stopwords
  ✅ averaged_perceptron_tagger

🧪 Testing Python imports...
  ✅ FastAPI
  ✅ PostgreSQL
  ✅ Groq API
  [... etc ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 Frontend Dependencies (Node.js)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Frontend packages installed successfully

========================================
✅ Installation Complete!
========================================
```

---

## 3. Configure Environment

### Create Environment File

```bash
cp .env.example .env
```

### Edit `.env` File

Open `.env` in your text editor and configure:

```bash
# ============================================
# Database Configuration
# ============================================
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/careerstar_db
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=careerstar_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# ============================================
# API Keys
# ============================================
# Get from: https://console.groq.com/
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx

# Optional: For GitHub footprint scanner
# Get from: https://github.com/settings/tokens
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxx

# ============================================
# Application Settings
# ============================================
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ENVIRONMENT=development

# CORS Settings
FRONTEND_URL=http://localhost:5173
```

### Get API Keys

1. **Groq API Key** (Required for AI features):
   - Visit: https://console.groq.com/
   - Sign up / Log in
   - Go to API Keys
   - Create new key
   - Copy and paste into `.env`

2. **GitHub Token** (Optional, for footprint scanner):
   - Visit: https://github.com/settings/tokens
   - Generate new token (classic)
   - Select scopes: `repo`, `user`
   - Copy and paste into `.env`

---

## 4. Set Up Database

Run the automated database setup script:

```bash
./setup_database.sh
```

### What This Script Does:

✅ Checks PostgreSQL installation
✅ Creates database (`careerstar_db`)
✅ Runs all SQL schema files:
  - `config/schema.sql` - Users, resumes, analyses
  - `config/footprint_schema.sql` - Footprint scanning
  - `config/interview_schema.sql` - Interview simulator
✅ Runs Python migrations (backup)
✅ Verifies all tables created

### Expected Output:
```
========================================
🗄️  CareerStar - Database Setup
========================================

📋 Loading environment variables...
✅ Environment loaded

📊 Database Configuration:
   Host: localhost
   Port: 5432
   Database: careerstar_db
   User: your_username

✅ PostgreSQL found: psql (PostgreSQL) 13.x
🔍 Testing database connection...
✅ Connected to PostgreSQL

📦 Creating database 'careerstar_db'...
✅ Database created

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Running SQL Schema Files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Running schema.sql...
✅ schema.sql applied successfully

📄 Running footprint_schema.sql...
✅ footprint_schema.sql applied successfully

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Verifying Database Tables
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Database tables created:
   • users
   • resumes
   • analyses
   • jobs
   • interviews
   • footprint_scans

========================================
✅ Database Setup Complete!
========================================
```

---

## 5. Start Application

### Terminal 1: Start Backend

```bash
cd backend
./start.sh
```

**Expected Output:**
```
========================================
🌟 CareerStar API
========================================

📦 Activating virtual environment...
🔍 Checking dependencies...
✅ Core dependencies found

📍 Project root: /path/to/team-xyz
📍 PYTHONPATH: /path/to/team-xyz:/path/to/team-xyz/backend

🚀 Starting CareerStar API Server...
🌐 Server: http://0.0.0.0:8000
🌐 Local: http://127.0.0.1:8000
📚 API Docs: http://127.0.0.1:8000/docs

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in 1234 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

---

## 🌐 Access the Application

Once both servers are running:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:5173 | Main application UI |
| **Backend API** | http://127.0.0.1:8000 | REST API server |
| **API Docs** | http://127.0.0.1:8000/docs | Interactive API documentation |
| **Health Check** | http://127.0.0.1:8000/health | API health status |

### Test the Setup

1. **Visit Frontend:** http://localhost:5173
2. **Register Account:** Click "Sign Up"
3. **Verify Backend:** Check that registration works
4. **Check API Docs:** http://127.0.0.1:8000/docs

---

## Troubleshooting

### Issue: Virtual Environment Not Found

**Error:** `⚠️ Virtual environment not found`

**Solution:**
```bash
python3 -m venv venv
./install_dependencies.sh
```

### Issue: PostgreSQL Connection Failed

**Error:** `❌ Failed to connect to PostgreSQL`

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Verify .env credentials match PostgreSQL user
psql -U your_username -d postgres
```

### Issue: Port Already in Use

**Error:** `Address already in use: 8000` or `5173`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Issue: NLTK Data Not Found

**Error:** `Resource 'punkt' not found`

**Solution:**
```bash
source venv/bin/activate
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

### Issue: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:**
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=/path/to/team-xyz:/path/to/team-xyz/backend:$PYTHONPATH

# Or use start.sh which sets it automatically
cd backend
./start.sh
```

---

## 📚 Additional Resources

- **Project Documentation:** See `/docs` folder
- **API Documentation:** http://127.0.0.1:8000/docs (when running)
- **Database Schema:** `/config/schema.sql`
- **Environment Variables:** `.env.example`

---

## 🎯 Quick Reference Commands

```bash
# Install everything
./install_dependencies.sh

# Set up database
./setup_database.sh

# Start backend
cd backend && ./start.sh

# Start frontend
cd frontend && npm run dev

# Run tests
cd backend && pytest

# Check logs
tail -f logs/backend.log
```

---

## ✅ Setup Complete!

You're now ready to develop on CareerStar! 🚀

If you encounter any issues not covered in this guide, please:
1. Check the `/docs` folder for module-specific documentation
2. Review error logs in `/logs`
3. Contact the team lead

Happy coding! 💻
