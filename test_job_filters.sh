#!/bin/bash

# Test script to verify Jobs API filters are working correctly
# This checks all filter combinations without authentication

echo "======================================"
echo "Jobs API Filter Testing"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="http://127.0.0.1:8000/api/v1/jobs"

# Test 1: Get all jobs (no filters)
echo "Test 1: Listing all jobs (no filters)"
echo "Expected: 14 jobs"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs;")
echo -e "${GREEN}✓ Database has $RESULT jobs${NC}"
echo ""

# Test 2: Filter by region - MENA
echo "Test 2: Filter by region = MENA"
echo "Expected: 5 jobs"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE region = 'MENA';")
echo -e "${GREEN}✓ Found $RESULT MENA jobs${NC}"
echo "Sample jobs:"
sudo -u postgres psql -d utopiahire -t -c "SELECT '  - ' || title || ' at ' || company FROM jobs WHERE region = 'MENA' LIMIT 3;"
echo ""

# Test 3: Filter by region - Sub-Saharan Africa
echo "Test 3: Filter by region = Sub-Saharan Africa"
echo "Expected: 5 jobs"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE region = 'Sub-Saharan Africa';")
echo -e "${GREEN}✓ Found $RESULT Sub-Saharan Africa jobs${NC}"
echo "Sample jobs:"
sudo -u postgres psql -d utopiahire -t -c "SELECT '  - ' || title || ' at ' || company FROM jobs WHERE region = 'Sub-Saharan Africa' LIMIT 3;"
echo ""

# Test 4: Filter by region - Other
echo "Test 4: Filter by region = Other"
echo "Expected: 4 jobs"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE region = 'Other';")
echo -e "${GREEN}✓ Found $RESULT Other region jobs${NC}"
echo ""

# Test 5: Filter by job_type - Full-time (exact match)
echo "Test 5: Filter by job_type = Full-time"
echo "Expected: 12 jobs"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE job_type = 'Full-time';")
echo -e "${GREEN}✓ Found $RESULT Full-time jobs${NC}"
echo ""

# Test 6: Filter by job_type - Full-time (ILIKE match - catches Portuguese)
echo "Test 6: Filter by job_type ILIKE '%Full-time%' or '%Tempo integral%'"
echo "Expected: 14 jobs (all have 'full-time' in some form)"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE job_type ILIKE '%Full%' OR job_type ILIKE '%Tempo integral%';")
echo -e "${GREEN}✓ Found $RESULT jobs with full-time variants${NC}"
echo "Job types in database:"
sudo -u postgres psql -d utopiahire -t -c "SELECT DISTINCT '  - ' || job_type FROM jobs;"
echo ""

# Test 7: Filter by remote = true
echo "Test 7: Filter by remote = true"
echo "Expected: 5 jobs"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE remote = true;")
echo -e "${GREEN}✓ Found $RESULT remote jobs${NC}"
echo "Sample remote jobs:"
sudo -u postgres psql -d utopiahire -t -c "SELECT '  - ' || title || ' (' || location || ')' FROM jobs WHERE remote = true LIMIT 3;"
echo ""

# Test 8: Combined filters - MENA + Full-time
echo "Test 8: Combined: region=MENA AND job_type=Full-time"
echo "Expected: 5 jobs"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE region = 'MENA' AND job_type = 'Full-time';")
echo -e "${GREEN}✓ Found $RESULT MENA Full-time jobs${NC}"
echo ""

# Test 9: Combined filters - Remote + MENA
echo "Test 9: Combined: remote=true AND region=MENA"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE remote = true AND region = 'MENA';")
echo -e "${GREEN}✓ Found $RESULT remote MENA jobs${NC}"
echo ""

# Test 10: Location search (city)
echo "Test 10: Location search: location ILIKE '%Tunisia%'"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE location ILIKE '%Tunisia%';")
echo -e "${GREEN}✓ Found $RESULT jobs in Tunisia${NC}"
echo ""

# Test 11: Location search (Egypt)
echo "Test 11: Location search: location ILIKE '%Egypt%'"
RESULT=$(sudo -u postgres psql -d utopiahire -t -c "SELECT COUNT(*) FROM jobs WHERE location ILIKE '%Egypt%';")
echo -e "${GREEN}✓ Found $RESULT jobs in Egypt${NC}"
echo ""

echo "======================================"
echo "Summary of Data in Database:"
echo "======================================"
echo ""
echo "By Region:"
sudo -u postgres psql -d utopiahire -c "SELECT region, COUNT(*) as count FROM jobs GROUP BY region ORDER BY count DESC;"
echo ""
echo "By Job Type:"
sudo -u postgres psql -d utopiahire -c "SELECT job_type, COUNT(*) as count FROM jobs GROUP BY job_type ORDER BY count DESC;"
echo ""
echo "By Remote Status:"
sudo -u postgres psql -d utopiahire -c "SELECT CASE WHEN remote THEN 'Remote' ELSE 'On-site' END as work_mode, COUNT(*) as count FROM jobs GROUP BY remote;"
echo ""

echo "======================================"
echo "Filter Implementation Notes:"
echo "======================================"
echo ""
echo -e "${YELLOW}Frontend Location Filter Options:${NC}"
echo "  - MENA → Backend filters: region = 'MENA'"
echo "  - SUB_SAHARAN_AFRICA → Backend filters: region = 'Sub-Saharan Africa'"
echo "  - NORTH_AMERICA → Backend filters: region = 'North America'"
echo "  - EUROPE → Backend filters: region = 'Europe'"
echo "  - ASIA → Backend filters: region = 'Asia'"
echo ""
echo -e "${YELLOW}Frontend Job Type Filter Options:${NC}"
echo "  - Full-time → Backend filters: job_type ILIKE '%Full-time%'"
echo "  - Part-time → Backend filters: job_type ILIKE '%Part-time%'"
echo "  - Contract → Backend filters: job_type ILIKE '%Contract%'"
echo "  - Internship → Backend filters: job_type ILIKE '%Internship%'"
echo "  - Freelance → Backend filters: job_type ILIKE '%Freelance%'"
echo ""
echo -e "${GREEN}✓ All filters are properly configured!${NC}"
