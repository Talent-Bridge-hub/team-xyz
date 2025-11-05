""""""

Database models and queries for Job managementJob Matcher Pydantic Models

Handles direct PostgreSQL database operations for the jobs tableData validation schemas for job scraping, matching, and search endpoints

""""""



from typing import Optional, Dict, Any, Listfrom pydantic import BaseModel, Field, validator

from datetime import datetimefrom typing import List, Optional, Dict, Any

import jsonfrom datetime import datetime

from enum import Enum



# ========== Database Schema Documentation ==========

"""# Enums

Jobs Table Schema (PostgreSQL):class JobType(str, Enum):

    """Job employment type"""

CREATE TABLE jobs (    FULL_TIME = "Full-time"

    id VARCHAR(255) PRIMARY KEY,    PART_TIME = "Part-time"

    title VARCHAR(500) NOT NULL,    CONTRACT = "Contract"

    company VARCHAR(255) NOT NULL,    INTERNSHIP = "Internship"

    location VARCHAR(255),    FREELANCE = "Freelance"

    region VARCHAR(100),

    type VARCHAR(50) DEFAULT 'Full-time',

    experience_level VARCHAR(50),class ExperienceLevel(str, Enum):

    description TEXT,    """Experience level categories"""

    required_skills TEXT[],    JUNIOR = "Junior"

    preferred_skills TEXT[],    MID_LEVEL = "Mid-level"

    salary_min INTEGER,    SENIOR = "Senior"

    salary_max INTEGER,    LEAD = "Lead"

    salary_currency VARCHAR(10) DEFAULT 'USD',    EXECUTIVE = "Executive"

    salary_text TEXT,

    posted_date TIMESTAMP,

    remote BOOLEAN DEFAULT FALSE,class Region(str, Enum):

    url TEXT NOT NULL,    """Geographic regions"""

    source VARCHAR(100),    MENA = "MENA"

    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    SUB_SAHARAN_AFRICA = "Sub-Saharan Africa"

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    NORTH_AMERICA = "North America"

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    EUROPE = "Europe"

);    ASIA = "Asia"

    OTHER = "Other"

CREATE INDEX idx_jobs_title ON jobs(title);

CREATE INDEX idx_jobs_location ON jobs(location);

CREATE INDEX idx_jobs_company ON jobs(company);# Salary Range Model

CREATE INDEX idx_jobs_fetched_at ON jobs(fetched_at DESC);class SalaryRange(BaseModel):

CREATE INDEX idx_jobs_remote ON jobs(remote);    """Salary range information"""

"""    min: Optional[int] = Field(None, description="Minimum salary")

    max: Optional[int] = Field(None, description="Maximum salary")

    currency: str = Field("USD", description="Currency code (USD, EUR, etc.)")

# ========== SQL Query Constants ==========    text: Optional[str] = Field(None, description="Original salary text")



