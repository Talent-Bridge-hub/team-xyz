"""
Job Matcher API Endpoints
Scrape jobs, match with resumes, search and filter opportunities
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional, Dict, Any
import logging
import time
from datetime import datetime
import json
from psycopg2.extras import Json

# Import models
from backend.app.models.job import (
    JobScrapingRequest,
    JobScrapingResponse,
    JobMatchingRequest,
    JobMatchingResponse,
    JobSearchRequest,
    JobListResponse,
    JobListItem,
    MarketInsights,
    JobPost,
    JobMatch,
    MatchScore,
    MatchScoreBreakdown,
    SalaryRange,
    JobDetailResponse
)
from backend.app.models.user import UserResponse

# Import dependencies
from backend.app.api.deps import get_current_user
from backend.app.core.database import DatabaseWrapper

# Import utilities
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from utils.job_scraper import RealJobScraper
from utils.job_matcher import JobMatcher

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])

# Initialize database wrapper
db = DatabaseWrapper()

# Initialize job utilities
scraper = RealJobScraper()
matcher = JobMatcher(use_real_jobs=True)


@router.post("/scrape", response_model=JobScrapingResponse)
async def scrape_jobs(
    request: JobScrapingRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Scrape jobs from external APIs and store in database
    
    - **queries**: List of job titles to search
    - **locations**: List of locations to search  
    - **num_results_per_query**: Results per query (max 50)
    
    Returns number of jobs scraped and stored
    """
    start_time = time.time()
    
    try:
        logger.info(f"User {current_user.id} initiated job scraping")
        logger.info(f"Queries: {request.queries}, Locations: {request.locations}")
        
        jobs_scraped = 0
        jobs_stored = 0
        queries_processed = len(request.queries)
        locations_processed = len(request.locations)
        
        # Scrape jobs from APIs
        for query in request.queries:
            for location in request.locations:
                try:
                    logger.info(f"Scraping: {query} in {location}")
                    
                    # Use job scraper to fetch jobs
                    jobs = scraper.search_jobs(
                        query=query,
                        location=location,
                        num_results=request.num_results_per_query
                    )
                    
                    jobs_scraped += len(jobs)
                    
                    # Store jobs in database
                    for job in jobs:
                        try:
                            # Check if job already exists
                            existing = db.get_one('jobs', f"job_id = %s", (job['id'],))
                            
                            # Prepare job data for database
                            job_data = {
                                'job_id': job['id'],
                                'title': job['title'],
                                'company': job['company'],
                                'location': job['location'],
                                'region': matcher._determine_region(job['location']),
                                'job_type': job.get('job_type', 'Full-time'),
                                'experience_level': matcher._extract_experience_level_from_job(
                                    job['title'],
                                    job.get('description', '')
                                ),
                                'description': job.get('description', ''),
                                'required_skills': Json(matcher._extract_skills_from_description(
                                    job.get('description', '')
                                )[:5]),
                                'preferred_skills': Json([]),
                                'salary_range': Json(job.get('salary_range')) if job.get('salary_range') else None,
                                'posted_date': job.get('posted_date'),
                                'remote': job.get('remote', False),
                                'url': job['url'],
                                'source': job.get('source', 'API'),
                                'fetched_at': datetime.now()
                            }
                            
                            if not existing:
                                # Insert new job
                                db.insert('jobs', job_data)
                                jobs_stored += 1
                            else:
                                # Update existing job (refresh data)
                                db.update(
                                    'jobs',
                                    job_data,
                                    f"job_id = %s",
                                    (job['id'],)
                                )
                                jobs_stored += 1
                                
                        except Exception as e:
                            logger.error(f"Error storing job {job.get('id')}: {e}")
                            continue
                    
                    logger.info(f"✓ Scraped and stored {len(jobs)} jobs for '{query}' in {location}")
                    
                except Exception as e:
                    logger.error(f"Error scraping {query} in {location}: {e}")
                    continue
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Get API stats
        stats = scraper.get_scraper_stats()
        
        return JobScrapingResponse(
            jobs_scraped=jobs_scraped,
            jobs_stored=jobs_stored,
            queries_processed=queries_processed,
            locations_processed=locations_processed,
            api_used=stats.get('last_api_used', 'Unknown'),
            scraping_duration_ms=duration_ms,
            message=f"Successfully scraped {jobs_scraped} jobs and stored {jobs_stored} in database"
        )
        
    except Exception as e:
        logger.error(f"Job scraping failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job scraping failed: {str(e)}"
        )


