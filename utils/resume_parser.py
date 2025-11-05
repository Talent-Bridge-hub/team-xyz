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
    
    # Section keywords for identification
    SECTION_KEYWORDS = {
        'contact': ['contact', 'email', 'phone', 'address', 'linkedin', 'github'],
        'summary': ['summary', 'objective', 'profile', 'about'],
        'education': ['education', 'academic', 'university', 'college', 'degree', 'bachelor', 'master', 'phd'],
        'experience': ['experience', 'employment', 'work history', 'professional experience', 'career'],
        'skills': ['skills', 'technical skills', 'competencies', 'expertise', 'proficiencies'],
        'projects': ['projects', 'portfolio', 'work samples'],
        'certifications': ['certifications', 'certificates', 'licenses'],
        'languages': ['languages', 'language proficiency']
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
        Extract text from PDF file
        
        WHY: PDF is the most common resume format
        Uses PyPDF2 to read PDF content page by page
        """
        text = ""
        try:
            with open(file_path, 'rb') as file:
                # Try with strict mode disabled to handle corrupted PDFs
                pdf_reader = PyPDF2.PdfReader(file, strict=False)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception as page_error:
                        logger.warning(f"Could not extract page {page_num + 1}: {page_error}")
                        continue
            
            if not text.strip():
                logger.warning("No text extracted from PDF, using filename as fallback")
                text = f"Resume document: {os.path.basename(file_path)}"
            
            logger.info(f"✓ Extracted {num_pages} pages from PDF")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting PDF: {e}")
            # Return a minimal text instead of failing completely
            logger.warning("PDF parsing failed, using fallback text")
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
        
        # Insert line breaks before section keywords (even if run together)
        section_patterns = [
            (r'([a-z\)])(\s*Education)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Experience)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Skills)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Summary)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Contact)', r'\1\n\n\2'),
            (r'([a-z\)])(\s*Projects)', r'\1\n\n\2'),
        ]
        
        for pattern, replacement in section_patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Split by potential section markers
        lines = text.split('\n')
        current_section = 'header'
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Skip empty lines
            if not line_lower:
                continue
            
            # Check if line contains section keyword (more aggressive matching)
            detected_section = None
            for section_name, keywords in self.SECTION_KEYWORDS.items():
                for keyword in keywords:
                    # Check if keyword appears at word boundary
                    if re.search(r'\b' + re.escape(keyword) + r'\b', line_lower):
                        # If keyword is prominent (appears in first 20 chars or line is short)
                        keyword_pos = line_lower.find(keyword)
                        if keyword_pos < 20 or len(line.split()) <= 6:
                            detected_section = section_name
                            break
                if detected_section:
                    break
            
            if detected_section:
                # Save previous section
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
            # Pattern: Years (like "1975 - Present" or "2000 - 2020")
            year_pattern = r'(19\d{2}|20[0-2]\d)\s*[-–]\s*(Present|19\d{2}|20[0-2]\d)'
            year_matches = list(re.finditer(year_pattern, exp_text))
            
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