class JobQueries:

    """SQL queries for job operations"""# Job Post Model (stored in database)

    class JobPost(BaseModel):

    # Create    """Complete job posting information"""

    INSERT_JOB = """    id: str = Field(..., description="Unique job identifier")

        INSERT INTO jobs (    title: str = Field(..., description="Job title")

            id, title, company, location, region, type, experience_level,    company: str = Field(..., description="Company name")

            description, required_skills, preferred_skills,    location: str = Field(..., description="Job location")

            salary_min, salary_max, salary_currency, salary_text,    region: Optional[str] = Field(None, description="Geographic region")

            posted_date, remote, url, source, fetched_at    type: str = Field("Full-time", description="Employment type")

        )    experience_level: Optional[str] = Field(None, description="Required experience level")

        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)    description: str = Field(..., description="Full job description")

        ON CONFLICT (id) DO UPDATE SET    required_skills: List[str] = Field(default_factory=list, description="Required skills")

            updated_at = CURRENT_TIMESTAMP    preferred_skills: List[str] = Field(default_factory=list, description="Preferred skills")

        RETURNING *    salary_range: Optional[SalaryRange] = Field(None, description="Salary information")

    """    posted_date: Optional[str] = Field(None, description="Date posted (ISO format)")

        remote: bool = Field(False, description="Is remote work available")

    # Read    url: str = Field(..., description="Application URL")

    SELECT_BY_ID = """    source: Optional[str] = Field(None, description="Job source (SerpAPI, LinkedIn, etc.)")

        SELECT * FROM jobs WHERE id = %s    fetched_at: Optional[str] = Field(None, description="When job was scraped")

    """

    

    SELECT_ALL = """# Job Scraping Request

        SELECT * FROM jobsclass JobScrapingRequest(BaseModel):

        ORDER BY fetched_at DESC    """Request to scrape jobs from external sources"""

        LIMIT %s OFFSET %s    queries: List[str] = Field(

    """        default=["Software Engineer", "Data Analyst", "Frontend Developer"],

            description="List of job titles to search"

    SELECT_WITH_FILTERS = """    )

        SELECT * FROM jobs    locations: List[str] = Field(

        WHERE 1=1        default=["Tunisia", "Egypt", "Nigeria"],

        {filters}        description="List of locations to search"

        ORDER BY fetched_at DESC    )

        LIMIT %s OFFSET %s    num_results_per_query: int = Field(

    """        default=15,

            ge=1,

    COUNT_ALL = """        le=50,

        SELECT COUNT(*) as count FROM jobs        description="Number of results per query (max 50)"

    """    )

    

    COUNT_WITH_FILTERS = """

        SELECT COUNT(*) as count FROM jobs# Job Scraping Response

        WHERE 1=1class JobScrapingResponse(BaseModel):

        {filters}    """Response from job scraping operation"""

    """    jobs_scraped: int = Field(..., description="Number of jobs scraped")

        jobs_stored: int = Field(..., description="Number of jobs stored in database")

    # Search by keywords    queries_processed: int = Field(..., description="Number of queries processed")

    SEARCH_JOBS = """    locations_processed: int = Field(..., description="Number of locations processed")

        SELECT * FROM jobs    api_used: Optional[str] = Field(None, description="Primary API used for scraping")

        WHERE (    scraping_duration_ms: int = Field(..., description="Time taken to scrape (milliseconds)")

            title ILIKE %s    message: str = Field(..., description="Status message")

            OR description ILIKE %s

            OR company ILIKE %s

        )# Match Score Breakdown

        ORDER BY fetched_at DESCclass MatchScoreBreakdown(BaseModel):

        LIMIT %s OFFSET %s    """Detailed breakdown of match score components"""

    """    matched_skills: List[str] = Field(default_factory=list, description="Skills that matched")

        missing_skills: List[str] = Field(default_factory=list, description="Required skills candidate lacks")

    # Get similar jobs (by skills)

    SELECT_SIMILAR_JOBS = """

        SELECT * FROM jobsclass MatchScore(BaseModel):

        WHERE id != %s    """Job match scoring details"""

        AND (    overall_score: int = Field(..., ge=0, le=100, description="Overall match score (0-100)")

            required_skills && %s::text[]    skill_score: int = Field(..., ge=0, le=100, description="Skill match score")

            OR company = %s    location_score: int = Field(..., ge=0, le=100, description="Location match score")

        )    experience_score: int = Field(..., ge=0, le=100, description="Experience level match score")

        ORDER BY fetched_at DESC    breakdown: MatchScoreBreakdown = Field(..., description="Detailed score breakdown")

        LIMIT %s

    """

    # Job Match (job + score)

    # Updateclass JobMatch(BaseModel):

    UPDATE_JOB = """    """A job posting with match score"""

        UPDATE jobs    job: JobPost = Field(..., description="Job posting details")

        SET {fields}, updated_at = CURRENT_TIMESTAMP    match_score: MatchScore = Field(..., description="Match scoring details")

        WHERE id = %s    matched_at: str = Field(..., description="When match was calculated (ISO format)")

        RETURNING *

    """

    # Job Matching Request

    # Deleteclass JobMatchingRequest(BaseModel):

    DELETE_JOB = """    """Request to find matching jobs for a resume"""

        DELETE FROM jobs WHERE id = %s    resume_id: int = Field(..., description="Resume ID to match against jobs")

    """    limit: int = Field(default=10, ge=1, le=50, description="Maximum number of matches to return")

        min_score: int = Field(default=50, ge=0, le=100, description="Minimum match score threshold")

    DELETE_OLD_JOBS = """    fetch_fresh_jobs: bool = Field(

        DELETE FROM jobs        default=True,

        WHERE fetched_at < %s        description="Whether to fetch fresh jobs from APIs before matching"

    """    )

        queries: Optional[List[str]] = Field(

    # Market insights        None,

    GET_TOP_SKILLS = """        description="Custom job titles to search (optional, uses intelligent defaults)"

        SELECT unnest(required_skills) as skill, COUNT(*) as demand    )

        FROM jobs    locations: Optional[List[str]] = Field(

        WHERE region = %s OR %s IS NULL        None,

        GROUP BY skill        description="Custom locations to search (optional, uses resume location)"

        ORDER BY demand DESC    )

        LIMIT 10

    """

    # Job Matching Response

    GET_AVERAGE_SALARIES = """class JobMatchingResponse(BaseModel):

        SELECT experience_level, AVG(salary_min) as avg_min, AVG(salary_max) as avg_max    """Response with matched jobs"""

        FROM jobs    resume_id: int = Field(..., description="Resume ID that was matched")

        WHERE region = %s OR %s IS NULL    matches: List[JobMatch] = Field(..., description="List of job matches with scores")

        AND salary_min IS NOT NULL    total_matches: int = Field(..., description="Total number of matches found")

        GROUP BY experience_level    matches_found: int = Field(..., description="Number of matches found (same as total_matches)")

    """    jobs_searched: int = Field(..., description="Total jobs searched")

        total_jobs_searched: int = Field(..., description="Total jobs searched (same as jobs_searched)")

    GET_REMOTE_PERCENTAGE = """    average_score: float = Field(..., description="Average match score of returned matches")

        SELECT     avg_match_score: float = Field(..., description="Average match score (same as average_score)")

            COUNT(*) FILTER (WHERE remote = TRUE) * 100.0 / NULLIF(COUNT(*), 0) as percentage    best_match_score: Optional[int] = Field(None, description="Highest match score")

        FROM jobs    processing_time_ms: float = Field(..., description="Time taken to process matches in milliseconds")

        WHERE region = %s OR %s IS NULL    matched_at: str = Field(..., description="When matching was performed (ISO format)")

    """    message: str = Field(..., description="Status message")





# ========== Database Row Converters ==========# Job Search Request

class JobSearchRequest(BaseModel):

def job_row_to_dict(row: Dict[str, Any]) -> Dict[str, Any]:    """Advanced job search with filters"""

    """    keywords: Optional[str] = Field(None, description="Keywords to search in title/description")

    Convert database row to dictionary    location: Optional[str] = Field(None, description="Location filter")

    """    job_type: Optional[JobType] = Field(None, description="Employment type filter")

    if not row:    experience_level: Optional[ExperienceLevel] = Field(None, description="Experience level filter")

        return None    remote_only: Optional[bool] = Field(False, description="Show only remote jobs")

        min_salary: Optional[int] = Field(None, description="Minimum salary filter")

    # Build salary_range    max_salary: Optional[int] = Field(None, description="Maximum salary filter")

    salary_range = None    required_skills: Optional[List[str]] = Field(None, description="Skills that must be present")

    if row.get('salary_min') or row.get('salary_max'):    page: int = Field(default=1, ge=1, description="Page number for pagination")

        salary_range = {    page_size: int = Field(default=20, ge=1, le=100, description="Results per page")

            'min': row.get('salary_min'),

            'max': row.get('salary_max'),

            'currency': row.get('salary_currency', 'USD'),# Job List Item (simplified job for list views)

            'text': row.get('salary_text')class JobListItem(BaseModel):

        }    """Simplified job information for list views"""

        id: str = Field(..., description="Job ID")

    return {    title: str = Field(..., description="Job title")

        'id': row.get('id'),    company: str = Field(..., description="Company name")

        'title': row.get('title'),    location: str = Field(..., description="Location")

        'company': row.get('company'),    remote: bool = Field(..., description="Remote work available")

        'location': row.get('location'),    job_type: str = Field(..., description="Employment type")

        'region': row.get('region'),    experience_level: Optional[str] = Field(None, description="Experience level")

        'type': row.get('type', 'Full-time'),    salary_range: Optional[SalaryRange] = Field(None, description="Salary information")

        'experience_level': row.get('experience_level'),    posted_date: Optional[str] = Field(None, description="Date posted")

        'description': row.get('description'),    url: str = Field(..., description="Application URL")

        'required_skills': row.get('required_skills', []),    required_skills: List[str] = Field(default_factory=list, description="Required skills (top 5)")

        'preferred_skills': row.get('preferred_skills', []),

        'salary_range': salary_range,

        'posted_date': row.get('posted_date').isoformat() if row.get('posted_date') else None,# Job List Response

        'remote': row.get('remote', False),class JobListResponse(BaseModel):

        'url': row.get('url'),    """Paginated list of jobs"""

        'source': row.get('source'),    jobs: List[JobListItem] = Field(..., description="List of jobs for current page")

        'fetched_at': row.get('fetched_at').isoformat() if row.get('fetched_at') else None    total: int = Field(..., description="Total number of jobs matching criteria")

    }    page: int = Field(..., description="Current page number")

    page_size: int = Field(..., description="Results per page")

    total_pages: int = Field(..., description="Total number of pages")

def job_row_to_list_item(row: Dict[str, Any]) -> Dict[str, Any]:

    """

    Convert database row to list item format (minimal fields)# Market Insights Response

    """class SkillDemand(BaseModel):

    if not row:    """Skill demand statistics"""

        return None    skill: str = Field(..., description="Skill name")

        demand: int = Field(..., description="Number of jobs requiring this skill")

    # Build salary_range

    salary_range = None

    if row.get('salary_min') or row.get('salary_max'):class AverageSalary(BaseModel):

        salary_range = {    """Average salary by experience level"""

            'min': row.get('salary_min'),    average: int = Field(..., description="Average salary")

            'max': row.get('salary_max'),    currency: str = Field(..., description="Currency code")

            'currency': row.get('salary_currency', 'USD'),

            'text': row.get('salary_text')

        }class MarketInsights(BaseModel):

        """Job market insights for a region"""

    # Get top 5 skills    region: str = Field(..., description="Region name")

    required_skills = row.get('required_skills', [])[:5]    total_jobs: int = Field(..., description="Total jobs analyzed")

        top_skills: List[SkillDemand] = Field(..., description="Top 10 in-demand skills")

    return {    average_salaries: Dict[str, AverageSalary] = Field(

        'id': row.get('id'),        ...,

        'title': row.get('title'),        description="Average salaries by experience level"

        'company': row.get('company'),    )

        'location': row.get('location'),    remote_jobs_percentage: float = Field(..., description="Percentage of remote jobs")

        'remote': row.get('remote', False),    generated_at: str = Field(..., description="When insights were generated (ISO format)")

        'job_type': row.get('type', 'Full-time'),

        'experience_level': row.get('experience_level'),

        'salary_range': salary_range,# Job Detail Response (single job with full details)

        'posted_date': row.get('posted_date').isoformat() if row.get('posted_date') else None,class JobDetailResponse(BaseModel):

        'url': row.get('url'),    """Complete job details"""

        'required_skills': required_skills    job: JobPost = Field(..., description="Full job information")

    }    similar_jobs: List[JobListItem] = Field(

        default_factory=list,

        description="Similar job recommendations"

def prepare_job_data(job_dict: Dict[str, Any]) -> tuple:    )

    """
    Prepare job data for insertion
    Returns tuple ready for SQL INSERT
    """
    # Extract salary info
    salary_range = job_dict.get('salary_range', {})
    salary_min = salary_range.get('min') if salary_range else None
    salary_max = salary_range.get('max') if salary_range else None
    salary_currency = salary_range.get('currency', 'USD') if salary_range else 'USD'
    salary_text = salary_range.get('text') if salary_range else None
    
    # Parse posted_date
    posted_date = None
    if job_dict.get('posted_date'):
        try:
            posted_date = datetime.fromisoformat(job_dict['posted_date'].replace('Z', '+00:00'))
        except:
            posted_date = None
    
    # Parse fetched_at
    fetched_at = datetime.utcnow()
    if job_dict.get('fetched_at'):
        try:
            fetched_at = datetime.fromisoformat(job_dict['fetched_at'].replace('Z', '+00:00'))
        except:
            pass
    
    return (
        job_dict.get('id'),
        job_dict.get('title'),
        job_dict.get('company'),
        job_dict.get('location'),
        job_dict.get('region'),
        job_dict.get('type', 'Full-time'),
        job_dict.get('experience_level'),
        job_dict.get('description'),
        job_dict.get('required_skills', []),
        job_dict.get('preferred_skills', []),
        salary_min,
        salary_max,
        salary_currency,
        salary_text,
        posted_date,
        job_dict.get('remote', False),
        job_dict.get('url'),
        job_dict.get('source'),
        fetched_at
    )


def build_filter_clause(filters: Dict[str, Any]) -> tuple:
    """
    Build SQL WHERE clause from filters
    Returns (filter_string, params_list)
    """
    clauses = []
    params = []
    
    if filters.get('keywords'):
        keyword = f"%{filters['keywords']}%"
        clauses.append("(title ILIKE %s OR description ILIKE %s)")
        params.extend([keyword, keyword])
    
    if filters.get('location'):
        clauses.append("location ILIKE %s")
        params.append(f"%{filters['location']}%")
    
    if filters.get('job_type'):
        clauses.append("type = %s")
        params.append(filters['job_type'])
    
    if filters.get('experience_level'):
        clauses.append("experience_level = %s")
        params.append(filters['experience_level'])
    
    if filters.get('remote_only'):
        clauses.append("remote = TRUE")
    
    if filters.get('min_salary'):
        clauses.append("salary_min >= %s")
        params.append(filters['min_salary'])
    
    if filters.get('max_salary'):
        clauses.append("salary_max <= %s")
        params.append(filters['max_salary'])
    
    if filters.get('required_skills'):
        clauses.append("required_skills && %s::text[]")
        params.append(filters['required_skills'])
    
    filter_string = ""
    if clauses:
        filter_string = "AND " + " AND ".join(clauses)
    
    return filter_string, params
