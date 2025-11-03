#!/usr/bin/env python3
"""
Test script to verify interview session deletion works
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_delete():
    # First, login to get a token
    login_data = {
        "username": "testuser",  # Update with actual username
        "password": "testpass"   # Update with actual password
    }
    
    print("1. Attempting to login...")
    login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"   Response: {login_response.text}")
        return
    
    token = login_response.json().get("access_token")
    print(f"✅ Login successful! Token: {token[:20]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get list of sessions
    print("\n2. Getting list of sessions...")
    sessions_response = requests.get(f"{BASE_URL}/interview/sessions", headers=headers)
    
    if sessions_response.status_code != 200:
        print(f"❌ Failed to get sessions: {sessions_response.status_code}")
        print(f"   Response: {sessions_response.text}")
        return
    
    sessions = sessions_response.json().get("sessions", [])
    print(f"✅ Found {len(sessions)} sessions")
    
    if not sessions:
        print("⚠️  No sessions to test deletion")
        return
    
    # Try to delete the last session
    session_to_delete = sessions[-1]["id"]
    print(f"\n3. Attempting to delete session {session_to_delete}...")
    
    delete_response = requests.delete(
        f"{BASE_URL}/interview/{session_to_delete}",
        headers=headers
    )
    
    print(f"   Status Code: {delete_response.status_code}")
    print(f"   Response: {delete_response.text}")
    
    if delete_response.status_code == 200:
        print("✅ Session deleted successfully!")
        
        # Verify it's gone
        print("\n4. Verifying deletion...")
        verify_response = requests.get(f"{BASE_URL}/interview/sessions", headers=headers)
        new_sessions = verify_response.json().get("sessions", [])
        print(f"   Sessions count before: {len(sessions)}")
        print(f"   Sessions count after: {len(new_sessions)}")
        
        if len(new_sessions) == len(sessions) - 1:
            print("✅ Deletion verified!")
        else:
            print("⚠️  Session count mismatch")
    else:
        print(f"❌ Delete failed: {delete_response.status_code}")

if __name__ == "__main__":
    test_delete()
