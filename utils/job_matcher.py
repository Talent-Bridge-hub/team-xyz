"""
Job Matcher Module for UtopiaHire
Matches candidates with relevant jobs based on their skills and experience

WHY THIS MODULE:
- Automatically discovers job opportunities
- Matches candidate skills to job requirements
- Provides regional job market insights
- Calculates match scores
- Filters by location, salary, experience level

APPROACH:
- Web scraping (LinkedIn, Indeed, local job boards)
- Skill matching algorithm
- Location-based filtering
- Salary range estimation
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import re
from collections import Counter

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import real job scraper
try:
    from utils.job_scraper import RealJobScraper
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False
    logger.warning("Job scraper not available - using sample data only")


class JobMatcher:
    """
    Match candidates with relevant job opportunities
    """
    
    # Job boards to scrape (starting with sample data, will add real scraping later)
    JOB_BOARDS = {
        'linkedin': 'https://www.linkedin.com/jobs',
        'indeed': 'https://www.indeed.com',
        'bayt': 'https://www.bayt.com',  # Popular in MENA
        'jobrapido': 'https://tn.jobrapido.com',  # Tunisia
        'tanqeeb': 'https://www.tanqeeb.com',  # MENA focused
    }
    
    # Sample job database (will be replaced with real scraping)
    SAMPLE_JOBS = [
        {
            'id': 'job_001',
            'title': 'Software Engineer',
            'company': 'TechCorp Tunisia',
            'location': 'Tunis, Tunisia',
            'region': 'MENA',
            'type': 'Full-time',
            'experience_level': 'Mid-level',
            'description': 'Develop and maintain web applications using Python, React, and PostgreSQL. Work with cross-functional teams.',
            'required_skills': ['Python', 'React', 'PostgreSQL', 'Git', 'REST APIs'],
            'preferred_skills': ['Docker', 'AWS', 'Agile'],
            'salary_range': {'min': 2500, 'max': 4000, 'currency': 'EUR'},
            'posted_date': '2025-10-10',
            'remote': True,
            'url': 'https://example.com/job/001'
        },
        {
            'id': 'job_002',
            'title': 'Frontend Developer',
            'company': 'Digital Solutions',
            'location': 'Lagos, Nigeria',
            'region': 'Sub-Saharan Africa',
            'type': 'Full-time',
            'experience_level': 'Junior',
            'description': 'Build responsive web interfaces using React, JavaScript, and modern CSS.',
            'required_skills': ['JavaScript', 'React', 'HTML', 'CSS', 'Git'],
            'preferred_skills': ['TypeScript', 'Redux', 'Tailwind CSS'],
            'salary_range': {'min': 1500, 'max': 2500, 'currency': 'USD'},
            'posted_date': '2025-10-12',
            'remote': False,
            'url': 'https://example.com/job/002'
        },
        {
            'id': 'job_003',
            'title': 'Data Analyst',
            'company': 'Analytics Hub',
            'location': 'Nairobi, Kenya',
            'region': 'Sub-Saharan Africa',
            'type': 'Contract',
            'experience_level': 'Mid-level',
            'description': 'Analyze business data, create dashboards, provide insights using SQL, Python, and visualization tools.',
            'required_skills': ['Python', 'SQL', 'Data Analysis', 'Excel'],
            'preferred_skills': ['Tableau', 'Power BI', 'Machine Learning'],
            'salary_range': {'min': 2000, 'max': 3500, 'currency': 'USD'},
            'posted_date': '2025-10-11',
            'remote': True,
            'url': 'https://example.com/job/003'
        },
        {
            'id': 'job_004',
            'title': 'Full Stack Developer',
            'company': 'Innovation Labs',
            'location': 'Cairo, Egypt',
            'region': 'MENA',
            'type': 'Full-time',
            'experience_level': 'Senior',
            'description': 'Lead development of scalable web applications. Mentor junior developers. Work with Node.js, React, MongoDB.',
            'required_skills': ['Node.js', 'React', 'MongoDB', 'JavaScript', 'REST APIs'],
            'preferred_skills': ['TypeScript', 'Docker', 'Kubernetes', 'AWS'],
            'salary_range': {'min': 3000, 'max': 5000, 'currency': 'EUR'},
            'posted_date': '2025-10-09',
            'remote': False,
            'url': 'https://example.com/job/004'
        },
        {
            'id': 'job_005',
            'title': 'Backend Developer',
            'company': 'Cloud Systems',
            'location': 'Casablanca, Morocco',
            'region': 'MENA',
            'type': 'Full-time',
            'experience_level': 'Mid-level',
            'description': 'Design and implement scalable backend services. Work with Django, PostgreSQL, Redis, and microservices.',
            'required_skills': ['Python', 'Django', 'PostgreSQL', 'REST APIs', 'Git'],
            'preferred_skills': ['Redis', 'Microservices', 'Docker'],
            'salary_range': {'min': 2800, 'max': 4200, 'currency': 'EUR'},
            'posted_date': '2025-10-13',
            'remote': True,
            'url': 'https://example.com/job/005'
        }
    ]
    
    def __init__(self, use_real_jobs: bool = True):
        """
        Initialize job matcher
        
        Args:
            use_real_jobs: If True, fetches real jobs from APIs. If False, uses sample data.
        
        NOTE: Real jobs are DEFAULT for frontend - they include apply URLs!
        """
        self.jobs_database = []  # Start empty - will be populated from real APIs
        self.use_real_jobs = use_real_jobs and SCRAPER_AVAILABLE
        self.scraper = RealJobScraper() if self.use_real_jobs else None
        
        if self.use_real_jobs:
            logger.info("✓ Job Matcher initialized with REAL job scraping (URLs included)")
        else:
            # Only use sample jobs as fallback
            self.jobs_database = self.SAMPLE_JOBS.copy()
            logger.info("⚠ Job Matcher initialized with sample jobs (no URLs)")
    
    def fetch_real_jobs(
        self,
        queries: List[str] = None,
        locations: List[str] = None,
        num_results: int = 20
    ) -> int:
        """
        Fetch real jobs from APIs and add to database
        
        Args:
            queries: List of job titles to search (default: common tech jobs)
            locations: List of locations (default: Tunisia, Egypt, Nigeria)
            num_results: Number of results per query
        
        Returns:
            Number of jobs fetched
        """
        if not self.use_real_jobs:
            logger.warning("Real job scraping is disabled")
            return 0
        
        # Default queries
        if not queries:
            queries = ['Software Engineer', 'Data Analyst', 'Frontend Developer']
        
        # Default locations
        if not locations:
            locations = ['Tunisia', 'Egypt', 'Nigeria', 'Kenya']
        
        logger.info(f"Fetching real jobs: {len(queries)} queries × {len(locations)} locations")
        
        total_jobs = 0
        for query in queries:
            for location in locations:
                try:
                    jobs = self.scraper.search_jobs(query, location, num_results=num_results)
                    
                    # Convert to our internal format
                    for job in jobs:
                        internal_job = self._convert_to_internal_format(job)
                        self.jobs_database.append(internal_job)
                        total_jobs += 1
                    
                    logger.info(f"✓ Added {len(jobs)} jobs for '{query}' in {location}")
                    
                except Exception as e:
                    logger.error(f"✗ Failed to fetch jobs for '{query}' in {location}: {e}")
        
        logger.info(f"✓ Total real jobs fetched: {total_jobs}")
        return total_jobs
    
    def _convert_to_internal_format(self, api_job: Dict) -> Dict:
        """
        Convert API job format to internal job format
        
        CRITICAL: Ensures 'url' field is always present for frontend "Apply Now" button!
        """
        # Extract skills from description if not provided
        skills = api_job.get('skills', [])
        if not skills:
            skills = self._extract_skills_from_description(api_job.get('description', ''))
        
        # Determine region from location
        location = api_job.get('location', '')
        region = self._determine_region(location)
        
        # Determine experience level from title/description
        experience_level = self._extract_experience_level_from_job(
            api_job.get('title', ''),
            api_job.get('description', '')
        )
        
        # IMPORTANT: Validate and ensure URL is present for frontend
        job_url = api_job.get('url', '')
        if not job_url or job_url == '':
            # Fallback: Try to construct a search URL if no direct apply link
            job_title = api_job.get('title', '').replace(' ', '+')
            company = api_job.get('company', '').replace(' ', '+')
            location_search = location.replace(' ', '+')
            job_url = f"https://www.google.com/search?q={job_title}+{company}+{location_search}+jobs"
            logger.debug(f"⚠ No direct URL for {api_job.get('title')} - using search fallback")
        
        return {
            'id': api_job.get('id', f"job_{len(self.jobs_database)}"),
            'title': api_job.get('title', 'N/A'),
            'company': api_job.get('company', 'N/A'),
            'location': location,
            'region': region,
            'type': api_job.get('job_type', 'Full-time'),
            'experience_level': experience_level,
            'description': api_job.get('description', ''),
            'required_skills': skills[:5],  # Top 5 skills
            'preferred_skills': skills[5:10] if len(skills) > 5 else [],
            'salary_range': api_job.get('salary_range') or {'min': 0, 'max': 0, 'currency': 'USD'},
            'posted_date': api_job.get('posted_date', ''),
            'remote': api_job.get('remote', False),
            'url': job_url,  # ALWAYS has a value (direct link or search fallback)
            'source': api_job.get('source', 'API'),
            'fetched_at': api_job.get('fetched_at', datetime.now().isoformat())
        }
    
    def _extract_skills_from_description(self, description: str) -> List[str]:
        """Extract skills from job description using keyword matching"""
        common_skills = [
            'python', 'javascript', 'java', 'c++', 'react', 'angular', 'vue',
            'node.js', 'django', 'flask', 'spring', 'postgresql', 'mongodb',
            'mysql', 'redis', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'git', 'rest api', 'graphql', 'tensorflow', 'pytorch', 'sql',
            'html', 'css', 'typescript', 'ruby', 'php', 'go', 'rust'
        ]
        
        description_lower = description.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in description_lower:
                found_skills.append(skill.title())
        
        return found_skills[:10]  # Max 10 skills
    
    def _determine_region(self, location: str) -> str:
        """Determine region from location string"""
        location_lower = location.lower()
        
        mena_keywords = ['tunisia', 'egypt', 'morocco', 'algeria', 'jordan', 
                        'lebanon', 'uae', 'saudi', 'qatar', 'kuwait', 'bahrain']
        africa_keywords = ['nigeria', 'kenya', 'south africa', 'ghana', 'ethiopia',
                          'tanzania', 'uganda', 'senegal', 'rwanda']
        
        for keyword in mena_keywords:
            if keyword in location_lower:
                return 'MENA'
        
        for keyword in africa_keywords:
            if keyword in location_lower:
                return 'Sub-Saharan Africa'
        
        return 'Other'
    
    def _extract_experience_level_from_job(self, title: str, description: str) -> str:
        """Extract experience level from job title and description"""
        text = (title + ' ' + description).lower()
        
        if any(word in text for word in ['senior', 'lead', 'principal', 'architect', '5+ years', '7+ years']):
            return 'Senior'
        elif any(word in text for word in ['junior', 'entry', 'graduate', '0-2 years', 'recent graduate']):
            return 'Junior'
        else:
            return 'Mid-level'
    
    def find_matches(self, candidate_profile: Dict, limit: int = 10, fetch_real: bool = True) -> List[Dict]:
        """
        Find job matches for a candidate
        
        Args:
            candidate_profile: Parsed resume data with skills, experience, etc.
            limit: Maximum number of matches to return
            fetch_real: If True, fetches fresh jobs from APIs before matching (DEFAULT for frontend)
            
        Returns:
            List of job matches with scores (includes apply URLs for frontend buttons)
        
        IMPORTANT: Real jobs include 'url' field for frontend "Apply Now" buttons!
        """
        # ALWAYS fetch real jobs if enabled (default behavior for frontend)
        if fetch_real and self.use_real_jobs:
            logger.info("🔍 Fetching fresh jobs from APIs...")
            self.fetch_real_jobs(num_results=15)  # More results for better matches
        
        if len(self.jobs_database) == 0:
            logger.warning("⚠ No jobs in database! Please run scrape command first.")
            return []
        
        logger.info(f"Finding job matches from {len(self.jobs_database)} jobs...")
        
        # Extract candidate information
        candidate_skills = self._extract_candidate_skills(candidate_profile)
        candidate_experience = self._extract_experience_level(candidate_profile)
        candidate_location = candidate_profile.get('contact_info', {}).get('location', '')
        
        # Calculate match score for each job
        matches = []
        for job in self.jobs_database:
            match_score = self._calculate_match_score(
                candidate_skills,
                candidate_experience,
                candidate_location,
                job
            )
            
            if match_score['overall_score'] >= 50:  # Minimum threshold
                matches.append({
                    'job': job,
                    'match_score': match_score,
                    'matched_at': datetime.now().isoformat()
                })
        
        # Sort by overall score (descending)
        matches.sort(key=lambda x: x['match_score']['overall_score'], reverse=True)
        
        logger.info(f"✓ Found {len(matches)} job matches")
        return matches[:limit]
    
    def _extract_candidate_skills(self, profile: Dict) -> List[str]:
        """Extract and normalize candidate skills"""
        skills = profile.get('structured_data', {}).get('skills', [])
        
        # Normalize skills (lowercase, strip whitespace)
        normalized = [skill.lower().strip() for skill in skills]
        
        return normalized
    
    def _extract_experience_level(self, profile: Dict) -> str:
        """
        Determine candidate experience level from resume
        
        Returns: 'Junior', 'Mid-level', or 'Senior'
        """
        experience_entries = profile.get('structured_data', {}).get('experience', [])
        
        # Count years (simplified - looks for year patterns)
        text = profile.get('raw_text', '')
        years = re.findall(r'\b(19|20)\d{2}\b', text)
        
        if len(years) >= 4:  # 2+ years range
            return 'Mid-level'
        elif len(years) >= 6:  # 3+ years range
            return 'Senior'
        else:
            return 'Junior'
    
    def _calculate_match_score(
        self,
        candidate_skills: List[str],
        candidate_experience: str,
        candidate_location: str,
        job: Dict
    ) -> Dict:
        """
        Calculate comprehensive match score with enhanced algorithm
        
        Returns: Dict with skill_score, location_score, experience_score, overall_score
        """
        # 1. Skill matching (50% weight) - most important
        skill_score = self._calculate_skill_score(candidate_skills, job)
        
        # 2. Experience level matching (25% weight) - critical for role fit
        experience_score = self._calculate_experience_score(candidate_experience, job)
        
        # 3. Location matching (15% weight) - flexible with remote work
        location_score = self._calculate_location_score(candidate_location, job)
        
        # 4. Job title relevance (10% weight) - semantic matching
        title_score = self._calculate_title_score(candidate_skills, job)
        
        # Calculate weighted overall score with enhanced formula
        overall_score = int(
            skill_score * 0.50 +
            experience_score * 0.25 +
            location_score * 0.15 +
            title_score * 0.10
        )
        
        return {
            'overall_score': overall_score,
            'skill_score': skill_score,
            'location_score': location_score,
            'experience_score': experience_score,
            'breakdown': {
                'matched_skills': self._get_matched_skills(candidate_skills, job),
                'missing_skills': self._get_missing_skills(candidate_skills, job)
            }
        }
    
    def _calculate_skill_score(self, candidate_skills: List[str], job: Dict) -> int:
        """
        Enhanced skill match score with fuzzy matching and skill categories
        (0-100)
        """
        required_skills = [s.lower().strip() for s in job.get('required_skills', [])]
        preferred_skills = [s.lower().strip() for s in job.get('preferred_skills', [])]
        
        if not required_skills and not preferred_skills:
            return 60  # Neutral score if no requirements specified
        
        # Fuzzy skill matching (handles variations like "React.js" vs "React")
        def fuzzy_match(skill: str, skill_list: List[str]) -> bool:
            skill_clean = re.sub(r'[.\-_]', '', skill.lower())
            for s in skill_list:
                s_clean = re.sub(r'[.\-_]', '', s.lower())
                # Check direct match or partial match for compound skills
                if skill_clean in s_clean or s_clean in skill_clean:
                    return True
                # Check word overlap for multi-word skills
                skill_words = set(skill_clean.split())
                s_words = set(s_clean.split())
                if skill_words and s_words and len(skill_words & s_words) > 0:
                    return True
            return False
        
        # Count matches with fuzzy matching
        required_matches = sum(1 for skill in required_skills if fuzzy_match(skill, candidate_skills))
        preferred_matches = sum(1 for skill in preferred_skills if fuzzy_match(skill, candidate_skills))
        
        # Calculate base scores
        if required_skills:
            required_percentage = (required_matches / len(required_skills)) * 100
        else:
            required_percentage = 100  # No requirements = perfect match
        
        if preferred_skills:
            preferred_percentage = (preferred_matches / len(preferred_skills)) * 100
        else:
            preferred_percentage = 50  # No preferences = neutral
        
        # Enhanced weighting: 75% required (critical), 25% preferred (bonus)
        score = int(required_percentage * 0.75 + preferred_percentage * 0.25)
        
        # Bonus: If candidate has significantly more skills than required (demonstrates expertise)
        if len(candidate_skills) > len(required_skills) + len(preferred_skills):
            bonus = min(10, (len(candidate_skills) - len(required_skills) - len(preferred_skills)) // 2)
            score = min(100, score + bonus)
        
        return min(100, max(0, score))
    
    def _calculate_location_score(self, candidate_location: str, job: Dict) -> int:
        """
        Enhanced location match score with better regional and remote matching
        (0-100)
        """
        job_location = job.get('location', '').lower()
        job_remote = job.get('remote', False)
        candidate_loc_lower = candidate_location.lower()
        
        # Remote jobs get perfect score (location doesn't matter)
        if job_remote:
            return 100
        
        # Exact city/country match
        if candidate_loc_lower in job_location or job_location in candidate_loc_lower:
            return 100
        
        # Enhanced regional matching with country awareness
        job_region = job.get('region', '').lower()
        
        # MENA region matching
        mena_countries = ['tunisia', 'egypt', 'morocco', 'algeria', 'libya', 'uae', 'saudi', 'jordan', 
                          'lebanon', 'qatar', 'kuwait', 'bahrain', 'oman', 'yemen', 'syria', 'iraq', 'palestine']
        candidate_in_mena = any(country in candidate_loc_lower for country in mena_countries)
        job_in_mena = 'mena' in job_region or any(country in job_location for country in mena_countries)
        
        if candidate_in_mena and job_in_mena:
            return 75  # Good match within region
        
        # Sub-Saharan Africa region matching
        ssa_countries = ['nigeria', 'kenya', 'ghana', 'south africa', 'ethiopia', 'tanzania', 
                         'uganda', 'rwanda', 'senegal', 'ivory coast', 'zimbabwe']
        candidate_in_ssa = any(country in candidate_loc_lower for country in ssa_countries)
        job_in_ssa = 'sub-saharan' in job_region or 'africa' in job_region or any(country in job_location for country in ssa_countries)
        
        if candidate_in_ssa and job_in_ssa:
            return 75  # Good match within region
        
        # Any Africa match (MENA or SSA)
        if (candidate_in_mena or candidate_in_ssa) and ('africa' in job_region or job_in_mena or job_in_ssa):
            return 60
        
        # Global/International jobs (if location says "global", "international", "anywhere")
        if any(keyword in job_location for keyword in ['global', 'international', 'anywhere', 'worldwide']):
            return 90
        
        # Different region but still relevant
        return 40
    
    def _calculate_experience_score(self, candidate_experience: str, job: Dict) -> int:
        """
        Enhanced experience level matching with better scoring
        (0-100)
        """
        job_experience = (job.get('experience_level') or '').lower()
        candidate_exp = candidate_experience.lower()
        
        # If job has no experience requirement, neutral score
        if not job_experience or job_experience == 'not specified':
            return 70
        
        # Exact match
        if candidate_exp == job_experience or candidate_exp in job_experience or job_experience in candidate_exp:
            return 100
        
        # Enhanced experience hierarchy with numeric mapping
        experience_levels = {
            'intern': 0,
            'entry': 1,
            'entry-level': 1,
            'junior': 1,
            'mid': 2,
            'mid-level': 2,
            'intermediate': 2,
            'senior': 3,
            'lead': 4,
            'principal': 5,
            'staff': 5,
            'expert': 5
        }
        
        # Find candidate and job levels
        candidate_level = None
        for exp_key, exp_val in experience_levels.items():
            if exp_key in candidate_exp:
                candidate_level = exp_val
                break
        
        job_level = None
        for exp_key, exp_val in experience_levels.items():
            if exp_key in job_experience:
                job_level = exp_val
                break
        
        # Default to mid-level if not specified
        if candidate_level is None:
            candidate_level = 2
        if job_level is None:
            job_level = 2
        
        # Calculate score based on level difference
        diff = abs(candidate_level - job_level)
        
        if diff == 0:
            return 100  # Perfect match
        elif diff == 1:
            # One level difference is acceptable
            # Overqualified is better than underqualified
            if candidate_level > job_level:
                return 90  # Overqualified (slight penalty)
            else:
                return 70  # Underqualified (more penalty)
        elif diff == 2:
            if candidate_level > job_level:
                return 70  # Significantly overqualified
            else:
                return 50  # Significantly underqualified
        else:
            # 3+ levels difference
            if candidate_level > job_level:
                return 50  # Way overqualified (might be bored)
            else:
                return 30  # Way underqualified (might struggle)
    
    def _calculate_title_score(self, candidate_skills: List[str], job: Dict) -> int:
        """
        Calculate job title relevance based on candidate skills
        (0-100)
        """
        job_title = job.get('title', '').lower()
        
        # Extract keywords from job title
        title_keywords = re.findall(r'\b\w+\b', job_title)
        title_keywords = [k for k in title_keywords if len(k) > 2]  # Remove short words
        
        # Check how many candidate skills appear in job title
        matches = sum(1 for skill in candidate_skills if any(skill.lower() in keyword or keyword in skill.lower() for keyword in title_keywords))
        
        if not title_keywords:
            return 50  # Neutral
        
        # Calculate relevance
        relevance = min(100, (matches / max(3, len(title_keywords) // 2)) * 100)
        
        return int(relevance)
    
    def _get_matched_skills(self, candidate_skills: List[str], job: Dict) -> List[str]:
        """Get list of matched skills with fuzzy matching"""
        required_skills = [s.lower().strip() for s in job.get('required_skills', [])]
        preferred_skills = [s.lower().strip() for s in job.get('preferred_skills', [])]
        all_job_skills = required_skills + preferred_skills
        
        # Enhanced fuzzy matching
        matched = []
        for cand_skill in candidate_skills:
            cand_clean = re.sub(r'[.\-_]', '', cand_skill.lower())
            for job_skill in all_job_skills:
                job_clean = re.sub(r'[.\-_]', '', job_skill.lower())
                # Check various match types
                if (cand_clean in job_clean or job_clean in cand_clean or 
                    cand_skill.lower() == job_skill or
                    any(word in job_clean.split() for word in cand_clean.split() if len(word) > 2)):
                    if cand_skill not in matched:
                        matched.append(cand_skill)
                    break
        
        return matched
    
    def _get_missing_skills(self, candidate_skills: List[str], job: Dict) -> List[str]:
        """Get list of missing required skills with fuzzy matching"""
        required_skills = [s.strip() for s in job.get('required_skills', [])]
        candidate_lower = [s.lower().strip() for s in candidate_skills]
        
        # Enhanced fuzzy matching for missing skills
        missing = []
        for req_skill in required_skills:
            req_clean = re.sub(r'[.\-_]', '', req_skill.lower())
            found = False
            for cand_skill in candidate_lower:
                cand_clean = re.sub(r'[.\-_]', '', cand_skill)
                # Check various match types
                if (req_clean in cand_clean or cand_clean in req_clean or
                    any(word in cand_clean.split() for word in req_clean.split() if len(word) > 2)):
                    found = True
                    break
            
            if not found:
                missing.append(req_skill)
        
        return missing
    
    def get_market_insights(self, region: str = 'MENA') -> Dict:
        """
        Get job market insights for a region
        
        Returns: Statistics about jobs, skills demand, salary ranges
        """
        logger.info(f"Generating market insights for {region}...")
        
        # Filter jobs by region
        regional_jobs = [job for job in self.jobs_database if region.lower() in job.get('region', '').lower()]
        
        if not regional_jobs:
            return {
                'total_jobs': 0,
                'message': f'No jobs found in {region}'
            }
        
        # Calculate insights
        total_jobs = len(regional_jobs)
        
        # Most in-demand skills
        all_skills = []
        for job in regional_jobs:
            all_skills.extend([s.lower() for s in job.get('required_skills', [])])
        
        skill_counts = Counter(all_skills)
        top_skills = skill_counts.most_common(10)
        
        # Average salary by experience level
        salary_by_level = {}
        for job in regional_jobs:
            level = job.get('experience_level', 'Unknown')
            salary_range = job.get('salary_range', {})
            
            if salary_range and 'min' in salary_range and 'max' in salary_range:
                avg_salary = (salary_range['min'] + salary_range['max']) / 2
                
                if level not in salary_by_level:
                    salary_by_level[level] = []
                salary_by_level[level].append(avg_salary)
        
        # Calculate averages
        avg_salaries = {}
        for level, salaries in salary_by_level.items():
            avg_salaries[level] = {
                'average': int(sum(salaries) / len(salaries)),
                'currency': 'EUR'  # Simplified
            }
        
        # Remote jobs percentage
        remote_jobs = sum(1 for job in regional_jobs if job.get('remote', False))
        remote_percentage = (remote_jobs / total_jobs) * 100
        
        insights = {
            'region': region,
            'total_jobs': total_jobs,
            'top_skills': [{'skill': skill, 'demand': count} for skill, count in top_skills],
            'average_salaries': avg_salaries,
            'remote_jobs_percentage': round(remote_percentage, 1),
            'generated_at': datetime.now().isoformat()
        }
        
        logger.info(f"✓ Market insights generated for {region}")
        return insights


# Test function
if __name__ == '__main__':
    print("Job Matcher Module - Ready to use!")
    print("\nUsage:")
    print("  from utils.job_matcher import JobMatcher")
    print("  matcher = JobMatcher()")
    print("  matches = matcher.find_matches(parsed_resume)")
    print("  insights = matcher.get_market_insights('MENA')")
