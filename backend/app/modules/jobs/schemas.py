"""
Job Matcher Pydantic Models
Data validation schemas for job scraping, matching, and search endpoints
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class JobType(str, Enum):
    """Job employment type"""
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    FREELANCE = "Freelance"


class ExperienceLevel(str, Enum):
    """Experience level categories"""
    JUNIOR = "Junior"
    MID_LEVEL = "Mid-level"
    SENIOR = "Senior"
    LEAD = "Lead"
    EXECUTIVE = "Executive"


class Region(str, Enum):
    """Geographic regions"""
    MENA = "MENA"
    SUB_SAHARAN_AFRICA = "Sub-Saharan Africa"
    NORTH_AMERICA = "North America"
    EUROPE = "Europe"
    ASIA = "Asia"
    OTHER = "Other"


# Salary Range Model
class SalaryRange(BaseModel):
    """Salary range information"""
    min: Optional[int] = Field(None, description="Minimum salary")
    max: Optional[int] = Field(None, description="Maximum salary")
    currency: str = Field("USD", description="Currency code (USD, EUR, etc.)")
    text: Optional[str] = Field(None, description="Original salary text")


# Job Post Model (stored in database)
class JobPost(BaseModel):
    """Complete job posting information"""
    id: str = Field(..., description="Unique job identifier")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    region: Optional[str] = Field(None, description="Geographic region")
    type: str = Field("Full-time", description="Employment type")
    experience_level: Optional[str] = Field(None, description="Required experience level")
    description: str = Field(..., description="Full job description")
    required_skills: List[str] = Field(default_factory=list, description="Required skills")
    preferred_skills: List[str] = Field(default_factory=list, description="Preferred skills")
    salary_range: Optional[SalaryRange] = Field(None, description="Salary information")
    posted_date: Optional[str] = Field(None, description="Date posted (ISO format)")
    remote: bool = Field(False, description="Is remote work available")
    url: str = Field(..., description="Application URL")
    source: Optional[str] = Field(None, description="Job source (SerpAPI, LinkedIn, etc.)")
    fetched_at: Optional[str] = Field(None, description="When job was scraped")


# Job Scraping Request
class JobScrapingRequest(BaseModel):
    """Request to scrape jobs from external sources"""
    queries: List[str] = Field(
        default=["Software Engineer", "Data Analyst", "Frontend Developer"],
        description="List of job titles to search"
    )
    locations: List[str] = Field(
        default=["Tunisia", "Egypt", "Nigeria"],
        description="List of locations to search"
    )
    num_results_per_query: int = Field(
        default=15,
        ge=1,
        le=50,
        description="Number of results per query (max 50)"
    )


# Job Scraping Response
class JobScrapingResponse(BaseModel):
    """Response from job scraping operation"""
    jobs_scraped: int = Field(..., description="Number of jobs scraped")
    jobs_stored: int = Field(..., description="Number of jobs stored in database")
    queries_processed: int = Field(..., description="Number of queries processed")
    locations_processed: int = Field(..., description="Number of locations processed")
    api_used: Optional[str] = Field(None, description="Primary API used for scraping")
    scraping_duration_ms: int = Field(..., description="Time taken to scrape (milliseconds)")
    message: str = Field(..., description="Status message")


# Match Score Breakdown
class MatchScoreBreakdown(BaseModel):
    """Detailed breakdown of match score components"""
    matched_skills: List[str] = Field(default_factory=list, description="Skills that matched")
    missing_skills: List[str] = Field(default_factory=list, description="Required skills candidate lacks")


class MatchScore(BaseModel):
    """Job match scoring details"""
    overall_score: int = Field(..., ge=0, le=100, description="Overall match score (0-100)")
    skill_score: int = Field(..., ge=0, le=100, description="Skill match score")
    location_score: int = Field(..., ge=0, le=100, description="Location match score")
    experience_score: int = Field(..., ge=0, le=100, description="Experience level match score")
    breakdown: MatchScoreBreakdown = Field(..., description="Detailed score breakdown")


# Job Match (job + score)
class JobMatch(BaseModel):
    """A job posting with match score"""
    job: JobPost = Field(..., description="Job posting details")
    match_score: MatchScore = Field(..., description="Match scoring details")
    matched_at: str = Field(..., description="When match was calculated (ISO format)")


# Job Matching Request
class JobMatchingRequest(BaseModel):
    """Request to find matching jobs for a resume"""
    resume_id: int = Field(..., description="Resume ID to match against jobs")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of matches to return")
    min_score: int = Field(default=50, ge=0, le=100, description="Minimum match score threshold")
    fetch_fresh_jobs: bool = Field(
        default=True,
        description="Whether to fetch fresh jobs from APIs before matching"
    )
    queries: Optional[List[str]] = Field(
        None,
        description="Custom job titles to search (optional, uses intelligent defaults)"
    )
    locations: Optional[List[str]] = Field(
        None,
        description="Custom locations to search (optional, uses resume location)"
    )


# Job Matching Response
class JobMatchingResponse(BaseModel):
    """Response with matched jobs"""
    resume_id: int = Field(..., description="Resume ID that was matched")
    matches: List[JobMatch] = Field(..., description="List of job matches with scores")
    total_matches: int = Field(..., description="Total number of matches found")
    matches_found: int = Field(..., description="Number of matches found (same as total_matches)")
    jobs_searched: int = Field(..., description="Total jobs searched")
    total_jobs_searched: int = Field(..., description="Total jobs searched (same as jobs_searched)")
    average_score: float = Field(..., description="Average match score of returned matches")
    avg_match_score: float = Field(..., description="Average match score (same as average_score)")
    best_match_score: Optional[int] = Field(None, description="Highest match score")
    processing_time_ms: float = Field(..., description="Time taken to process matches in milliseconds")
    matched_at: str = Field(..., description="When matching was performed (ISO format)")
    message: str = Field(..., description="Status message")


# Job Search Request
class JobSearchRequest(BaseModel):
    """Advanced job search with filters"""
    keywords: Optional[str] = Field(None, description="Keywords to search in title/description")
    location: Optional[str] = Field(None, description="Location filter")
    job_type: Optional[JobType] = Field(None, description="Employment type filter")
    experience_level: Optional[ExperienceLevel] = Field(None, description="Experience level filter")
    remote_only: Optional[bool] = Field(False, description="Show only remote jobs")
    min_salary: Optional[int] = Field(None, description="Minimum salary filter")
    max_salary: Optional[int] = Field(None, description="Maximum salary filter")
    required_skills: Optional[List[str]] = Field(None, description="Skills that must be present")
    page: int = Field(default=1, ge=1, description="Page number for pagination")
    page_size: int = Field(default=20, ge=1, le=100, description="Results per page")


# Job List Item (simplified job for list views)
class JobListItem(BaseModel):
    """Simplified job information for list views"""
    id: str = Field(..., description="Job ID")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str = Field(..., description="Location")
    remote: bool = Field(..., description="Remote work available")
    job_type: str = Field(..., description="Employment type")
    experience_level: Optional[str] = Field(None, description="Experience level")
    salary_range: Optional[SalaryRange] = Field(None, description="Salary information")
    posted_date: Optional[str] = Field(None, description="Date posted")
    url: str = Field(..., description="Application URL")
    required_skills: List[str] = Field(default_factory=list, description="Required skills (top 5)")


# Job List Response
class JobListResponse(BaseModel):
    """Paginated list of jobs"""
    jobs: List[JobListItem] = Field(..., description="List of jobs for current page")
    total: int = Field(..., description="Total number of jobs matching criteria")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Results per page")
    total_pages: int = Field(..., description="Total number of pages")


# Market Insights Response
class SkillDemand(BaseModel):
    """Skill demand statistics"""
    skill: str = Field(..., description="Skill name")
    demand: int = Field(..., description="Number of jobs requiring this skill")


class AverageSalary(BaseModel):
    """Average salary by experience level"""
    average: int = Field(..., description="Average salary")
    currency: str = Field(..., description="Currency code")


class MarketInsights(BaseModel):
    """Job market insights for a region"""
    region: str = Field(..., description="Region name")
    total_jobs: int = Field(..., description="Total jobs analyzed")
    top_skills: List[SkillDemand] = Field(..., description="Top 10 in-demand skills")
    average_salaries: Dict[str, AverageSalary] = Field(
        ...,
        description="Average salaries by experience level"
    )
    remote_jobs_percentage: float = Field(..., description="Percentage of remote jobs")
    generated_at: str = Field(..., description="When insights were generated (ISO format)")


# Job Detail Response (single job with full details)
class JobDetailResponse(BaseModel):
    """Complete job details"""
    job: JobPost = Field(..., description="Full job information")
    similar_jobs: List[JobListItem] = Field(
        default_factory=list,
        description="Similar job recommendations"
    )
