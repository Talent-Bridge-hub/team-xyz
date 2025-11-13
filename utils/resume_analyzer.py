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

# Groq AI Integration
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

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
            use_ai_models: If True, use Groq API for intelligent analysis
                          If False, use rule-based analysis only
        """
        self.use_ai_models = use_ai_models and HAS_GROQ
        self.groq_client = None
        
        if self.use_ai_models:
            try:
                api_key = os.getenv('GROQ_API_KEY')
                if not api_key:
                    logger.warning("⚠️ GROQ_API_KEY not found - using rule-based analysis only")
                    self.use_ai_models = False
                else:
                    self.groq_client = Groq(api_key=api_key)
                    logger.info("✓ Resume analyzer initialized with Groq AI")
            except Exception as e:
                logger.error(f"Failed to initialize Groq: {e}")
                self.use_ai_models = False
        
        if not self.use_ai_models:
            logger.info("Resume analyzer initialized (rule-based analysis)")
    
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
        
        # LOG EXTRACTED DATA FOR DEBUGGING
        logger.info(f"📄 Resume Text Length: {len(raw_text)} characters, {len(raw_text.split())} words")
        logger.info(f"📑 Sections Found: {list(sections.keys())}")
        logger.info(f"📋 Structured Data Keys: {list(structured_data.keys())}")
        if structured_data.get('skills'):
            logger.info(f"🔧 Skills Extracted: {len(structured_data.get('skills', []))} skills")
        if structured_data.get('experience'):
            logger.info(f"💼 Experience Entries: {len(structured_data.get('experience', []))}")
        if structured_data.get('education'):
            logger.info(f"🎓 Education Entries: {len(structured_data.get('education', []))}")
        
        # Calculate scores
        ats_score = self._calculate_ats_score(raw_text, sections, structured_data)
        formatting_score = self._calculate_formatting_score(raw_text, sections)
        keyword_score = self._calculate_keyword_score(raw_text, structured_data)
        content_score = self._calculate_content_score(sections, structured_data)
        
        # Calculate section-specific scores (NEW STRICT SCORES)
        skill_match_score = self._calculate_skills_score(structured_data)
        experience_score = self._calculate_experience_score(structured_data, sections)
        education_score = self._calculate_education_score(structured_data, sections)
        
        # LOG INDIVIDUAL SCORES FOR DEBUGGING
        logger.info(f"📊 Score Breakdown:")
        logger.info(f"  ATS Score: {ats_score}/100")
        logger.info(f"  Content Score: {content_score}/100")
        logger.info(f"  Skill Match Score: {skill_match_score}/100")
        logger.info(f"  Experience Score: {experience_score}/100")
        logger.info(f"  Education Score: {education_score}/100")
        logger.info(f"  Formatting Score: {formatting_score}/100")
        logger.info(f"  Keyword Score: {keyword_score}/100")
        
        # Overall score (weighted average) - BALANCED APPROACH
        # Use both old and new scoring methods for fairness
        # ATS: 25%, Content: 30%, Skills: 20%, Experience: 15%, Education: 10%
        overall_score = int(
            ats_score * 0.25 +
            content_score * 0.30 +
            skill_match_score * 0.20 +
            experience_score * 0.15 +
            education_score * 0.10
        )
        
        logger.info(f"🎯 Overall Score Calculation: {ats_score}*0.25 + {content_score}*0.30 + {skill_match_score}*0.20 + {experience_score}*0.15 + {education_score}*0.10 = {overall_score}")
        
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
        
        # AI-POWERED ENHANCEMENTS (if enabled)
        ai_suggestions = []
        ai_ats_insights = {}
        ai_keyword_gaps = {}
        ai_writing_quality = {}
        ai_benchmark = {}
        
        if self.use_ai_models and self.groq_client:
            logger.info("🤖 Generating comprehensive AI-powered insights...")
            
            # Get AI suggestions
            ai_suggestions = self._get_ai_suggestions(parsed_resume, {
                'overall_score': overall_score,
                'ats_score': ats_score,
                'content_score': content_score,
                'skills_score': skill_match_score
            })
            
            # Get ATS insights
            ai_ats_insights = self._get_ai_ats_insights(parsed_resume)
            
            # Get keyword gap analysis
            ai_keyword_gaps = self._get_ai_keyword_gap_analysis(parsed_resume, target_role="general")
            
            # Get writing quality assessment
            ai_writing_quality = self._get_ai_writing_quality_score(parsed_resume)
            
            # Get competitive benchmark
            ai_benchmark = self._get_ai_competitive_benchmark(parsed_resume, {
                'overall_score': overall_score
            })
        
        # Merge AI suggestions with rule-based suggestions
        all_suggestions = suggestions + ai_suggestions if ai_suggestions else suggestions
        
        # Build comprehensive AI insights object
        comprehensive_ai_insights = {}
        if self.use_ai_models:
            comprehensive_ai_insights = {
                'ats_analysis': ai_ats_insights.get('ai_ats_analysis', None),
                'missing_keywords': ai_keyword_gaps.get('missing_keywords', []),
                'writing_quality': ai_writing_quality,
                'competitive_benchmark': ai_benchmark
            }
        
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
            'suggestions': all_suggestions,
            'missing_sections': missing_sections,
            'analyzed_at': datetime.now().isoformat(),
            'word_count': metadata.get('word_count', 0),
            'ai_powered': self.use_ai_models,
            'ai_insights': comprehensive_ai_insights if comprehensive_ai_insights else None
        }
        
        logger.info(f"✓ Analysis complete - Overall Score: {overall_score}/100 ({grade})")
        if self.use_ai_models:
            logger.info(f"🤖 AI insights included: {len(ai_suggestions)} suggestions + advanced analysis")
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
            return 30  # Low score but not terrible - they might list skills elsewhere
        
        num_skills = len(skills)
        
        # 1. Number of skills (optimal: 8-15) - BALANCED
        if num_skills < 3:
            score -= 40  # Very few skills
        elif num_skills < 5:
            score -= 30
        elif num_skills < 7:
            score -= 20
        elif num_skills < 8:
            score -= 10
        elif num_skills > 20:
            score -= 10  # Too many can dilute impact
        
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
        
        logger.info(f"🔍 Experience Debug: Found {len(experience)} entries, section length: {len(experience_section)} chars")
        
        if not experience and not experience_section:
            logger.info(f"⚠️ No experience section found")
            return 35  # Low but not terrible - some people are entry-level
        
        exp_text = str(experience_section).lower()
        word_count = len(exp_text.split())
        logger.info(f"📝 Experience text: {word_count} words")
        
        # 1. Check for experience entries - BALANCED
        if not experience:
            # Try to estimate from text
            if word_count < 10:
                score -= 30  # Almost nothing
            elif word_count < 30:
                score -= 20
            elif word_count < 50:
                score -= 10
        else:
            num_positions = len(experience)
            if num_positions < 1:
                score -= 40
            elif num_positions < 2:
                score -= 15
            # Having 1-2 positions is acceptable, don't penalize too much
        
        # 2. Check for action verbs - BALANCED
        all_action_verbs = []
        for category, verbs in self.ACTION_VERBS.items():
            all_action_verbs.extend(verbs)
        
        words = exp_text.split()
        action_verb_count = sum(1 for word in words if word in all_action_verbs)
        
        # Also give credit for job-related keywords
        job_keywords = ['founder', 'co-founder', 'ceo', 'chair', 'co-chair', 'director', 'manager', 
                       'lead', 'engineer', 'developer', 'analyst', 'consultant', 'associate', 'representative']
        job_keyword_count = sum(1 for keyword in job_keywords if keyword in exp_text)
        
        total_relevant_words = action_verb_count + job_keyword_count
        
        if total_relevant_words == 0:
            score -= 30  # No relevant words at all
        elif total_relevant_words < 3:
            score -= 20
        elif total_relevant_words < 6:
            score -= 10
        elif total_relevant_words >= 10:
            score += 5  # Bonus for many action verbs
        
        # 3. Check for quantifiable achievements - numbers, percentages (BALANCED)
        numbers = re.findall(r'\d+[%$]?|\$\d+|[\d,]+\+?', exp_text)
        if len(numbers) == 0:
            score -= 20  # No quantification
        elif len(numbers) < 3:
            score -= 10
        elif len(numbers) >= 5:
            score += 10  # Bonus for strong quantification
        
        # 4. Check for bullet points - ENCOURAGED for readability
        has_bullets = any(char in experience_section for char in ['•', '-', '*', '○', '▪'])
        if not has_bullets:
            if word_count > 80:
                score -= 15  # Long text without bullets
            elif word_count > 50:
                score -= 10
        else:
            score += 5  # Bonus for using bullets
        
        # 5. Check length (not too short, not too long) - BALANCED
        length_penalty = 0
        if word_count < 30:
            length_penalty = 25  # Too short
        elif word_count < 50:
            length_penalty = 15
        elif word_count < 80:
            length_penalty = 5
        elif word_count > 500:
            length_penalty = 10  # Too long
        
        if length_penalty > 0:
            logger.info(f"⚠️ Length penalty: -{length_penalty} (word_count: {word_count})")
            score -= length_penalty
        elif word_count >= 100 and word_count <= 400:
            score += 5  # Bonus for good length
        
        # 6. Check for placeholder/template text - only if multiple indicators
        template_phrases = ['please use', 'describe your', 'official company name', 
                           'concentrate on', 'examples that may']
        template_count = sum(1 for phrase in template_phrases if phrase in exp_text)
        if template_count >= 2:
            logger.info(f"⚠️ Template text detected: -{40}")
            score -= 40  # Multiple template indicators
        
        final_score = max(55, min(85, score))  # Cap between 55-85 for realistic scoring
        logger.info(f"🎯 Experience final score: {final_score}/100 (penalties applied: action_verbs, numbers, bullets, length)")
        return final_score
    
    def _calculate_education_score(self, structured_data: Dict, sections: Dict) -> int:
        """
        Calculate education section quality score (BALANCED)
        
        Factors:
        - Presence of education
        - Degree level
        - Institution mentioned
        - Dates included
        - Relevant details (GPA, honors, etc.)
        """
        score = 100
        education = structured_data.get('education', [])
        education_section = sections.get('education', sections.get('academic', sections.get('qualifications', '')))
        
        if not education and not education_section:
            return 40  # Low but reasonable - education isn't always required
        
        edu_text = str(education_section).lower()
        original_edu_text = str(education_section)  # Keep original for case-sensitive checks
        word_count = len(edu_text.split())
        
        # Check for template text - only if multiple indicators
        template_phrases = [
            'university/universities',
            'degree and subject',
            'forename surname',
            'professional email address'
        ]
        template_count = sum(1 for phrase in template_phrases if phrase in edu_text)
        
        if template_count >= 2:
            score -= 50  # Multiple templates detected
        
        # 1. Check for education entries
        if not education:
            if word_count < 5:
                score -= 30
            elif word_count < 10:
                score -= 15
        
        # 2. Check for degree level keywords
        specific_degree_keywords = [
            'bachelor', 'master', 'phd', 'diploma', 'certificate',
            'bsc', 'msc', 'ba', 'ma', 'b.sc', 'm.sc', 'b.a', 'm.a',
            'doctorate', 'associate', 'undergraduate', 'graduate', 'bba', 'mba'
        ]
        has_specific_degree = any(kw in edu_text for kw in specific_degree_keywords)
        
        # Check for institution keywords
        institution_keywords = ['university', 'college', 'school', 'institute', 
                               'academy', 'polytechnic']
        has_institution = any(kw in edu_text for kw in institution_keywords)
        
        if not has_specific_degree:
            if has_institution:
                score -= 15  # Has institution but no specific degree
            else:
                score -= 25  # No degree or institution
        
        # 3. Check for years/dates
        years = re.findall(r'20\d{2}|19\d{2}', edu_text)
        if not years:
            score -= 10  # No dates
        elif len(years) >= 2:
            score += 5  # Bonus for date range
        
        # 4. Check for additional details (GPA, honors, etc.)
        detail_keywords = ['gpa', 'honor', 'distinction', 'cum laude', 'thesis', 
                          'coursework', 'major', 'minor', 'dean',
                          'scholarship', 'award', '3.', '4.0']
        details_count = sum(1 for kw in detail_keywords if kw in edu_text)
        
        if details_count >= 2:
            score += 10  # Good details bonus
        
        # 5. Check length
        if word_count < 8:
            score -= 20
        elif word_count < 12:
            score -= 10
        elif word_count >= 20 and word_count <= 80:
            score += 5  # Good length
        
        return max(60, min(85, score))  # Cap between 60-85 for realistic scoring
    
    def _get_ai_suggestions(self, parsed_resume: Dict, scores: Dict) -> List[str]:
        """
        Use Groq AI to generate intelligent, personalized improvement suggestions
        """
        if not self.groq_client:
            return []
        
        try:
            # Extract resume summary for AI
            raw_text = parsed_resume.get('raw_text', '')
            sections = parsed_resume.get('sections', {})
            structured_data = parsed_resume.get('structured_data', {})
            
            # Create a concise summary for AI
            summary = {
                'scores': {
                    'overall': scores.get('overall_score', 0),
                    'ats': scores.get('ats_score', 0),
                    'content': scores.get('content_score', 0),
                    'skills': scores.get('skills_score', 0)
                },
                'experience_count': len(structured_data.get('experience', [])),
                'education_count': len(structured_data.get('education', [])),
                'skills_count': len(structured_data.get('skills', [])),
                'total_words': len(raw_text.split())
            }
            
            prompt = f"""You are an expert resume consultant. Analyze this resume and provide 5 specific, actionable improvement suggestions.

