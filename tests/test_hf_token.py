#!/usr/bin/env python3
"""
Test Hugging Face Token Authentication
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("🔐 HUGGING FACE TOKEN VERIFICATION")
print("=" * 70)

token = os.getenv('HUGGINGFACE_TOKEN')

if not token:
    print("\n❌ ERROR: No HUGGINGFACE_TOKEN found in .env file!")
    sys.exit(1)

print(f"\n✅ Token found in environment")
print(f"   Length: {len(token)} characters")
print(f"   Format: {token[:15]}...{token[-8:]}")
print(f"   Valid format: {'✅' if token.startswith('hf_') and len(token) > 30 else '❌'}")

# Test API connection
print("\n" + "=" * 70)
print("🌐 TESTING API CONNECTION")
print("=" * 70)

try:
    from huggingface_hub import InferenceClient
    
    print("\n🔄 Initializing Hugging Face InferenceClient...")
    client = InferenceClient(token=token)
    
    print("✅ Client initialized successfully!")
    
    # Test with a simple prompt
    print("\n🧪 Testing API with simple prompt...")
    try:
        response = client.text_generation(
            "Hello, how are you?",
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_new_tokens=20,
            temperature=0.7
        )
        print("✅ API call successful!")
        print(f"   Response: {response[:100]}...")
        
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg or "not authenticated" in error_msg:
            print(f"\n❌ AUTHENTICATION FAILED!")
            print(f"   Error: {error_msg}")
            print(f"\n💡 Solutions:")
            print(f"   1. Check if token is valid at: https://huggingface.co/settings/tokens")
            print(f"   2. Make sure token has 'Read' permission")
            print(f"   3. Generate new token if expired")
            print(f"   4. Update .env file with correct token")
        else:
            print(f"\n⚠️  API Error (not auth related): {error_msg}")
    
except ImportError:
    print("\n❌ Error: huggingface_hub not installed")
    print("   Run: pip install huggingface_hub")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
