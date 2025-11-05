"""
Resume Analyzer Module for UtopiaHire
AI-powered analysis of resumes for ATS compatibility, formatting, and content quality

WHY THIS MODULE:
- Scores resumes on multiple criteria (ATS, formatting, keywords, content)
- Identifies strengths and weaknesses
- Provides actionable improvement suggestions
- Optimized for MENA and Sub-Saharan Africa job markets
"""

import os
import re
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

# NLP libraries
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))


class ResumeAnalyzer:
    """
    Analyze resumes for ATS compatibility and quality
    """
    
    # Common action verbs for strong bullet points
    ACTION_VERBS = {
        'leadership': ['led', 'managed', 'directed', 'coordinated', 'supervised', 'oversaw', 'mentored', 'guided'],
        'achievement': ['achieved', 'accomplished', 'delivered', 'exceeded', 'surpassed', 'improved', 'enhanced', 'optimized'],
        'technical': ['developed', 'designed', 'implemented', 'built', 'created', 'engineered', 'programmed', 'coded'],
        'collaboration': ['collaborated', 'partnered', 'worked', 'contributed', 'cooperated', 'assisted', 'supported'],
        'analysis': ['analyzed', 'evaluated', 'assessed', 'researched', 'investigated', 'examined', 'studied'],
        'communication': ['presented', 'communicated', 'documented', 'reported', 'wrote', 'published', 'spoke']
    }
    
    # Keywords commonly found in MENA/Sub-Saharan Africa job postings
    REGIONAL_KEYWORDS = [
        # Technical
        'python', 'java', 'javascript', 'sql', 'react', 'node.js', 'django', 'flask',
        'data analysis', 'machine learning', 'ai', 'cloud', 'aws', 'azure',
        # Business
        'project management', 'agile', 'scrum', 'team leadership', 'problem solving',
        'communication', 'collaboration', 'strategic planning',
        # Regional specific
        'bilingual', 'french', 'arabic', 'english', 'multicultural', 'remote work',
        'startup', 'fintech', 'e-commerce', 'mobile development'
    ]
    
    # Essential resume sections
    REQUIRED_SECTIONS = ['education', 'experience', 'skills']
    RECOMMENDED_SECTIONS = ['summary', 'contact', 'projects', 'certifications']
    
    def __init__(self, use_ai_models: bool = False):
        """
        Initialize analyzer
        
        Args:
            use_ai_models: If True, use transformer models for advanced analysis
                          If False, use rule-based analysis (faster, no downloads)
        """
        # Note: All AI analysis is now handled via Groq API in the API layer
        # This analyzer focuses on rule-based metrics and pattern matching
        self.use_ai_models = False
        self.models_loaded = False
        logger.info("Resume analyzer initialized (AI features via Groq API)")
    
    def analyze(self, parsed_resume: Dict) -> Dict:
        """
        Main analysis function
        
        Args:
            parsed_resume: Output from ResumeParser.parse_file()
            
        Returns:
            Comprehensive analysis with scores, suggestions, strengths, weaknesses
        """
        logger.info("Starting resume analysis...")
        
        # Extract data
        raw_text = parsed_resume.get('raw_text', '')
        sections = parsed_resume.get('sections', {})
        structured_data = parsed_resume.get('structured_data', {})
        metadata = parsed_resume.get('metadata', {})
        
        # Calculate scores
        ats_score = self._calculate_ats_score(raw_text, sections, structured_data)
        formatting_score = self._calculate_formatting_score(raw_text, sections)
        keyword_score = self._calculate_keyword_score(raw_text, structured_data)
        content_score = self._calculate_content_score(sections, structured_data)
        
        # Calculate section-specific scores (NEW STRICT SCORES)
        skill_match_score = self._calculate_skills_score(structured_data)
        experience_score = self._calculate_experience_score(structured_data, sections)
        education_score = self._calculate_education_score(structured_data, sections)
        
        # Overall score (weighted average) - NOW USES NEW STRICT SCORES!
        # Skills: 35%, Experience: 40%, Education: 25%
        overall_score = int(
            skill_match_score * 0.35 +
            experience_score * 0.40 +
            education_score * 0.25
        )
        
        # Identify strengths and weaknesses
        strengths = self._identify_strengths(sections, structured_data, {
            'ats': ats_score,
            'formatting': formatting_score,
            'keywords': keyword_score,
            'content': content_score
        })
        
        weaknesses = self._identify_weaknesses(sections, structured_data, {
            'ats': ats_score,
            'formatting': formatting_score,
            'keywords': keyword_score,
            'content': content_score
        })
        
        # Generate suggestions
        suggestions = self._generate_suggestions(sections, structured_data, {
            'ats': ats_score,
            'formatting': formatting_score,
            'keywords': keyword_score,
            'content': content_score
        })
        
        # Check for missing sections
        missing_sections = self._check_missing_sections(sections)
        
        # Determine grade
        grade = self._get_grade(overall_score)
        
        analysis_result = {
            'scores': {
                'overall_score': overall_score,
                'ats_score': ats_score,
                'formatting_score': formatting_score,
                'keyword_score': keyword_score,
                'content_score': content_score,
                'skill_match_score': skill_match_score,
                'experience_score': experience_score,
                'education_score': education_score
            },
            'grade': grade,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions,
            'missing_sections': missing_sections,
            'analyzed_at': datetime.now().isoformat(),
            'word_count': metadata.get('word_count', 0)
        }
        
        logger.info(f"✓ Analysis complete - Overall Score: {overall_score}/100 ({grade})")
        return analysis_result
    
    def _calculate_ats_score(self, raw_text: str, sections: Dict, structured_data: Dict) -> int:
        """
        Calculate ATS (Applicant Tracking System) compatibility score
        
        WHY: Many companies use ATS to filter resumes automatically
        ATS-friendly resumes have better chances of reaching human recruiters
        """
        score = 100
        
        # Check for common ATS-friendly elements
        
        # 1. Has email address (critical)
        if not structured_data.get('contact_info', {}).get('email'):
            score -= 15
        
        # 2. Has phone number
        if not structured_data.get('contact_info', {}).get('phone'):
            score -= 10
        
        # 3. Has clear section headers
        if len(sections) < 3:
            score -= 20
        
        # 4. Not too short (at least 150 words)
        word_count = len(raw_text.split())
        if word_count < 150:
            score -= 15
        elif word_count > 1000:
            score -= 10  # Too long
        
        # 5. Has education section
        if 'education' not in sections:
            score -= 15
        
        # 6. Has experience/skills section
        if 'experience' not in sections and 'skills' not in sections:
            score -= 15
        
        # 7. Avoid special characters that confuse ATS
        special_chars = len(re.findall(r'[^\w\s\-.,;:()\[\]@/]', raw_text))
        if special_chars > 50:
            score -= 10
        
        return max(0, min(100, score))
    
    def _calculate_formatting_score(self, raw_text: str, sections: Dict) -> int:
        """
        Calculate formatting and readability score
        """
        score = 100
        
        # 1. Consistent structure
        if len(sections) < 4:
            score -= 15
        
        # 2. Appropriate length per section
        for section_name, section_text in sections.items():
            words = len(section_text.split())
            if words < 10 and section_name in ['experience', 'education']:
                score -= 10
        
        # 3. Bullet points usage (good for readability)
        bullet_chars = ['•', '-', '*', '○']
        has_bullets = any(char in raw_text for char in bullet_chars)
        if not has_bullets:
            score -= 15
        
        # 4. Not too dense (check average words per line)
        lines = [line for line in raw_text.split('\n') if line.strip()]
        if lines:
            avg_words_per_line = len(raw_text.split()) / len(lines)
            if avg_words_per_line > 15:
                score -= 10
        
        # 5. Proper capitalization (section headers should be capitalized)
        section_headers_caps = sum(1 for s in sections.keys() if s[0].isupper())
        if section_headers_caps < len(sections) * 0.5:
            score -= 5
        
        return max(0, min(100, score))
    
    def _calculate_keyword_score(self, raw_text: str, structured_data: Dict) -> int:
        """
        Calculate keyword optimization score
        
        WHY: Resumes with relevant keywords rank higher in ATS systems
        """
        score = 0
        text_lower = raw_text.lower()
        
        # Count how many regional keywords are present
        keywords_found = []
        for keyword in self.REGIONAL_KEYWORDS:
            if keyword.lower() in text_lower:
                keywords_found.append(keyword)
        
        # Score based on keyword density
        keyword_percentage = (len(keywords_found) / len(self.REGIONAL_KEYWORDS)) * 100
        score = int(keyword_percentage * 1.5)  # Scale up
        
        # Bonus for action verbs
        all_action_verbs = [verb for category in self.ACTION_VERBS.values() for verb in category]
        action_verbs_found = sum(1 for verb in all_action_verbs if verb in text_lower)
        
        if action_verbs_found >= 10:
            score += 20
        elif action_verbs_found >= 5:
            score += 10
        elif action_verbs_found >= 3:
            score += 5
        
        # Bonus for skills
        skills = structured_data.get('skills', [])
        if len(skills) >= 10:
            score += 15
        elif len(skills) >= 5:
            score += 10
        elif len(skills) >= 3:
            score += 5
        
        return max(0, min(100, score))
    
    def _calculate_content_score(self, sections: Dict, structured_data: Dict) -> int:
        """
        Calculate content quality score
        """
        score = 100
        
        # 1. Experience section quality
        experience = structured_data.get('experience', [])
        if not experience:
            score -= 30
        else:
            # Check for bullet points in experience
            total_bullets = sum(len(exp.get('bullet_points', [])) for exp in experience)
            if total_bullets == 0:
                score -= 15
            elif total_bullets < 3:
                score -= 10
        
        # 2. Education section
        education = structured_data.get('education', [])
        if not education:
            score -= 20
        
        # 3. Skills section
        skills = structured_data.get('skills', [])
        if not skills:
            score -= 20
        elif len(skills) < 5:
            score -= 10
        
        # 4. Professional summary
        summary = structured_data.get('summary', '')
        if not summary:
            score -= 10
        elif len(summary.split()) < 20:
            score -= 5
        
        # 5. Contact information completeness
        contact = structured_data.get('contact_info', {})
        if not contact.get('email'):
            score -= 15
        if not contact.get('phone'):
            score -= 5
        
        return max(0, min(100, score))
    
    def _identify_strengths(self, sections: Dict, structured_data: Dict, scores: Dict) -> List[str]:
        """
        Identify resume strengths
        """
        strengths = []
        
        # Score-based strengths
        if scores['ats'] >= 80:
            strengths.append("✓ Excellent ATS compatibility")
        if scores['formatting'] >= 80:
            strengths.append("✓ Well-formatted and easy to read")
        if scores['keywords'] >= 80:
            strengths.append("✓ Strong keyword optimization")
        if scores['content'] >= 80:
            strengths.append("✓ Comprehensive content coverage")
        
        # Content-based strengths
        contact = structured_data.get('contact_info', {})
        if contact.get('email') and contact.get('phone'):
            strengths.append("✓ Complete contact information")
        
        if contact.get('linkedin') or contact.get('github'):
            strengths.append("✓ Professional online presence included")
        
        skills = structured_data.get('skills', [])
        if len(skills) >= 10:
            strengths.append(f"✓ Extensive skills list ({len(skills)} skills)")
        
        experience = structured_data.get('experience', [])
        total_bullets = sum(len(exp.get('bullet_points', [])) for exp in experience)
        if total_bullets >= 5:
            strengths.append("✓ Detailed achievement descriptions")
        
        education = structured_data.get('education', [])
        if education and any('bachelor' in e.get('degree', '').lower() or 'master' in e.get('degree', '').lower() for e in education):
            strengths.append("✓ Strong educational background")
        
        if 'summary' in sections and len(sections['summary'].split()) >= 30:
            strengths.append("✓ Compelling professional summary")
        
        return strengths if strengths else ["Resume has good foundational elements"]
    
    def _identify_weaknesses(self, sections: Dict, structured_data: Dict, scores: Dict) -> List[str]:
        """
        Identify resume weaknesses
        """
        weaknesses = []
        
        # Score-based weaknesses
        if scores['ats'] < 60:
            weaknesses.append("⚠ Low ATS compatibility - may not pass automated screening")
        if scores['formatting'] < 60:
            weaknesses.append("⚠ Formatting needs improvement for better readability")
        if scores['keywords'] < 60:
            weaknesses.append("⚠ Insufficient relevant keywords")
        if scores['content'] < 60:
            weaknesses.append("⚠ Content lacks depth and detail")
        
        # Content-based weaknesses
        contact = structured_data.get('contact_info', {})
        if not contact.get('email'):
            weaknesses.append("⚠ Missing email address (critical!)")
        if not contact.get('phone'):
            weaknesses.append("⚠ Missing phone number")
        
        skills = structured_data.get('skills', [])
        if len(skills) < 5:
            weaknesses.append("⚠ Limited skills section - add more relevant skills")
        
        experience = structured_data.get('experience', [])
        if not experience:
            weaknesses.append("⚠ No work experience section found")
        else:
            total_bullets = sum(len(exp.get('bullet_points', [])) for exp in experience)
            if total_bullets < 3:
                weaknesses.append("⚠ Experience section lacks detailed achievements")
        
        if 'summary' not in sections or len(sections.get('summary', '').split()) < 20:
            weaknesses.append("⚠ Missing or weak professional summary")
        
        if 'education' not in sections:
            weaknesses.append("⚠ Education section is missing")
        
        return weaknesses if weaknesses else []
    
    def _generate_suggestions(self, sections: Dict, structured_data: Dict, scores: Dict) -> List[Dict]:
        """
        Generate actionable improvement suggestions
        """
        suggestions = []
        
        # Priority: high, medium, low
        
        # Critical suggestions
        contact = structured_data.get('contact_info', {})
        if not contact.get('email'):
            suggestions.append({
                'priority': 'high',
                'category': 'contact',
                'message': 'Add your email address at the top of your resume',
                'impact': 'Critical for ATS and recruiters to contact you'
            })
        
        if not contact.get('phone'):
            suggestions.append({
                'priority': 'high',
                'category': 'contact',
                'message': 'Add your phone number for direct contact',
                'impact': 'Enables immediate recruiter outreach'
            })
        
        # ATS improvements
        if scores['ats'] < 70:
            suggestions.append({
                'priority': 'high',
                'category': 'ats',
                'message': 'Improve ATS compatibility by using standard section headers',
                'impact': 'Increases chances of passing automated screening'
            })
        
        # Keyword optimization
        if scores['keywords'] < 70:
            suggestions.append({
                'priority': 'high',
                'category': 'keywords',
                'message': 'Add more relevant technical and soft skills keywords',
                'impact': 'Better matching with job descriptions'
            })
        
        # Content improvements
        experience = structured_data.get('experience', [])
        if experience:
            total_bullets = sum(len(exp.get('bullet_points', [])) for exp in experience)
            if total_bullets < 5:
                suggestions.append({
                    'priority': 'medium',
                    'category': 'content',
                    'message': 'Add more bullet points to experience section (aim for 3-5 per role)',
                    'impact': 'Better showcase of achievements and responsibilities'
                })
        
        # Action verbs
        text_lower = sections.get('experience', '').lower()
        all_action_verbs = [verb for category in self.ACTION_VERBS.values() for verb in category]
        action_verbs_found = sum(1 for verb in all_action_verbs if verb in text_lower)
        
        if action_verbs_found < 5:
            suggestions.append({
                'priority': 'medium',
                'category': 'content',
                'message': 'Start bullet points with strong action verbs (e.g., "Developed", "Led", "Achieved")',
                'impact': 'Makes accomplishments more impactful'
            })
        
        # Skills section
        skills = structured_data.get('skills', [])
        if len(skills) < 10:
            suggestions.append({
                'priority': 'medium',
                'category': 'skills',
                'message': f'Expand skills section (currently {len(skills)} skills, aim for 10-15)',
                'impact': 'Better keyword matching and skill visibility'
            })
        
        # Professional summary
        if 'summary' not in sections or len(sections.get('summary', '').split()) < 30:
            suggestions.append({
                'priority': 'medium',
                'category': 'summary',
                'message': 'Add or expand professional summary (30-50 words)',
                'impact': 'Provides clear value proposition to recruiters'
            })
        
        # Formatting
        if scores['formatting'] < 70:
            suggestions.append({
                'priority': 'low',
                'category': 'formatting',
                'message': 'Use consistent formatting with clear section headers and bullet points',
                'impact': 'Improves readability and professional appearance'
            })
        
        # LinkedIn/GitHub
        if not contact.get('linkedin') and not contact.get('github'):
            suggestions.append({
                'priority': 'low',
                'category': 'contact',
                'message': 'Add LinkedIn profile or GitHub link to showcase professional presence',
                'impact': 'Allows recruiters to see more about your work'
            })
        
        # Quantifiable achievements
        if 'experience' in sections:
            has_numbers = bool(re.search(r'\d+%|\d+x|\$\d+|\d+ (million|thousand|projects|users|clients)', sections['experience'], re.IGNORECASE))
            if not has_numbers:
                suggestions.append({
                    'priority': 'medium',
                    'category': 'content',
                    'message': 'Add quantifiable achievements (e.g., "Increased efficiency by 40%", "Managed 5-person team")',
                    'impact': 'Makes achievements more concrete and impressive'
                })
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        suggestions.sort(key=lambda x: priority_order[x['priority']])
        
        return suggestions
    
    def _check_missing_sections(self, sections: Dict) -> List[str]:
        """
        Check for missing important sections
        """
        missing = []
        
        section_names_lower = [s.lower() for s in sections.keys()]
        
        for required in self.REQUIRED_SECTIONS:
            if not any(required in s for s in section_names_lower):
                missing.append(required.title())
        
        return missing
    
    def _get_grade(self, score: int) -> str:
        """
        Convert numerical score to letter grade
        """
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Fair)"
        elif score >= 60:
            return "D (Needs Improvement)"
        else:
            return "F (Poor)"
    
    def _calculate_skills_score(self, structured_data: Dict) -> int:
        """
        Calculate skills section quality score (STRICT)
        
        Factors:
        - Number of skills listed
        - Presence of technical skills
        - Skills categorization
        - Relevance to modern job market
        """
        score = 100
        skills = structured_data.get('skills', [])
        
        if not skills:
            return 10  # Very low score for missing skills
        
        num_skills = len(skills)
        
        # 1. Number of skills (optimal: 10-15) - STRICTER
        if num_skills < 3:
            score -= 50  # Very few skills
        elif num_skills < 5:
            score -= 40
        elif num_skills < 8:
            score -= 25
        elif num_skills < 10:
            score -= 15
        elif num_skills > 20:
            score -= 15  # Too many can dilute impact
        
        # 2. Check for technical/hard skills - REQUIRED
        technical_keywords = ['python', 'java', 'sql', 'javascript', 'aws', 'azure', 
                             'react', 'node', 'docker', 'kubernetes', 'git',
                             'data', 'analysis', 'excel', 'tableau', 'power bi',
                             'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin']
        skills_lower = [s.lower() for s in skills]
        technical_count = sum(1 for skill in skills_lower for kw in technical_keywords if kw in skill)
        
        if technical_count == 0:
            score -= 35  # No technical skills at all
        elif technical_count < 3:
            score -= 20  # Very few technical skills
        elif technical_count < 5:
            score -= 10
        
        # 3. Balance of hard and soft skills
        soft_keywords = ['communication', 'leadership', 'team', 'problem', 'management',
                        'collaboration', 'analytical', 'creative', 'organization']
        soft_count = sum(1 for skill in skills_lower for kw in soft_keywords if kw in skill)
        
        if soft_count == 0:
            score -= 15
        
        # 4. Check for empty or very generic skills ONLY
        generic_skills = ['microsoft office', 'internet', 'computer', 'typing', 'email']
        has_real_skills = any(not any(gen in skill.lower() for gen in generic_skills) for skill in skills)
        
        if not has_real_skills:
            score -= 40  # Only generic skills
        
        # 5. Penalty for very short skill names (likely incomplete)
        short_skills = sum(1 for skill in skills if len(skill.strip()) < 3)
        if short_skills > len(skills) / 2:
            score -= 20
        
        return max(0, min(100, score))
    
    def _calculate_experience_score(self, structured_data: Dict, sections: Dict) -> int:
        """
        Calculate experience section quality score (STRICT)
        
        Factors:
        - Presence of experience section
        - Number of positions
        - Use of action verbs
        - Quantifiable achievements
        - Appropriate detail level
        """
        score = 100
        experience = structured_data.get('experience', [])
        experience_section = sections.get('experience', sections.get('work experience', ''))
        
        if not experience and not experience_section:
            return 10  # Very low score for missing experience
        
        exp_text = str(experience_section).lower()
        word_count = len(exp_text.split())
        
        # 1. Check for experience entries - MORE LENIENT
        if not experience:
            # Try to estimate from text
            if word_count < 10:
                score -= 40  # Almost nothing
            elif word_count < 30:
                score -= 25
            elif word_count < 50:
                score -= 15
        else:
            num_positions = len(experience)
            if num_positions < 1:
                score -= 40
            elif num_positions < 2:
                score -= 15
            # Having 1-2 positions is acceptable, don't penalize too much
        
        # 2. Check for action verbs - MORE LENIENT
        all_action_verbs = []
        for category, verbs in self.ACTION_VERBS.items():
            all_action_verbs.extend(verbs)
        
        words = exp_text.split()
        action_verb_count = sum(1 for word in words if word in all_action_verbs)
        
        # Also give credit for job-related keywords
        job_keywords = ['founder', 'co-founder', 'ceo', 'chair', 'co-chair', 'director', 'manager', 
                       'lead', 'engineer', 'developer', 'analyst', 'consultant']
        job_keyword_count = sum(1 for keyword in job_keywords if keyword in exp_text)
        
        total_relevant_words = action_verb_count + job_keyword_count
        
        if total_relevant_words == 0:
            score -= 25  # No relevant words at all
        elif total_relevant_words < 2:
            score -= 15
        elif total_relevant_words < 4:
            score -= 5
        
        # 3. Check for quantifiable achievements (CRITICAL) - numbers, percentages
        numbers = re.findall(r'\d+[%$]?|\$\d+|[\d,]+\+?', exp_text)
        if len(numbers) == 0:
            score -= 35  # No quantification at all
        elif len(numbers) < 2:
            score -= 25
        elif len(numbers) < 4:
            score -= 15
        elif len(numbers) < 6:
            score -= 5
        
        # 4. Check for bullet points - REQUIRED for readability
        has_bullets = any(char in experience_section for char in ['•', '-', '*', '○', '▪'])
        if not has_bullets:
            if word_count > 50:
                score -= 25  # Long text without bullets
            else:
                score -= 15
        
        # 5. Check length (not too short, not too long) - STRICTER
        if word_count < 20:
            score -= 40  # Way too short
        elif word_count < 30:
            score -= 30
        elif word_count < 50:
            score -= 20
        elif word_count < 100:
            score -= 10
        elif word_count > 600:
            score -= 15  # Too long
        
        # 6. Check for placeholder/template text
        template_phrases = ['please use', 'describe your', 'official company name', 
                           'job title', 'city, country', 'concentrate on', 'examples that may']
        has_template = any(phrase in exp_text for phrase in template_phrases)
        if has_template:
            score -= 45  # Major penalty for template text
        
        return max(0, min(100, score))
    
    def _calculate_education_score(self, structured_data: Dict, sections: Dict) -> int:
        """
        Calculate education section quality score (VERY STRICT)
        
        Factors:
        - Presence of education
        - Degree level (must be SPECIFIC)
        - Institution mentioned (must be REAL NAME)
        - Dates included
        - Relevant details (GPA, honors, etc.)
        - Template/placeholder detection (CRITICAL)
        """
        score = 100
        education = structured_data.get('education', [])
        education_section = sections.get('education', sections.get('academic', sections.get('qualifications', '')))
        
        if not education and not education_section:
            return 10  # Very low score for missing education (was 15, now 10)
        
        edu_text = str(education_section).lower()
        original_edu_text = str(education_section)  # Keep original for case-sensitive checks
        word_count = len(edu_text.split())
        
        # CRITICAL: Check for template/placeholder text FIRST (automatic fail basically)
        template_phrases = [
            'university/universities',
            'degree and subject',
            'location; city and country',
            'applicable additional info',
            'city, country',
            'qualifications',
            'forename surname',
            'professional email',
            'landline or mobile'
        ]
        has_template = any(phrase in edu_text for phrase in template_phrases)
        if has_template:
            # Template detected - should get VERY low score
            return 10  # Automatic 10% for template text!
        
        # 1. Check for education entries - MORE LENIENT
        if not education:
            if word_count < 3:
                score -= 40  # Almost nothing
            elif word_count < 8:
                score -= 25
            elif word_count < 15:
                score -= 10
        else:
            # Having at least one education entry is good!
            if len(education) < 1:
                score -= 30
            # Don't penalize for having just 1 education entry
        
        # 2. Check for SPECIFIC degree level keywords (not generic "degree") - MORE LENIENT
        specific_degree_keywords = [
            'bachelor', 'master', 'phd', 'diploma', 'certificate',
            'bsc', 'msc', 'ba', 'ma', 'b.sc', 'm.sc', 'b.a', 'm.a',
            'doctorate', 'associate', 'undergraduate', 'graduate', 'bba', 'mba'
        ]
        has_specific_degree = any(kw in edu_text for kw in specific_degree_keywords)
        
        # Check for generic "degree" only (template indicator)
        has_generic_degree_only = 'degree' in edu_text and not has_specific_degree
        
        # Also check for institution keywords which indicate education is present
        institution_keywords = ['university', 'college', 'school', 'institute', 
                               'academy', 'polytechnic', 'conservatory']
        has_institution = any(kw in edu_text for kw in institution_keywords)
        
        if not has_specific_degree:
            if has_generic_degree_only:
                score -= 35  # Just says "degree" - likely template (reduced from 45)
            elif has_institution:
                score -= 20  # Has institution but no specific degree (reduced from 40)
            else:
                score -= 30  # No degree or institution (reduced from 40)
        
        # 3. Check for REAL institution name (must be specific, not generic)
        # Generic institution keywords (these are RED FLAGS)
        generic_institution = ['university/universities', 'college/colleges', 
                              'school/schools', 'institute/institutes']
        has_generic_institution = any(kw in edu_text for kw in generic_institution)
        
        # Real institution indicators (proper nouns, specific names)
        # Check if there's a capitalized institution name (proper noun)
        has_real_institution = False
        institution_patterns = [
            r'\b[A-Z][a-z]+ University\b',  # e.g., "Harvard University"
            r'\b[A-Z][a-z]+ College\b',     # e.g., "Boston College"
            r'\bUniversity of [A-Z][a-z]+\b',  # e.g., "University of Oxford"
            r'\b[A-Z]{2,}\b.*(?:University|College|Institute)',  # e.g., "MIT", "UCLA"
        ]
        for pattern in institution_patterns:
            if re.search(pattern, original_edu_text):
                has_real_institution = True
                break
        
        if has_generic_institution:
            score -= 35  # Generic "university/universities" - template (reduced from 45)
        elif not has_real_institution:
            # More lenient - if we found institution keywords earlier, it's okay
            if has_institution:
                score -= 10  # Has institution keyword but not proper name (reduced from 40)
            else:
                score -= 25  # No institution at all (reduced from 40)
        
        # 4. Check for dates (graduation year) - MORE LENIENT
        years = re.findall(r'20\d{2}|19\d{2}', edu_text)
        
        # Check if dates are obviously fake/examples
        fake_year_patterns = ['2000-2003', '2001-2004', '2020-2024', 'xxxx']
        has_fake_years = any(pattern in edu_text for pattern in fake_year_patterns)
        
        if has_fake_years:
            score -= 25  # Fake/example years (reduced from 35)
        elif not years:
            score -= 15  # No dates at all (reduced from 25)
        elif len(years) < 2:
            score -= 5  # Only one date is fine (reduced from 15)
        
        # 5. Check for additional details (GPA, honors, relevant coursework) - MORE LENIENT
        detail_keywords = ['gpa', 'honor', 'distinction', 'cum laude', 'thesis', 
                          'coursework', 'major', 'minor', 'concentration', 'dean',
                          'scholarship', 'award', 'summa', 'magna', '3.', '4.0']
        details_count = sum(1 for kw in detail_keywords if kw in edu_text)
        
        if details_count == 0:
            score -= 5  # No additional details (reduced from 15)
        elif details_count >= 2:
            score += 10  # Good details bonus (increased from 5)
        
        # 6. Check appropriate length - MORE LENIENT
        if word_count < 5:
            score -= 25  # Very short (reduced from 35)
        elif word_count < 10:
            score -= 15  # Short (reduced from 25)
        elif word_count < 15:
            score -= 5  # Minimal but okay (reduced from 15)
        
        # 7. Check for vague/placeholder text patterns
        vague_patterns = ['city', 'country', 'location', 'applicable', 'additional info',
                         'subject', 'field', 'major here', 'degree type']
        vague_count = sum(1 for pattern in vague_patterns if pattern in edu_text)
        if vague_count >= 2:
            score -= 35  # Multiple vague terms - likely template
        
        # 8. Check for generic/incomplete entries
        generic_phrases = ['high school', 'secondary school']
        only_generic = all(phrase in edu_text for phrase in generic_phrases) and not has_specific_degree
        if only_generic:
            score -= 30  # Increased from 25
        
        return max(0, min(100, score))


# Test function
if __name__ == '__main__':
    print("Resume Analyzer Module - Ready to use!")
    print("\nUsage:")
    print("  from utils.resume_analyzer import ResumeAnalyzer")
    print("  analyzer = ResumeAnalyzer(use_ai_models=False)")
    print("  analysis = analyzer.analyze(parsed_resume)")
    print("  print(analysis['scores'])")
