#!/bin/bash
# Test Interview Simulator API

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZW1haWwiOiJpbnRlcnZpZXdfdGVzdEBleGFtcGxlLmNvbSIsImV4cCI6MTc2MDYyMDk0OH0.w5usoR6R-QvcnqrvtVNCm5zQcVQnBcQn1pNXgdSyULI"
BASE_URL="http://127.0.0.1:8000/api/v1/interview"

echo "========================================"
echo "Testing Interview Simulator API"
echo "========================================"
echo ""

# Test 1: Start Interview Session
echo "1. Starting interview session..."
START_RESPONSE=$(curl -s -X POST "$BASE_URL/start" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"session_type":"mixed","job_role":"Software Engineer","difficulty_level":"mid","num_questions":5}')

echo "$START_RESPONSE" | python3 -m json.tool
SESSION_ID=$(echo "$START_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('session_id', 'ERROR'))")
echo "Session ID: $SESSION_ID"
echo ""

if [ "$SESSION_ID" = "ERROR" ]; then
  echo "❌ Failed to start session"
  exit 1
fi

# Test 2: List Sessions
echo "2. Listing all sessions..."
curl -s -X GET "$BASE_URL/sessions" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

# Test 3: Get Session Stats
echo "3. Getting user statistics..."
curl -s -X GET "$BASE_URL/stats/overview" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "========================================"
echo "✅ Basic tests complete!"
echo "Note: Answer submission needs actual interview flow"
echo "========================================"
