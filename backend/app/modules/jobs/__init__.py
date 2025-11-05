"""
Jobs Module

Handles job scraping, matching, and search functionality.

Features:
- Job scraping from external APIs (SerpAPI, LinkedIn, etc.)
- AI-powered job matching against resumes
- Advanced job search and filtering
- Market insights and salary trends
- Job recommendations
"""

from .router import router
from .service import JobService
from .schemas import (
    # Request schemas
    JobScrapingRequest,
    JobMatchingRequest,
    JobSearchRequest,
    
    # Response schemas
    JobScrapingResponse,
    JobMatchingResponse,
    JobListResponse,
    JobDetailResponse,
    MarketInsights,
    
    # Job models
    JobPost,
    JobListItem,
    JobMatch,
    MatchScore,
    MatchScoreBreakdown,
    SalaryRange,
    SkillDemand,
    AverageSalary,
    
    # Enums
    JobType,
    ExperienceLevel,
    Region
)
from .models import (
    JobQueries,
    job_row_to_dict,
    job_row_to_list_item,
    prepare_job_data,
    build_filter_clause
)
from .matcher import (
    JobMatcher,
    JobRecommendationEngine,
    calculate_job_freshness_score,
    extract_salary_value
)
from .scraper import (
    JobScraperService,
    scrape_jobs_for_queries,
    scrape_single_job_query
)

__all__ = [
    # Router
    "router",
    
    # Service
    "JobService",
    
    # Request schemas
    "JobScrapingRequest",
    "JobMatchingRequest",
    "JobSearchRequest",
    
    # Response schemas
    "JobScrapingResponse",
    "JobMatchingResponse",
    "JobListResponse",
    "JobDetailResponse",
    "MarketInsights",
    
    # Job models
    "JobPost",
    "JobListItem",
    "JobMatch",
    "MatchScore",
    "MatchScoreBreakdown",
    "SalaryRange",
    "SkillDemand",
    "AverageSalary",
    
    # Enums
    "JobType",
    "ExperienceLevel",
    "Region",
    
    # Database functions
    "JobQueries",
    "job_row_to_dict",
    "job_row_to_list_item",
    "prepare_job_data",
    "build_filter_clause",
    
    # Matcher
    "JobMatcher",
    "JobRecommendationEngine",
    "calculate_job_freshness_score",
    "extract_salary_value",
    
    # Scraper
    "JobScraperService",
    "scrape_jobs_for_queries",
    "scrape_single_job_query",
]
