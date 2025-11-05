"""
Job Compatibility Analyzer
Analyzes compatibility between a candidate's CV and a job description using AI
"""

import os
import logging
from typing import Dict, List, Optional
from groq import Groq
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobCompatibilityAnalyzer:
    """
    Analyzes how well a candidate's resume matches a job description
    Uses Groq API for intelligent analysis
    """
    
    def __init__(self):
        """Initialize the analyzer with Groq API"""
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            logger.warning("GROQ_API_KEY not found. AI analysis will be unavailable.")
            self.client = None
        else:
            self.client = Groq(api_key=self.groq_api_key)
            logger.info("✓ Job Compatibility Analyzer initialized with Groq API")
    
    def analyze(
        self,
        parsed_resume: Dict,
        job_description: str,
        job_title: Optional[str] = None,
        company: Optional[str] = None,
        required_skills: Optional[List[str]] = None
    ) -> Dict:
        """
        Perform comprehensive compatibility analysis
        
        Args:
            parsed_resume: Parsed resume data from ResumeParser
            job_description: Job description text
            job_title: Optional job title
            company: Optional company name
            required_skills: Optional list of required skills
        
        Returns:
            Dictionary with scores, matched/missing skills, and recommendations
        """
        logger.info(f"Analyzing compatibility for job: {job_title or 'Untitled Position'}")
        
        # Extract candidate information
        candidate_skills = self._extract_skills(parsed_resume)
        candidate_experience = parsed_resume.get('structured_data', {}).get('experience', [])
        candidate_education = parsed_resume.get('structured_data', {}).get('education', [])
        candidate_summary = parsed_resume.get('sections', {}).get('summary', '')
        
        # Extract job requirements
        job_skills = required_skills or self._extract_skills_from_description(job_description)
        job_experience_level = self._extract_experience_level(job_description)
        
        # Calculate match scores
        skill_score = self._calculate_skill_match(candidate_skills, job_skills)
        experience_score = self._calculate_experience_match(
            candidate_experience,
            job_description,
            job_experience_level
        )
        education_score = self._calculate_education_match(
            candidate_education,
            job_description
        )
        
        # Calculate overall score (weighted)
        overall_score = int(
            skill_score * 0.50 +     # Skills are most important
            experience_score * 0.35 + # Experience is critical
            education_score * 0.15    # Education is supportive
        )
        
        # Identify matched and missing skills
        matched_skills = [skill for skill in candidate_skills if skill.lower() in [s.lower() for s in job_skills]]
        missing_skills = [skill for skill in job_skills if skill.lower() not in [s.lower() for s in candidate_skills]]
        
        # Identify strengths and gaps
        strengths = self._identify_strengths(
            parsed_resume,
            job_description,
            matched_skills,
            skill_score,
            experience_score
        )
        gaps = self._identify_gaps(
            missing_skills,
            skill_score,
            experience_score,
            education_score
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            missing_skills,
            gaps,
            skill_score,
            experience_score
        )
        
        # Get AI analysis if available
        ai_summary = None
        ai_detailed_analysis = None
        if self.client:
            try:
                ai_analysis = self._get_ai_analysis(
                    parsed_resume,
                    job_description,
                    job_title,
                    company,
                    overall_score,
                    matched_skills,
                    missing_skills
                )
                ai_summary = ai_analysis.get('summary')
                ai_detailed_analysis = ai_analysis.get('detailed')
            except Exception as e:
                logger.error(f"AI analysis failed: {e}")
        
        result = {
            'overall_match_score': overall_score,
            'skill_match_score': skill_score,
            'experience_match_score': experience_score,
            'education_match_score': education_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'strengths': strengths,
            'gaps': gaps,
            'recommendations': recommendations,
            'ai_summary': ai_summary,
            'ai_detailed_analysis': ai_detailed_analysis
        }
        
        logger.info(f"✓ Compatibility analysis complete - Overall Score: {overall_score}%")
        return result
    
    def _extract_skills(self, parsed_resume: Dict) -> List[str]:
        """Extract skills from parsed resume"""
        skills = parsed_resume.get('structured_data', {}).get('skills', [])
        return [skill.strip() for skill in skills if skill.strip()]
    
    def _extract_skills_from_description(self, description: str) -> List[str]:
        """Extract skills from job description using keyword matching"""
        common_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Go', 'Rust', 'Swift',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Express',
            'PostgreSQL', 'MongoDB', 'MySQL', 'Redis', 'Cassandra', 'Oracle',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Jenkins', 'GitLab',
            'Git', 'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
            'HTML', 'CSS', 'TypeScript', 'SASS', 'Tailwind', 'Bootstrap',
            'SQL', 'NoSQL', 'Linux', 'Windows', 'MacOS', 'CI/CD', 'DevOps',
            'Machine Learning', 'Deep Learning', 'Data Analysis', 'Data Science',
            'UI/UX', 'Figma', 'Sketch', 'Adobe XD', 'Photoshop', 'Illustrator'
        ]
        
        description_lower = description.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill.lower() in description_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_experience_level(self, description: str) -> str:
        """Extract required experience level from job description"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['senior', 'lead', 'principal', '5+ years', '7+ years', '10+ years']):
            return 'Senior'
        elif any(word in description_lower for word in ['junior', 'entry', 'graduate', '0-2 years', 'recent graduate']):
            return 'Junior'
        else:
            return 'Mid-level'
    
    def _calculate_skill_match(self, candidate_skills: List[str], job_skills: List[str]) -> int:
        """Calculate skill match score (0-100)"""
        if not job_skills:
            return 70  # Neutral if no skills specified
        
        candidate_lower = [s.lower() for s in candidate_skills]
        job_lower = [s.lower() for s in job_skills]
        
        # Count matches with fuzzy matching
        matches = 0
        for job_skill in job_lower:
            for cand_skill in candidate_lower:
                if job_skill in cand_skill or cand_skill in job_skill:
                    matches += 1
                    break
        
        score = int((matches / len(job_skills)) * 100)
        
        # Bonus if candidate has many relevant skills
        if len(candidate_skills) > len(job_skills):
            bonus = min(10, (len(candidate_skills) - len(job_skills)) // 2)
            score = min(100, score + bonus)
        
        return score
    
    def _calculate_experience_match(
        self,
        candidate_experience: List[Dict],
        job_description: str,
        job_experience_level: str
    ) -> int:
        """Calculate experience match score (0-100)"""
        if not candidate_experience:
            return 30
        
        # Check if experience is relevant
        description_lower = job_description.lower()
        relevant_experience = 0
        
        for exp in candidate_experience:
            exp_text = str(exp.get('text', '')).lower()
            exp_title = str(exp.get('title', '')).lower()
            
            # Check if experience contains relevant keywords from job description
            relevant_keywords = 0
            words = description_lower.split()
            tech_words = [w for w in words if len(w) > 4][:20]  # Get key technical words
            
            for word in tech_words:
                if word in exp_text or word in exp_title:
                    relevant_keywords += 1
            
            if relevant_keywords > 3:
                relevant_experience += 1
        
        # Base score from relevant experience
        if relevant_experience == 0:
            base_score = 40
        elif relevant_experience == 1:
            base_score = 70
        else:
            base_score = 90
        
        # Adjust based on number of experiences
        num_experiences = len(candidate_experience)
        if job_experience_level == 'Senior' and num_experiences < 2:
            base_score -= 20
        elif job_experience_level == 'Junior' and num_experiences > 3:
            base_score = min(100, base_score + 10)  # Bonus for overqualification
        
        return max(0, min(100, base_score))
    
    def _calculate_education_match(
        self,
        candidate_education: List[Dict],
        job_description: str
    ) -> int:
        """Calculate education match score (0-100)"""
        if not candidate_education:
            # Check if education is required
            if any(word in job_description.lower() for word in ['degree required', 'bachelor', 'master', 'phd']):
                return 40  # Missing required education
            else:
                return 70  # Education not emphasized
        
        # Education present, give good score
        base_score = 80
        
        # Bonus for advanced degrees
        for edu in candidate_education:
            edu_text = str(edu).lower()
            if any(word in edu_text for word in ['master', 'phd', 'doctorate']):
                base_score = min(100, base_score + 10)
                break
        
        return base_score
    
    def _identify_strengths(
        self,
        parsed_resume: Dict,
        job_description: str,
        matched_skills: List[str],
        skill_score: int,
        experience_score: int
    ) -> List[str]:
        """Identify candidate strengths for this role"""
        strengths = []
        
        if skill_score >= 80:
            strengths.append(f"Strong skill match with {len(matched_skills)} relevant skills")
        elif skill_score >= 60:
            strengths.append(f"Good skill alignment with {len(matched_skills)} matching skills")
        
        if experience_score >= 80:
            strengths.append("Relevant professional experience for this role")
        
        # Check for standout skills
        high_value_skills = ['AWS', 'Azure', 'GCP', 'Kubernetes', 'Docker', 'React', 'Python', 'Machine Learning']
        standout = [skill for skill in matched_skills if skill in high_value_skills]
        if standout:
            strengths.append(f"Expertise in high-demand skills: {', '.join(standout[:3])}")
        
        if not strengths:
            strengths.append("Foundational skills that can be built upon")
        
        return strengths
    
    def _identify_gaps(
        self,
        missing_skills: List[str],
        skill_score: int,
        experience_score: int,
        education_score: int
    ) -> List[str]:
        """Identify areas for improvement"""
        gaps = []
        
        if skill_score < 50:
            gaps.append(f"Missing {len(missing_skills)} key required skills")
        elif missing_skills:
            gaps.append(f"Could strengthen profile by adding: {', '.join(missing_skills[:3])}")
        
        if experience_score < 60:
            gaps.append("Limited relevant experience for this role")
        
        if education_score < 60:
            gaps.append("Educational background could be enhanced")
        
        return gaps
    
    def _generate_recommendations(
        self,
        missing_skills: List[str],
        gaps: List[str],
        skill_score: int,
        experience_score: int
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if missing_skills:
            top_missing = missing_skills[:3]
            recommendations.append(
                f"Consider learning these in-demand skills: {', '.join(top_missing)}"
            )
        
        if skill_score < 70:
            recommendations.append(
                "Expand technical skillset through online courses or certifications"
            )
        
        if experience_score < 60:
            recommendations.append(
                "Gain relevant experience through projects, freelance work, or internships"
            )
        
        if not recommendations:
            recommendations.append(
                "Strong profile! Consider highlighting specific achievements and quantifiable results"
            )
        
        return recommendations
    
    def _get_ai_analysis(
        self,
        parsed_resume: Dict,
        job_description: str,
        job_title: Optional[str],
        company: Optional[str],
        overall_score: int,
        matched_skills: List[str],
        missing_skills: List[str]
    ) -> Dict[str, str]:
        """Get AI-powered analysis from Groq"""
        # Prepare resume summary
        skills = parsed_resume.get('structured_data', {}).get('skills', [])
        experience = parsed_resume.get('structured_data', {}).get('experience', [])
        education = parsed_resume.get('structured_data', {}).get('education', [])
        
        resume_summary = f"""
