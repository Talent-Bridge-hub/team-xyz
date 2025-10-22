"""
Job API Configuration and Credentials
Manages API keys and endpoints for multiple job scraping services
"""

import os
from typing import Dict, Optional

# API Credentials
API_CREDENTIALS = {
    'serpapi': {
        'api_key': '18610838c49525ce1cbb77e2952480d6a2b4b02a618b8787a9e3a94da0e5a3ae',
        'endpoint': 'https://serpapi.com/search',
        'free_limit': 100,  # searches per month
        'priority': 1  # Try first
    },
    'linkedin_rapidapi': {
        'api_key': '6554b3f7f8msh9faf98ba1b2a94fp175d5fjsn0dea53747946',
        'host': 'linkedin-job-search-api.p.rapidapi.com',
        'endpoint': 'https://linkedin-job-search-api.p.rapidapi.com/active-jb-1h',
        'free_limit': 500,  # requests per month
        'priority': 2  # Fallback #1
    },
    'jsearch_rapidapi': {
        'api_key': '6554b3f7f8msh9faf98ba1b2a94fp175d5fjsn0dea53747946',
        'host': 'jsearch.p.rapidapi.com',
        'endpoint': 'https://jsearch.p.rapidapi.com/search',
        'free_limit': 250,  # requests per month
        'priority': 3  # Fallback #2
    }
}


def get_api_credentials(api_name: str) -> Optional[Dict]:
    """
    Get API credentials by name
    
    Args:
        api_name: 'serpapi', 'linkedin_rapidapi', or 'jsearch_rapidapi'
    
    Returns:
        Dictionary with API credentials or None
    """
    return API_CREDENTIALS.get(api_name)


def get_all_apis_by_priority():
    """Get all APIs sorted by priority"""
    return sorted(API_CREDENTIALS.items(), key=lambda x: x[1]['priority'])


# Job search parameters
SEARCH_REGIONS = {
    'MENA': [
        'Tunisia', 'Egypt', 'Morocco', 'Algeria', 'Libya',
        'Jordan', 'Lebanon', 'UAE', 'Saudi Arabia', 'Qatar',
        'Kuwait', 'Bahrain', 'Oman', 'Yemen', 'Iraq', 'Syria'
    ],
    'Sub-Saharan Africa': [
        'Nigeria', 'Kenya', 'South Africa', 'Ghana', 'Ethiopia',
        'Tanzania', 'Uganda', 'Senegal', 'Rwanda', 'Zambia',
        'Zimbabwe', 'Mozambique', 'Cameroon', 'Ivory Coast'
    ]
}

COMMON_JOB_TITLES = [
    'Software Engineer',
    'Frontend Developer',
    'Backend Developer',
    'Full Stack Developer',
    'Data Analyst',
    'Data Scientist',
    'Product Manager',
    'DevOps Engineer',
    'Mobile Developer',
    'UI/UX Designer',
    'Business Analyst',
    'Project Manager',
    'QA Engineer',
    'System Administrator'
]


if __name__ == '__main__':
    print("API Configuration loaded successfully!")
    print(f"\nConfigured APIs: {len(API_CREDENTIALS)}")
    for name, config in get_all_apis_by_priority():
        print(f"  {config['priority']}. {name} - Limit: {config['free_limit']}/month")
