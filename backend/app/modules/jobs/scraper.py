"""
Job Scraper Integration

Wrapper around the existing job scraper utility for the jobs module.
Provides a clean interface to fetch jobs from external APIs.
"""

from typing import List, Dict, Any
from datetime import datetime
import sys
from pathlib import Path

# Import existing job scraper
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from utils.job_scraper import RealJobScraper


class JobScraperService:
    """
    Service for scraping jobs from external APIs.
    
    Wraps the existing RealJobScraper utility with additional
    features for the jobs module.
    """
    
    def __init__(self):
        """Initialize the job scraper."""
        self.scraper = RealJobScraper()
    
    def scrape_jobs(
        self,
        queries: List[str],
        locations: List[str],
        num_results_per_query: int = 15
    ) -> List[Dict[str, Any]]:
        """
        Scrape jobs for multiple queries and locations.
        
        Args:
            queries: List of job titles to search
            locations: List of locations to search
            num_results_per_query: Number of results per query
            
        Returns:
            List of job dictionaries
        """
        all_jobs = []
        
        for query in queries:
            for location in locations:
                try:
                    jobs = self.scraper.search_jobs(
                        query=query,
                        location=location,
                        num_results=num_results_per_query
                    )
                    all_jobs.extend(jobs)
                except Exception as e:
                    # Log error but continue with other queries
                    print(f"Error scraping '{query}' in {location}: {e}")
                    continue
        
        # Deduplicate jobs by ID
        unique_jobs = {}
        for job in all_jobs:
            job_id = job.get('id')
            if job_id and job_id not in unique_jobs:
                unique_jobs[job_id] = job
        
        return list(unique_jobs.values())
    
    def scrape_single_query(
        self,
        query: str,
        location: str,
        num_results: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Scrape jobs for a single query.
        
        Args:
            query: Job title to search
            location: Location to search
            num_results: Number of results
            
        Returns:
            List of job dictionaries
        """
        return self.scraper.search_jobs(query, location, num_results)
    
    def get_last_api_used(self) -> str:
        """
        Get the last API that was successfully used.
        
        Returns:
            API name (e.g., 'serpapi', 'linkedin_rapidapi')
        """
        return self.scraper.last_api_used or "unknown"
    
    def normalize_job_data(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize job data from scraper format to database format.
        
        Args:
            raw_job: Job data from scraper
            
        Returns:
            Normalized job data ready for database insertion
        """
        # The scraper already returns normalized data,
        # but we can add additional transformations here if needed
        
        normalized = {
            'id': raw_job.get('id', ''),
            'title': raw_job.get('title', ''),
            'company': raw_job.get('company', ''),
            'location': raw_job.get('location', ''),
            'region': raw_job.get('region'),
            'type': raw_job.get('type', 'Full-time'),
            'experience_level': raw_job.get('experience_level'),
            'description': raw_job.get('description', ''),
            'required_skills': raw_job.get('required_skills', []),
            'preferred_skills': raw_job.get('preferred_skills', []),
            'salary_range': raw_job.get('salary_range'),
            'posted_date': raw_job.get('posted_date'),
            'remote': raw_job.get('remote', False),
            'url': raw_job.get('url', ''),
            'source': raw_job.get('source', 'unknown'),
            'fetched_at': raw_job.get('fetched_at', datetime.utcnow().isoformat())
        }
        
        return normalized


# Convenience functions

def scrape_jobs_for_queries(
    queries: List[str],
    locations: List[str],
    num_results_per_query: int = 15
) -> List[Dict[str, Any]]:
    """
    Convenience function to scrape jobs.
    
    Args:
        queries: Job titles to search
        locations: Locations to search
        num_results_per_query: Results per query
        
    Returns:
        List of normalized job dictionaries
    """
    scraper_service = JobScraperService()
    jobs = scraper_service.scrape_jobs(queries, locations, num_results_per_query)
    return [scraper_service.normalize_job_data(job) for job in jobs]


def scrape_single_job_query(
    query: str,
    location: str,
    num_results: int = 20
) -> List[Dict[str, Any]]:
    """
    Convenience function to scrape jobs for single query.
    
    Args:
        query: Job title to search
        location: Location to search
        num_results: Number of results
        
    Returns:
        List of normalized job dictionaries
    """
    scraper_service = JobScraperService()
    jobs = scraper_service.scrape_single_query(query, location, num_results)
    return [scraper_service.normalize_job_data(job) for job in jobs]
