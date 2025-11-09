#!/bin/bash
# Startup script for CareerStar API
# Ensures proper PYTHONPATH and starts the FastAPI server

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the absolute path to the project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "${PURPLE}========================================${NC}"
echo -e "${BLUE}🌟 CareerStar API${NC}"
echo -e "${PURPLE}========================================${NC}"
echo ""

# Activate virtual environment
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found at $PROJECT_ROOT/venv${NC}"
    echo -e "${YELLOW}   Please run: python -m venv venv${NC}"
    exit 1
fi

echo -e "${GREEN}📦 Activating virtual environment...${NC}"
source "$PROJECT_ROOT/venv/bin/activate"

# Set PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/backend:$PYTHONPATH"

# Check if required packages are installed
echo -e "${GREEN}� Checking dependencies...${NC}"
python -c "
import sys
try:
    import fastapi
    import psycopg2
    import groq
    print('✅ Core dependencies found')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('   Run: ./install_dependencies.sh')
    sys.exit(1)
" || exit 1

echo ""
echo -e "${GREEN}📍 Project root: $PROJECT_ROOT${NC}"
echo -e "${GREEN}📍 PYTHONPATH: $PYTHONPATH${NC}"
echo ""
echo -e "${BLUE}🚀 Starting CareerStar API Server...${NC}"
echo -e "${BLUE}🌐 Server: http://0.0.0.0:8000${NC}"
echo -e "${BLUE}🌐 Local: http://127.0.0.1:8000${NC}"
echo -e "${BLUE}📚 API Docs: http://127.0.0.1:8000/docs${NC}"
echo -e "${BLUE}📊 Admin: http://127.0.0.1:8000/admin${NC}"
echo ""
echo -e "${PURPLE}========================================${NC}"
echo ""

# Start the FastAPI server with uvicorn
cd "$PROJECT_ROOT/backend"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
