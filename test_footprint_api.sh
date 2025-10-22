#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# API base URL
BASE_URL="http://127.0.0.1:8000/api/v1/footprint"

# Test user token (interview_test user)
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OCwidXNlcm5hbWUiOiJpbnRlcnZpZXdfdGVzdCIsImVtYWlsIjoiaW50ZXJ2aWV3LnRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3NjAyODQ0NzN9.3QJsX43pYEqt1GgVbV1t4oQyqFbhGCVr5QXhv6WRdlY"

echo "========================================="
echo "Testing Footprint Scanner API - With Fix"
echo "========================================="
echo ""

# Test: Get recommendations for existing scan
echo "Testing Recommendations Endpoint (Scan ID: 1)..."
echo "This should now work without JSON parsing errors"
echo ""
curl -s "$BASE_URL/scans/1/recommendations" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "========================================="
echo "Test Complete!"
echo "========================================="