#!/usr/bin/env python3
"""
Quick Job Database Populator (No Authentication Required)
Uses the job scraper directly to populate the database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.job_scraper import RealJobScraper
from config import database as db
from datetime import datetime
import json
import time

# Initialize
scraper = RealJobScraper()

# Job search configuration
QUICK_SEARCHES = [
    # MENA Region
    {'query': 'Software Engineer', 'location': 'Cairo, Egypt', 'count': 20},
    {'query': 'Frontend Developer', 'location': 'Dubai, UAE', 'count': 15},
    {'query': 'Data Analyst', 'location': 'Tunis, Tunisia', 'count': 15},
    {'query': 'Backend Developer', 'location': 'Casablanca, Morocco', 'count': 15},
    {'query': 'Full Stack Developer', 'location': 'Riyadh, Saudi Arabia', 'count': 15},
    {'query': 'Mobile Developer', 'location': 'Amman, Jordan', 'count': 10},
    {'query': 'DevOps Engineer', 'location': 'Beirut, Lebanon', 'count': 10},
    {'query': 'Product Manager', 'location': 'Doha, Qatar', 'count': 10},
    
    # Sub-Saharan Africa
    {'query': 'Software Engineer', 'location': 'Lagos, Nigeria', 'count': 20},
    {'query': 'Data Analyst', 'location': 'Nairobi, Kenya', 'count': 15},
    {'query': 'Frontend Developer', 'location': 'Johannesburg, South Africa', 'count': 15},
    {'query': 'Backend Developer', 'location': 'Accra, Ghana', 'count': 15},
    {'query': 'Mobile Developer', 'location': 'Kigali, Rwanda', 'count': 10},
    {'query': 'Full Stack Developer', 'location': 'Dar es Salaam, Tanzania', 'count': 10},
    {'query': 'UI/UX Designer', 'location': 'Kampala, Uganda', 'count': 10},
    {'query': 'Business Analyst', 'location': 'Dakar, Senegal', 'count': 10},
    
    # Remote
    {'query': 'Remote Software Engineer', 'location': 'Anywhere', 'count': 20},
    {'query': 'Remote Frontend Developer', 'location': 'Remote', 'count': 15},
    {'query': 'Remote Data Analyst', 'location': 'Remote', 'count': 15},
    {'query': 'Remote Full Stack Developer', 'location': 'Work from Home', 'count': 15},
]


def store_job_in_db(job_data):
    """Store a single job in the database"""
    try:
        # Check if job already exists
        check_query = "SELECT id FROM jobs WHERE job_id = %s"
        existing = db.execute_query(check_query, (job_data['id'],))
        
        if existing:
            return False  # Already exists
        
        # Determine region based on location
        region = 'Other'
        location_lower = job_data['location'].lower()
        
        mena_keywords = ['egypt', 'tunisia', 'morocco', 'algeria', 'uae', 'dubai', 
                        'saudi', 'jordan', 'lebanon', 'qatar', 'kuwait', 'bahrain', 
                        'oman', 'cairo', 'tunis', 'casablanca', 'riyadh', 'amman', 
                        'beirut', 'doha', 'abu dhabi']
        
        africa_keywords = ['nigeria', 'kenya', 'south africa', 'ghana', 'ethiopia',
                          'tanzania', 'uganda', 'rwanda', 'senegal', 'zambia',
                          'lagos', 'nairobi', 'johannesburg', 'accra', 'kigali',
                          'kampala', 'dakar', 'dar es salaam']
        
        if any(keyword in location_lower for keyword in mena_keywords):
            region = 'MENA'
        elif any(keyword in location_lower for keyword in africa_keywords):
            region = 'Sub-Saharan Africa'
        elif 'anywhere' in location_lower or 'remote' in location_lower:
            region = 'Other'
        
        # Insert job
        insert_query = """
            INSERT INTO jobs (
                job_id, title, company, location, region, job_type,
                experience_level, description, required_skills, preferred_skills,
                salary_range, posted_date, remote, url, source, fetched_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        
        db.execute_query(insert_query, (
            job_data['id'],
            job_data['title'],
            job_data['company'],
            job_data['location'],
            region,
            job_data.get('type', 'Full-time'),
            job_data.get('experience_level'),
            job_data['description'],
            json.dumps(job_data.get('skills', [])),
            json.dumps([]),
            json.dumps(job_data.get('salary')) if job_data.get('salary') else None,
            job_data.get('posted_date'),
            job_data.get('remote', False),
            job_data['url'],
            job_data.get('source', 'API'),
            datetime.now().isoformat()
        ), fetch=False)
        
        return True
        
    except Exception as e:
        print(f"   ⚠️  Error storing job: {e}")
        return False


def main():
    """Main function"""
    print("=" * 70)
    print("🚀 QUICK JOB DATABASE POPULATOR")
    print("=" * 70)
    print("\nThis script will scrape approximately 300+ jobs from free APIs")
    print("  • No authentication required")
    print("  • Uses 3 free APIs with automatic fallback")
    print("  • Covers MENA, Sub-Saharan Africa, and Remote positions")
    print("\n" + "=" * 70)
    
    print("\n⏱️  Estimated time: 5-10 minutes")
    print("    (Includes delays to respect API rate limits)")
    
    print("\n🔍 APIs available:")
    print("    1. SerpAPI - 100 searches/month")
    print("    2. LinkedIn RapidAPI - 500 requests/month")
    print("    3. JSearch RapidAPI - 250 requests/month")
    
    print("\nPress Enter to start...")
    input()
    
    total_scraped = 0
    total_stored = 0
    
    for i, search in enumerate(QUICK_SEARCHES, 1):
        print(f"\n{'=' * 70}")
        print(f"🔄 Search {i}/{len(QUICK_SEARCHES)}")
        print(f"{'=' * 70}")
        print(f"   Query: {search['query']}")
        print(f"   Location: {search['location']}")
        print(f"   Target: {search['count']} jobs")
        
        try:
            # Scrape jobs
            jobs = scraper.search_jobs(
                query=search['query'],
                location=search['location'],
                num_results=search['count']
            )
            
            if jobs:
                print(f"   ✅ Scraped {len(jobs)} jobs")
                
                # Store in database
                stored_count = 0
                for job in jobs:
                    if store_job_in_db(job):
                        stored_count += 1
                
                print(f"   💾 Stored {stored_count} new jobs (skipped {len(jobs) - stored_count} duplicates)")
                
                total_scraped += len(jobs)
                total_stored += stored_count
            else:
                print("   ⚠️  No jobs found")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Delay between searches
        if i < len(QUICK_SEARCHES):
            delay = 3  # 3 seconds between searches
            print(f"   ⏳ Waiting {delay} seconds...")
            time.sleep(delay)
    
    # Final summary
    print("\n" + "=" * 70)
    print("🎉 SCRAPING COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Statistics:")
    print(f"   Total jobs scraped: {total_scraped}")
    print(f"   New jobs stored: {total_stored}")
    print(f"   Duplicates skipped: {total_scraped - total_stored}")
    
    # Check database totals
    try:
        count_query = "SELECT COUNT(*) as total FROM jobs"
        result = db.execute_query(count_query)
        total_in_db = result[0]['total'] if result else 0
        
        print(f"\n📈 Database Summary:")
        print(f"   Total jobs in database: {total_in_db}")
        
        # Count by region
        region_query = "SELECT region, COUNT(*) as count FROM jobs GROUP BY region ORDER BY count DESC"
        regions = db.execute_query(region_query)
        print(f"\n   Jobs by Region:")
        for row in regions:
            print(f"      • {row['region']}: {row['count']}")
        
        # Count by type
        type_query = "SELECT job_type, COUNT(*) as count FROM jobs GROUP BY job_type ORDER BY count DESC LIMIT 5"
        types = db.execute_query(type_query)
        print(f"\n   Top Job Types:")
        for row in types:
            print(f"      • {row['job_type']}: {row['count']}")
        
        # Count remote
        remote_query = "SELECT COUNT(*) as count FROM jobs WHERE remote = true"
        remote_result = db.execute_query(remote_query)
        remote_count = remote_result[0]['count'] if remote_result else 0
        print(f"\n   Remote Jobs: {remote_count}")
        
    except Exception as e:
        print(f"\n⚠️  Could not fetch database stats: {e}")
    
    print("\n✅ Your database is now populated!")
    print("\n🔍 Next steps:")
    print("   1. Visit: http://localhost:5174/dashboard/jobs")
    print("   2. Try the filters:")
    print("      • Location: MENA → should show 100+ jobs")
    print("      • Location: Sub-Saharan Africa → should show 100+ jobs")
    print("      • Job Type: Full-time")
    print("      • Remote Only: Check the box")
    print("   3. Go to 'Matched for You' tab and match jobs with your resume!")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
