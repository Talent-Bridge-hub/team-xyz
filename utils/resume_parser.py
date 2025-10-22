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
        
        Returns:
            Dictionary mapping section name to section text
        """
        sections = {}
        lines = self.text.split('\n')
        current_section = 'header'
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Skip empty lines
            if not line_lower:
                continue
            
            # Check if line is a section header
            detected_section = None
            for section_name, keywords in self.SECTION_KEYWORDS.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Line matches a section keyword
                    if len(line.split()) <= 5:  # Likely a header (short line)
                        detected_section = section_name
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
        text = self.sections.get('header', '') + self.sections.get('contact', '')
        
        # Extract email using regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact['email'] = emails[0]
        
        # Extract phone using regex
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact['phone'] = phones[0]
        
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
        Extract education entries
        """
        education = []
        education_text = self.sections.get('education', '')
        
        if education_text:
            # Look for degree keywords
            degrees = ['bachelor', 'master', 'phd', 'doctorate', 'diploma', 'certificate', 'b.sc', 'm.sc']
            lines = education_text.split('\n')
            
            current_entry = {}
            for line in lines:
                line_lower = line.lower()
                
                # Check if line contains a degree
                if any(degree in line_lower for degree in degrees):
                    if current_entry:
                        education.append(current_entry)
                    current_entry = {'degree': line.strip()}
                elif current_entry:
                    # Add additional info to current entry
                    if 'institution' not in current_entry:
                        current_entry['institution'] = line.strip()
                    elif 'year' not in current_entry and re.search(r'\d{4}', line):
                        current_entry['year'] = line.strip()
            
            if current_entry:
                education.append(current_entry)
        
        return education
    
    def _extract_experience(self) -> List[Dict]:
        """
        Extract work experience entries
        """
        experience = []
        exp_text = self.sections.get('experience', '')
        
        if exp_text:
            # Split into entries (assuming blank lines separate them)
            entries = exp_text.split('\n\n')
            
            for entry in entries:
                if entry.strip():
                    experience.append({
                        'text': entry.strip(),
                        'bullet_points': [line.strip() for line in entry.split('\n') if line.strip().startswith(('•', '-', '*'))]
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
            
            # Remove common words
            stop_words = ['skills', 'technical', 'and', 'the', 'or']
            skills = [s for s in skills if s.lower() not in stop_words and len(s) > 2]
        
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
