"""
Create a sample resume PDF for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_sample_resume(output_path: str):
    """Create a sample resume PDF"""
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Set margins
    margin = inch
    y = height - margin
    
    # Header - Name and Contact
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, y, "Ahmed Ben Ali")
    y -= 0.3 * inch
    
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "Email: ahmed.benali@email.com | Phone: +216 98 765 432")
    y -= 0.15 * inch
    c.drawString(margin, y, "LinkedIn: linkedin.com/in/ahmedbenali | GitHub: github.com/ahmedbenali")
    y -= 0.15 * inch
    c.drawString(margin, y, "Location: Tunis, Tunisia")
    y -= 0.5 * inch
    
    # Professional Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "PROFESSIONAL SUMMARY")
    y -= 0.25 * inch
    c.setFont("Helvetica", 10)
    summary_text = ("Software Engineer with 3+ years of experience in full-stack development. "
                   "Passionate about building scalable applications and solving complex problems.")
    c.drawString(margin, y, summary_text[:80])
    y -= 0.15 * inch
    c.drawString(margin, y, summary_text[80:])
    y -= 0.4 * inch
    
    # Education
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "EDUCATION")
    y -= 0.25 * inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "Bachelor of Science in Computer Science")
    y -= 0.18 * inch
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "University of Tunis El Manar, Tunisia")
    y -= 0.15 * inch
    c.drawString(margin, y, "Graduated: June 2020 | GPA: 3.8/4.0")
    y -= 0.4 * inch
    
    # Experience
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "PROFESSIONAL EXPERIENCE")
    y -= 0.25 * inch
    
    # Job 1
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "Software Engineer - Tech Solutions Ltd")
    y -= 0.18 * inch
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(margin, y, "January 2021 - Present | Tunis, Tunisia")
    y -= 0.18 * inch
    c.setFont("Helvetica", 10)
    c.drawString(margin + 0.2*inch, y, "• Developed and maintained web applications using React and Node.js")
    y -= 0.15 * inch
    c.drawString(margin + 0.2*inch, y, "• Improved application performance by 40% through code optimization")
    y -= 0.15 * inch
    c.drawString(margin + 0.2*inch, y, "• Collaborated with cross-functional teams to deliver projects on time")
    y -= 0.15 * inch
    c.drawString(margin + 0.2*inch, y, "• Mentored 3 junior developers in best coding practices")
    y -= 0.3 * inch
    
    # Job 2
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "Junior Developer - Digital Innovations")
    y -= 0.18 * inch
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(margin, y, "June 2020 - December 2020 | Tunis, Tunisia")
    y -= 0.18 * inch
    c.setFont("Helvetica", 10)
    c.drawString(margin + 0.2*inch, y, "• Built responsive web interfaces using HTML, CSS, and JavaScript")
    y -= 0.15 * inch
    c.drawString(margin + 0.2*inch, y, "• Integrated RESTful APIs with front-end applications")
    y -= 0.4 * inch
    
    # Skills
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "TECHNICAL SKILLS")
    y -= 0.25 * inch
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "Languages: Python, JavaScript, TypeScript, Java, SQL")
    y -= 0.15 * inch
    c.drawString(margin, y, "Frameworks: React, Node.js, Express, Django, Flask")
    y -= 0.15 * inch
    c.drawString(margin, y, "Tools: Git, Docker, Jenkins, AWS, PostgreSQL, MongoDB")
    y -= 0.15 * inch
    c.drawString(margin, y, "Soft Skills: Team Collaboration, Problem Solving, Agile Methodologies")
    y -= 0.4 * inch
    
    # Languages
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "LANGUAGES")
    y -= 0.25 * inch
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "Arabic: Native | French: Fluent | English: Professional Working Proficiency")
    
    c.save()
    print(f"✓ Sample resume created: {output_path}")

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/home/firas/Utopia')
    
    output = "/home/firas/Utopia/data/resumes/sample_resume.pdf"
    create_sample_resume(output)