Resume Summary:
- Overall Score: {summary['scores']['overall']}/100
- ATS Score: {summary['scores']['ats']}/100
- Content Score: {summary['scores']['content']}/100
- Skills Score: {summary['scores']['skills']}/100
- Experience Entries: {summary['experience_count']}
- Skills Listed: {summary['skills_count']}
- Total Words: {summary['total_words']}

Provide 5 specific, actionable suggestions to improve this resume. Focus on:
1. ATS optimization (if score < 80)
2. Content improvements (quantification, action verbs)
3. Missing sections or skills
4. Formatting and structure
5. Industry-specific recommendations

Return ONLY a JSON array of 5 suggestion strings, nothing else. Format:
["suggestion 1", "suggestion 2", "suggestion 3", "suggestion 4", "suggestion 5"]"""

            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content.strip()
            
            # Try to extract JSON array
            import json
            try:
                suggestions = json.loads(ai_response)
                if isinstance(suggestions, list):
                    logger.info(f"✓ Generated {len(suggestions)} AI-powered suggestions")
                    return suggestions[:5]  # Limit to 5
            except:
                # Fallback: split by lines if JSON parsing fails
                suggestions = [line.strip('- "\'') for line in ai_response.split('\n') if line.strip()]
                return suggestions[:5]
                
        except Exception as e:
            logger.error(f"Groq AI suggestions failed: {e}")
            return []
        
        return []
    
    def _get_ai_ats_insights(self, parsed_resume: Dict) -> Dict[str, any]:
        """
        Use Groq AI to provide intelligent ATS compatibility insights
        """
        if not self.groq_client:
            return {}
        
        try:
            raw_text = parsed_resume.get('raw_text', '')[:2000]  # First 2000 chars
            
            prompt = f"""Analyze this resume for ATS (Applicant Tracking System) compatibility.

