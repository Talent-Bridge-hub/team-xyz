"""
Cover Letter Generator
Generates personalized cover letters based on CV and job description using AI
"""

import os
import logging
from typing import Dict, Optional, List
from groq import Groq
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoverLetterGenerator:
    """
    Generates professional cover letters tailored to specific job applications
    Uses Groq API (llama-3.3-70b-versatile) for intelligent generation
    """
    
    def __init__(self):
        """Initialize the generator with Groq API"""
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            logger.warning("GROQ_API_KEY not found. Cover letter generation will be unavailable.")
            self.client = None
        else:
            self.client = Groq(api_key=self.groq_api_key)
            logger.info("✓ Cover Letter Generator initialized with Groq API")
    
    def generate(
        self,
        parsed_resume: Dict,
        job_description: str,
        job_title: str,
        company: str,
        tone: str = "professional",
        length: str = "medium",
        highlights: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate a personalized cover letter
        
        Args:
            parsed_resume: Parsed resume data from ResumeParser
            job_description: Job description text
            job_title: Job title/position
            company: Company name
            tone: Writing tone - 'professional', 'enthusiastic', 'formal', 'conversational'
            length: Letter length - 'short' (250 words), 'medium' (350 words), 'long' (500 words)
            highlights: Optional specific achievements/skills to emphasize
        
        Returns:
            Dict containing:
                - cover_letter: Generated cover letter text
                - word_count: Number of words
                - sections: Breakdown of letter sections
                - suggestions: Tips for customization
        """
        if not self.client:
            return {
                'error': 'Groq API not configured. Please set GROQ_API_KEY environment variable.',
                'cover_letter': None
            }
        
        try:
            # Extract candidate information
            candidate_name = parsed_resume.get('name', 'Your Name')
            candidate_email = parsed_resume.get('email', 'your.email@example.com')
            candidate_phone = parsed_resume.get('phone', '')
            candidate_skills = parsed_resume.get('skills', [])
            candidate_experience = parsed_resume.get('experience_years', 0)
            candidate_education = parsed_resume.get('education', [])
            
            # Build the AI prompt
            prompt = self._build_prompt(
                candidate_name=candidate_name,
                candidate_email=candidate_email,
                candidate_phone=candidate_phone,
                candidate_skills=candidate_skills,
                candidate_experience=candidate_experience,
                candidate_education=candidate_education,
                job_title=job_title,
                company=company,
                job_description=job_description,
                tone=tone,
                length=length,
                highlights=highlights
            )
            
            # Call Groq API
            logger.info(f"Generating cover letter for {job_title} at {company}...")
            response = self.client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career advisor and professional cover letter writer. Write compelling, ATS-friendly cover letters that showcase candidates' strengths."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            cover_letter_text = response.choices[0].message.content.strip()
            
            # Parse the response into sections
            sections = self._parse_sections(cover_letter_text)
            
            # Count words
            word_count = len(cover_letter_text.split())
            
            # Generate suggestions
            suggestions = self._generate_suggestions(
                parsed_resume=parsed_resume,
                job_description=job_description,
                tone=tone
            )
            
            logger.info(f"✓ Cover letter generated successfully ({word_count} words)")
            
            return {
                'cover_letter': cover_letter_text,
                'word_count': word_count,
                'sections': sections,
                'suggestions': suggestions,
                'metadata': {
                    'job_title': job_title,
                    'company': company,
                    'tone': tone,
                    'length': length,
                    'generated_at': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating cover letter: {str(e)}")
            return {
                'error': f'Failed to generate cover letter: {str(e)}',
                'cover_letter': None
            }
    
    def _build_prompt(
        self,
        candidate_name: str,
        candidate_email: str,
        candidate_phone: str,
        candidate_skills: List[str],
        candidate_experience: int,
        candidate_education: List[str],
        job_title: str,
        company: str,
        job_description: str,
        tone: str,
        length: str,
        highlights: Optional[List[str]]
    ) -> str:
        """Build the prompt for Groq API"""
        
        # Define word count targets
        word_targets = {
            'short': '250-300',
            'medium': '350-400',
            'long': '450-500'
        }
        target_words = word_targets.get(length, '350-400')
        
        # Define tone descriptions
        tone_descriptions = {
            'professional': 'professional and polished',
            'enthusiastic': 'energetic and passionate',
            'formal': 'formal and traditional',
            'conversational': 'warm and personable'
        }
        tone_style = tone_descriptions.get(tone, 'professional and polished')
        
        # Format education
        education_text = ', '.join(candidate_education[:2]) if candidate_education else 'relevant educational background'
        
        # Format skills
        top_skills = ', '.join(candidate_skills[:8]) if candidate_skills else 'relevant technical skills'
        
        # Format highlights
        highlights_text = ''
        if highlights:
            highlights_text = f"\n\nSpecific achievements to emphasize:\n" + '\n'.join([f"- {h}" for h in highlights])
        
        prompt = f"""Write a compelling, ATS-friendly cover letter for the following job application:

**CANDIDATE INFORMATION:**
- Name: {candidate_name}
- Email: {candidate_email}
- Phone: {candidate_phone if candidate_phone else 'Not provided'}
- Years of Experience: {candidate_experience}
- Education: {education_text}
- Key Skills: {top_skills}
{highlights_text}

**JOB DETAILS:**
- Position: {job_title}
- Company: {company}
- Job Description:
{job_description[:1500]}

**WRITING REQUIREMENTS:**
1. Tone: {tone_style}
2. Length: {target_words} words
3. Structure:
   - Professional header with contact information
   - Opening paragraph: Hook and express interest in the role
   - Body paragraphs (2-3): 
     * Match candidate's skills to job requirements
     * Highlight relevant experience and achievements
     * Show knowledge of the company/role
   - Closing paragraph: Call to action and availability
   - Professional sign-off

4. Content Guidelines:
   - Use specific examples from the candidate's background
   - Match keywords from the job description naturally
   - Show enthusiasm for the role and company
   - Demonstrate value proposition clearly
   - Avoid generic phrases
   - Use action verbs and quantifiable achievements
   - Make it ATS-friendly (avoid tables, special formatting)

5. DO NOT:
   - Use placeholder text like [Your Name] or [Date]
   - Include generic statements that could apply to any job
   - Repeat the entire resume
   - Use clichés like "I'm a hard worker" or "I'm a team player" without context

Write the complete cover letter now, ready to be sent. Include the header, date, recipient address (use "Hiring Manager"), and full letter body."""

        return prompt
    
    def _parse_sections(self, cover_letter: str) -> Dict[str, str]:
        """Parse the cover letter into sections"""
        sections = {
            'header': '',
            'greeting': '',
            'opening': '',
            'body': '',
            'closing': '',
            'signature': ''
        }
        
        lines = cover_letter.split('\n')
        current_section = 'header'
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Detect sections based on content
            if 'dear' in line_lower or 'hiring manager' in line_lower:
                current_section = 'greeting'
            elif current_section == 'greeting' and len(line.strip()) > 20:
                current_section = 'opening'
            elif 'sincerely' in line_lower or 'regards' in line_lower or 'best' in line_lower:
                current_section = 'signature'
            elif current_section in ['opening', 'body'] and len(sections['opening']) > 100:
                current_section = 'body'
            
            sections[current_section] += line + '\n'
        
        return {k: v.strip() for k, v in sections.items() if v.strip()}
    
    def _generate_suggestions(
        self,
        parsed_resume: Dict,
        job_description: str,
        tone: str
    ) -> List[str]:
        """Generate customization suggestions"""
        suggestions = []
        
        # Tone-specific suggestions
        if tone == 'professional':
            suggestions.append("Consider adding specific metrics or KPIs to quantify your achievements")
        elif tone == 'enthusiastic':
            suggestions.append("Emphasize your passion for the company's mission and industry")
        elif tone == 'formal':
            suggestions.append("Ensure all language is formal and traditional business-appropriate")
        
        # Skills matching
        candidate_skills = set([s.lower() for s in parsed_resume.get('skills', [])])
        job_desc_lower = job_description.lower()
        
        missing_keywords = []
        for skill in candidate_skills:
            if skill not in job_desc_lower:
                missing_keywords.append(skill)
        
        if missing_keywords[:3]:
            suggestions.append(f"Consider emphasizing these skills from your resume: {', '.join(missing_keywords[:3])}")
        
        # Experience
        experience_years = parsed_resume.get('experience_years', 0)
        if experience_years < 2:
            suggestions.append("Highlight relevant projects, internships, or academic work to compensate for limited experience")
        elif experience_years > 10:
            suggestions.append("Focus on leadership and strategic impact rather than day-to-day tasks")
        
        # General tips
        suggestions.extend([
            "Proofread carefully for typos and grammatical errors",
            "Research the company and mention specific initiatives or values that resonate with you",
            "Save as PDF with a professional filename: FirstName_LastName_CoverLetter_Company.pdf"
        ])
        
        return suggestions
    
    def generate_multiple_versions(
        self,
        parsed_resume: Dict,
        job_description: str,
        job_title: str,
        company: str
    ) -> Dict[str, Dict]:
        """
        Generate multiple cover letter versions with different tones
        
        Returns:
            Dict with keys: 'professional', 'enthusiastic', 'formal'
        """
        tones = ['professional', 'enthusiastic', 'formal']
        versions = {}
        
        for tone in tones:
            logger.info(f"Generating {tone} version...")
            result = self.generate(
                parsed_resume=parsed_resume,
                job_description=job_description,
                job_title=job_title,
                company=company,
                tone=tone,
                length='medium'
            )
            versions[tone] = result
        
        return versions


# Example usage
if __name__ == "__main__":
    # Test the cover letter generator
    generator = CoverLetterGenerator()
    
    # Sample resume data
    sample_resume = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '+1 (555) 123-4567',
        'skills': ['Python', 'React', 'PostgreSQL', 'AWS', 'Docker', 'REST APIs'],
        'experience_years': 5,
        'education': ['B.S. Computer Science, University XYZ']
    }
    
    # Sample job
    sample_job_desc = """
    We are seeking a Full Stack Developer to join our team. 
    Requirements:
    - 3+ years of experience with Python and JavaScript
    - Experience with React and modern web frameworks
    - Knowledge of databases (PostgreSQL, MongoDB)
    - Cloud deployment experience (AWS preferred)
    - Strong problem-solving skills
    """
    
    result = generator.generate(
        parsed_resume=sample_resume,
        job_description=sample_job_desc,
        job_title='Full Stack Developer',
        company='Tech Innovators Inc',
        tone='professional',
        length='medium'
    )
    
    if result.get('cover_letter'):
        print("\n" + "="*80)
        print("GENERATED COVER LETTER")
        print("="*80)
        print(result['cover_letter'])
        print("\n" + "="*80)
        print(f"Word Count: {result['word_count']}")
        print("\nSuggestions:")
        for suggestion in result['suggestions']:
            print(f"  • {suggestion}")
    else:
        print(f"Error: {result.get('error')}")