Skills: {', '.join(skills[:10]) if skills else 'Not specified'}
Experience: {len(experience)} positions
Education: {len(education)} entries
"""
        
        # Create prompt
        prompt = f"""You are a professional career advisor analyzing a candidate's fit for a job position.

Job Title: {job_title or 'Untitled Position'}
Company: {company or 'Not specified'}

Job Description:
{job_description[:1500]}

Candidate Profile:
{resume_summary}

Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}
Missing Skills: {', '.join(missing_skills[:5]) if missing_skills else 'None'}

Overall Compatibility Score: {overall_score}/100

Please provide:
1. A brief 2-3 sentence summary of the candidate's fit for this role
2. A detailed analysis covering:
   - Key strengths for this position
   - Areas of concern or gaps
   - Specific recommendations to improve their candidacy
   - Overall hiring recommendation

Keep the response professional, constructive, and actionable."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career advisor and HR professional specializing in job-candidate matching."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            full_analysis = response.choices[0].message.content
            
            # Split into summary and detailed
            lines = full_analysis.split('\n\n')
            summary = lines[0] if lines else full_analysis[:200]
            detailed = full_analysis
            
            return {
                'summary': summary,
                'detailed': detailed
            }
            
        except Exception as e:
            logger.error(f"Failed to get AI analysis: {e}")
            return {
                'summary': None,
                'detailed': None
            }


# Test function
if __name__ == '__main__':
    print("Job Compatibility Analyzer - Ready to use!")
    print("\nUsage:")
    print("  from utils.job_compatibility_analyzer import JobCompatibilityAnalyzer")
    print("  analyzer = JobCompatibilityAnalyzer()")
    print("  result = analyzer.analyze(parsed_resume, job_description)")