Resume excerpt:
{raw_text}

Provide a brief analysis (3-4 sentences) covering:
1. Format compatibility (PDF, sections, headers)
2. Keyword optimization
3. Readability for ATS scanners
4. One specific improvement recommendation

Return ONLY the analysis text, nothing else."""

            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=200
            )
            
            analysis = response.choices[0].message.content.strip()
            logger.info("✓ Generated AI ATS insights")
            
            return {
                'ai_ats_analysis': analysis,
                'source': 'groq_ai'
            }
            
        except Exception as e:
            logger.error(f"Groq ATS insights failed: {e}")
            return {}
    
    def _get_ai_keyword_gap_analysis(self, parsed_resume: Dict, target_role: str = "general") -> Dict[str, any]:
        """
        Use Groq AI to identify missing keywords for target job role
        """
        if not self.groq_client:
            return {}
        
        try:
            skills = parsed_resume.get('structured_data', {}).get('skills', [])
            experience_text = ""
            for exp in parsed_resume.get('structured_data', {}).get('experience', [])[:3]:
                experience_text += exp.get('text', '') + "\n"
            
            prompt = f"""Analyze this resume for keyword gaps.

Current Skills: {', '.join(skills[:15])}
Recent Experience: {experience_text[:500]}
Target Role: {target_role}

