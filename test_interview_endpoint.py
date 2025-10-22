#!/usr/bin/env python3
"""
Quick test to verify interview endpoint is accessible
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("🧪 Testing Interview Endpoint Registration\n")
print("=" * 60)

# Test 1: Check if endpoint responds to OPTIONS (CORS preflight)
print("\n1️⃣ Testing CORS preflight (OPTIONS)...")
try:
    response = requests.options(f"{BASE_URL}/api/v1/interview/start", timeout=5)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Endpoint is registered and CORS is configured")
    else:
        print(f"   ❌ Unexpected status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Check if endpoint exists (without auth - should get 401 or 422, not 404)
print("\n2️⃣ Testing endpoint existence (POST without auth)...")
try:
    response = requests.post(
        f"{BASE_URL}/api/v1/interview/start",
        json={},
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 404:
        print("   ❌ ENDPOINT NOT FOUND (404) - Router not registered!")
    elif response.status_code in [401, 403]:
        print("   ✅ Endpoint exists! (Authentication required)")
    elif response.status_code == 422:
        print("   ✅ Endpoint exists! (Validation error - missing fields)")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ℹ️  Unexpected status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: List all available routes
print("\n3️⃣ Checking OpenAPI spec for interview routes...")
try:
    response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
    if response.status_code == 200:
        openapi_spec = response.json()
        interview_paths = [path for path in openapi_spec.get('paths', {}).keys() if 'interview' in path]
        
        if interview_paths:
            print(f"   ✅ Found {len(interview_paths)} interview endpoints:")
            for path in interview_paths[:10]:
                print(f"      • {path}")
        else:
            print("   ❌ No interview endpoints found in OpenAPI spec")
    else:
        print(f"   ❌ Could not fetch OpenAPI spec: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("\n✅ Test Complete!")
print("\nIf you see '404 Not Found' above, the router is NOT registered.")
print("If you see '401 Unauthorized' or '422 Validation Error', the router IS working! ✨")
