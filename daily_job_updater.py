#!/usr/bin/env python3
"""
Daily Job Updater with Smart API Usage Management
Automatically updates job opportunities daily while respecting API limits

FEATURES:
- Runs automatically every day
- Smart API usage tracking (stays within monthly limits)
- Calculates daily budget based on remaining days in month
- Prioritizes different regions/roles each day
- Removes old jobs (30+ days)
- Logs all operations for monitoring

USAGE:
  python daily_job_updater.py                    # Run once manually
  python daily_job_updater.py --setup-cron       # Setup daily automation
  python daily_job_updater.py --check-usage      # Check API usage stats
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.job_scraper import RealJobScraper
from config import database as db
from config.job_apis import API_CREDENTIALS
from datetime import datetime, timedelta
from calendar import monthrange
import json
import time
import logging
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/firas/Utopia/logs/job_updater.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DailyJobUpdater:
    """
    Smart daily job updater that manages API usage carefully
    """
    
    def __init__(self):
        self.scraper = RealJobScraper()
        self.usage_file = '/home/firas/Utopia/logs/api_usage.json'
        self.ensure_log_directory()
    
    def ensure_log_directory(self):
        """Create logs directory if it doesn't exist"""
        os.makedirs('/home/firas/Utopia/logs', exist_ok=True)
    
    def load_api_usage(self):
        """Load API usage stats from file"""
        try:
            if os.path.exists(self.usage_file):
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load usage file: {e}")
        
        # Return default structure
        current_month = datetime.now().strftime('%Y-%m')
        return {
            'month': current_month,
            'serpapi': 0,
            'linkedin_rapidapi': 0,
            'jsearch_rapidapi': 0,
            'last_updated': None
        }
    
    def save_api_usage(self, usage):
        """Save API usage stats to file"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(usage, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save usage file: {e}")
    
    def reset_usage_if_new_month(self, usage):
        """Reset usage counters if it's a new month"""
        current_month = datetime.now().strftime('%Y-%m')
        
        if usage['month'] != current_month:
            logger.info(f"📅 New month detected! Resetting API usage counters")
            usage = {
                'month': current_month,
                'serpapi': 0,
                'linkedin_rapidapi': 0,
                'jsearch_rapidapi': 0,
                'last_updated': None
            }
        
        return usage
    
    def calculate_daily_budget(self):
        """
        Calculate how many API calls we can make today
        Ensures we don't run out before month ends
        """
        usage = self.load_api_usage()
        usage = self.reset_usage_if_new_month(usage)
        
        # Get days remaining in month
        now = datetime.now()
        days_in_month = monthrange(now.year, now.month)[1]
        days_remaining = days_in_month - now.day + 1
        
        # Calculate daily budget for each API
        budgets = {}
        
        for api_name, api_config in API_CREDENTIALS.items():
            used = usage.get(api_name, 0)
            limit = api_config['free_limit']
            remaining = limit - used
            
            # Reserve 10% for emergencies
            safe_remaining = int(remaining * 0.9)
            
            # Calculate daily budget
            daily = max(1, safe_remaining // days_remaining)
            
            budgets[api_name] = {
                'limit': limit,
                'used': used,
                'remaining': remaining,
                'safe_remaining': safe_remaining,
                'daily_budget': daily,
                'days_remaining': days_remaining
            }
            
            logger.info(f"📊 {api_name}: {used}/{limit} used, {daily} calls/day budget")
        
        return budgets, usage
    
    def get_todays_search_strategy(self):
        """
        Determine what to search today based on day of week
        This distributes searches across different regions/roles
        """
        day_of_week = datetime.now().weekday()  # 0=Monday, 6=Sunday
        
        strategies = {
            0: {  # Monday - MENA Tech
                'name': 'MENA Tech Jobs',
                'searches': [
                    {'query': 'Software Engineer', 'location': 'Cairo, Egypt', 'count': 10},
                    {'query': 'Frontend Developer', 'location': 'Dubai, UAE', 'count': 10},
                    {'query': 'Backend Developer', 'location': 'Tunis, Tunisia', 'count': 10},
                ]
            },
            1: {  # Tuesday - Sub-Saharan Africa Tech
                'name': 'Sub-Saharan Africa Tech Jobs',
                'searches': [
                    {'query': 'Software Engineer', 'location': 'Lagos, Nigeria', 'count': 10},
                    {'query': 'Full Stack Developer', 'location': 'Nairobi, Kenya', 'count': 10},
                    {'query': 'Mobile Developer', 'location': 'Johannesburg, South Africa', 'count': 10},
                ]
            },
            2: {  # Wednesday - Data & Analytics
                'name': 'Data & Analytics Jobs',
                'searches': [
                    {'query': 'Data Analyst', 'location': 'Casablanca, Morocco', 'count': 10},
                    {'query': 'Data Scientist', 'location': 'Accra, Ghana', 'count': 10},
                    {'query': 'Business Intelligence', 'location': 'Riyadh, Saudi Arabia', 'count': 10},
                ]
            },
            3: {  # Thursday - DevOps & Cloud
                'name': 'DevOps & Cloud Jobs',
                'searches': [
                    {'query': 'DevOps Engineer', 'location': 'Amman, Jordan', 'count': 10},
                    {'query': 'Cloud Engineer', 'location': 'Kigali, Rwanda', 'count': 10},
                    {'query': 'Site Reliability Engineer', 'location': 'Doha, Qatar', 'count': 10},
                ]
            },
            4: {  # Friday - Design & Product
                'name': 'Design & Product Jobs',
                'searches': [
                    {'query': 'UI/UX Designer', 'location': 'Beirut, Lebanon', 'count': 10},
                    {'query': 'Product Manager', 'location': 'Kampala, Uganda', 'count': 10},
                    {'query': 'Product Designer', 'location': 'Dar es Salaam, Tanzania', 'count': 10},
                ]
            },
            5: {  # Saturday - Remote Opportunities
                'name': 'Remote Opportunities',
                'searches': [
                    {'query': 'Remote Software Engineer', 'location': 'Remote', 'count': 15},
                    {'query': 'Remote Full Stack Developer', 'location': 'Anywhere', 'count': 15},
                ]
            },
            6: {  # Sunday - Mixed (all regions, popular roles)
                'name': 'Popular Roles (All Regions)',
                'searches': [
                    {'query': 'Full Stack Developer', 'location': 'Egypt', 'count': 10},
                    {'query': 'Software Engineer', 'location': 'Kenya', 'count': 10},
                    {'query': 'Frontend Developer', 'location': 'Morocco', 'count': 10},
                ]
            }
        }
        
        return strategies[day_of_week]
    
    def store_job_in_db(self, job_data):
        """Store a single job in the database"""
        try:
            # Check if job already exists
            check_query = "SELECT id FROM jobs WHERE job_id = %s"
            existing = db.execute_query(check_query, (job_data['id'],))
            
            if existing:
                return False  # Already exists
            
            # Determine region based on location
            region = self._determine_region(job_data['location'])
            
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
                job_data.get('job_type', 'Full-time'),
                job_data.get('experience_level'),
                job_data['description'],
                json.dumps(job_data.get('skills', [])),
                json.dumps([]),
                json.dumps(job_data.get('salary_range')) if job_data.get('salary_range') else None,
                job_data.get('posted_date'),
                job_data.get('remote', False),
                job_data['url'],
                job_data.get('source', 'API'),
                datetime.now().isoformat()
            ), fetch=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Error storing job: {e}")
            return False
    
    def _determine_region(self, location):
        """Determine region based on location string"""
        location_lower = location.lower()
        
        mena_keywords = [
            'egypt', 'tunisia', 'morocco', 'algeria', 'uae', 'dubai', 
            'saudi', 'jordan', 'lebanon', 'qatar', 'kuwait', 'bahrain', 
            'oman', 'cairo', 'tunis', 'casablanca', 'riyadh', 'amman', 
            'beirut', 'doha', 'abu dhabi', 'alexandria', 'rabat', 'jeddah',
            'mecca', 'medina', 'muscat', 'manama', 'kuwait city'
        ]
        
        africa_keywords = [
            'nigeria', 'kenya', 'south africa', 'ghana', 'ethiopia',
            'tanzania', 'uganda', 'rwanda', 'senegal', 'zambia',
            'lagos', 'nairobi', 'johannesburg', 'accra', 'kigali',
            'kampala', 'dakar', 'dar es salaam', 'pretoria', 'cape town',
            'durban', 'abuja', 'kano', 'kumasi', 'addis ababa'
        ]
        
        if any(keyword in location_lower for keyword in mena_keywords):
            return 'MENA'
        elif any(keyword in location_lower for keyword in africa_keywords):
            return 'Sub-Saharan Africa'
        else:
            return 'Other'
    
    def cleanup_old_jobs(self):
        """Remove jobs older than 30 days"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            delete_query = "DELETE FROM jobs WHERE posted_date < %s"
            result = db.execute_query(delete_query, (cutoff_date,), fetch=False)
            
            logger.info(f"🗑️  Cleaned up jobs older than {cutoff_date}")
            
        except Exception as e:
            logger.error(f"Error cleaning up old jobs: {e}")
    
    def run_daily_update(self):
        """
        Main function - runs daily job update
        """
        logger.info("=" * 70)
        logger.info("🚀 STARTING DAILY JOB UPDATE")
        logger.info("=" * 70)
        
        # Calculate budget
        budgets, usage = self.calculate_daily_budget()
        
        # Get today's search strategy
        strategy = self.get_todays_search_strategy()
        logger.info(f"📋 Today's Strategy: {strategy['name']}")
        logger.info(f"🔍 Planned searches: {len(strategy['searches'])}")
        
        # Check if we have enough budget
        total_calls_needed = len(strategy['searches'])
        serpapi_budget = budgets['serpapi']['daily_budget']
        
        if serpapi_budget < total_calls_needed:
            logger.warning(f"⚠️  Daily budget ({serpapi_budget}) < searches needed ({total_calls_needed})")
            logger.warning(f"   Limiting to {serpapi_budget} searches")
            strategy['searches'] = strategy['searches'][:serpapi_budget]
        
        # Run searches
        total_scraped = 0
        total_stored = 0
        api_calls_made = 0
        
        for i, search in enumerate(strategy['searches'], 1):
            logger.info(f"\n🔄 Search {i}/{len(strategy['searches'])}")
            logger.info(f"   Query: {search['query']}")
            logger.info(f"   Location: {search['location']}")
            
            try:
                # Scrape jobs
                jobs = self.scraper.search_jobs(
                    query=search['query'],
                    location=search['location'],
                    num_results=search['count']
                )
                
                api_calls_made += 1
                
                if jobs:
                    logger.info(f"   ✅ Scraped {len(jobs)} jobs")
                    
                    # Store in database
                    stored_count = 0
                    for job in jobs:
                        if self.store_job_in_db(job):
                            stored_count += 1
                    
                    logger.info(f"   💾 Stored {stored_count} new jobs (skipped {len(jobs) - stored_count} duplicates)")
                    
                    total_scraped += len(jobs)
                    total_stored += stored_count
                else:
                    logger.warning("   ⚠️  No jobs found")
                
            except Exception as e:
                logger.error(f"   ❌ Error: {e}")
            
            # Delay between searches (respect rate limits)
            if i < len(strategy['searches']):
                delay = 3
                time.sleep(delay)
        
        # Update usage
        api_used = self.scraper.last_api_used or 'serpapi'
        usage[api_used] = usage.get(api_used, 0) + api_calls_made
        usage['last_updated'] = datetime.now().isoformat()
        self.save_api_usage(usage)
        
        # Cleanup old jobs
        logger.info("\n🗑️  Cleaning up old jobs...")
        self.cleanup_old_jobs()
        
        # Generate summary
        logger.info("\n" + "=" * 70)
        logger.info("✅ DAILY UPDATE COMPLETE")
        logger.info("=" * 70)
        logger.info(f"\n📊 Statistics:")
        logger.info(f"   Jobs scraped: {total_scraped}")
        logger.info(f"   New jobs stored: {total_stored}")
        logger.info(f"   API calls made: {api_calls_made}")
        logger.info(f"   API used: {api_used}")
        
        # Get database stats
        try:
            count_query = "SELECT COUNT(*) as total FROM jobs"
            result = db.execute_query(count_query)
            total_in_db = result[0]['total'] if result else 0
            
            logger.info(f"\n📈 Database Summary:")
            logger.info(f"   Total jobs: {total_in_db}")
            
            # Recent jobs (last 7 days)
            recent_query = """
                SELECT COUNT(*) as count 
                FROM jobs 
                WHERE posted_date >= %s
            """
            recent_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            recent_result = db.execute_query(recent_query, (recent_date,))
            recent_count = recent_result[0]['count'] if recent_result else 0
            
            logger.info(f"   Jobs from last 7 days: {recent_count}")
            
        except Exception as e:
            logger.error(f"Could not fetch database stats: {e}")
        
        logger.info("\n" + "=" * 70)
    
    def check_usage_stats(self):
        """Display API usage statistics"""
        usage = self.load_api_usage()
        usage = self.reset_usage_if_new_month(usage)
        
        print("\n" + "=" * 70)
        print("📊 API USAGE STATISTICS")
        print("=" * 70)
        print(f"\nMonth: {usage['month']}")
        print(f"Last Updated: {usage.get('last_updated', 'Never')}")
        
        print("\n📈 Usage by API:")
        for api_name, api_config in API_CREDENTIALS.items():
            used = usage.get(api_name, 0)
            limit = api_config['free_limit']
            percentage = (used / limit) * 100 if limit > 0 else 0
            
            print(f"\n  {api_name}:")
            print(f"    Used: {used}/{limit} ({percentage:.1f}%)")
            print(f"    Remaining: {limit - used}")
            
            # Progress bar
            bar_length = 30
            filled = int((used / limit) * bar_length) if limit > 0 else 0
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"    [{bar}]")
        
        # Calculate remaining budget
        now = datetime.now()
        days_in_month = monthrange(now.year, now.month)[1]
        days_remaining = days_in_month - now.day + 1
        
        print(f"\n📅 Days remaining this month: {days_remaining}")
        
        print("\n💰 Daily Budget:")
        for api_name, api_config in API_CREDENTIALS.items():
            used = usage.get(api_name, 0)
            limit = api_config['free_limit']
            remaining = limit - used
            safe_remaining = int(remaining * 0.9)
            daily = max(1, safe_remaining // days_remaining)
            
            print(f"  {api_name}: {daily} calls/day")
        
        print("\n" + "=" * 70)


def setup_cron_job():
    """
    Setup cron job to run daily at 2 AM
    """
    print("\n" + "=" * 70)
    print("⚙️  SETTING UP DAILY AUTOMATION")
    print("=" * 70)
    
    script_path = os.path.abspath(__file__)
    cron_command = f"0 2 * * * cd {os.path.dirname(script_path)} && /usr/bin/python3 {script_path} >> /home/firas/Utopia/logs/cron.log 2>&1"
    
    print("\n📋 Add this line to your crontab:")
    print(f"\n  {cron_command}")
    print("\n📝 To add it:")
    print("  1. Run: crontab -e")
    print("  2. Paste the line above")
    print("  3. Save and exit")
    print("\n⏰ This will run daily at 2:00 AM")
    print("\n" + "=" * 70)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Daily Job Updater')
    parser.add_argument('--setup-cron', action='store_true', help='Show cron setup instructions')
    parser.add_argument('--check-usage', action='store_true', help='Check API usage statistics')
    
    args = parser.parse_args()
    
    updater = DailyJobUpdater()
    
    if args.setup_cron:
        setup_cron_job()
    elif args.check_usage:
        updater.check_usage_stats()
    else:
        # Run daily update
        updater.run_daily_update()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
