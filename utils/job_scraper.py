"""
Real Job Scraper - Multi-API with Automatic Fallback
Fetches REAL job opportunities from multiple sources with intelligent fallback

FEATURES:
- SerpAPI (primary) - Google Jobs aggregation
- LinkedIn RapidAPI (fallback #1)
- JSearch RapidAPI (fallback #2)
- Automatic fallback on rate limits or failures
- Caches results to minimize API calls
- Regional filtering (MENA, Sub-Saharan Africa)
"""

import requests
import logging
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from urllib.parse import urlencode

# Import API credentials
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.job_apis import get_api_credentials, get_all_apis_by_priority

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealJobScraper:
    """
    Scrapes real jobs from multiple APIs with automatic fallback
    """
    
    def __init__(self):
        """Initialize scraper with API credentials"""
        self.apis = get_all_apis_by_priority()
        self.cache = {}
        self.cache_expiry = timedelta(hours=6)  # Cache for 6 hours
        self.last_api_used = None
        logger.info("Real Job Scraper initialized with 3 APIs")
    
    def search_jobs(
        self,
        query: str,
        location: str = 'Tunisia',
        num_results: int = 20
    ) -> List[Dict]:
        """
        Search for jobs using multiple APIs with automatic fallback
        
        Args:
            query: Job title or keywords (e.g., "Software Engineer")
            location: Location/city/country (e.g., "Tunisia", "Lagos, Nigeria")
            num_results: Number of results to fetch (max 50)
        
        Returns:
            List of job dictionaries
        """
        # Check cache first
        cache_key = f"{query}_{location}_{num_results}"
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < self.cache_expiry:
                logger.info(f"✓ Using cached results for '{query}' in {location}")
                return cached_data
        
        logger.info(f"Searching for '{query}' jobs in {location}...")
        
        # Try each API in priority order
        for api_name, api_config in self.apis:
            try:
                logger.info(f"Trying {api_name}...")
                
                if api_name == 'serpapi':
                    jobs = self._search_serpapi(query, location, num_results)
                elif api_name == 'linkedin_rapidapi':
                    jobs = self._search_linkedin_rapidapi(query, location, num_results)
                elif api_name == 'jsearch_rapidapi':
                    jobs = self._search_jsearch_rapidapi(query, location, num_results)
                else:
                    continue
                
                if jobs:
                    logger.info(f"✓ Successfully fetched {len(jobs)} jobs from {api_name}")
                    self.last_api_used = api_name
                    
                    # Cache results
                    self.cache[cache_key] = (jobs, datetime.now())
                    
                    return jobs
                
            except Exception as e:
                logger.warning(f"✗ {api_name} failed: {e}")
                continue
        
        # All APIs failed
        logger.error("✗ All APIs failed! Using fallback sample data")
        return self._get_fallback_jobs(query, location)
    
    def _search_serpapi(self, query: str, location: str, num_results: int) -> List[Dict]:
        """
        Search using SerpAPI (Google Jobs)
        """
        creds = get_api_credentials('serpapi')
        
        params = {
            'engine': 'google_jobs',
            'q': query,
            'location': location,
            'api_key': creds['api_key'],
            'num': min(num_results, 50)
        }
        
        response = requests.get(creds['endpoint'], params=params, timeout=10)
        
        if response.status_code == 429:
            raise Exception("Rate limit exceeded")
        
        response.raise_for_status()
        data = response.json()
        
        # Parse SerpAPI response
        jobs = []
        for job_data in data.get('jobs_results', [])[:num_results]:
            # IMPORTANT: Extract best available URL for frontend "Apply Now" button
            # Priority: related_links > apply_options > share_url > search fallback
            job_url = ''
            
            # Try apply options first (direct apply links)
            apply_options = job_data.get('apply_options', [])
            if apply_options and len(apply_options) > 0:
                job_url = apply_options[0].get('link', '')
            
            # Try related links (company career page, LinkedIn, etc.)
            if not job_url:
                related_links = job_data.get('related_links', [])
                for link in related_links:
                    if 'apply' in link.get('text', '').lower() or 'career' in link.get('text', '').lower():
                        job_url = link.get('link', '')
                        break
            
            # Fallback to share URL
            if not job_url:
                job_url = job_data.get('share_url', '')
            
            # Last resort: construct Google Jobs search link
            if not job_url:
                job_title = job_data.get('title', '').replace(' ', '+')
                company = job_data.get('company_name', '').replace(' ', '+')
                job_url = f"https://www.google.com/search?q={job_title}+{company}+jobs&ibp=htl;jobs"
            
            job = {
                'id': f"serp_{job_data.get('job_id', '')}",
                'title': job_data.get('title', 'N/A'),
                'company': job_data.get('company_name', 'N/A'),
                'location': job_data.get('location', location),
                'description': job_data.get('description', ''),
                'url': job_url,  # ALWAYS has a valid URL now
                'posted_date': self._parse_date(job_data.get('detected_extensions', {}).get('posted_at', '')),
                'source': 'SerpAPI (Google Jobs)',
                'salary_range': self._extract_salary(job_data.get('detected_extensions', {})),
                'job_type': job_data.get('detected_extensions', {}).get('schedule_type', 'Full-time'),
                'remote': 'remote' in job_data.get('description', '').lower(),
                'skills': [],  # SerpAPI doesn't provide skills directly
                'fetched_at': datetime.now().isoformat()
            }
            jobs.append(job)
        
        return jobs
    
    def _search_linkedin_rapidapi(self, query: str, location: str, num_results: int) -> List[Dict]:
        """
        Search using LinkedIn RapidAPI
        """
        creds = get_api_credentials('linkedin_rapidapi')
        
        headers = {
            'x-rapidapi-host': creds['host'],
            'x-rapidapi-key': creds['api_key']
        }
        
        params = {
            'offset': 0,
            'description_type': 'text'
        }
        
        response = requests.get(creds['endpoint'], headers=headers, params=params, timeout=10)
        
        if response.status_code == 429:
            raise Exception("Rate limit exceeded")
        
        response.raise_for_status()
        data = response.json()
        
        # Parse LinkedIn API response
        jobs = []
        job_list = data.get('data', [])[:num_results] if isinstance(data, dict) else data[:num_results]
        
        for job_data in job_list:
            job = {
                'id': f"linkedin_{job_data.get('id', '')}",
                'title': job_data.get('title', 'N/A'),
                'company': job_data.get('company', 'N/A'),
                'location': job_data.get('location', location),
                'description': job_data.get('description', ''),
                'url': job_data.get('url', ''),
                'posted_date': job_data.get('posted_date', ''),
                'source': 'LinkedIn',
                'salary_range': None,
                'job_type': job_data.get('employment_type', 'Full-time'),
                'remote': job_data.get('remote', False),
                'skills': job_data.get('skills', []),
                'fetched_at': datetime.now().isoformat()
            }
            jobs.append(job)
        
        return jobs
    
    def _search_jsearch_rapidapi(self, query: str, location: str, num_results: int) -> List[Dict]:
        """
        Search using JSearch RapidAPI
        """
        creds = get_api_credentials('jsearch_rapidapi')
        
        headers = {
            'x-rapidapi-host': creds['host'],
            'x-rapidapi-key': creds['api_key']
        }
        
        # Determine country code from location
        country = self._location_to_country_code(location)
        
        params = {
            'query': f"{query} jobs in {location}",
            'page': 1,
            'num_pages': 1,
            'country': country,
            'date_posted': 'all'
        }
        
        response = requests.get(creds['endpoint'], headers=headers, params=params, timeout=10)
        
        if response.status_code == 429:
            raise Exception("Rate limit exceeded")
        
        response.raise_for_status()
        data = response.json()
        
        # Parse JSearch API response
        jobs = []
        for job_data in data.get('data', [])[:num_results]:
            job = {
                'id': f"jsearch_{job_data.get('job_id', '')}",
                'title': job_data.get('job_title', 'N/A'),
                'company': job_data.get('employer_name', 'N/A'),
                'location': f"{job_data.get('job_city', '')}, {job_data.get('job_country', location)}",
                'description': job_data.get('job_description', ''),
                'url': job_data.get('job_apply_link', ''),
                'posted_date': job_data.get('job_posted_at_datetime_utc', ''),
                'source': 'JSearch',
                'salary_range': self._parse_jsearch_salary(job_data),
                'job_type': job_data.get('job_employment_type', 'Full-time'),
                'remote': job_data.get('job_is_remote', False),
                'skills': job_data.get('job_required_skills', []),
                'fetched_at': datetime.now().isoformat()
            }
            jobs.append(job)
        
        return jobs
    
    def _location_to_country_code(self, location: str) -> str:
        """Convert location to country code for APIs"""
        location_lower = location.lower()
        
        country_codes = {
            'tunisia': 'tn',
            'egypt': 'eg',
            'morocco': 'ma',
            'algeria': 'dz',
            'nigeria': 'ng',
            'kenya': 'ke',
            'south africa': 'za',
            'ghana': 'gh',
            'ethiopia': 'et',
            'united states': 'us',
            'united kingdom': 'uk',
            'france': 'fr',
            'germany': 'de'
        }
        
        for country, code in country_codes.items():
            if country in location_lower:
                return code
        
        return 'us'  # Default fallback
    
    def _extract_salary(self, extensions: Dict) -> Optional[Dict]:
        """Extract salary information from job extensions"""
        if not extensions:
            return None
        
        # Try to find salary info
        salary_text = extensions.get('salary', '')
        if not salary_text:
            return None
        
        # Basic parsing (can be improved)
        return {
            'text': salary_text,
            'min': None,
            'max': None,
            'currency': 'USD'
        }
    
    def _parse_jsearch_salary(self, job_data: Dict) -> Optional[Dict]:
        """Parse salary from JSearch response"""
        min_salary = job_data.get('job_min_salary')
        max_salary = job_data.get('job_max_salary')
        
        if min_salary or max_salary:
            return {
                'min': min_salary,
                'max': max_salary,
                'currency': job_data.get('job_salary_currency', 'USD')
            }
        
        return None
    
    def _parse_date(self, date_str: str) -> str:
        """Parse and normalize date strings"""
        if not date_str:
            return datetime.now().strftime('%Y-%m-%d')
        
        # Handle relative dates like "2 days ago"
        if 'ago' in date_str.lower():
            # Simple approximation
            if 'hour' in date_str:
                return datetime.now().strftime('%Y-%m-%d')
            elif 'day' in date_str:
                days = int(''.join(filter(str.isdigit, date_str)) or 1)
                return (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            elif 'week' in date_str:
                weeks = int(''.join(filter(str.isdigit, date_str)) or 1)
                return (datetime.now() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
        
        return date_str
    
    def _get_fallback_jobs(self, query: str, location: str) -> List[Dict]:
        """
        Fallback sample jobs when all APIs fail
        """
        logger.warning("Using fallback sample jobs")
        
        return [
            {
                'id': 'fallback_001',
                'title': query,
                'company': 'Sample Company',
                'location': location,
                'description': f'Sample job for {query} in {location}. Real API data temporarily unavailable.',
                'url': 'https://example.com/job/001',
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Fallback',
                'salary_range': {'min': 2000, 'max': 4000, 'currency': 'EUR'},
                'job_type': 'Full-time',
                'remote': True,
                'skills': [],
                'fetched_at': datetime.now().isoformat()
            }
        ]
    
    def bulk_search(
        self,
        queries: List[str],
        locations: List[str],
        num_results: int = 10
    ) -> Dict[str, List[Dict]]:
        """
        Search multiple queries and locations
        
        Args:
            queries: List of job titles
            locations: List of locations
            num_results: Results per query
        
        Returns:
            Dictionary mapping query_location to job lists
        """
        all_jobs = {}
        
        for query in queries:
            for location in locations:
                key = f"{query}_{location}"
                logger.info(f"Searching: {query} in {location}")
                
                jobs = self.search_jobs(query, location, num_results)
                all_jobs[key] = jobs
                
                # Rate limiting - be nice to APIs
                time.sleep(1)
        
        return all_jobs
    
    def get_scraper_stats(self) -> Dict:
        """Get statistics about scraper usage"""
        return {
            'last_api_used': self.last_api_used,
            'cache_size': len(self.cache),
            'apis_available': len(self.apis)
        }


# Test function
if __name__ == '__main__':
    print("=" * 70)
    print("Testing Real Job Scraper with Multi-API Fallback")
    print("=" * 70)
    
    scraper = RealJobScraper()
    
    # Test search
    print("\n1. Testing: Software Engineer in Tunisia")
    jobs = scraper.search_jobs('Software Engineer', 'Tunisia', num_results=5)
    
    print(f"\n✓ Found {len(jobs)} jobs!\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")
        print(f"   URL: {job['url'][:60]}...")
        print()
    
    # Stats
    stats = scraper.get_scraper_stats()
    print(f"Stats: Last API used = {stats['last_api_used']}, Cache size = {stats['cache_size']}")
