# 🚀 UtopiaHire Quick Reference

## Available Commands

### Resume Reviewer (Module 1)
```bash
# Analyze a resume
./utopiahire analyze resume.pdf

# Get enhancement suggestions
./utopiahire enhance resume.pdf

# Full pipeline (analyze + enhance + save)
./utopiahire full resume.pdf

# View database statistics
./utopiahire stats
```

### Job Matcher (Module 2) ✨ NEW
```bash
# Find matching jobs
./utopiahire match resume.pdf

# Limit results
./utopiahire match resume.pdf --limit 5

# Save matches to JSON
./utopiahire match resume.pdf --save

# Get market insights
./utopiahire market --region MENA
./utopiahire market --region "Sub-Saharan Africa"
```

## Python API

### Resume Analysis
```python
from utils.resume_parser import ResumeParser
from utils.resume_analyzer import ResumeAnalyzer
from utils.resume_enhancer import ResumeEnhancer

parser = ResumeParser()
analyzer = ResumeAnalyzer()
enhancer = ResumeEnhancer()

parsed = parser.parse_file('resume.pdf')
analysis = analyzer.analyze(parsed)
enhanced = enhancer.enhance_resume(parsed, analysis)
```

### Job Matching
```python
from utils.job_matcher import JobMatcher

matcher = JobMatcher()
matches = matcher.find_matches(parsed, limit=10)

for match in matches:
    print(f"{match['job']['title']}: {match['match_score']['overall_score']}/100")
```

## Testing
```bash
# Run all tests
bash test_all.sh

# Test specific module
python test_job_matcher.py
```

## Documentation
- `README.md` - Project overview
- `PROGRESS.md` - Current progress (50%)
- `docs/MODULE_2_JOB_MATCHER.md` - Job Matcher guide
- `COMPLETE.md` - Resume Reviewer guide
- `QUICKSTART.md` - Daily workflow

## Status: 50% Complete
✅ Module 1: Resume Reviewer  
✅ Module 2: Job Matcher  
⏳ Module 3: AI Interviewer  
⏳ Module 4: Footprint Scanner
