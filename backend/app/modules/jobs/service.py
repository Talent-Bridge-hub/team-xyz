"""
Job Service Layer

Business logic for job scraping, matching, and search.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
import math

from .schemas import (
    JobScrapingRequest,
    JobScrapingResponse,
    JobMatchingRequest,
    JobMatchingResponse,
    JobSearchRequest,
    JobListResponse,
    JobDetailResponse,
    JobPost,
    JobListItem,
    JobMatch,
    MatchScore,
    MatchScoreBreakdown,
    MarketInsights,
    SkillDemand,
    AverageSalary
)
from .models import (
    JobQueries,
    job_row_to_dict,
    job_row_to_list_item,
    prepare_job_data,
    build_filter_clause
)
from .scraper import JobScraperService
from shared.database import DatabaseWrapper


class JobService:
    """
    Service class for job operations.
    
    Handles:
    - Job scraping and storage
    - Job search and filtering
    - Job matching against resumes
    - Market insights generation
    """
    
    def __init__(self, db: DatabaseWrapper):
        """
        Initialize job service.
        
        Args:
            db: Database wrapper instance
        """
        self.db = db
        self.scraper = JobScraperService()
    
    async def scrape_and_store_jobs(
        self,
        queries: List[str],
        locations: List[str],
        num_results_per_query: int = 15
    ) -> JobScrapingResponse:
        """
        Scrape jobs from external APIs and store them.
        
        Args:
            queries: Job titles to search
            locations: Locations to search
            num_results_per_query: Results per query
            
        Returns:
            Scraping response with statistics
        """
        start_time = datetime.utcnow()
        
        # Scrape jobs using the scraper service
        raw_jobs = self.scraper.scrape_jobs(queries, locations, num_results_per_query)
        
        jobs_scraped = len(raw_jobs)
        jobs_stored = 0
        
        # Store each job in database
        for raw_job in raw_jobs:
            try:
                normalized_job = self.scraper.normalize_job_data(raw_job)
                stored_job = await self.store_job(normalized_job)
                if stored_job:
                    jobs_stored += 1
            except Exception as e:
                # Log error but continue with other jobs
                print(f"Error storing job {raw_job.get('id')}: {e}")
                continue
        
        end_time = datetime.utcnow()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        api_used = self.scraper.get_last_api_used()
        
        return JobScrapingResponse(
            jobs_scraped=jobs_scraped,
            jobs_stored=jobs_stored,
            queries_processed=len(queries),
            locations_processed=len(locations),
            api_used=api_used,
            scraping_duration_ms=duration_ms,
            message=f"Successfully scraped {jobs_scraped} jobs and stored {jobs_stored}"
        )
    
    async def store_job(self, job_data: Dict[str, Any]) -> Optional[JobPost]:
        """
        Store a single job in database.
        
        Args:
            job_data: Job data dictionary
            
        Returns:
            Stored job or None if failed
        """
        job_tuple = prepare_job_data(job_data)
        
        result = self.db.execute_query(JobQueries.INSERT_JOB, job_tuple)
        
        if not result:
            return None
        
        job_dict = job_row_to_dict(result[0])
        return JobPost(**job_dict)
    
    async def get_job_by_id(self, job_id: str) -> Optional[JobPost]:
        """
        Get job by ID.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job data or None if not found
        """
        result = self.db.execute_query(JobQueries.SELECT_BY_ID, (job_id,))
        
        if not result:
            return None
        
        job_dict = job_row_to_dict(result[0])
        return JobPost(**job_dict)
    
    async def search_jobs(
        self,
        filters: JobSearchRequest
    ) -> JobListResponse:
        """
        Search jobs with filters.
        
        Args:
            filters: Search filters
            
        Returns:
            Paginated job list
        """
        offset = (filters.page - 1) * filters.page_size
        
        # Build filter clause
        filter_dict = {
            'keywords': filters.keywords,
            'location': filters.location,
            'job_type': filters.job_type,
            'experience_level': filters.experience_level,
            'remote_only': filters.remote_only,
            'min_salary': filters.min_salary,
            'max_salary': filters.max_salary,
            'required_skills': filters.required_skills
        }
        
        filter_string, params = build_filter_clause(filter_dict)
        
        # Get total count
        count_query = JobQueries.COUNT_WITH_FILTERS.format(filters=filter_string)
        count_result = self.db.execute_query(count_query, tuple(params))
        total = count_result[0]['count'] if count_result else 0
        
        # Get jobs
        select_query = JobQueries.SELECT_WITH_FILTERS.format(filters=filter_string)
        all_params = tuple(params) + (filters.page_size, offset)
        result = self.db.execute_query(select_query, all_params)
        
        jobs = []
        if result:
            jobs = [JobListItem(**job_row_to_list_item(row)) for row in result]
        
        total_pages = math.ceil(total / filters.page_size) if total > 0 else 0
        
        return JobListResponse(
            jobs=jobs,
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            total_pages=total_pages
        )
    
    async def get_job_detail(self, job_id: str) -> JobDetailResponse:
        """
        Get job details with similar jobs.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job detail response
            
        Raises:
            HTTPException: If job not found
        """
        job = await self.get_job_by_id(job_id)
        
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        # Get similar jobs
        similar_result = self.db.execute_query(
            JobQueries.SELECT_SIMILAR_JOBS,
            (job_id, job.required_skills, job.company, 5)
        )
        
        similar_jobs = []
        if similar_result:
            similar_jobs = [JobListItem(**job_row_to_list_item(row)) for row in similar_result]
        
        return JobDetailResponse(
            job=job,
            similar_jobs=similar_jobs
        )
    
    async def match_jobs_to_resume(
        self,
        resume_id: int,
        resume_skills: List[str],
        limit: int = 10,
        min_score: int = 50
    ) -> JobMatchingResponse:
        """
        Find matching jobs for a resume.
        
        Args:
            resume_id: Resume ID
            resume_skills: Skills extracted from resume
            limit: Maximum matches to return
            min_score: Minimum match score threshold
            
        Returns:
            Job matching response with scores
        """
        start_time = datetime.utcnow()
        
        # Get all jobs (or filtered subset)
        result = self.db.execute_query(JobQueries.SELECT_ALL, (100, 0))
        
        if not result:
            return JobMatchingResponse(
                resume_id=resume_id,
                matches=[],
                total_matches=0,
                matches_found=0,
                jobs_searched=0,
                total_jobs_searched=0,
                average_score=0.0,
                avg_match_score=0.0,
                best_match_score=None,
                processing_time_ms=0,
                matched_at=datetime.utcnow().isoformat(),
                message="No jobs found"
            )
        
        # TODO: Implement actual matching algorithm in matcher.py
        # For now, create placeholder matches
        matches = []
        all_jobs = [job_row_to_dict(row) for row in result]
        
        for job_dict in all_jobs[:limit]:
            # Simple skill matching
            job_skills = job_dict.get('required_skills', [])
            matched_skills = list(set(resume_skills) & set(job_skills))
            missing_skills = list(set(job_skills) - set(resume_skills))
            
            skill_score = int((len(matched_skills) / len(job_skills) * 100)) if job_skills else 50
            
            if skill_score >= min_score:
                match_score = MatchScore(
                    overall_score=skill_score,
                    skill_score=skill_score,
                    location_score=75,
                    experience_score=75,
                    breakdown=MatchScoreBreakdown(
                        matched_skills=matched_skills,
                        missing_skills=missing_skills
                    )
                )
                
                job_match = JobMatch(
                    job=JobPost(**job_dict),
                    match_score=match_score,
                    matched_at=datetime.utcnow().isoformat()
                )
                matches.append(job_match)
        
        # Sort by score
        matches.sort(key=lambda x: x.match_score.overall_score, reverse=True)
        matches = matches[:limit]
        
        # Calculate statistics
        avg_score = sum(m.match_score.overall_score for m in matches) / len(matches) if matches else 0.0
        best_score = max((m.match_score.overall_score for m in matches), default=None)
        
        end_time = datetime.utcnow()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        
        return JobMatchingResponse(
            resume_id=resume_id,
            matches=matches,
            total_matches=len(matches),
            matches_found=len(matches),
            jobs_searched=len(all_jobs),
            total_jobs_searched=len(all_jobs),
            average_score=avg_score,
            avg_match_score=avg_score,
            best_match_score=best_score,
            processing_time_ms=duration_ms,
            matched_at=datetime.utcnow().isoformat(),
            message=f"Found {len(matches)} matching jobs"
        )
    
    async def get_market_insights(self, region: Optional[str] = None) -> MarketInsights:
        """
        Get job market insights for a region.
        
        Args:
            region: Region name (None for all regions)
            
        Returns:
            Market insights
        """
        # Get top skills
        skills_result = self.db.execute_query(
            JobQueries.GET_TOP_SKILLS,
            (region, region)
        )
        
        top_skills = []
        if skills_result:
            top_skills = [
                SkillDemand(skill=row['skill'], demand=row['demand'])
                for row in skills_result
            ]
        
        # Get average salaries
        salary_result = self.db.execute_query(
            JobQueries.GET_AVERAGE_SALARIES,
            (region, region)
        )
        
        average_salaries = {}
        if salary_result:
            for row in salary_result:
                level = row['experience_level']
                avg = int((row['avg_min'] + row['avg_max']) / 2)
                average_salaries[level] = AverageSalary(
                    average=avg,
                    currency="USD"
                )
        
        # Get remote percentage
        remote_result = self.db.execute_query(
            JobQueries.GET_REMOTE_PERCENTAGE,
            (region, region)
        )
        
        remote_percentage = remote_result[0]['percentage'] if remote_result else 0.0
        
        # Get total jobs count
        count_result = self.db.execute_query(JobQueries.COUNT_ALL)
        total_jobs = count_result[0]['count'] if count_result else 0
        
        return MarketInsights(
            region=region or "Global",
            total_jobs=total_jobs,
            top_skills=top_skills,
            average_salaries=average_salaries,
            remote_jobs_percentage=float(remote_percentage or 0.0),
            generated_at=datetime.utcnow().isoformat()
        )
    
    async def delete_old_jobs(self, days: int = 30) -> int:
        """
        Delete jobs older than specified days.
        
        Args:
            days: Number of days to keep
            
        Returns:
            Number of jobs deleted
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        count_before = self.db.execute_query(JobQueries.COUNT_ALL)
        before = count_before[0]['count'] if count_before else 0
        
        self.db.execute_query(JobQueries.DELETE_OLD_JOBS, (cutoff_date,))
        
        count_after = self.db.execute_query(JobQueries.COUNT_ALL)
        after = count_after[0]['count'] if count_after else 0
        
        return before - after