@router.post("/match", response_model=JobMatchingResponse)
async def match_jobs_with_resume(
    request: JobMatchingRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Match jobs with a resume and return ranked results
    
    - **resume_id**: Resume to match against jobs
    - **limit**: Maximum number of matches to return (default 10)
    - **min_score**: Minimum match score threshold (default 50)
    - **fetch_fresh_jobs**: Whether to fetch fresh jobs before matching (default True)
    - **queries**: Optional custom job titles to search
    - **locations**: Optional custom locations to search
    
    Returns ranked job matches with scores
    """
    start_time = time.time()
    
    try:
        logger.info(f"User {current_user.id} initiated job matching for resume {request.resume_id}")
        
        # Get resume from database
        resume = db.get_one('resumes', f"id = %s AND user_id = %s", (request.resume_id, current_user.id))
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resume {request.resume_id} not found or does not belong to user"
            )
        
        # Parse resume data
        parsed_data = resume.get('parsed_data', {})
        if isinstance(parsed_data, str):
            parsed_data = json.loads(parsed_data)
        
        parsed_text = resume.get('parsed_text', '')
        
        # Build candidate profile for matching
        candidate_profile = {
            'raw_text': parsed_text,
            'sections': parsed_data,
            'structured_data': parsed_data,
            'metadata': {
                'word_count': resume.get('word_count', 0)
            },
            'contact_info': parsed_data.get('contact_info', {})
        }
        
        # Fetch fresh jobs if requested
        if request.fetch_fresh_jobs:
            logger.info("Fetching fresh jobs from APIs...")
            
            # Determine queries - use custom or intelligent defaults
            queries = request.queries
            if not queries:
                # Extract job-relevant keywords from resume
                queries = ["Software Engineer", "Developer", "Data Analyst"]  # Default tech jobs
            
            # Determine locations - use custom or resume location
            locations = request.locations
            if not locations:
                resume_location = parsed_data.get('contact_info', {}).get('location', 'Tunisia')
                locations = [resume_location]
            
            # Fetch jobs
            matcher.fetch_real_jobs(queries=queries, locations=locations, num_results=15)
        
        # Get all jobs from database for matching
        db_jobs = db.get_many('jobs', limit=500)  # Get recent 500 jobs
        
        if not db_jobs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No jobs in database. Please run /scrape endpoint first."
            )
        
        logger.info(f"Matching against {len(db_jobs)} jobs from database")
        
        # Convert DB jobs to matcher format
        matcher.jobs_database = []
        for job in db_jobs:
            required_skills = job.get('required_skills', [])
            if isinstance(required_skills, str):
                required_skills = json.loads(required_skills)
            
            preferred_skills = job.get('preferred_skills', [])
            if isinstance(preferred_skills, str):
                preferred_skills = json.loads(preferred_skills)
            
            salary_range = job.get('salary_range')
            if isinstance(salary_range, str):
                salary_range = json.loads(salary_range) if salary_range else None
            
            # Convert datetime fields to strings for Pydantic
            fetched_at = job.get('fetched_at', '')
            if fetched_at and hasattr(fetched_at, 'isoformat'):
                fetched_at = fetched_at.isoformat()
            elif fetched_at:
                fetched_at = str(fetched_at)
            
            posted_date = job.get('posted_date', '')
            if posted_date and hasattr(posted_date, 'isoformat'):
                posted_date = posted_date.isoformat()
            elif posted_date and not isinstance(posted_date, str):
                posted_date = str(posted_date)
            
            matcher.jobs_database.append({
                'id': job['job_id'],
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'region': job.get('region', 'Other'),
                'type': job.get('job_type', 'Full-time'),
                'experience_level': job.get('experience_level', 'Mid-level'),
                'description': job.get('description', ''),
                'required_skills': required_skills,
                'preferred_skills': preferred_skills,
                'salary_range': salary_range,
                'posted_date': posted_date,
                'remote': job.get('remote', False),
                'url': job['url'],
                'source': job.get('source', 'API'),
                'fetched_at': fetched_at
            })
        
        # Find matches
        matches = matcher.find_matches(
            candidate_profile=candidate_profile,
            limit=request.limit,
            fetch_real=False  # Already fetched above if requested
        )
        
        # Filter by min_score
        filtered_matches = [m for m in matches if m['match_score']['overall_score'] >= request.min_score]
        
        # Convert to response format
        job_matches = []
        for match in filtered_matches:
            job_data = match['job']
            score_data = match['match_score']
            
            # Build SalaryRange model
            salary = None
            if job_data.get('salary_range'):
                sr = job_data['salary_range']
                salary = SalaryRange(
                    min=sr.get('min'),
                    max=sr.get('max'),
                    currency=sr.get('currency', 'USD'),
                    text=sr.get('text')
                )
            
            # Build JobPost model
            job_post = JobPost(
                id=job_data['id'],
                title=job_data['title'],
                company=job_data['company'],
                location=job_data['location'],
                region=job_data.get('region'),
                type=job_data.get('type', 'Full-time'),
                experience_level=job_data.get('experience_level'),
                description=job_data.get('description', ''),
                required_skills=job_data.get('required_skills', []),
                preferred_skills=job_data.get('preferred_skills', []),
                salary_range=salary,
                posted_date=job_data.get('posted_date'),
                remote=job_data.get('remote', False),
                url=job_data['url'],
                source=job_data.get('source'),
                fetched_at=str(job_data.get('fetched_at')) if job_data.get('fetched_at') else None
            )
            
            # Build MatchScore model
            match_score = MatchScore(
                overall_score=score_data['overall_score'],
                skill_score=score_data['skill_score'],
                location_score=score_data['location_score'],
                experience_score=score_data['experience_score'],
                breakdown=MatchScoreBreakdown(
                    matched_skills=score_data['breakdown']['matched_skills'],
                    missing_skills=score_data['breakdown']['missing_skills']
                )
            )
            
            # Build JobMatch model
            job_match = JobMatch(
                job=job_post,
                match_score=match_score,
                matched_at=match['matched_at']
            )
            
            job_matches.append(job_match)
        
        # Calculate statistics
        total_matches = len(job_matches)
        jobs_searched = len(db_jobs)
        average_score = sum(m.match_score.overall_score for m in job_matches) / total_matches if total_matches > 0 else 0
        best_match_score = max((m.match_score.overall_score for m in job_matches), default=None)
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        return JobMatchingResponse(
            resume_id=request.resume_id,
            matches=job_matches,
            total_matches=total_matches,
            matches_found=total_matches,  # Duplicate for frontend compatibility
            jobs_searched=jobs_searched,
            total_jobs_searched=jobs_searched,  # Duplicate for frontend compatibility
            average_score=round(average_score, 1),
            avg_match_score=round(average_score, 1),  # Duplicate for frontend compatibility
            best_match_score=best_match_score,
            processing_time_ms=round(processing_time_ms, 2),
            matched_at=datetime.now().isoformat(),
            message=f"Found {total_matches} job matches with average score {average_score:.1f}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Job matching failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job matching failed: {str(e)}"
        )


@router.get("/list", response_model=JobListResponse)
async def list_jobs(
    page: int = 1,
    page_size: int = 20,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    remote_only: bool = False,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get paginated list of jobs with optional filters
    
    - **page**: Page number (default 1)
    - **page_size**: Results per page (default 20, max 100)
    - **location**: Filter by location
    - **job_type**: Filter by employment type
    - **remote_only**: Show only remote jobs
    
    Returns paginated job list
    """
    try:
        logger.info(f"User {current_user.id} requested job list (page {page})")
        
        # Validate pagination
        page = max(1, page)
        page_size = min(100, max(1, page_size))
        offset = (page - 1) * page_size
        
        # Build WHERE clause
        where_conditions = []
        where_params = []
        
        if location:
            # Check if it's a region filter (predefined regions) or location search
            regions = ['MENA', 'SUB_SAHARAN_AFRICA', 'NORTH_AMERICA', 'EUROPE', 'ASIA', 'OTHER']
            if location.upper().replace(' ', '_') in regions:
                # Filter by region column
                where_conditions.append("region = %s")
                where_params.append(location.replace('_', ' '))  # Convert underscore to space for DB
            else:
                # Filter by location column (city/country)
                where_conditions.append("location ILIKE %s")
                where_params.append(f"%{location}%")
        
        if job_type:
            # Use ILIKE for flexible matching (handles different languages)
            where_conditions.append("job_type ILIKE %s")
            where_params.append(f"%{job_type}%")
        
        if remote_only:
            where_conditions.append("remote = TRUE")
        
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        # Get total count
        count_query = f"SELECT COUNT(*) as count FROM jobs WHERE {where_clause}"
        count_result = db.execute_query(count_query, tuple(where_params))
        total = count_result[0]['count'] if count_result else 0
        
        # Get jobs for current page
        jobs_query = f"""
            SELECT * FROM jobs 
            WHERE {where_clause}
            ORDER BY fetched_at DESC
            LIMIT %s OFFSET %s
        """
        jobs = db.execute_query(jobs_query, tuple(where_params + [page_size, offset]))
        
        # Convert to JobListItem models
        job_items = []
        for job in jobs:
            # Parse JSONB fields
            required_skills = job.get('required_skills', [])
            if isinstance(required_skills, str):
                required_skills = json.loads(required_skills)
            
            salary_range = job.get('salary_range')
            if isinstance(salary_range, str):
                salary_range = json.loads(salary_range) if salary_range else None
            
            # Build SalaryRange model
            salary = None
            if salary_range:
                salary = SalaryRange(
                    min=salary_range.get('min'),
                    max=salary_range.get('max'),
                    currency=salary_range.get('currency', 'USD'),
                    text=salary_range.get('text')
                )
            
            job_item = JobListItem(
                id=job['job_id'],
                title=job['title'],
                company=job['company'],
                location=job['location'],
                remote=job.get('remote', False),
                job_type=job.get('job_type', 'Full-time'),
                experience_level=job.get('experience_level'),
                salary_range=salary,
                posted_date=job.get('posted_date'),
                url=job['url'],
                required_skills=required_skills[:5]  # Top 5 skills
            )
            job_items.append(job_item)
        
        total_pages = (total + page_size - 1) // page_size
        
        return JobListResponse(
            jobs=job_items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Job list failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve job list: {str(e)}"
        )


@router.post("/search", response_model=JobListResponse)
async def search_jobs(
    request: JobSearchRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Advanced job search with multiple filters
    
    - **keywords**: Search in title/description
    - **location**: Location filter
    - **job_type**: Employment type filter
    - **experience_level**: Experience level filter
    - **remote_only**: Show only remote jobs
    - **min_salary/max_salary**: Salary range filter
    - **required_skills**: Must have these skills
    - **page/page_size**: Pagination
    
    Returns filtered and paginated job list
    """
    try:
        logger.info(f"User {current_user.id} initiated job search")
        
        # Build WHERE clause
        where_conditions = ["1=1"]  # Always true base condition
        where_params = []
        
        # Keyword search in title and description
        if request.keywords:
            where_conditions.append("(title ILIKE %s OR description ILIKE %s)")
            search_pattern = f"%{request.keywords}%"
            where_params.extend([search_pattern, search_pattern])
        
        # Location filter
        if request.location:
            where_conditions.append("location ILIKE %s")
            where_params.append(f"%{request.location}%")
        
        # Job type filter
        if request.job_type:
            where_conditions.append("job_type = %s")
            where_params.append(request.job_type.value)
        
        # Experience level filter
        if request.experience_level:
            where_conditions.append("experience_level = %s")
            where_params.append(request.experience_level.value)
        
        # Remote only filter
        if request.remote_only:
            where_conditions.append("remote = TRUE")
        
        # Salary range filter (more complex due to JSONB)
        if request.min_salary:
            where_conditions.append("(salary_range->>'min')::int >= %s")
            where_params.append(request.min_salary)
        
        if request.max_salary:
            where_conditions.append("(salary_range->>'max')::int <= %s")
            where_params.append(request.max_salary)
        
        # Required skills filter (JSONB array contains)
        if request.required_skills:
            for skill in request.required_skills:
                where_conditions.append("required_skills @> %s")
                where_params.append(json.dumps([skill]))
        
        where_clause = " AND ".join(where_conditions)
        
        # Pagination
        page = max(1, request.page)
        page_size = min(100, max(1, request.page_size))
        offset = (page - 1) * page_size
        
        # Get total count
        count_query = f"SELECT COUNT(*) as count FROM jobs WHERE {where_clause}"
        count_result = db.execute_query(count_query, tuple(where_params))
        total = count_result[0]['count'] if count_result else 0
        
        # Get jobs for current page
        jobs_query = f"""
            SELECT * FROM jobs 
            WHERE {where_clause}
            ORDER BY fetched_at DESC
            LIMIT %s OFFSET %s
        """
        jobs = db.execute_query(jobs_query, tuple(where_params + [page_size, offset]))
        
        # Convert to JobListItem models (same as list endpoint)
        job_items = []
        for job in jobs:
            required_skills = job.get('required_skills', [])
            if isinstance(required_skills, str):
                required_skills = json.loads(required_skills)
            
            salary_range = job.get('salary_range')
            if isinstance(salary_range, str):
                salary_range = json.loads(salary_range) if salary_range else None
            
            salary = None
            if salary_range:
                salary = SalaryRange(
                    min=salary_range.get('min'),
                    max=salary_range.get('max'),
                    currency=salary_range.get('currency', 'USD'),
                    text=salary_range.get('text')
                )
            
            job_item = JobListItem(
                id=job['job_id'],
                title=job['title'],
                company=job['company'],
                location=job['location'],
                remote=job.get('remote', False),
                job_type=job.get('job_type', 'Full-time'),
                experience_level=job.get('experience_level'),
                salary_range=salary,
                posted_date=job.get('posted_date'),
                url=job['url'],
                required_skills=required_skills[:5]
            )
            job_items.append(job_item)
        
        total_pages = (total + page_size - 1) // page_size
        
        logger.info(f"Search returned {len(job_items)} jobs (total: {total})")
        
        return JobListResponse(
            jobs=job_items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
    except Exception as e:
        logger.error(f"Job search failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job search failed: {str(e)}"
        )


@router.get("/insights", response_model=MarketInsights)
async def get_market_insights(
    region: str = "MENA",
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get job market insights for a region
    
    - **region**: Region name (MENA, Sub-Saharan Africa, etc.)
    
    Returns market statistics, top skills, salary ranges
    """
    try:
        logger.info(f"User {current_user.id} requested market insights for {region}")
        
        # Get jobs for region from database
        jobs_query = """
            SELECT * FROM jobs 
            WHERE region ILIKE %s
            ORDER BY fetched_at DESC
            LIMIT 500
        """
        jobs = db.execute_query(jobs_query, (f"%{region}%",))
        
        if not jobs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No jobs found in region: {region}"
            )
        
        # Convert to matcher format and use matcher's insights method
        matcher.jobs_database = []
        for job in jobs:
            required_skills = job.get('required_skills', [])
            if isinstance(required_skills, str):
                required_skills = json.loads(required_skills)
            
            preferred_skills = job.get('preferred_skills', [])
            if isinstance(preferred_skills, str):
                preferred_skills = json.loads(preferred_skills)
            
            salary_range = job.get('salary_range')
            if isinstance(salary_range, str):
                salary_range = json.loads(salary_range) if salary_range else None
            
            matcher.jobs_database.append({
                'id': job['job_id'],
                'title': job['title'],
                'company': job['company'],
                'location': job['location'],
                'region': job.get('region', 'Other'),
                'type': job.get('job_type', 'Full-time'),
                'experience_level': job.get('experience_level', 'Mid-level'),
                'description': job.get('description', ''),
                'required_skills': required_skills,
                'preferred_skills': preferred_skills,
                'salary_range': salary_range,
                'posted_date': job.get('posted_date', ''),
                'remote': job.get('remote', False),
                'url': job['url']
            })
        
        # Generate insights
        insights_data = matcher.get_market_insights(region=region)
        
        # Convert to response model
        from backend.app.models.job import SkillDemand, AverageSalary
        
        insights = MarketInsights(
            region=insights_data['region'],
            total_jobs=insights_data['total_jobs'],
            top_skills=[
                SkillDemand(skill=s['skill'], demand=s['demand'])
                for s in insights_data['top_skills']
            ],
            average_salaries={
                level: AverageSalary(average=data['average'], currency=data['currency'])
                for level, data in insights_data['average_salaries'].items()
            },
            remote_jobs_percentage=insights_data['remote_jobs_percentage'],
            generated_at=insights_data['generated_at']
        )
        
        return insights
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Market insights failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate market insights: {str(e)}"
        )


