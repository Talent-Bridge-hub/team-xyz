#!/usr/bin/env python3
"""
Test Job Matcher Module
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.job_matcher import JobMatcher
from utils.resume_parser import ResumeParser


def test_job_matcher():
    """Test job matching functionality"""
    
    print("=" * 60)
    print("Testing Job Matcher Module")
    print("=" * 60)
    
    # Initialize
    matcher = JobMatcher()
    parser = ResumeParser()
    
    # Parse sample resume
    resume_path = 'data/resumes/sample_resume.pdf'
    print(f"\n1. Parsing resume: {resume_path}")
    parsed = parser.parse_file(resume_path)
    print(f"   ✓ Found {len(parsed['structured_data']['skills'])} skills")
    
    # Find job matches
    print("\n2. Finding job matches...")
    matches = matcher.find_matches(parsed, limit=5)
    
    print(f"\n✓ Found {len(matches)} job matches:\n")
    
    for i, match in enumerate(matches, 1):
        job = match['job']
        score = match['match_score']
        
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Location: {job['location']} (Remote: {'Yes' if job['remote'] else 'No'})")
        print(f"   Match Score: {score['overall_score']}/100")
        print(f"     - Skills: {score['skill_score']}/100")
        print(f"     - Location: {score['location_score']}/100")
        print(f"     - Experience: {score['experience_score']}/100")
        print(f"   Matched Skills: {', '.join(score['breakdown']['matched_skills'])}")
        
        if score['breakdown']['missing_skills']:
            print(f"   Missing Skills: {', '.join(score['breakdown']['missing_skills'])}")
        
        salary = job['salary_range']
        print(f"   Salary: {salary['min']}-{salary['max']} {salary['currency']}/month")
        print()
    
    # Test market insights
    print("\n3. Getting market insights...")
    insights = matcher.get_market_insights('MENA')
    
    print(f"\n✓ Market Insights for {insights['region']}:")
    print(f"   Total Jobs: {insights['total_jobs']}")
    print(f"   Remote Jobs: {insights['remote_jobs_percentage']}%")
    print(f"\n   Top 5 In-Demand Skills:")
    for i, skill_data in enumerate(insights['top_skills'][:5], 1):
        print(f"     {i}. {skill_data['skill']} (demand: {skill_data['demand']})")
    
    print(f"\n   Average Salaries:")
    for level, salary_data in insights['average_salaries'].items():
        print(f"     {level}: {salary_data['average']} {salary_data['currency']}/month")
    
    print("\n" + "=" * 60)
    print("✓ Job Matcher Test Complete!")
    print("=" * 60)


if __name__ == '__main__':
    test_job_matcher()
