"""
Resume Parser Module for UtopiaHire
Extracts text and structured data from PDF/DOCX resumes

WHY THIS MODULE:
- Converts resume files (PDF/DOCX) into analyzable text
- Identifies key sections: Contact Info, Education, Experience, Skills
- Structures unstructured data for AI analysis
"""

import os
import re
import logging
from typing import Dict, List, Optional
from datetime import datetime

# PDF Processing
import PyPDF2
from io import BytesIO
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

# DOCX Processing  
from docx import Document

# NLP for section detection
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

class ResumeParser:
    """
    Parse resumes and extract structured information
    """
    
    # Section keywords for identification (POWERFUL MULTILINGUAL - English + French + Variations)
    # All keywords are lowercase - matching is done on lowercased text
    SECTION_KEYWORDS = {
        'contact': [
            # English
            'contact', 'contact info', 'contact information', 'personal details', 'personal info',
            'email', 'phone', 'address', 'linkedin', 'github', 'portfolio',
            # French
            'coordonnées', 'informations personnelles', 'contact personnel'
        ],
        'summary': [
            # English
            'summary', 'professional summary', 'executive summary', 'career summary',
            'objective', 'career objective', 'professional objective',
            'profile', 'professional profile', 'personal profile',
            'about', 'about me', 'introduction', 'overview',
            # French
            'à propos', 'a propos', 'résumé', 'résumé professionnel', 
            'profil', 'profil professionnel', 'objectif', 'objectif professionnel'
        ],
        'education': [
            # English
            'education', 'educational background', 'academic background', 'academic qualifications',
            'academic', 'academics', 'university', 'college', 'school', 'institute', 'academy',
            'degree', 'degrees', 'bachelor', 'master', 'phd', 'doctorate', 'mba',
            'qualifications', 'training', 'coursework',
            # French
            'éducation', 'formation', 'formations', 'diplôme', 'diplômes',
            'université', 'école', 'ingénieur', 'études', 'parcours académique'
        ],
        'experience': [
            # English
            'experience', 'work experience', 'professional experience', 'employment history',
            'employment', 'work history', 'career history', 'professional background',
            'career', 'positions', 'roles', 'responsibilities',
            'volunteer', 'volunteer experience', 'volunteering', 'community service',
            'internship', 'internships', 'co-op', 'practicum',
            # French
            'expérience', 'expériences', 'expérience professionnelle',
            'parcours', 'parcours professionnel', 'emploi', 'travail',
            'professionnel', 'projet', 'projets', 'bénévolat'
        ],
        'skills': [
            # English
            'skills', 'skill set', 'core skills', 'key skills',
            'technical skills', 'professional skills', 'core competencies',
            'competencies', 'expertise', 'proficiencies', 'abilities',
            'tools', 'technologies', 'programming languages', 'languages',
            # French
            'compétences', 'compétence', 'aptitudes', 'savoir-faire',
            'technologies', 'outils', 'langages'
        ],
        'projects': [
            # English
            'projects', 'key projects', 'major projects', 'notable projects',
            'portfolio', 'work samples', 'selected works', 'achievements',
            'accomplishments', 'publications',
            # French
            'projets', 'projets clés', 'réalisations', 'travaux', 'publications'
        ],
        'certifications': [
            # English
            'certifications', 'certificates', 'certification', 'certificate',
            'licenses', 'license', 'credentials', 'professional development',
            'awards', 'honors', 'recognition',
            # French
            'certificats', 'certifications', 'diplômes professionnels',
            'distinctions', 'récompenses'
        ],
        'languages': [
            # English
            'languages', 'language skills', 'language proficiency',
            'spoken languages', 'foreign languages', 'linguistic skills',
            # French
            'langues', 'langues parlées', 'compétences linguistiques'
        ]
    }
    
    def __init__(self):
        self.text = ""
        self.metadata = {}
        self.sections = {}
        
    def parse_file(self, file_path: str) -> Dict:
        """
        Main entry point - parses a resume file
        
        Args:
            file_path: Path to PDF or DOCX file
            
        Returns:
            Dictionary with parsed data
            
        Example:
            parser = ResumeParser()
            result = parser.parse_file('/path/to/resume.pdf')
        """
        logger.info(f"Parsing resume: {file_path}")
        
        # Validate file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Extract text based on file type
        if file_extension == '.pdf':
            self.text = self._extract_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            self.text = self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Extract metadata
        self.metadata = {
            'filename': os.path.basename(file_path),
            'file_size': os.path.getsize(file_path),
            'file_type': file_extension[1:],  # Remove the dot
            'parsed_at': datetime.now().isoformat(),
            'text_length': len(self.text),
            'word_count': len(self.text.split())
        }
        
        # Parse sections
        self.sections = self._identify_sections()
        
        # Extract structured data
        structured_data = self._extract_structured_data()
        
        logger.info(f"✓ Successfully parsed resume: {self.metadata['word_count']} words")
        
        return {
            'raw_text': self.text,
            'metadata': self.metadata,
            'sections': self.sections,
            'structured_data': structured_data
        }
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF file - ENHANCED with pdfplumber
        
        WHY: PDF is the most common resume format
        Uses pdfplumber (best) with PyPDF2 fallback
        """
        text = ""
        
        
        if HAS_PDFPLUMBER:
            try:
                logger.info("Using pdfplumber for extraction...")
                with pdfplumber.open(file_path) as pdf:
                    num_pages = len(pdf.pages)
                    for page_num, page in enumerate(pdf.pages):
                        try:
                            # Extract text with better layout handling
                            page_text = page.extract_text(layout=True, x_tolerance=2, y_tolerance=3)
                            
                            # If layout mode didn't work, try standard extraction
                            if not page_text or len(page_text.strip()) < 50:
                                page_text = page.extract_text()
                            
                            # Also extract text from tables (common in resumes)
                            tables = page.extract_tables()
                            table_text = ""
                            if tables:
                                for table in tables:
                                    for row in table:
                                        if row:
                                            table_text += " ".join([str(cell) if cell else "" for cell in row]) + "\n"
                            
                            # Combine regular text and table text
                            combined_text = page_text if page_text else ""
                            if table_text:
                                combined_text += "\n" + table_text
                            
                            if combined_text:
                                text += combined_text + "\n"
                                logger.info(f"✓ Page {page_num + 1}: Extracted {len(combined_text)} characters ({len(combined_text.split())} words)")
                            else:
                                logger.warning(f"⚠️ Page {page_num + 1}: No text extracted")
                        except Exception as page_error:
                            logger.warning(f"Could not extract page {page_num + 1}: {page_error}")
                            continue
                
                if text.strip():
                    word_count = len(text.split())
                    logger.info(f"✓ pdfplumber: Extracted {len(text)} characters, {word_count} words from {num_pages} pages")
                    return text.strip()
                else:
                    logger.warning("pdfplumber extracted no text, trying PyPDF2...")
            except Exception as e:
                logger.warning(f"pdfplumber failed: {e}, trying PyPDF2...")
        
        # Fallback to PyPDF2
        try:
            logger.info("Using PyPDF2 for extraction...")
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file, strict=False)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        
                        if page_text:
                            text += page_text + "\n"
                            logger.info(f"✓ Page {page_num + 1}: Extracted {len(page_text)} characters")
                        else:
                            logger.warning(f"⚠️ Page {page_num + 1}: No text extracted")
                    except Exception as page_error:
                        logger.warning(f"Could not extract page {page_num + 1}: {page_error}")
                        continue
            
            if not text.strip():
                logger.warning("No text extracted from PDF, using filename as fallback")
                text = f"Resume document: {os.path.basename(file_path)}"
            else:
                logger.info(f"✓ PyPDF2: Extracted {len(text)} characters, {len(text.split())} words from {num_pages} pages")
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
            logger.warning("PDF parsing failed completely, using fallback text")
            return f"Resume document: {os.path.basename(file_path)}\n\nNote: Unable to extract text from PDF. Please ensure the PDF is not corrupted or password-protected."
    
    def _extract_from_docx(self, file_path: str) -> str:
        """
        Extract text from DOCX file
        
        WHY: DOCX is easier to parse than DOC
        Extracts paragraph by paragraph
        """
        text = ""
        try:
            doc = Document(file_path)
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Also extract from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += cell.text + " "
                text += "\n"
            
            logger.info(f"✓ Extracted {len(doc.paragraphs)} paragraphs from DOCX")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting DOCX: {e}")
            raise
    
    def _identify_sections(self) -> Dict[str, str]:
        """
        Identify different sections in the resume
        
        WHY: Resumes have standard sections (Education, Experience, etc.)
        We need to identify where each section starts/ends
        
        IMPROVED: Handles poorly formatted PDFs with run-together text
        """
        sections = {}
        
        # Aggressive cleanup for poorly formatted PDFs
        text = self.text
        
        # Insert spaces before capital letters that follow lowercase (camelCase fix)
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        
        # Insert line breaks before section keywords (even if run together) - COMPREHENSIVE
        section_patterns = [
            # English patterns - both upper and lowercase
            (r'([a-z\)])(\s*Education)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*EDUCATION)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Experience)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*EXPERIENCE)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*[Ww]ork\s+[Ee]xperience)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*WORK\s+EXPERIENCE)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Skills)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*SKILLS)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Summary)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*SUMMARY)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Objective)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*OBJECTIVE)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Contact)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*CONTACT)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Projects)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*PROJECTS)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Certifications?)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*CERTIFICATIONS?)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Languages?)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*LANGUAGES?)', r'\1\n\n\2'),
            # French patterns
            (r'([a-z\)])(\s*Éducation)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*ÉDUCATION)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Expériences?)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*EXPÉRIENCES?)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Compétences)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*COMPÉTENCES)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Projets?)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*PROJETS?)', r'\1\n\n\2'),
        ]
        
        for pattern, replacement in section_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Split by potential section markers
        lines = text.split('\n')
        current_section = 'header'
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            line_clean = re.sub(r'[^\w\s]', ' ', line_lower)  # Remove punctuation for better matching
            
            # Skip empty lines
            if not line_lower:
                continue
            
            # Check if line contains section keyword (STRICT - avoid false positives)
            detected_section = None
            for section_name, keywords in self.SECTION_KEYWORDS.items():
                for keyword in keywords:
                    # Skip if line is too long (likely not a header)
                    if len(line.split()) > 12:
                        continue
                    
                    keyword_clean = re.sub(r'[^\w\s]', ' ', keyword).strip()
                    line_stripped = line_lower.lstrip('•-*›▪○ \t')
                    
                    # STRICT DETECTION: Only match if it's clearly a header
                    # 1. Line starts with keyword (after bullets) AND is short (≤4 words) or has colon
                    if line_stripped.startswith(keyword):
                        # Must be short OR have a colon (header pattern)
                        if len(line.split()) <= 4 or ':' in line:
                            detected_section = section_name
                            logger.info(f"  → Detected '{section_name}' section (start) from: '{line[:60]}'")
                            break
                    
                    # 2. Keyword followed by colon (e.g., "WORK EXPERIENCE:", "Skills:")
                    if re.search(r'\b' + re.escape(keyword) + r'\s*:', line_lower):
                        detected_section = section_name
                        logger.info(f"  → Detected '{section_name}' section (colon) from: '{line[:60]}'")
                        break
                    
                    # 3. Standalone keyword in uppercase (1-3 words total)
                    if keyword.upper() in line.upper() and len(line.split()) <= 3:
                        detected_section = section_name
                        logger.info(f"  → Detected '{section_name}' section (caps) from: '{line[:60]}'")
                        break
                        
                if detected_section:
                    break
            
            if detected_section:
                # If it's the SAME section type, don't restart - just add a separator
                # This handles cases like "WORK EXPERIENCE" followed by "VOLUNTEER EXPERIENCE"
                if detected_section == current_section and current_content:
                    # Add the header line as content (keep subsection headers)
                    current_content.append(line)
                    logger.info(f"  ↳ Continuing '{current_section}' section (subsection detected)")
                else:
                    # Save previous section (different section type)
                    if current_content:
                        sections[current_section] = '\n'.join(current_content).strip()
                    
                    # Start new section
                    current_section = detected_section
                    current_content = []
            else:
                # Add line to current section
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        # Debug: Log section lengths
        for section_name, section_content in sections.items():
            word_count = len(section_content.split())
            logger.info(f"  📄 Section '{section_name}': {len(section_content)} chars, {word_count} words")
        
        logger.info(f"✓ Identified sections: {', '.join(sections.keys())}")
        return sections
    
    def _extract_structured_data(self) -> Dict:
        """
        Extract specific data points from the resume
        
        Returns:
            Dictionary with structured information
        """
        structured = {
            'contact_info': self._extract_contact_info(),
            'education': self._extract_education(),
            'experience': self._extract_experience(),
            'skills': self._extract_skills(),
            'summary': self._extract_summary()
        }
        
        return structured
    
    def _extract_contact_info(self) -> Dict:
        """
        Extract contact information (email, phone, etc.)
        """
        contact = {}
        # Search in ALL text, not just header/contact sections
        text = self.text  # Use full resume text
        
        # Extract email using regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact['email'] = emails[0]
        
        # Extract phone using regex - improved pattern
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]|\(\d{3}\)\s*\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact['phone'] = phones[0].strip()
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedins = re.findall(linkedin_pattern, text, re.IGNORECASE)
        if linkedins:
            contact['linkedin'] = linkedins[0]
        
        # Extract GitHub
        github_pattern = r'github\.com/[\w-]+'
        githubs = re.findall(github_pattern, text, re.IGNORECASE)
        if githubs:
            contact['github'] = githubs[0]
        
        return contact
    
    def _extract_education(self) -> List[Dict]:
        """
        Extract education entries - IMPROVED for poorly formatted PDFs
        """
        education = []
        education_text = self.sections.get('education', '')
        
        if education_text:
            # Look for institutions, degrees, and years
            institutions = ['university', 'college', 'school', 'institute', 'academy']
            degrees = ['bachelor', 'master', 'phd', 'doctorate', 'diploma', 'certificate', 'b.sc', 'm.sc', 'b.a', 'm.a']
            
            # Find all year patterns (1970-2025)
            years = re.findall(r'\b(19\d{2}|20[0-2]\d)\b', education_text)
            
            # Find institution names
            text_lower = education_text.lower()
            found_institutions = []
            for inst in institutions:
                # Find sentences containing institution keywords
                matches = re.finditer(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+' + inst + r')', education_text, re.IGNORECASE)
                for match in matches:
                    found_institutions.append(match.group(1).strip())
            
            # Find degree mentions
            found_degrees = []
            for degree in degrees:
                if degree in text_lower:
                    # Extract context around degree
                    pattern = r'([^.]*' + re.escape(degree) + r'[^.]*)'
                    matches = re.findall(pattern, education_text, re.IGNORECASE)
                    found_degrees.extend(matches)
            
            # Build education entries
            if found_institutions or years or found_degrees:
                entry = {}
                if found_institutions:
                    entry['institution'] = found_institutions[0]
                if found_degrees:
                    entry['degree'] = found_degrees[0].strip()
                if years:
                    entry['year'] = f"{years[0]} - {years[-1]}" if len(years) > 1 else years[0]
                
                # If we found anything education-related, add a generic entry
                if not entry:
                    entry = {
                        'institution': 'Education listed',
                        'description': education_text[:100]
                    }
                
                education.append(entry)
        
        return education
    
    def _extract_experience(self) -> List[Dict]:
        """
        Extract work experience entries - IMPROVED for poorly formatted PDFs
        """
        experience = []
        exp_text = self.sections.get('experience', '')
        
        if not exp_text:
            # Try alternate section names
            exp_text = self.sections.get('work experience', '') or self.sections.get('employment', '')
        
        if exp_text:
            # Look for job titles and company patterns
            # Pattern: Years with optional months (like "July 2009 - present" or "2000 - 2020")
            # Supports: "2009", "July 2009", "Jul. 2009", "2009-2010", etc.
            year_pattern = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.]*\s+)?(19\d{2}|20[0-2]\d)\s*[-–]\s*(present|ongoing|current|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z.]*\s+)?(19\d{2}|20[0-2]\d|present|ongoing|current)'
            year_matches = list(re.finditer(year_pattern, exp_text, re.IGNORECASE))
            
            # Common job title keywords
            job_keywords = ['founder', 'co-founder', 'ceo', 'cto', 'director', 'manager', 'engineer', 
                           'developer', 'chair', 'co-chair', 'lead', 'senior', 'junior', 'analyst']
            
            # If we found years, split by year patterns
            if year_matches:
                for match in year_matches:
                    # Get text around this year range
                    start_pos = max(0, match.start() - 100)
                    end_pos = min(len(exp_text), match.end() + 200)
                    context = exp_text[start_pos:end_pos]
                    
                    # Try to find job title in context
                    title = None
                    for keyword in job_keywords:
                        pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+' + keyword + r')'
                        title_match = re.search(pattern, context, re.IGNORECASE)
                        if title_match:
                            title = title_match.group(1).strip()
                            break
                    
                    if not title:
                        # Extract capitalized words before the year as potential title
                        before_year = exp_text[:match.start()].split()[-5:]
                        title = ' '.join(before_year) if before_year else 'Position'
                    
                    experience.append({
                        'title': title,
                        'years': match.group(0),
                        'text': context.strip()
                    })
            
            # If no year patterns found, create a single entry with all experience text
            if not experience and exp_text.strip():
                experience.append({
                    'title': 'Professional Experience',
                    'text': exp_text.strip(),
                    'bullet_points': []
                })
        
        return experience
    
    def _extract_skills(self) -> List[str]:
        """
        Extract skills list
        """
        skills = []
        skills_text = self.sections.get('skills', '')
        
        if skills_text:
            # Common separators in skills sections
            separators = [',', '•', '|', ';', '\n']
            
            # Replace all separators with comma
            for sep in separators:
                skills_text = skills_text.replace(sep, ',')
            
            # Split and clean
            skills = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
            
            # Remove common prefix words but keep the skill
            # e.g., "Languages: Python" -> "Python"
            cleaned_skills = []
            stop_words = ['skills', 'technical', 'and', 'the', 'or', 'languages', 'frameworks', 'tools', 'technologies']
            
            for skill in skills:
                # Remove prefix words
                words = skill.split(':')
                if len(words) > 1:
                    # Take everything after the colon
                    skill = words[-1].strip()
                
                # Check if it's not just a stop word
                if skill.lower() not in stop_words and len(skill) > 2:
                    cleaned_skills.append(skill)
            
            skills = cleaned_skills
        
        return skills
    
    def _extract_summary(self) -> str:
        """
        Extract professional summary/objective
        """
        return self.sections.get('summary', '').strip()


# Test function
if __name__ == '__main__':
    print("Resume Parser Module - Ready to use!")
    print("\nUsage:")
    print("  from utils.resume_parser import ResumeParser")
    print("  parser = ResumeParser()")
    print("  result = parser.parse_file('/path/to/resume.pdf')")
    print("  print(result['structured_data'])")