Identify 5 high-impact keywords/skills that are MISSING but should be added for this role.
Consider:
1. Industry-standard tools and technologies
2. Soft skills relevant to the role
3. Certifications or qualifications
4. Technical competencies
5. Role-specific terminology

Return ONLY a JSON array of 5 keywords, nothing else. Format:
["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]"""

            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            
            keywords_response = response.choices[0].message.content.strip()
            
            # Parse JSON array
            import json
            try:
                missing_keywords = json.loads(keywords_response)
                if isinstance(missing_keywords, list):
                    logger.info(f"✓ Identified {len(missing_keywords)} missing keywords")
                    return {
                        'missing_keywords': missing_keywords[:5],
                        'target_role': target_role
                    }
            except:
                pass
                
        except Exception as e:
            logger.error(f"Groq keyword gap analysis failed: {e}")
        
        return {}
    
    def _get_ai_writing_quality_score(self, parsed_resume: Dict) -> Dict[str, any]:
        """
        Use Groq AI to assess writing quality, tone, and professionalism
        """
        if not self.groq_client:
            return {}
        
        try:
            # Get sample text from experience
            experience_samples = []
            for exp in parsed_resume.get('structured_data', {}).get('experience', [])[:2]:
                bullets = exp.get('bullet_points', [])[:3]
                experience_samples.extend(bullets)
            
            sample_text = '\n'.join(experience_samples[:5])
            
            if not sample_text:
                return {}
            
            prompt = f"""Analyze the writing quality of these resume bullet points:

{sample_text}

Rate (0-100) and explain briefly:
1. Clarity: Is the writing clear and easy to understand?
2. Professionalism: Is the tone appropriate for a resume?
3. Impact: Do the statements convey meaningful achievements?
4. Grammar: Are there any grammatical issues?

Return as JSON:
{{"clarity_score": 0-100, "professionalism_score": 0-100, "impact_score": 0-100, "grammar_score": 0-100, "brief_feedback": "2-3 sentences"}}"""

            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=300
            )
            
            quality_response = response.choices[0].message.content.strip()
            
            # Parse JSON
            import json
            try:
                quality_data = json.loads(quality_response)
                logger.info("✓ Generated AI writing quality analysis")
                return quality_data
            except:
                # Fallback: return text response
                return {'brief_feedback': quality_response}
                
        except Exception as e:
            logger.error(f"Groq writing quality analysis failed: {e}")
        
        return {}
    
    def _get_ai_competitive_benchmark(self, parsed_resume: Dict, scores: Dict) -> Dict[str, any]:
        """
        Use Groq AI to benchmark resume against industry standards
        """
        if not self.groq_client:
            return {}
        
        try:
            overall_score = scores.get('overall_score', 0)
            experience_count = len(parsed_resume.get('structured_data', {}).get('experience', []))
            skills_count = len(parsed_resume.get('structured_data', {}).get('skills', []))
            
            prompt = f"""Based on this resume profile, provide competitive benchmarking:

Overall Score: {overall_score}/100
Experience Entries: {experience_count}
Skills Listed: {skills_count}

Compare this resume to industry standards and provide:
1. Percentile ranking (e.g., "Top 25% of candidates")
2. One key strength vs. competitors
3. One area where competitors are stronger
4. One quick win to improve competitiveness

Return as JSON:
{{"percentile": "Top X% of candidates", "strength": "...", "weakness_vs_competitors": "...", "quick_win": "..."}}"""

            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=250
            )
            
            benchmark_response = response.choices[0].message.content.strip()
            
            # Parse JSON
            import json
            try:
                benchmark_data = json.loads(benchmark_response)
                logger.info("✓ Generated AI competitive benchmark")
                return benchmark_data
            except:
                return {}
                
        except Exception as e:
            logger.error(f"Groq competitive benchmark failed: {e}")
        
        return {}


# Test function
if __name__ == '__main__':
    print("Resume Analyzer Module - Ready to use!")
    print("\nUsage:")
    print("  from utils.resume_analyzer import ResumeAnalyzer")
    print("  analyzer = ResumeAnalyzer(use_ai_models=False)")
    print("  analysis = analyzer.analyze(parsed_resume)")
    print("  print(analysis['scores'])")