@router.get("/{job_id}", response_model=JobDetailResponse)
async def get_job_details(
    job_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get detailed information about a specific job
    
    - **job_id**: Unique job identifier
    
    Returns full job details with similar job recommendations
    """
    try:
        logger.info(f"User {current_user.id} requested details for job {job_id}")
        
        # Get job from database
        job = db.get_one('jobs', f"job_id = %s", (job_id,))
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job {job_id} not found"
            )
        
        # Parse JSONB fields
        required_skills = job.get('required_skills', [])
        if isinstance(required_skills, str):
            required_skills = json.loads(required_skills)
        
        preferred_skills = job.get('preferred_skills', [])
        if isinstance(preferred_skills, str):
            preferred_skills = json.loads(preferred_skills)
        
        salary_range = job.get('salary_range')
        if isinstance(salary_range, str):
            salary_range = json.loads(salary_range) if salary_range else None
        
        # Build SalaryRange model
        salary = None
        if salary_range:
            salary = SalaryRange(
                min=salary_range.get('min'),
                max=salary_range.get('max'),
                currency=salary_range.get('currency', 'USD'),
                text=salary_range.get('text')
            )
        
        # Build JobPost model
        fetched_at_str = job.get('fetched_at', '')
        if isinstance(fetched_at_str, datetime):
            fetched_at_str = fetched_at_str.isoformat()
        elif fetched_at_str and not isinstance(fetched_at_str, str):
            fetched_at_str = str(fetched_at_str)
        
        job_post = JobPost(
            id=job['job_id'],
            title=job['title'],
            company=job['company'],
            location=job['location'],
            region=job.get('region'),
            type=job.get('job_type', 'Full-time'),
            experience_level=job.get('experience_level'),
            description=job.get('description', ''),
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            salary_range=salary,
            posted_date=job.get('posted_date'),
            remote=job.get('remote', False),
            url=job['url'],
            source=job.get('source'),
            fetched_at=fetched_at_str
        )
        
        # Find similar jobs (same location or similar title)
        similar_query = """
            SELECT * FROM jobs 
            WHERE job_id != %s 
            AND (location = %s OR title ILIKE %s)
            ORDER BY fetched_at DESC
            LIMIT 5
        """
        similar_jobs_data = db.execute_query(
            similar_query,
            (job_id, job['location'], f"%{job['title'][:20]}%")
        )
        
        # Convert similar jobs to JobListItem
        similar_jobs = []
        for similar_job in similar_jobs_data:
            similar_skills = similar_job.get('required_skills', [])
            if isinstance(similar_skills, str):
                similar_skills = json.loads(similar_skills)
            
            similar_salary = similar_job.get('salary_range')
            if isinstance(similar_salary, str):
                similar_salary = json.loads(similar_salary) if similar_salary else None
            
            similar_salary_obj = None
            if similar_salary:
                similar_salary_obj = SalaryRange(
                    min=similar_salary.get('min'),
                    max=similar_salary.get('max'),
                    currency=similar_salary.get('currency', 'USD'),
                    text=similar_salary.get('text')
                )
            
            similar_item = JobListItem(
                id=similar_job['job_id'],
                title=similar_job['title'],
                company=similar_job['company'],
                location=similar_job['location'],
                remote=similar_job.get('remote', False),
                job_type=similar_job.get('job_type', 'Full-time'),
                experience_level=similar_job.get('experience_level'),
                salary_range=similar_salary_obj,
                posted_date=similar_job.get('posted_date'),
                url=similar_job['url'],
                required_skills=similar_skills[:5]
            )
            similar_jobs.append(similar_item)
        
        return JobDetailResponse(
            job=job_post,
            similar_jobs=similar_jobs
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get job details failed: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get job details: {str(e)}"
        )
