#!/usr/bin/env python3
"""
Test script to debug enhancement download issues
"""

import sys
sys.path.insert(0, '/home/firas/Utopia')

from utils.resume_enhancer import ResumeEnhancer
from pathlib import Path
import json

# Test data similar to what backend receives
parsed_data = {
    'raw_text': '''
    John Doe
    john@example.com
    
    EXPERIENCE
    Software Engineer at Tech Company
    - Worked on projects
    - Used Python
    
    SKILLS
    Python, JavaScript, SQL
    
    EDUCATION
    BS Computer Science, University
    ''',
    'sections': {
        'contact': 'John Doe\njohn@example.com',
        'experience': 'Software Engineer at Tech Company\n- Worked on projects\n- Used Python',
        'skills': 'Python, JavaScript, SQL',
        'education': 'BS Computer Science, University'
    },
    'structured_data': {
        'skills': ['Python', 'JavaScript', 'SQL'],
        'experience': [{
            'title': 'Software Engineer',
            'company': 'Tech Company',
            'duration': '2020-Present',
            'bullets': ['Worked on projects', 'Used Python']
        }],
        'education': [{
            'degree': 'BS Computer Science',
            'institution': 'University',
            'year': '2020'
        }]
    },
    'metadata': {
        'filename': 'test_resume.pdf'
    }
}

analysis_data = {
    'overall_score': 75,
    'skill_match': {'score': 70, 'matched': ['Python'], 'missing': ['Docker']},
    'experience_quality': {'score': 80, 'issues': []},
    'education_quality': {'score': 75}
}

print("=" * 60)
print("Testing Resume Enhancement Download")
print("=" * 60)

try:
    # Step 1: Enhance resume
    print("\n1. Creating enhancer...")
    enhancer = ResumeEnhancer()
    
    print("2. Enhancing resume...")
    enhancement_result = enhancer.enhance_resume(parsed_data, analysis_data)
    print(f"   ✅ Enhancement complete")
    print(f"   Keys: {list(enhancement_result.keys())}")
    print(f"   Changes: {len(enhancement_result.get('changes_made', []))}")
    
    # Step 2: Generate PDF
    print("\n3. Generating enhanced PDF...")
    output_path = "/tmp/test_enhanced_resume.pdf"
    success = enhancer.generate_enhanced_pdf(enhancement_result, output_path)
    print(f"   ✅ PDF generation: {success}")
    
    # Step 3: Verify file
    print("\n4. Verifying file...")
    pdf_path = Path(output_path)
    if pdf_path.exists():
        size = pdf_path.stat().st_size
        print(f"   ✅ File exists: {size} bytes")
        
        if size > 0:
            print(f"\n{'='*60}")
            print("✅ SUCCESS: Enhancement download would work!")
            print(f"{'='*60}")
        else:
            print(f"\n{'='*60}")
            print("❌ FAIL: File is empty!")
            print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("❌ FAIL: File was not created!")
        print(f"{'='*60}")
        
except Exception as e:
    print(f"\n{'='*60}")
    print(f"❌ ERROR: {e}")
    print(f"{'='*60}")
    import traceback
    traceback.print_exc()
