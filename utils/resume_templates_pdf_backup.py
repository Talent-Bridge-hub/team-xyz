"""
Resume Templates Module
Pre-designed professional resume templates for users to download and customize
"""

from typing import Dict, List
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import logging

logger = logging.getLogger(__name__)


class ResumeTemplateGenerator:
    """
    Generate professional resume templates for users to download
    """
    
    TEMPLATES = {
        'professional_chronological': {
            'name': 'Professional Chronological',
            'description': 'Traditional format highlighting work experience. Best for professionals with 3+ years of experience.',
            'best_for': 'Experienced Professionals',
            'ats_friendly': True,
            'sections': ['Contact', 'Professional Summary', 'Experience', 'Skills', 'Education', 'Certifications']
        },
        'modern_skills_focused': {
            'name': 'Modern Skills-Focused',
            'description': 'Emphasizes technical skills and projects. Ideal for developers and tech professionals.',
            'best_for': 'Tech & Engineering Roles',
            'ats_friendly': True,
            'sections': ['Contact', 'Skills', 'Technical Projects', 'Experience', 'Education']
        },
        'entry_level_student': {
            'name': 'Entry-Level / Student',
            'description': 'Perfect for students, recent graduates, and career changers with limited work experience.',
            'best_for': 'Students & New Graduates',
            'ats_friendly': True,
            'sections': ['Contact', 'Education', 'Skills', 'Projects', 'Internships/Experience', 'Activities']
        }
    }
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles for templates"""
        
        # Name style (large, bold, centered)
        self.styles.add(ParagraphStyle(
            name='TemplateName',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Contact style (centered, smaller)
        self.styles.add(ParagraphStyle(
            name='TemplateContact',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='TemplateSectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#d1d5db'),
            borderPadding=4
        ))
        
        # Placeholder text style (italic, gray)
        self.styles.add(ParagraphStyle(
            name='TemplatePlaceholder',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6b7280'),
            fontName='Helvetica-Oblique',
            spaceAfter=6
        ))
        
        # Instruction style
        self.styles.add(ParagraphStyle(
            name='TemplateInstruction',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#9ca3af'),
            fontName='Helvetica-Oblique',
            spaceAfter=4
        ))
    
    def generate_template(self, template_type: str, output_path: str) -> bool:
        """
        Generate a resume template PDF
        
        Args:
            template_type: Type of template ('professional_chronological', 'modern_skills_focused', 'entry_level_student')
            output_path: Path to save the PDF
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if template_type not in self.TEMPLATES:
                logger.error(f"Unknown template type: {template_type}")
                return False
            
            template_info = self.TEMPLATES[template_type]
            
            # Create PDF
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.5*inch
            )
            
            story = []
            
            # Add template-specific content
            if template_type == 'professional_chronological':
                story = self._generate_professional_chronological()
            elif template_type == 'modern_skills_focused':
                story = self._generate_modern_skills_focused()
            elif template_type == 'entry_level_student':
                story = self._generate_entry_level_student()
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"✓ Template generated: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate template: {e}")
            return False
    
    def _generate_professional_chronological(self) -> List:
        """Generate Professional Chronological template content"""
        story = []
        
        # Name
        story.append(Paragraph("YOUR FULL NAME", self.styles['TemplateName']))
        story.append(Spacer(1, 6))
        
        # Contact Info
        story.append(Paragraph(
            "your.email@example.com | +1-XXX-XXX-XXXX | City, State | LinkedIn: linkedin.com/in/yourprofile",
            self.styles['TemplateContact']
        ))
        story.append(Spacer(1, 12))
        
        # Professional Summary
        story.append(Paragraph("PROFESSIONAL SUMMARY", self.styles['TemplateSectionHeader']))
        story.append(Paragraph(
            "<i>Results-driven [Your Title] with X+ years of experience in [Industry/Field]. "
            "Proven track record of [Key Achievement]. Strong expertise in [Skill 1], [Skill 2], and [Skill 3]. "
            "Seeking to leverage technical skills and leadership experience to drive innovation at [Target Company].</i>",
            self.styles['TemplatePlaceholder']
        ))
        story.append(Spacer(1, 12))
        
        # Professional Experience
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['TemplateSectionHeader']))
        
        # Job 1
        story.append(Paragraph("<b>Job Title</b> | Company Name | City, State", self.styles['Normal']))
        story.append(Paragraph("<i>Start Date – End Date (or Present)</i>", self.styles['TemplateInstruction']))
        story.append(Spacer(1, 4))
        story.append(Paragraph("• Led/Managed/Developed [achievement] resulting in [X% improvement/$ savings/metric]", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Implemented [solution] that increased [metric] by X% across Y projects", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Collaborated with [team size] team members to deliver [project] serving X+ users", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Reduced [process/cost] by X% through [action], saving $Y annually", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 10))
        
        # Job 2
        story.append(Paragraph("<b>Previous Job Title</b> | Previous Company | City, State", self.styles['Normal']))
        story.append(Paragraph("<i>Start Date – End Date</i>", self.styles['TemplateInstruction']))
        story.append(Spacer(1, 4))
        story.append(Paragraph("• Developed [project/feature] using [technologies] for X+ users", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Achieved [metric] by optimizing [process] through [method]", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Mentored team of X engineers on [technology/practice]", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 12))
        
        # Skills
        story.append(Paragraph("TECHNICAL SKILLS", self.styles['TemplateSectionHeader']))
        story.append(Paragraph(
            "<b>Programming Languages:</b> Python, Java, JavaScript, SQL, C++",
            self.styles['TemplatePlaceholder']
        ))
        story.append(Paragraph(
            "<b>Frameworks & Tools:</b> React, Node.js, Django, Docker, Kubernetes, Git",
            self.styles['TemplatePlaceholder']
        ))
        story.append(Paragraph(
            "<b>Cloud & Databases:</b> AWS, Azure, PostgreSQL, MongoDB, Redis",
            self.styles['TemplatePlaceholder']
        ))
        story.append(Paragraph(
            "<b>Soft Skills:</b> Team Leadership, Agile Development, Problem Solving, Communication",
            self.styles['TemplatePlaceholder']
        ))
        story.append(Spacer(1, 12))
        
        # Education
        story.append(Paragraph("EDUCATION", self.styles['TemplateSectionHeader']))
        story.append(Paragraph(
            "<b>Bachelor of Science in Computer Science</b> | University Name | City, State",
            self.styles['Normal']
        ))
        story.append(Paragraph("<i>Graduation Year</i> | GPA: 3.X/4.0", self.styles['TemplateInstruction']))
        story.append(Paragraph("• Relevant Coursework: Data Structures, Algorithms, Machine Learning, Databases", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 12))
        
        # Certifications
        story.append(Paragraph("CERTIFICATIONS", self.styles['TemplateSectionHeader']))
        story.append(Paragraph("• AWS Certified Solutions Architect – Associate (Year)", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Certified Kubernetes Administrator (CKA) (Year)", self.styles['TemplatePlaceholder']))
        
        return story
    
    def _generate_modern_skills_focused(self) -> List:
        """Generate Modern Skills-Focused template content"""
        story = []
        
        # Name
        story.append(Paragraph("YOUR FULL NAME", self.styles['TemplateName']))
        story.append(Paragraph("Software Engineer | Full Stack Developer", self.styles['TemplateContact']))
        story.append(Spacer(1, 6))
        
        # Contact
        story.append(Paragraph(
            "your.email@example.com | +1-XXX-XXX-XXXX | github.com/yourusername | linkedin.com/in/yourprofile",
            self.styles['TemplateContact']
        ))
        story.append(Spacer(1, 12))
        
        # Technical Skills (prominent)
        story.append(Paragraph("TECHNICAL SKILLS", self.styles['TemplateSectionHeader']))
        story.append(Paragraph(
            "<b>Languages:</b> Python, JavaScript, TypeScript, Java, Go, SQL, HTML/CSS",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "<b>Frontend:</b> React, Vue.js, Next.js, TailwindCSS, Redux, Material-UI",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "<b>Backend:</b> Node.js, Express, FastAPI, Django, Spring Boot, REST APIs, GraphQL",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "<b>Databases:</b> PostgreSQL, MongoDB, Redis, MySQL, Elasticsearch",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "<b>DevOps & Cloud:</b> Docker, Kubernetes, AWS (EC2, S3, Lambda), Azure, CI/CD, GitHub Actions",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "<b>Tools:</b> Git, VS Code, Postman, Jest, Pytest, Webpack, npm/yarn",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 12))
        
        # Technical Projects
        story.append(Paragraph("TECHNICAL PROJECTS", self.styles['TemplateSectionHeader']))
        
        # Project 1
        story.append(Paragraph("<b>Project Name</b> | <i>Technologies: React, Node.js, PostgreSQL, AWS</i>", self.styles['Normal']))
        story.append(Paragraph("<i>GitHub: github.com/yourusername/project | Live: yourproject.com</i>", self.styles['TemplateInstruction']))
        story.append(Spacer(1, 4))
        story.append(Paragraph("• Built full-stack application serving X+ users with feature Y and Z", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Implemented authentication system with JWT, achieving 99.9% uptime", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Optimized database queries reducing load time by X%", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 10))
        
        # Project 2
        story.append(Paragraph("<b>Another Project</b> | <i>Technologies: Python, FastAPI, Docker, MongoDB</i>", self.styles['Normal']))
        story.append(Paragraph("<i>GitHub: github.com/yourusername/project2</i>", self.styles['TemplateInstruction']))
        story.append(Spacer(1, 4))
        story.append(Paragraph("• Developed RESTful API handling X requests/second with Y ms latency", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Containerized application with Docker, deployed on AWS ECS", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 12))
        
        # Professional Experience
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.styles['TemplateSectionHeader']))
        
        story.append(Paragraph("<b>Software Engineer</b> | Company Name | City, State", self.styles['Normal']))
        story.append(Paragraph("<i>Start Date – Present</i>", self.styles['TemplateInstruction']))
        story.append(Spacer(1, 4))
        story.append(Paragraph("• Developed X features using [tech stack] impacting Y+ users", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Improved system performance by X% through code optimization", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Collaborated in Agile environment with team of X developers", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 12))
        
        # Education
        story.append(Paragraph("EDUCATION", self.styles['TemplateSectionHeader']))
        story.append(Paragraph(
            "<b>Bachelor of Science in Computer Science</b> | University Name",
            self.styles['Normal']
        ))
        story.append(Paragraph("<i>Graduation Year</i> | GPA: 3.X/4.0", self.styles['TemplateInstruction']))
        
        return story
    
    def _generate_entry_level_student(self) -> List:
        """Generate Entry-Level/Student template content"""
        story = []
        
        # Name
        story.append(Paragraph("YOUR FULL NAME", self.styles['TemplateName']))
        story.append(Spacer(1, 6))
        
        # Contact
        story.append(Paragraph(
            "your.email@university.edu | +1-XXX-XXX-XXXX | linkedin.com/in/yourprofile | github.com/yourusername",
            self.styles['TemplateContact']
        ))
        story.append(Spacer(1, 12))
        
        # Education (first for students)
        story.append(Paragraph("EDUCATION", self.styles['TemplateSectionHeader']))
        story.append(Paragraph(
            "<b>Bachelor of Science in Computer Science</b> | University Name | City, State",
            self.styles['Normal']
        ))
        story.append(Paragraph("<i>Expected Graduation: Month Year</i> | GPA: 3.X/4.0", self.styles['TemplateInstruction']))
        story.append(Spacer(1, 4))
        story.append(Paragraph("• <b>Relevant Coursework:</b> Data Structures, Algorithms, Database Systems, Web Development, Software Engineering", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• <b>Honors:</b> Dean's List (Semester/Year), Academic Scholarship", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 12))
        
        # Technical Skills
        story.append(Paragraph("TECHNICAL SKILLS", self.styles['TemplateSectionHeader']))
        story.append(Paragraph(
            "<b>Programming:</b> Python, Java, JavaScript, C++, SQL, HTML/CSS",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "<b>Technologies:</b> React, Node.js, Git, Docker, PostgreSQL, MongoDB",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "<b>Tools:</b> VS Code, IntelliJ, Jupyter Notebook, Postman, GitHub",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 12))
        
        # Projects
        story.append(Paragraph("ACADEMIC & PERSONAL PROJECTS", self.styles['TemplateSectionHeader']))
        
        # Project 1
        story.append(Paragraph("<b>Project Name</b> | <i>Course: Software Engineering | Technologies: React, Python, SQL</i>", self.styles['Normal']))
        story.append(Paragraph("<i>GitHub: github.com/yourusername/project</i>", self.styles['TemplateInstruction']))
        story.append(Spacer(1, 4))
        story.append(Paragraph("• Developed web application for [purpose] as part of team project", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Implemented [feature] using [technology], improving [metric]", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Collaborated with team of X students using Agile methodology", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 10))
        
        # Project 2
        story.append(Paragraph("<b>Another Project</b> | <i>Personal Project | Technologies: Python, Flask, MongoDB</i>", self.styles['Normal']))
        story.append(Spacer(1, 4))
        story.append(Paragraph("• Built [application] to solve [problem] with X+ users/downloads", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Integrated [API/service] to provide [functionality]", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 12))
        
        # Experience
        story.append(Paragraph("EXPERIENCE", self.styles['TemplateSectionHeader']))
        
        # Internship
        story.append(Paragraph("<b>Software Engineering Intern</b> | Company Name | City, State", self.styles['Normal']))
        story.append(Paragraph("<i>Month Year – Month Year</i>", self.styles['TemplateInstruction']))
        story.append(Spacer(1, 4))
        story.append(Paragraph("• Contributed to [project/feature] using [technologies]", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Wrote unit tests achieving X% code coverage", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• Participated in code reviews and daily standups", self.styles['TemplatePlaceholder']))
        story.append(Spacer(1, 12))
        
        # Activities & Leadership
        story.append(Paragraph("ACTIVITIES & LEADERSHIP", self.styles['TemplateSectionHeader']))
        story.append(Paragraph("• <b>Computer Science Club</b> – Member/Officer (Year-Year): Organized hackathons and tech talks", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• <b>Hackathon Participant</b> – Won [award] at [Hackathon Name] (Year)", self.styles['TemplatePlaceholder']))
        story.append(Paragraph("• <b>Volunteer Tutor</b> – Tutored X students in programming and mathematics", self.styles['TemplatePlaceholder']))
        
        return story
    
    def get_template_info(self, template_type: str) -> Dict:
        """Get information about a template"""
        return self.TEMPLATES.get(template_type, {})
    
    def list_templates(self) -> List[Dict]:
        """List all available templates"""
        return [
            {
                'id': key,
                **value
            }
            for key, value in self.TEMPLATES.items()
        ]


# Test function
if __name__ == '__main__':
    generator = ResumeTemplateGenerator()
    
    # Generate all templates
    for template_id in ['professional_chronological', 'modern_skills_focused', 'entry_level_student']:
        output = f"/tmp/template_{template_id}.pdf"
        success = generator.generate_template(template_id, output)
        print(f"{'✓' if success else '✗'} Generated: {output}")
