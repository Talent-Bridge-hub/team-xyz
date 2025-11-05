"""
Job Matcher

Advanced algorithms for matching jobs to resumes based on skills,
experience, location, and other factors.
"""

from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime


class JobMatcher:
    """
    Job matching algorithms.
    
    Calculates match scores between jobs and resumes based on:
    - Skill overlap
    - Experience level match
    - Location compatibility
    - Job type preferences
    """
    
    @staticmethod
    def calculate_skill_score(
        resume_skills: List[str],
        required_skills: List[str],
        preferred_skills: List[str] = None
    ) -> Tuple[int, Dict[str, List[str]]]:
        """
        Calculate skill match score.
        
        Args:
            resume_skills: Skills from resume
            required_skills: Required skills for job
            preferred_skills: Preferred skills for job
            
        Returns:
            Tuple of (score, breakdown_dict)
        """
        if not required_skills:
            return 50, {"matched": [], "missing": []}
        
        # Normalize skills to lowercase for comparison
        resume_skills_lower = [s.lower() for s in resume_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        preferred_skills_lower = [s.lower() for s in (preferred_skills or [])]
        
        # Find matches
        matched_required = [
            s for s in required_skills 
            if s.lower() in resume_skills_lower
        ]
        missing_required = [
            s for s in required_skills 
            if s.lower() not in resume_skills_lower
        ]
        
        matched_preferred = []
        if preferred_skills:
            matched_preferred = [
                s for s in preferred_skills
                if s.lower() in resume_skills_lower
            ]
        
        # Calculate score
        # Required skills: 80% weight
        # Preferred skills: 20% weight
        required_score = (len(matched_required) / len(required_skills) * 80) if required_skills else 0
        preferred_score = (len(matched_preferred) / len(preferred_skills_lower) * 20) if preferred_skills_lower else 10
        
        total_score = int(required_score + preferred_score)
        
        breakdown = {
            "matched": matched_required + matched_preferred,
            "missing": missing_required
        }
        
        return total_score, breakdown
    
    @staticmethod
    def calculate_experience_score(
        resume_years: int,
        job_level: str
    ) -> int:
        """
        Calculate experience level match score.
        
        Args:
            resume_years: Years of experience from resume
            job_level: Job experience level (Junior, Mid-level, Senior, etc.)
            
        Returns:
            Score from 0-100
        """
        # Define experience ranges for each level
        level_ranges = {
            "Junior": (0, 2),
            "Mid-level": (2, 5),
            "Senior": (5, 10),
            "Lead": (8, 15),
            "Executive": (12, 30)
        }
        
        if not job_level or job_level not in level_ranges:
            return 75  # Default score if level unknown
        
        min_years, max_years = level_ranges[job_level]
        
        # Perfect match
        if min_years <= resume_years <= max_years:
            return 100
        
        # Overqualified (slight penalty)
        if resume_years > max_years:
            excess = resume_years - max_years
            penalty = min(excess * 5, 30)  # Max 30 point penalty
            return 100 - penalty
        
        # Underqualified (larger penalty)
        if resume_years < min_years:
            deficit = min_years - resume_years
            penalty = min(deficit * 15, 60)  # Max 60 point penalty
            return 100 - penalty
        
        return 50  # Fallback
    
    @staticmethod
    def calculate_location_score(
        resume_location: str,
        job_location: str,
        job_remote: bool
    ) -> int:
        """
        Calculate location compatibility score.
        
        Args:
            resume_location: Candidate's location
            job_location: Job location
            job_remote: Whether job is remote
            
        Returns:
            Score from 0-100
        """
        if job_remote:
            return 100  # Perfect match for remote jobs
        
        if not resume_location or not job_location:
            return 60  # Neutral score if location unknown
        
        # Normalize for comparison
        resume_loc_lower = resume_location.lower()
        job_loc_lower = job_location.lower()
        
        # Exact match
        if resume_loc_lower == job_loc_lower:
            return 100
        
        # Same city
        if resume_loc_lower in job_loc_lower or job_loc_lower in resume_loc_lower:
            return 90
        
        # Same country (rough heuristic - last word often country)
        resume_parts = resume_loc_lower.split(',')
        job_parts = job_loc_lower.split(',')
        
        if resume_parts and job_parts:
            resume_country = resume_parts[-1].strip()
            job_country = job_parts[-1].strip()
            if resume_country == job_country:
                return 75  # Same country, different city
        
        # Different location
        return 40
    
    @staticmethod
    def calculate_overall_score(
        skill_score: int,
        experience_score: int,
        location_score: int,
        weights: Dict[str, float] = None
    ) -> int:
        """
        Calculate weighted overall match score.
        
        Args:
            skill_score: Skill match score
            experience_score: Experience match score
            location_score: Location match score
            weights: Custom weights (default: skills=0.5, experience=0.3, location=0.2)
            
        Returns:
            Overall score from 0-100
        """
        if weights is None:
            weights = {
                "skills": 0.5,
                "experience": 0.3,
                "location": 0.2
            }
        
        overall = (
            skill_score * weights.get("skills", 0.5) +
            experience_score * weights.get("experience", 0.3) +
            location_score * weights.get("location", 0.2)
        )
        
        return int(overall)
    
    @staticmethod
    def match_job_to_resume(
        job_data: Dict[str, Any],
        resume_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Complete matching algorithm for job-resume pair.
        
        Args:
            job_data: Job information
            resume_data: Resume information
            
        Returns:
            Match result with scores and breakdown
        """
        # Extract data
        resume_skills = resume_data.get('skills', [])
        resume_years = resume_data.get('years_experience', 0)
        resume_location = resume_data.get('location', '')
        
        job_required_skills = job_data.get('required_skills', [])
        job_preferred_skills = job_data.get('preferred_skills', [])
        job_level = job_data.get('experience_level', '')
        job_location = job_data.get('location', '')
        job_remote = job_data.get('remote', False)
        
        # Calculate scores
        skill_score, skill_breakdown = JobMatcher.calculate_skill_score(
            resume_skills,
            job_required_skills,
            job_preferred_skills
        )
        
        experience_score = JobMatcher.calculate_experience_score(
            resume_years,
            job_level
        )
        
        location_score = JobMatcher.calculate_location_score(
            resume_location,
            job_location,
            job_remote
        )
        
        overall_score = JobMatcher.calculate_overall_score(
            skill_score,
            experience_score,
            location_score
        )
        
        return {
            "overall_score": overall_score,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "location_score": location_score,
            "breakdown": {
                "matched_skills": skill_breakdown["matched"],
                "missing_skills": skill_breakdown["missing"]
            },
            "matched_at": datetime.utcnow().isoformat()
        }


class JobRecommendationEngine:
    """
    Job recommendation engine.
    
    Suggests jobs based on:
    - Career trajectory
    - Skill development path
    - Market trends
    """
    
    @staticmethod
    def suggest_skill_upgrades(
        current_skills: List[str],
        target_job_skills: List[str]
    ) -> List[str]:
        """
        Suggest skills to learn for target job.
        
        Args:
            current_skills: Current skill set
            target_job_skills: Skills required for target job
            
        Returns:
            List of skills to learn
        """
        current_lower = [s.lower() for s in current_skills]
        missing = [
            s for s in target_job_skills
            if s.lower() not in current_lower
        ]
        
        return missing
    
    @staticmethod
    def find_growth_opportunities(
        current_level: str,
        years_experience: int
    ) -> List[str]:
        """
        Suggest next career steps.
        
        Args:
            current_level: Current experience level
            years_experience: Years of experience
            
        Returns:
            List of recommended next levels
        """
        # Career progression path
        progression = {
            "Junior": ["Mid-level"] if years_experience >= 2 else ["Junior"],
            "Mid-level": ["Senior", "Lead"] if years_experience >= 4 else ["Mid-level"],
            "Senior": ["Lead", "Executive"] if years_experience >= 7 else ["Senior"],
            "Lead": ["Executive"] if years_experience >= 10 else ["Lead", "Senior"],
            "Executive": ["Executive"]
        }
        
        return progression.get(current_level, ["Mid-level"])


def calculate_job_freshness_score(posted_date: datetime) -> int:
    """
    Calculate freshness score based on job posting date.
    
    Args:
        posted_date: When job was posted
        
    Returns:
        Freshness score (100 = today, decreases over time)
    """
    if not posted_date:
        return 50  # Unknown date
    
    days_old = (datetime.utcnow() - posted_date).days
    
    if days_old == 0:
        return 100
    elif days_old <= 7:
        return 90
    elif days_old <= 14:
        return 75
    elif days_old <= 30:
        return 60
    elif days_old <= 60:
        return 40
    else:
        return 20


def extract_salary_value(salary_text: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Extract salary range from text.
    
    Args:
        salary_text: Salary description text
        
    Returns:
        Tuple of (min_salary, max_salary)
    """
    # TODO: Implement salary parsing from text
    # Handle formats like: "$50K-$70K", "$50,000 - $70,000", "50-70k USD"
    return None, None
