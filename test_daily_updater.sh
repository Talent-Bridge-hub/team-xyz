#!/bin/bash

# Test script for Daily Job Updater
# Tests all functionality before deploying to production

echo "======================================================================"
echo "🧪 TESTING DAILY JOB UPDATER"
echo "======================================================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check script exists and is executable
echo ""
echo "Test 1: Script exists and is executable"
if [ -f "daily_job_updater.py" ]; then
    echo -e "${GREEN}✓${NC} Script exists"
else
    echo -e "${RED}✗${NC} Script not found"
    exit 1
fi

if [ -x "daily_job_updater.py" ]; then
    echo -e "${GREEN}✓${NC} Script is executable"
else
    echo -e "${YELLOW}⚠${NC} Making script executable..."
    chmod +x daily_job_updater.py
fi

# Test 2: Check dependencies
echo ""
echo "Test 2: Check Python dependencies"
python3 -c "import requests; import psycopg2; print('✓ Dependencies OK')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All dependencies installed"
else
    echo -e "${RED}✗${NC} Missing dependencies"
    echo "Install with: pip install requests psycopg2-binary"
    exit 1
fi

# Test 3: Check configuration files
echo ""
echo "Test 3: Check configuration files"
if [ -f "config/job_apis.py" ]; then
    echo -e "${GREEN}✓${NC} API config exists"
else
    echo -e "${RED}✗${NC} config/job_apis.py not found"
    exit 1
fi

if [ -f "utils/job_scraper.py" ]; then
    echo -e "${GREEN}✓${NC} Job scraper exists"
else
    echo -e "${RED}✗${NC} utils/job_scraper.py not found"
    exit 1
fi

# Test 4: Check log directory
echo ""
echo "Test 4: Check log directory"
if [ -d "logs" ]; then
    echo -e "${GREEN}✓${NC} Logs directory exists"
else
    echo -e "${YELLOW}⚠${NC} Creating logs directory..."
    mkdir -p logs
    echo -e "${GREEN}✓${NC} Logs directory created"
fi

# Test 5: Test API usage checker
echo ""
echo "Test 5: Test API usage checker"
python3 daily_job_updater.py --check-usage > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} API usage checker works"
    echo ""
    echo "Current API Usage:"
    python3 daily_job_updater.py --check-usage
else
    echo -e "${RED}✗${NC} API usage checker failed"
    exit 1
fi

# Test 6: Database connection
echo ""
echo "Test 6: Test database connection"
python3 -c "
from config.database import DatabaseWrapper
db = DatabaseWrapper()
result = db.execute_query('SELECT COUNT(*) as count FROM jobs')
print(f'✓ Database connected: {result[0][\"count\"]} jobs in database')
" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Database connection successful"
else
    echo -e "${RED}✗${NC} Database connection failed"
    exit 1
fi

# Test 7: Check cron readiness
echo ""
echo "Test 7: Check cron readiness"
if command -v crontab &> /dev/null; then
    echo -e "${GREEN}✓${NC} Crontab available"
    
    # Check if already in crontab
    if crontab -l 2>/dev/null | grep -q "daily_job_updater.py"; then
        echo -e "${GREEN}✓${NC} Already configured in crontab"
    else
        echo -e "${YELLOW}⚠${NC} Not yet configured in crontab"
        echo "   Run: python3 daily_job_updater.py --setup-cron"
    fi
else
    echo -e "${YELLOW}⚠${NC} Cron not available"
fi

# Test 8: Test search strategy logic
echo ""
echo "Test 8: Test search strategy logic"
python3 -c "
import sys
sys.path.insert(0, '.')
from daily_job_updater import DailyJobUpdater
updater = DailyJobUpdater()
strategy = updater.get_todays_search_strategy()
print(f'✓ Today\\'s strategy: {strategy[\"name\"]}')
print(f'  Number of searches: {len(strategy[\"searches\"])}')
" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Search strategy logic works"
else
    echo -e "${RED}✗${NC} Search strategy logic failed"
    exit 1
fi

# Test 9: Dry run (without actually scraping)
echo ""
echo "Test 9: Dry run test"
echo -e "${YELLOW}⚠${NC} This will test budget calculation and strategy selection"
python3 -c "
import sys
sys.path.insert(0, '.')
from daily_job_updater import DailyJobUpdater
updater = DailyJobUpdater()
budgets, usage = updater.calculate_daily_budget()
print('✓ Budget calculation successful')
print(f'  SerpAPI daily budget: {budgets[\"serpapi\"][\"daily_budget\"]} calls/day')
print(f'  Days remaining: {budgets[\"serpapi\"][\"days_remaining\"]} days')
" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Dry run successful"
else
    echo -e "${RED}✗${NC} Dry run failed"
    exit 1
fi

# Summary
echo ""
echo "======================================================================"
echo "✅ ALL TESTS PASSED!"
echo "======================================================================"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Initial Database Population (optional):"
echo "   python3 quick_populate_jobs.py"
echo ""
echo "2. Test Manual Run:"
echo "   python3 daily_job_updater.py"
echo ""
echo "3. Setup Automation:"
echo "   python3 daily_job_updater.py --setup-cron"
echo "   crontab -e  # Add the cron line shown"
echo ""
echo "4. Monitor:"
echo "   tail -f logs/job_updater.log"
echo ""
echo "======================================================================"
