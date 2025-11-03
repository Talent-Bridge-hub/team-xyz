#!/usr/bin/env python3
"""
Comprehensive Job Database Populator
Scrapes jobs from multiple APIs to fill the database with diverse opportunities
across all regions, job types, and experience levels
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
import time
from datetime import datetime

# API endpoint
API_BASE = "http://127.0.0.1:8000/api/v1"

# You'll need to get a valid auth token first
# For now, we'll use a placeholder - replace with real token
AUTH_TOKEN = "YOUR_AUTH_TOKEN_HERE"

# Comprehensive job search queries
SEARCH_QUERIES = {
    'MENA': {
        'locations': [
            'Tunisia', 'Egypt', 'Cairo', 'Alexandria', 
            'Morocco', 'Casablanca', 'Algeria', 'Algiers',
            'UAE', 'Dubai', 'Abu Dhabi', 'Saudi Arabia', 'Riyadh',
            'Jordan', 'Amman', 'Lebanon', 'Beirut',
            'Qatar', 'Doha', 'Kuwait', 'Bahrain', 'Oman'
        ],
        'queries': [
            'Software Engineer', 'Software Developer',
            'Frontend Developer', 'React Developer', 'Vue Developer',
            'Backend Developer', 'Python Developer', 'Node.js Developer',
            'Full Stack Developer', 'Java Developer', '.NET Developer',
            'Mobile Developer', 'iOS Developer', 'Android Developer',
            'Data Analyst', 'Data Scientist', 'Machine Learning Engineer',
            'DevOps Engineer', 'Cloud Engineer', 'System Administrator',
            'UI/UX Designer', 'Product Designer', 'Graphic Designer',
            'Product Manager', 'Project Manager', 'Scrum Master',
            'Business Analyst', 'QA Engineer', 'Test Automation Engineer',
            'Database Administrator', 'Network Engineer', 'Security Engineer',
            'Sales Manager', 'Marketing Manager', 'HR Manager',
            'Accountant', 'Financial Analyst', 'Customer Support'
        ]
    },
    'Sub-Saharan Africa': {
        'locations': [
            'Nigeria', 'Lagos', 'Abuja', 'Port Harcourt',
            'Kenya', 'Nairobi', 'Mombasa',
            'South Africa', 'Johannesburg', 'Cape Town', 'Pretoria',
            'Ghana', 'Accra', 'Kumasi',
            'Ethiopia', 'Addis Ababa',
            'Tanzania', 'Dar es Salaam',
            'Uganda', 'Kampala',
            'Rwanda', 'Kigali',
            'Senegal', 'Dakar',
            'Zambia', 'Lusaka',
            'Zimbabwe', 'Harare',
            'Cameroon', 'Yaoundé', 'Douala'
        ],
        'queries': [
            'Software Engineer', 'Software Developer',
            'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
            'Mobile Developer', 'Data Analyst', 'Data Scientist',
            'DevOps Engineer', 'Product Manager', 'UI/UX Designer',
            'Business Analyst', 'Project Manager', 'QA Engineer',
            'Sales Representative', 'Marketing Specialist', 'HR Officer',
            'Accountant', 'Financial Analyst', 'Customer Service'
        ]
    },
    'Remote': {
        'locations': [
            'Remote', 'Anywhere', 'Work from Home',
            'Remote - Worldwide', 'Remote - Africa', 'Remote - MENA'
        ],
        'queries': [
            'Remote Software Engineer',
            'Remote Frontend Developer',
            'Remote Backend Developer',
            'Remote Full Stack Developer',
            'Remote Data Analyst',
            'Remote DevOps Engineer',
            'Remote Mobile Developer',
            'Remote UI/UX Designer',
            'Remote Product Manager',
            'Remote Customer Support',
            'Remote Content Writer',
            'Remote Marketing Manager'
        ]
    }
}


def get_auth_token():
    """
    Get authentication token by logging in
    You need to replace with your actual credentials
    """
    login_url = f"{API_BASE}/auth/login"
    
    # Replace with your actual credentials
    credentials = {
        "email": "your_email@example.com",
        "password": "your_password"
    }
    
    try:
        response = requests.post(login_url, json=credentials)
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
        else:
            print(f"Login failed: {response.status_code}")
            print("Please update the credentials in the script")
            return None
    except Exception as e:
        print(f"Error getting token: {e}")
        return None


def scrape_jobs(token, queries, locations, num_results=20):
    """
    Scrape jobs using the backend API
    """
    scrape_url = f"{API_BASE}/jobs/scrape"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "queries": queries,
        "locations": locations,
        "num_results_per_query": num_results
    }
    
    try:
        print(f"\n📡 Scraping jobs...")
        print(f"   Queries: {len(queries)}")
        print(f"   Locations: {len(locations)}")
        print(f"   Results per query: {num_results}")
        
        response = requests.post(scrape_url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"   Jobs scraped: {data.get('jobs_scraped', 0)}")
            print(f"   Jobs stored: {data.get('jobs_stored', 0)}")
            print(f"   API used: {data.get('api_used', 'unknown')}")
            print(f"   Duration: {data.get('scraping_duration_ms', 0)}ms")
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None


def main():
    """
    Main function to populate database with comprehensive job data
    """
    print("=" * 70)
    print("🚀 COMPREHENSIVE JOB DATABASE POPULATOR")
    print("=" * 70)
    print("\nThis script will scrape hundreds of job opportunities across:")
    print("  • MENA region (20+ countries)")
    print("  • Sub-Saharan Africa (15+ countries)")
    print("  • Remote positions (worldwide)")
    print("  • 30+ job titles per region")
    print("\n" + "=" * 70)
    
    # Get authentication token
    print("\n🔐 Step 1: Authentication")
    print("\n⚠️  IMPORTANT: Update the script with your credentials!")
    print("    Edit line 63-64 with your actual email/password")
    print("\nPress Enter to continue (or Ctrl+C to exit and update credentials)...")
    input()
    
    token = get_auth_token()
    if not token:
        print("\n❌ Could not get authentication token")
        print("\n📝 To fix this:")
        print("   1. Edit this script: populate_jobs_comprehensive.py")
        print("   2. Update lines 63-64 with your actual credentials:")
        print("      credentials = {")
        print('          "email": "your_actual_email@example.com",')
        print('          "password": "your_actual_password"')
        print("      }")
        print("   3. Run the script again")
        return
    
    print(f"✅ Authenticated successfully!")
    
    # Scraping strategy
    print("\n" + "=" * 70)
    print("📊 Step 2: Scraping Strategy")
    print("=" * 70)
    
    strategy = [
        {
            'name': 'MENA - High Priority Cities',
            'queries': SEARCH_QUERIES['MENA']['queries'][:10],  # Top 10 job titles
            'locations': ['Cairo', 'Dubai', 'Riyadh', 'Tunis', 'Casablanca'],
            'num_results': 15
        },
        {
            'name': 'Sub-Saharan Africa - Major Cities',
            'queries': SEARCH_QUERIES['Sub-Saharan Africa']['queries'][:10],
            'locations': ['Lagos', 'Nairobi', 'Johannesburg', 'Accra', 'Kigali'],
            'num_results': 15
        },
        {
            'name': 'Remote Opportunities',
            'queries': SEARCH_QUERIES['Remote']['queries'][:8],
            'locations': ['Remote', 'Anywhere'],
            'num_results': 20
        },
        {
            'name': 'MENA - Secondary Cities',
            'queries': SEARCH_QUERIES['MENA']['queries'][10:20],
            'locations': ['Alexandria', 'Abu Dhabi', 'Amman', 'Beirut', 'Doha'],
            'num_results': 10
        },
        {
            'name': 'Sub-Saharan Africa - Growing Cities',
            'queries': SEARCH_QUERIES['Sub-Saharan Africa']['queries'][10:18],
            'locations': ['Dar es Salaam', 'Kampala', 'Dakar', 'Addis Ababa'],
            'num_results': 10
        }
    ]
    
    total_expected = sum(
        len(s['queries']) * len(s['locations']) * s['num_results']
        for s in strategy
    )
    
    print(f"\n📈 Expected to scrape approximately {total_expected} job opportunities")
    print(f"   Across {len(strategy)} batches")
    print("\n⏱️  Estimated time: 5-10 minutes (with API delays)")
    print("\nPress Enter to start scraping...")
    input()
    
    # Execute scraping strategy
    total_scraped = 0
    total_stored = 0
    
    for i, batch in enumerate(strategy, 1):
        print("\n" + "=" * 70)
        print(f"🔄 Batch {i}/{len(strategy)}: {batch['name']}")
        print("=" * 70)
        
        result = scrape_jobs(
            token,
            batch['queries'],
            batch['locations'],
            batch['num_results']
        )
        
        if result:
            total_scraped += result.get('jobs_scraped', 0)
            total_stored += result.get('jobs_stored', 0)
        
        # Delay between batches to respect API limits
        if i < len(strategy):
            print("\n⏳ Waiting 30 seconds before next batch...")
            time.sleep(30)
    
    # Final summary
    print("\n" + "=" * 70)
    print("🎉 SCRAPING COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Final Statistics:")
    print(f"   Total jobs scraped: {total_scraped}")
    print(f"   Total jobs stored: {total_stored}")
    print(f"   Duplicates avoided: {total_scraped - total_stored}")
    
    print("\n✅ Your database is now populated with comprehensive job data!")
    print("\n🔍 Next steps:")
    print("   1. Visit: http://localhost:5174/dashboard/jobs")
    print("   2. Try different filters:")
    print("      • Location: MENA, Sub-Saharan Africa")
    print("      • Job Type: Full-time, Part-time, Contract")
    print("      • Remote Only: Check/Uncheck")
    print("   3. Test job matching with your resume!")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        print("You can run this script again anytime to add more jobs")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Please check the error and try again")
