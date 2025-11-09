#!/bin/bash
# CareerStar - Complete Dependency Installation
# Installs all required packages for backend and frontend

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the absolute path to the project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo -e "${PURPLE}========================================${NC}"
echo -e "${BLUE}🌟 CareerStar - Dependency Installation${NC}"
echo -e "${PURPLE}========================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "$PROJECT_ROOT/requirements.txt" ]; then
    echo -e "${RED}❌ Error: requirements.txt not found${NC}"
    echo -e "${YELLOW}   Please run this script from the CareerStar root directory${NC}"
    exit 1
fi

# ============================================
# Python Backend Dependencies
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📦 Python Backend Dependencies${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python3 -m venv "$PROJECT_ROOT/venv"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Virtual environment created${NC}"
    else
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${GREEN}📦 Activating virtual environment...${NC}"
source "$PROJECT_ROOT/venv/bin/activate"

# Upgrade pip
echo -e "${GREEN}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip -q

# Install Python packages
echo -e "${GREEN}📥 Installing Python packages from requirements.txt...${NC}"
pip install -r "$PROJECT_ROOT/requirements.txt" -q

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python packages installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install Python packages${NC}"
    exit 1
fi

# Download NLTK data
echo ""
echo -e "${GREEN}📥 Downloading NLTK data...${NC}"
python -c "
import nltk
import os

# Set download directory
nltk_data_dir = os.path.expanduser('~/nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)

print('  📦 Downloading punkt tokenizer...')
nltk.download('punkt', quiet=True)
print('  ✅ punkt')

print('  📦 Downloading punkt_tab...')
nltk.download('punkt_tab', quiet=True)
print('  ✅ punkt_tab')

print('  📦 Downloading stopwords...')
nltk.download('stopwords', quiet=True)
print('  ✅ stopwords')

print('  📦 Downloading averaged_perceptron_tagger...')
nltk.download('averaged_perceptron_tagger', quiet=True)
print('  ✅ averaged_perceptron_tagger')

print('  📦 Downloading averaged_perceptron_tagger_eng...')
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
print('  ✅ averaged_perceptron_tagger_eng')
"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ NLTK data downloaded successfully${NC}"
else
    echo -e "${YELLOW}⚠️  Warning: NLTK data download may have issues${NC}"
fi

# Test imports
echo ""
echo -e "${GREEN}🧪 Testing Python imports...${NC}"
python -c "
import sys

packages = {
    'FastAPI': 'fastapi',
    'Uvicorn': 'uvicorn',
    'PostgreSQL': 'psycopg2',
    'Groq API': 'groq',
    'PyPDF2': 'PyPDF2',
    'python-docx': 'docx',
    'ReportLab': 'reportlab',
    'NLTK': 'nltk',
    'Pydantic': 'pydantic',
    'python-jose': 'jose',
    'passlib': 'passlib',
    'httpx': 'httpx',
    'requests': 'requests',
}

failed = []
for name, module in packages.items():
    try:
        __import__(module)
        print(f'  ✅ {name}')
    except ImportError:
        print(f'  ❌ {name} - FAILED')
        failed.append(name)

if failed:
    print(f'\n⚠️  Failed packages: {', '.join(failed)}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Some Python packages failed to import${NC}"
    exit 1
fi

# ============================================
# Frontend Dependencies
# ============================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🎨 Frontend Dependencies (Node.js)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠️  Node.js is not installed${NC}"
    echo -e "${YELLOW}   Please install Node.js from https://nodejs.org/${NC}"
    echo -e "${YELLOW}   Skipping frontend dependencies...${NC}"
else
    echo -e "${GREEN}📦 Node.js version: $(node --version)${NC}"
    echo -e "${GREEN}📦 npm version: $(npm --version)${NC}"
    echo ""
    
    if [ -d "$PROJECT_ROOT/frontend" ]; then
        echo -e "${GREEN}📥 Installing frontend packages...${NC}"
        cd "$PROJECT_ROOT/frontend"
        
        # Check if node_modules exists
        if [ ! -d "node_modules" ]; then
            npm install
        else
            echo -e "${YELLOW}⚠️  node_modules already exists. Run 'npm install' manually if needed.${NC}"
        fi
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Frontend packages installed successfully${NC}"
        else
            echo -e "${RED}❌ Failed to install frontend packages${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Frontend directory not found${NC}"
    fi
fi

# ============================================
# Summary
# ============================================
echo ""
echo -e "${PURPLE}========================================${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${PURPLE}========================================${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo ""
echo -e "${YELLOW}1. Configure environment:${NC}"
echo -e "   cp .env.example .env"
echo -e "   # Edit .env with your settings"
echo ""
echo -e "${YELLOW}2. Set up database:${NC}"
echo -e "   # Create PostgreSQL database and run schema.sql"
echo ""
echo -e "${YELLOW}3. Start backend:${NC}"
echo -e "   cd backend && ./start.sh"
echo -e "   # or: cd backend && source ../venv/bin/activate && uvicorn app.main:app --reload"
echo ""
echo -e "${YELLOW}4. Start frontend:${NC}"
echo -e "   cd frontend && npm run dev"
echo ""
echo -e "${BLUE}🌐 Access Points:${NC}"
echo -e "   Backend API: http://127.0.0.1:8000"
echo -e "   API Docs: http://127.0.0.1:8000/docs"
echo -e "   Frontend: http://localhost:5173"
echo ""
echo -e "${PURPLE}========================================${NC}"
echo ""
