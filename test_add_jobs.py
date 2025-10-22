#!/usr/bin/env python3
"""Quick test script to add a few jobs to the database"""

import sys
sys.path.insert(0, '/home/firas/Utopia')

from utils.job_scraper import RealJobScraper
from config import database as db
from datetime import datetime
import json

scraper = RealJobScraper()

# Just 2 quick searches
searches = [
    {'query': 'Software Engineer', 'location': 'Tunis, Tunisia', 'count': 10},
    {'query': 'Data Analyst', 'location': 'Cairo, Egypt', 'count': 10},
]

print("🔍 Fetching jobs...")
total_added = 0

for search in searches:
    print(f"\n  Searching: {search['query']} in {search['location']}")
    
    try:
        jobs = scraper.search_jobs(
            query=search['query'],
            location=search['location'],
            num_results=search['count']
        )
        
        for job in jobs:
            try:
                # Check if exists
                check = db.execute_query("SELECT id FROM jobs WHERE job_id = %s", (job['id'],))
                if check:
                    continue
                
                # Determine region
                location_lower = job['location'].lower()
                if any(k in location_lower for k in ['tunisia', 'egypt', 'morocco', 'algeria', 'uae', 'dubai']):
                    region = 'MENA'
                elif any(k in location_lower for k in ['nigeria', 'kenya', 'south africa']):
                    region = 'Sub-Saharan Africa'
                else:
                    region = 'Other'
                
                # Insert
                db.execute_query("""
                    INSERT INTO jobs (
                        job_id, title, company, location, region, job_type,
                        description, required_skills, url, source, posted_date, 
                        remote, fetched_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    job['id'], job['title'], job['company'], job['location'],
                    region, job.get('job_type', 'Full-time'), job['description'],
                    json.dumps(job.get('skills', [])), job['url'], job.get('source', 'API'),
                    job.get('posted_date', datetime.now().strftime('%Y-%m-%d')),
                    job.get('remote', False), datetime.now().isoformat()
                ), fetch=False)
                
                total_added += 1
                
            except Exception as e:
                print(f"  ⚠️  Error storing job: {e}")
                continue
        
        print(f"  ✅ Added {len(jobs)} jobs")
        
    except Exception as e:
        print(f"  ❌ Search failed: {e}")

print(f"\n✅ Total jobs added: {total_added}")

# Check database
result = db.execute_query("SELECT COUNT(*) as total FROM jobs")
print(f"📊 Total jobs in database: {result[0]['total']}")
