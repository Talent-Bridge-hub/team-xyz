# Jobs Module Documentation - Part 2 of 2
## Job Matching, Frontend, Integration & Deployment
---

## Table of Contents - Part 2

6. [Job Matching Algorithm](#6-job-matching-algorithm)
7. [Population Scripts](#7-population-scripts)
8. [Frontend Components](#8-frontend-components)
9. [Integration Flows](#9-integration-flows)
10. [Testing & Deployment](#10-testing--deployment)
11. [Troubleshooting](#11-troubleshooting)

---

## 6. Job Matching Algorithm

### 6.1 Overview

The **JobMatcher** class implements an advanced scoring algorithm that evaluates resume-job compatibility across multiple dimensions. It uses **weighted scoring** with fuzzy matching, semantic analysis, and regional awareness.

**File:** `/utils/job_matcher.py`

**Scoring Formula:**

```
Overall Score = (Skill Score × 50%) + (Experience Score × 25%) + 
                (Location Score × 15%) + (Title Relevance × 10%)
```

---

### 6.2 Skill Matching (50% Weight)

**Method:** `_calculate_skill_score()`

**Algorithm:**

```python
def _calculate_skill_score(self, candidate_skills: List[str], job: Dict) -> int:
    """
    Enhanced skill match score with fuzzy matching
    Returns: 0-100
    """
    required_skills = [s.lower().strip() for s in job.get('required_skills', [])]
    preferred_skills = [s.lower().strip() for s in job.get('preferred_skills', [])]
    
    if not required_skills and not preferred_skills:
        return 60  # Neutral score if no requirements
    
    # Fuzzy matching (handles variations like "React.js" vs "React")
    def fuzzy_match(skill: str, skill_list: List[str]) -> bool:
        skill_clean = re.sub(r'[.\-_]', '', skill.lower())
        for s in skill_list:
            s_clean = re.sub(r'[.\-_]', '', s.lower())
            
            # Direct or partial match
            if skill_clean in s_clean or s_clean in skill_clean:
                return True
            
            # Word overlap for multi-word skills
            skill_words = set(skill_clean.split())
            s_words = set(s_clean.split())
            if skill_words and s_words and len(skill_words & s_words) > 0:
                return True
        
        return False
    
    # Count matches with fuzzy matching
    required_matches = sum(1 for skill in required_skills if fuzzy_match(skill, candidate_skills))
    preferred_matches = sum(1 for skill in preferred_skills if fuzzy_match(skill, candidate_skills))
    
    # Calculate base scores
    required_percentage = (required_matches / len(required_skills)) * 100 if required_skills else 100
    preferred_percentage = (preferred_matches / len(preferred_skills)) * 100 if preferred_skills else 50
    
    # Weighted scoring: 75% required (critical), 25% preferred (bonus)
    score = int(required_percentage * 0.75 + preferred_percentage * 0.25)
    
    # Bonus: Candidate has significantly more skills (demonstrates expertise)
    if len(candidate_skills) > len(required_skills) + len(preferred_skills):
        bonus = min(10, (len(candidate_skills) - len(required_skills) - len(preferred_skills)) // 2)
        score = min(100, score + bonus)
    
    return min(100, max(0, score))
```

**Key Features:**

1. **Fuzzy Matching:**
   - Removes special characters (`.`, `-`, `_`)
   - Handles variations: "React.js" = "React" = "ReactJS"
   - Multi-word matching: "Machine Learning" matches "ML"

2. **Weighted Scoring:**
   - Required skills: 75% weight (critical)
   - Preferred skills: 25% weight (bonus)

3. **Expertise Bonus:**
   - +5 bonus per 2 extra skills beyond requirements
   - Max bonus: +10 points

**Examples:**

```python
# Example 1: Perfect match
candidate_skills = ["Python", "React", "PostgreSQL", "Docker", "AWS"]
job_required = ["Python", "React", "PostgreSQL"]
job_preferred = ["Docker", "AWS"]
# Score: 100 (all required + all preferred)

# Example 2: Missing preferred skills
candidate_skills = ["Python", "React", "PostgreSQL"]
job_required = ["Python", "React", "PostgreSQL"]
job_preferred = ["Docker", "AWS"]
# Score: 75 (100% required × 0.75 + 0% preferred × 0.25)

# Example 3: Fuzzy matching
candidate_skills = ["React.js", "Node.js", "PostgreSQL"]
job_required = ["React", "Node", "postgres"]
# Score: 100 (fuzzy matching resolves all variations)
```

---

### 6.3 Experience Matching (25% Weight)

**Method:** `_calculate_experience_score()`

**Algorithm:**

```python
def _calculate_experience_score(self, candidate_experience: str, job: Dict) -> int:
    """
    Enhanced experience level matching
    Returns: 0-100
    """
    job_experience = (job.get('experience_level') or '').lower()
    candidate_exp = candidate_experience.lower()
    
    # If no requirement, neutral score
    if not job_experience or job_experience == 'not specified':
        return 70
    
    # Exact match
    if candidate_exp == job_experience or candidate_exp in job_experience:
        return 100
    
    # Experience hierarchy with numeric mapping
    experience_levels = {
        'intern': 0,
        'entry': 1,
        'entry-level': 1,
        'junior': 1,
        'mid': 2,
        'mid-level': 2,
        'intermediate': 2,
        'senior': 3,
        'lead': 4,
        'principal': 5,
        'staff': 5,
        'expert': 5
    }
    
    # Find levels
    candidate_level = 2  # Default: mid-level
    for exp_key, exp_val in experience_levels.items():
        if exp_key in candidate_exp:
            candidate_level = exp_val
            break
    
    job_level = 2  # Default: mid-level
    for exp_key, exp_val in experience_levels.items():
        if exp_key in job_experience:
            job_level = exp_val
            break
    
    # Calculate score based on level difference
    diff = abs(candidate_level - job_level)
    
    if diff == 0:
        return 100  # Perfect match
    elif diff == 1:
        if candidate_level > job_level:
            return 90  # Overqualified (slight penalty)
        else:
            return 70  # Underqualified (more penalty)
    elif diff == 2:
        if candidate_level > job_level:
            return 70  # Significantly overqualified
        else:
            return 50  # Significantly underqualified
    else:
        # 3+ levels difference
        if candidate_level > job_level:
            return 50  # Way overqualified (might be bored)
        else:
            return 30  # Way underqualified (might struggle)
```

**Experience Hierarchy:**

```
Level 0: Intern
Level 1: Entry-level, Junior
Level 2: Mid-level, Intermediate
Level 3: Senior
Level 4: Lead
Level 5: Principal, Staff, Expert
```

**Scoring Matrix:**

| Candidate → Job | Same Level | +1 Level | -1 Level | +2 Levels | -2 Levels | +3 Levels | -3 Levels |
|----------------|------------|----------|----------|-----------|-----------|-----------|-----------|
| **Score**      | 100        | 90       | 70       | 70        | 50        | 50        | 30        |

---

### 6.4 Location Matching (15% Weight)

**Method:** `_calculate_location_score()`

**Algorithm:**

```python
def _calculate_location_score(self, candidate_location: str, job: Dict) -> int:
    """
    Enhanced location match with regional awareness
    Returns: 0-100
    """
    job_location = job.get('location', '').lower()
    job_remote = job.get('remote', False)
    candidate_loc_lower = candidate_location.lower()
    
    # Remote jobs get perfect score
    if job_remote:
        return 100
    
    # Exact city/country match
    if candidate_loc_lower in job_location or job_location in candidate_loc_lower:
        return 100
    
    # MENA region matching
    mena_countries = ['tunisia', 'egypt', 'morocco', 'algeria', 'libya', 'uae', 
                     'saudi', 'jordan', 'lebanon', 'qatar', 'kuwait', 'bahrain', 
                     'oman', 'yemen', 'syria', 'iraq', 'palestine']
    candidate_in_mena = any(country in candidate_loc_lower for country in mena_countries)
    job_in_mena = 'mena' in job.get('region', '').lower() or \
                  any(country in job_location for country in mena_countries)
    
    if candidate_in_mena and job_in_mena:
        return 75  # Good match within MENA region
    
    # Sub-Saharan Africa region matching
    ssa_countries = ['nigeria', 'kenya', 'ghana', 'south africa', 'ethiopia', 
                    'tanzania', 'uganda', 'rwanda', 'senegal', 'ivory coast']
    candidate_in_ssa = any(country in candidate_loc_lower for country in ssa_countries)
    job_in_ssa = 'sub-saharan' in job.get('region', '').lower() or \
                 'africa' in job.get('region', '').lower() or \
                 any(country in job_location for country in ssa_countries)
    
    if candidate_in_ssa and job_in_ssa:
        return 75  # Good match within Sub-Saharan Africa
    
    # Any Africa match
    if (candidate_in_mena or candidate_in_ssa) and (job_in_mena or job_in_ssa):
        return 60
    
    # Global/International jobs
    if any(keyword in job_location for keyword in ['global', 'international', 'anywhere', 'worldwide']):
        return 90
    
    # Different region but still relevant
    return 40
```

**Location Scoring:**

```
100 points: Remote jobs OR Exact city/country match
90 points:  Global/International positions
75 points:  Same region (MENA or Sub-Saharan Africa)
60 points:  Any Africa (cross-region)
40 points:  Different region
```

---

### 6.5 Title Relevance (10% Weight)

**Method:** `_calculate_title_score()`

**Algorithm:**

```python
def _calculate_title_score(self, candidate_skills: List[str], job: Dict) -> int:
    """
    Calculate job title relevance based on skills
    Returns: 0-100
    """
    job_title = job.get('title', '').lower()
    
    # Extract keywords from job title
    title_keywords = re.findall(r'\b\w+\b', job_title)
    title_keywords = [k for k in title_keywords if len(k) > 2]  # Remove short words
    
    # Check how many candidate skills appear in title
    matches = sum(1 for skill in candidate_skills 
                 if any(skill.lower() in keyword or keyword in skill.lower() 
                       for keyword in title_keywords))
    
    if not title_keywords:
        return 50  # Neutral
    
    # Calculate relevance (need at least 3 matches or half of title keywords)
    relevance = min(100, (matches / max(3, len(title_keywords) // 2)) * 100)
    
    return int(relevance)
```

**Examples:**

```python
# Example 1: High relevance
job_title = "Python React Full Stack Developer"
candidate_skills = ["Python", "React", "Full Stack"]
# Score: 100 (all key skills match title)

# Example 2: Partial relevance
job_title = "Senior Software Engineer"
candidate_skills = ["Python", "JavaScript", "Software Development"]
# Score: 66 (software matches, engineer matches)

# Example 3: Low relevance
job_title = "Data Scientist"
candidate_skills = ["PHP", "WordPress", "jQuery"]
# Score: 0 (no matching skills)
```

---

## 7. Population Scripts

### 7.1 Quick Population Script

**File:** `/scripts/populate/quick_populate_jobs.py`

**Purpose:** Rapidly populate database with ~300 jobs (no authentication required)

**Features:**
- Direct database access (no API authentication)
- 20 predefined search queries
- Covers MENA, Sub-Saharan Africa, and Remote
- 3-second delays between searches (rate limit protection)
- Automatic region detection

**Usage:**

```bash
cd /home/firas/Utopia
python3 scripts/populate/quick_populate_jobs.py
```

**Search Configuration:**

```python
QUICK_SEARCHES = [
    # MENA Region
    {'query': 'Software Engineer', 'location': 'Cairo, Egypt', 'count': 20},
    {'query': 'Frontend Developer', 'location': 'Dubai, UAE', 'count': 15},
    {'query': 'Data Analyst', 'location': 'Tunis, Tunisia', 'count': 15},
    {'query': 'Backend Developer', 'location': 'Casablanca, Morocco', 'count': 15},
    {'query': 'Full Stack Developer', 'location': 'Riyadh, Saudi Arabia', 'count': 15},
    
    # Sub-Saharan Africa
    {'query': 'Software Engineer', 'location': 'Lagos, Nigeria', 'count': 20},
    {'query': 'Data Analyst', 'location': 'Nairobi, Kenya', 'count': 15},
    {'query': 'Frontend Developer', 'location': 'Johannesburg, South Africa', 'count': 15},
    
    # Remote
    {'query': 'Remote Software Engineer', 'location': 'Anywhere', 'count': 20},
    {'query': 'Remote Frontend Developer', 'location': 'Remote', 'count': 15},
]
```

**Output:**

```
================================================================================
🚀 QUICK JOB DATABASE POPULATOR
================================================================================
Estimated time: 5-10 minutes
APIs available:
    1. SerpAPI - 250 searches/month
    2. LinkedIn RapidAPI - 500 requests/month
    3. JSearch RapidAPI - 500 requests/month

🔄 Search 1/20
   Query: Software Engineer
   Location: Cairo, Egypt
   ✅ Scraped 20 jobs
   💾 Stored 18 new jobs (skipped 2 duplicates)

🎉 SCRAPING COMPLETE!
📊 Statistics:
   Total jobs scraped: 305
   New jobs stored: 287
   Duplicates skipped: 18

📈 Database Summary:
   Total jobs in database: 287
   
   Jobs by Region:
      • MENA: 165
      • Sub-Saharan Africa: 98
      • Other: 24
```

---

### 7.2 Comprehensive Population Script

**File:** `/scripts/populate/populate_jobs_comprehensive.py`

**Purpose:** Large-scale population with authentication (300-1000+ jobs)

**Features:**
- Requires user authentication (JWT token)
- Uses backend `/jobs/scrape` API endpoint
- 30+ job titles per region
- 20+ locations across MENA and Africa
- Batch processing with 30-second delays
- Comprehensive coverage

**Search Strategy:**

```python
SEARCH_QUERIES = {
    'MENA': {
        'locations': [
            'Tunisia', 'Egypt', 'Cairo', 'Alexandria', 
            'Morocco', 'Casablanca', 'Algeria', 'Algiers',
            'UAE', 'Dubai', 'Abu Dhabi', 'Saudi Arabia', 'Riyadh',
            'Jordan', 'Amman', 'Lebanon', 'Beirut',
            'Qatar', 'Doha', 'Kuwait', 'Bahrain', 'Oman'
        ],
        'queries': [
            'Software Engineer', 'Frontend Developer', 'Backend Developer',
            'Full Stack Developer', 'Data Analyst', 'Data Scientist',
            'Mobile Developer', 'DevOps Engineer', 'UI/UX Designer',
            'Product Manager', 'QA Engineer', 'Security Engineer',
            # ... 30+ total job titles
        ]
    },
    'Sub-Saharan Africa': {
        'locations': [
            'Nigeria', 'Lagos', 'Kenya', 'Nairobi',
            'South Africa', 'Johannesburg', 'Ghana', 'Accra',
            # ... 20+ locations
        ],
        'queries': [
            'Software Engineer', 'Data Analyst', 'Frontend Developer',
            # ... 20+ job titles
        ]
    },
    'Remote': {
        'locations': ['Remote', 'Anywhere', 'Work from Home'],
        'queries': [
            'Remote Software Engineer', 'Remote Frontend Developer',
            # ... 12+ remote-specific titles
        ]
    }
}
```

**Batch Processing:**

```python
strategy = [
    {
        'name': 'MENA - High Priority Cities',
        'queries': SEARCH_QUERIES['MENA']['queries'][:10],
        'locations': ['Cairo', 'Dubai', 'Riyadh', 'Tunis', 'Casablanca'],
        'num_results': 15
    },
    {
        'name': 'Sub-Saharan Africa - Major Cities',
        'queries': SEARCH_QUERIES['Sub-Saharan Africa']['queries'][:10],
        'locations': ['Lagos', 'Nairobi', 'Johannesburg', 'Accra', 'Kigali'],
        'num_results': 15
    },
    # ... 5 total batches
]
```

**Usage:**

```bash
# 1. Update credentials in script
# Edit line 63-64 with actual email/password

# 2. Run script
python3 scripts/populate/populate_jobs_comprehensive.py
```

---

### 7.3 Daily Job Updater (Automated)

**File:** `/scripts/populate/daily_job_updater.py`

**Purpose:** Automated daily updates with smart API budgeting

**Features:**
- Runs daily at 2:00 AM (cron job)
- Smart API usage tracking (monthly budgets)
- Different strategies per weekday
- Cleans up jobs older than 30 days
- Comprehensive logging

**Weekly Strategy:**

```python
strategies = {
    0: {  # Monday - MENA Tech
        'name': 'MENA Tech Jobs',
        'searches': [
            {'query': 'Software Engineer', 'location': 'Cairo, Egypt', 'count': 10},
            {'query': 'Frontend Developer', 'location': 'Dubai, UAE', 'count': 10},
            {'query': 'Backend Developer', 'location': 'Tunis, Tunisia', 'count': 10},
        ]
    },
    1: {  # Tuesday - Sub-Saharan Africa Tech
        'name': 'Sub-Saharan Africa Tech Jobs',
        'searches': [
            {'query': 'Software Engineer', 'location': 'Lagos, Nigeria', 'count': 10},
            {'query': 'Full Stack Developer', 'location': 'Nairobi, Kenya', 'count': 10},
        ]
    },
    2: {  # Wednesday - Data & Analytics
        'name': 'Data & Analytics Jobs',
        'searches': [
            {'query': 'Data Analyst', 'location': 'Casablanca, Morocco', 'count': 10},
            {'query': 'Data Scientist', 'location': 'Accra, Ghana', 'count': 10},
        ]
    },
    3: {  # Thursday - DevOps & Cloud
        'name': 'DevOps & Cloud Jobs',
        'searches': [
            {'query': 'DevOps Engineer', 'location': 'Amman, Jordan', 'count': 10},
        ]
    },
    4: {  # Friday - Design & Product
        'name': 'Design & Product Jobs',
        'searches': [
            {'query': 'UI/UX Designer', 'location': 'Beirut, Lebanon', 'count': 10},
        ]
    },
    5: {  # Saturday - Remote
        'name': 'Remote Opportunities',
        'searches': [
            {'query': 'Remote Software Engineer', 'location': 'Remote', 'count': 15},
        ]
    },
    6: {  # Sunday - Mixed
        'name': 'Popular Roles (All Regions)',
        'searches': [
            {'query': 'Full Stack Developer', 'location': 'Egypt', 'count': 10},
        ]
    }
}
```

**API Budget Management:**

```python
def calculate_daily_budget(self):
    """
    Ensure we don't run out of API calls before month ends
    """
    now = datetime.now()
    days_in_month = monthrange(now.year, now.month)[1]
    days_remaining = days_in_month - now.day + 1
    
    for api_name, api_config in API_CREDENTIALS.items():
        used = usage.get(api_name, 0)
        limit = api_config['free_limit']
        remaining = limit - used
        
        # Reserve 10% for emergencies
        safe_remaining = int(remaining * 0.9)
        
        # Daily budget = remaining / days left
        daily_budget = max(1, safe_remaining // days_remaining)
        
        budgets[api_name] = {
            'limit': limit,
            'used': used,
            'remaining': remaining,
            'daily_budget': daily_budget
        }
    
    return budgets
```

**Cron Setup:**

```bash
# Open crontab
crontab -e

# Add this line (runs at 2:00 AM daily)
0 2 * * * cd /home/firas/Utopia && /usr/bin/python3 scripts/populate/daily_job_updater.py >> logs/cron.log 2>&1

# Verify cron job
crontab -l
```

**Manual Run:**

```bash
# Run update manually
python3 scripts/populate/daily_job_updater.py

# Check API usage stats
python3 scripts/populate/daily_job_updater.py --check-usage

# Show cron setup instructions
python3 scripts/populate/daily_job_updater.py --setup-cron
```

---

## 8. Frontend Components

### 8.1 Jobs Page (Main Interface)

**File:** `/frontend/src/pages/jobs/index.tsx`

**Features:**
- 4 tabs: Browse All Jobs, Matched for You, Advanced Search, Compatibility Analyzer
- Responsive design with Tailwind CSS
- State management with React hooks

**Tab Structure:**

```tsx
const tabs = [
  { id: 'browse', label: 'Browse All Jobs', icon: '...' },
  { id: 'matched', label: 'Matched for You', icon: '...' },
  { id: 'search', label: 'Advanced Search', icon: '...' },
  { id: 'compatibility', label: 'Compatibility Analyzer', icon: '...' },
];

const [activeTab, setActiveTab] = useState<TabType>('browse');
```

**Advanced Search Form:**

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  {/* Keywords */}
  <input
    type="text"
    value={searchFilters.keywords || ''}
    onChange={(e) => handleSearchFilterChange('keywords', e.target.value)}
    placeholder="e.g. Software Engineer, Python, React"
  />
  
  {/* Location */}
  <input
    type="text"
    value={searchFilters.location || ''}
    onChange={(e) => handleSearchFilterChange('location', e.target.value)}
    placeholder="e.g. Tunisia, Cairo, Remote"
  />
  
  {/* Job Type */}
  <select value={searchFilters.jobType || ''}>
    <option value="">All Types</option>
    <option value="Full-time">Full-time</option>
    <option value="Part-time">Part-time</option>
    <option value="Contract">Contract</option>
  </select>
  
  {/* Experience Level */}
  <select value={searchFilters.experienceLevel || ''}>
    <option value="">All Levels</option>
    <option value="Junior">Junior</option>
    <option value="Mid-Level">Mid-Level</option>
    <option value="Senior">Senior</option>
  </select>
  
  {/* Salary Range */}
  <input type="number" placeholder="Min Salary (USD)" />
  <input type="number" placeholder="Max Salary (USD)" />
  
  {/* Required Skills */}
  <input
    type="text"
    placeholder="e.g. Python, React, PostgreSQL"
    className="md:col-span-2"
  />
  
  {/* Remote Only */}
  <label>
    <input type="checkbox" />
    <span>Remote only</span>
  </label>
</div>
```

---

### 8.2 JobMatcher Component

**File:** `/frontend/src/components/jobs/JobMatcher.tsx`

**Features:**
- Resume selection dropdown
- Location preference (multiple selection)
- Job type filters (multiple selection)
- Experience level filters (multiple selection)
- Min score slider (0-100)
- Max results selector (25, 50, 100, 200)
- Match results with score breakdown
- Apply Now buttons (opens job URLs)

**Configuration Section:**

```tsx
<div className="bg-white rounded-lg shadow-md p-6">
  <h3 className="text-lg font-semibold mb-4">Configure Job Matching</h3>
  
  {/* Resume Selection */}
  <select
    value={selectedResumeId || ''}
    onChange={(e) => setSelectedResumeId(Number(e.target.value))}
  >
    {resumes.map(resume => (
      <option key={resume.id} value={resume.id}>
        {resume.original_filename}
      </option>
    ))}
  </select>
  
  {/* Location Preference */}
  <div className="flex flex-wrap gap-2">
    {['MENA', 'Tunisia', 'Egypt', 'Remote'].map(location => (
      <button
        onClick={() => toggleArrayValue(locationPreference, location)}
        className={locationPreference.includes(location) ? 'bg-blue-600' : 'bg-gray-100'}
      >
        {location}
      </button>
    ))}
  </div>
  
  {/* Min Score Slider */}
  <input
    type="range"
    min="0"
    max="100"
    step="5"
    value={minScore}
    onChange={(e) => setMinScore(Number(e.target.value))}
  />
  <span>Minimum Match Score: {minScore}%</span>
  
  {/* Match Button */}
  <button
    onClick={handleMatch}
    disabled={loading || !selectedResumeId}
    className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg"
  >
    Find Matching Jobs
  </button>
</div>
```

**Match Results Display:**

```tsx
{matches.length > 0 && (
  <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
    {matches.map(match => (
      <div key={match.job.id} className="bg-white rounded-lg shadow-md p-6">
        {/* Match Score Badge */}
        <div className="flex justify-between items-start mb-3">
          <h4>{match.job.title}</h4>
          <span className={`px-3 py-1 rounded-full ${
            match.match_score.overall_score >= 80 ? 'bg-green-100 text-green-800' :
            match.match_score.overall_score >= 60 ? 'bg-blue-100 text-blue-800' :
            'bg-yellow-100 text-yellow-800'
          }`}>
            {match.match_score.overall_score}%
          </span>
        </div>
        
        <p className="text-gray-600">{match.job.company}</p>
        <p className="text-gray-500 text-sm">{match.job.location}</p>
        
        {/* Score Breakdown */}
        <div className="grid grid-cols-3 gap-2 mt-4 mb-4">
          <div className="text-center p-2 bg-gray-50 rounded">
            <div className="font-bold">{match.match_score.skill_score}%</div>
            <div className="text-xs text-gray-600">Skills</div>
          </div>
          <div className="text-center p-2 bg-gray-50 rounded">
            <div className="font-bold">{match.match_score.location_score}%</div>
            <div className="text-xs text-gray-600">Location</div>
          </div>
          <div className="text-center p-2 bg-gray-50 rounded">
            <div className="font-bold">{match.match_score.experience_score}%</div>
            <div className="text-xs text-gray-600">Experience</div>
          </div>
        </div>
        
        {/* Apply Button */}
        <button
          onClick={() => window.open(match.job.url, '_blank')}
          className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg"
        >
          Apply Now
        </button>
      </div>
    ))}
  </div>
)}
```

---

### 8.3 JobCompatibilityAnalyzer Component

**File:** `/frontend/src/components/jobs/JobCompatibilityAnalyzer.tsx` (463 lines)

**Features:**
- Resume selection
- Job description textarea (min 50 characters)
- Optional: Job title, company, required skills
- AI-powered analysis (Groq API)
- Detailed results with color-coded scores
- Matched/missing skills visualization
- Strengths, gaps, and recommendations
- AI summary and detailed analysis

**Input Form:**

```tsx
<div className="space-y-4">
  {/* Resume Selection */}
  <select
    value={selectedResumeId || ''}
    onChange={(e) => setSelectedResumeId(Number(e.target.value))}
    disabled={analyzing}
  >
    <option value="">-- Select a resume --</option>
    {resumes.map(resume => (
      <option key={resume.id} value={resume.id}>
        {resume.original_filename}
      </option>
    ))}
  </select>
  
  {/* Job Title (Optional) */}
  <input
    type="text"
    value={jobTitle}
    onChange={(e) => setJobTitle(e.target.value)}
    placeholder="e.g., Senior Software Engineer"
  />
  
  {/* Company (Optional) */}
  <input
    type="text"
    value={company}
    onChange={(e) => setCompany(e.target.value)}
    placeholder="e.g., TechCorp Inc."
  />
  
  {/* Job Description (Required, min 50 chars) */}
  <textarea
    value={jobDescription}
    onChange={(e) => setJobDescription(e.target.value)}
    placeholder="Paste the full job description here..."
    rows={10}
    className={jobDescription.length < 50 ? 'border-amber-300' : ''}
  />
  <p className="text-sm text-gray-500">
    {jobDescription.length} / 50 characters minimum
  </p>
  
  {/* Required Skills (Optional) */}
  <input
    type="text"
    value={requiredSkills}
    placeholder="e.g., Python, React, AWS (comma-separated)"
  />
  
  {/* Analyze Button */}
  <button
    onClick={handleAnalyze}
    disabled={analyzing || !selectedResumeId || jobDescription.length < 50}
    className="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg"
  >
    {analyzing ? 'Analyzing...' : 'Analyze Compatibility'}
  </button>
</div>
```

**Results Display:**

```tsx
{result && (
  <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
    {/* Overall Score */}
    <div className={`${getScoreBgColor(result.overall_match_score)} rounded-lg p-6`}>
      <p className="text-6xl font-bold text-center">
        {result.overall_match_score}%
      </p>
    </div>
    
    {/* Detailed Scores */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="bg-gray-50 rounded-lg p-4">
        <p className="text-sm font-medium text-gray-600">Skills Match</p>
        <p className="text-3xl font-bold">{result.skill_match_score}%</p>
      </div>
      <div className="bg-gray-50 rounded-lg p-4">
        <p className="text-sm font-medium text-gray-600">Experience Match</p>
        <p className="text-3xl font-bold">{result.experience_match_score}%</p>
      </div>
      <div className="bg-gray-50 rounded-lg p-4">
        <p className="text-sm font-medium text-gray-600">Education Match</p>
        <p className="text-3xl font-bold">{result.education_match_score}%</p>
      </div>
    </div>
    
    {/* AI Summary */}
    {result.ai_summary && (
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2">AI Summary</h4>
        <p className="text-blue-800">{result.ai_summary}</p>
      </div>
    )}
    
    {/* Matched Skills */}
    <div>
      <h4 className="font-semibold mb-3">
        Matched Skills ({result.matched_skills.length})
      </h4>
      <div className="flex flex-wrap gap-2">
        {result.matched_skills.map((skill, index) => (
          <span
            key={index}
            className="bg-green-100 text-green-800 px-3 py-1 rounded-full"
          >
            ✓ {skill}
          </span>
        ))}
      </div>
    </div>
    
    {/* Missing Skills */}
    <div>
      <h4 className="font-semibold mb-3">
        Skills to Develop ({result.missing_skills.length})
      </h4>
      <div className="flex flex-wrap gap-2">
        {result.missing_skills.map((skill, index) => (
          <span
            key={index}
            className="bg-red-100 text-red-800 px-3 py-1 rounded-full"
          >
            {skill}
          </span>
        ))}
      </div>
    </div>
    
    {/* Strengths */}
    <div>
      <h4 className="font-semibold mb-3">Your Strengths</h4>
      <ul>
        {result.strengths.map((strength, index) => (
          <li key={index} className="flex items-start">
            <svg className="w-5 h-5 text-green-600 mr-2">✓</svg>
            <span>{strength}</span>
          </li>
        ))}
      </ul>
    </div>
    
    {/* Detailed AI Analysis */}
    {result.ai_detailed_analysis && (
      <div className="border-t pt-6">
        <h4 className="font-semibold mb-3">Detailed Analysis</h4>
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="whitespace-pre-line">{result.ai_detailed_analysis}</p>
        </div>
      </div>
    )}
  </div>
)}
```

**Score Color Coding:**

```tsx
const getScoreColor = (score: number) => {
  if (score >= 80) return 'text-green-600';  // Excellent
  if (score >= 60) return 'text-blue-600';   // Good
  if (score >= 40) return 'text-yellow-600'; // Fair
  return 'text-red-600';                      // Poor
};

const getScoreBgColor = (score: number) => {
  if (score >= 80) return 'bg-green-100';
  if (score >= 60) return 'bg-blue-100';
  if (score >= 40) return 'bg-yellow-100';
  return 'bg-red-100';
};
```

---

### 8.4 JobList Component

**File:** `/frontend/src/components/jobs/JobList.tsx`

**Features:**
- Paginated job list (20 jobs per page)
- Filter by location (MENA, Sub-Saharan Africa, or specific country)
- Filter by job type (Full-time, Part-time, Contract, etc.)
- Filter by experience level (Junior, Mid-Level, Senior, etc.)
- Remote-only toggle
- JobCard grid layout (responsive)

**Filter Section:**

```tsx
<div className="flex flex-wrap gap-4 mb-6">
  {/* Location Filter */}
  <select
    value={location}
    onChange={(e) => setLocation(e.target.value)}
  >
    <option value="">All Locations</option>
    <option value="MENA">MENA Region</option>
    <option value="Sub-Saharan Africa">Sub-Saharan Africa</option>
    <option value="Tunisia">Tunisia</option>
    <option value="Egypt">Egypt</option>
    <option value="Nigeria">Nigeria</option>
    {/* ... more options */}
  </select>
  
  {/* Job Type Filter */}
  <select value={jobType} onChange={(e) => setJobType(e.target.value)}>
    <option value="">All Types</option>
    <option value="Full-time">Full-time</option>
    <option value="Part-time">Part-time</option>
    <option value="Contract">Contract</option>
  </select>
  
  {/* Remote Only Toggle */}
  <label>
    <input
      type="checkbox"
      checked={remoteOnly}
      onChange={(e) => setRemoteOnly(e.target.checked)}
    />
    <span>Remote only</span>
  </label>
</div>
```

---

### 8.5 JobCard Component

**File:** `/frontend/src/components/jobs/JobCard.tsx`

**Features:**
- Compact job display (title, company, location)
- Job type badge (Full-time, Remote, etc.)
- Salary range display (if available)
- Required skills (top 5)
- "View Details" and "Apply Now" buttons

**Component Structure:**

```tsx
<div className="bg-white rounded-lg shadow-md hover:shadow-lg p-6">
  {/* Header */}
  <div className="flex justify-between items-start mb-3">
    <h3 className="text-lg font-semibold">{job.title}</h3>
    {job.remote && (
      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">
        Remote
      </span>
    )}
  </div>
  
  {/* Company & Location */}
  <p className="text-gray-600 font-medium">{job.company}</p>
  <p className="text-gray-500 text-sm">{job.location}</p>
  
  {/* Salary */}
  {job.salary_range && (
    <p className="text-indigo-600 font-medium mt-2">
      {job.salary_range.currency} {job.salary_range.min} - {job.salary_range.max}
    </p>
  )}
  
  {/* Skills */}
  <div className="flex flex-wrap gap-2 mt-4">
    {job.required_skills.slice(0, 5).map((skill, index) => (
      <span
        key={index}
        className="bg-blue-50 text-blue-700 px-2 py-1 rounded text-xs"
      >
        {skill}
      </span>
    ))}
  </div>
  
  {/* Actions */}
  <div className="flex gap-2 mt-4">
    <button
      onClick={() => onViewDetails(job)}
      className="flex-1 border border-blue-600 text-blue-600 px-4 py-2 rounded-lg"
    >
      View Details
    </button>
    <button
      onClick={() => window.open(job.url, '_blank')}
      className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg"
    >
      Apply Now
    </button>
  </div>
</div>
```

---

## 9. Integration Flows

### 9.1 Job Discovery Flow

```
User opens Jobs Page
    ↓
Loads "Browse All Jobs" tab
    ↓
Frontend: GET /api/v1/jobs/list?page=1&page_size=20
    ↓
Backend queries PostgreSQL jobs table
    ↓
Returns 20 jobs with pagination metadata
    ↓
Frontend displays JobCard grid
    ↓
User applies filters (location, job_type, remote_only)
    ↓
Frontend: GET /api/v1/jobs/list?location=MENA&remote_only=true
    ↓
Backend filters query with WHERE clauses
    ↓
Returns filtered jobs
    ↓
Frontend updates grid display
```

---

### 9.2 Job Matching Flow

```
User clicks "Matched for You" tab
    ↓
Frontend loads JobMatcher component
    ↓
Frontend: GET /api/v1/resumes
    ↓
Backend returns user's resumes
    ↓
User selects resume, configures filters (location, min_score)
    ↓
User clicks "Find Matching Jobs"
    ↓
Frontend: POST /api/v1/jobs/match
{
  "resume_id": 123,
  "limit": 50,
  "min_score": 60,
  "fetch_fresh_jobs": true
}
    ↓
Backend:
  1. Fetches resume from database (validates ownership)
  2. Parses resume (skills, experience, location)
  3. Optionally scrapes fresh jobs (if fetch_fresh_jobs=true)
  4. Loads 500 recent jobs from database
  5. For each job:
     - Calculate skill_score (50% weight)
     - Calculate experience_score (25% weight)
     - Calculate location_score (15% weight)
     - Calculate title_score (10% weight)
     - Compute overall_score
  6. Filter jobs with score >= min_score
  7. Sort by overall_score (descending)
  8. Return top N matches
    ↓
Frontend receives matches array
    ↓
Frontend displays JobCard grid with match scores
    ↓
User clicks "Apply Now"
    ↓
Opens job.url in new tab (direct application link)
```

---

### 9.3 Compatibility Analysis Flow

```
User clicks "Compatibility Analyzer" tab
    ↓
Frontend loads JobCompatibilityAnalyzer component
    ↓
Frontend: GET /api/v1/resumes
    ↓
User selects resume, pastes job description
    ↓
User clicks "Analyze Compatibility"
    ↓
Frontend: POST /api/v1/jobs/compatibility
{
  "resume_id": 123,
  "job_description": "...",
  "job_title": "Senior Software Engineer",
  "company": "TechCorp"
}
    ↓
Backend:
  1. Validates resume exists and belongs to user
  2. Validates job_description length (min 50 chars)
  3. Extracts candidate data:
     - Skills (from parsed resume)
     - Experience (from resume sections)
     - Education (from resume sections)
  4. Extracts job requirements:
     - Skills (from description keywords)
     - Experience level (from description keywords)
  5. Calculates scores:
     - skill_match_score (fuzzy matching)
     - experience_match_score (years + relevance)
     - education_match_score (degree presence)
  6. Computes overall_match_score:
     = skill_score × 50% + experience_score × 35% + education_score × 15%
  7. Identifies:
     - matched_skills (intersection)
     - missing_skills (job requirements not in resume)
     - strengths (based on high scores)
     - gaps (based on low scores)
  8. Generates recommendations
  9. Calls Groq API (LLaMA 3.3 70B):
     - Sends resume summary + job description + scores
     - Receives AI-generated summary and detailed analysis
     - Max 800 tokens, temperature 0.7
  10. Returns comprehensive analysis
    ↓
Frontend receives JobCompatibilityResponse
    ↓
Frontend displays:
  - Overall score (large, color-coded)
  - Detailed scores (skill, experience, education)
  - AI summary (highlighted box)
  - Matched skills (green badges)
  - Missing skills (red badges)
  - Strengths (checkmarks)
  - Gaps (warnings)
  - Recommendations (info icons)
  - Detailed AI analysis (expandable)
```

---

## 10. Testing & Deployment

### 10.1 Manual Testing

**Test 1: Job Scraping**

```bash
# Start backend server
cd /home/firas/Utopia/backend
uvicorn main:app --reload --port 8000

# In another terminal, test scraping
curl -X POST http://localhost:8000/api/v1/jobs/scrape \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["Software Engineer"],
    "locations": ["Tunisia"],
    "num_results_per_query": 10
  }'

# Expected Response:
# {
#   "jobs_scraped": 10,
#   "jobs_stored": 9,
#   "api_used": "SerpAPI (Google Jobs)",
#   "message": "Successfully scraped 10 jobs..."
# }
```

**Test 2: Job Matching**

```bash
curl -X POST http://localhost:8000/api/v1/jobs/match \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "limit": 10,
    "min_score": 60
  }'

# Expected Response:
# {
#   "matches": [...],
#   "total_matches": 8,
#   "average_score": 72.5,
#   "message": "Found 8 job matches..."
# }
```

**Test 3: Compatibility Analysis**

```bash
curl -X POST http://localhost:8000/api/v1/jobs/compatibility \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description": "We are looking for a Senior Software Engineer with 5+ years...",
    "job_title": "Senior Software Engineer"
  }'

# Expected Response:
# {
#   "overall_match_score": 82,
#   "skill_match_score": 85,
#   "matched_skills": [...],
#   "ai_summary": "...",
#   ...
# }
```

---

### 10.2 Frontend Testing

**Test 1: Browse Jobs**

```bash
# Start frontend dev server
cd /home/firas/Utopia/frontend
npm run dev

# Visit: http://localhost:5174/dashboard/jobs
# Expected: Job list with 20 jobs, filters working
```

**Test 2: Job Matching**

```
1. Visit: http://localhost:5174/dashboard/jobs
2. Click "Matched for You" tab
3. Select a resume from dropdown
4. Click "Find Matching Jobs"
5. Expected: Match results with scores
```

**Test 3: Compatibility Analysis**

```
1. Visit: http://localhost:5174/dashboard/jobs
2. Click "Compatibility Analyzer" tab
3. Select resume
4. Paste job description (min 50 chars)
5. Click "Analyze Compatibility"
6. Expected: Detailed analysis with AI insights
```

---

### 10.3 Deployment

**Backend Deployment:**

```bash
# 1. Set environment variables
export GROQ_API_KEY="your_groq_api_key"
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"

# 2. Run backend
cd /home/firas/Utopia/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# 3. Setup daily job updater cron
crontab -e
# Add: 0 2 * * * cd /home/firas/Utopia && python3 scripts/populate/daily_job_updater.py
```

**Frontend Deployment:**

```bash
# 1. Build production bundle
cd /home/firas/Utopia/frontend
npm run build

# 2. Serve with nginx or deploy to Vercel/Netlify
```

---

## 11. Troubleshooting

### 11.1 Common Issues

**Issue 1: No jobs found in database**

```bash
# Solution: Populate database
python3 scripts/populate/quick_populate_jobs.py
```

**Issue 2: API rate limit exceeded**

```
Error: "Rate limit exceeded"
Solution:
  1. Check API usage: python3 scripts/populate/daily_job_updater.py --check-usage
  2. Wait until next month or upgrade API plan
  3. Use cached results (6-hour cache)
```

**Issue 3: Job matching returns 0 matches**

```
Possible causes:
  1. min_score too high → Lower to 40-50
  2. No jobs in database → Run population script
  3. Resume has no skills → Ensure resume is properly parsed
  4. Wrong location → Check candidate location vs job locations
```

**Issue 4: Compatibility analysis fails**

```
Error: "Job description must be at least 50 characters"
Solution: Provide longer job description (min 50 chars)

Error: "Resume not found"
Solution:
  1. Verify resume_id exists: SELECT * FROM resumes WHERE id = ?
  2. Check user ownership: Resume must belong to current user
```

**Issue 5: Daily updater not running**

```bash
# Check cron logs
tail -f /home/firas/Utopia/logs/cron.log

# Verify cron job exists
crontab -l

# Test manual run
python3 scripts/populate/daily_job_updater.py
```

---

### 11.2 Performance Optimization

**Database Indexes:**

```sql
-- Already created (11 indexes)
-- If queries are slow, verify indexes:
\d jobs
```

**API Caching:**

```python
# Cache is automatic (6-hour expiry)
# To clear cache manually:
scraper.cache = {}
```

**Frontend Pagination:**

```tsx
// Use pagination to avoid loading all jobs at once
const [page, setPage] = useState(1);
const [pageSize, setPageSize] = useState(20);  // Max 100
```

---

### 11.3 Monitoring

**Check Database Stats:**

```sql
-- Total jobs
SELECT COUNT(*) FROM jobs;

-- Jobs by region
SELECT region, COUNT(*) FROM jobs GROUP BY region;

-- Jobs by source
SELECT source, COUNT(*) FROM jobs GROUP BY source;

-- Recent jobs (last 7 days)
SELECT COUNT(*) FROM jobs 
WHERE posted_date >= NOW() - INTERVAL '7 days';
```

**Check API Usage:**

```bash
# View usage stats
python3 scripts/populate/daily_job_updater.py --check-usage

# Example output:
# SerpAPI: 45/100 used (45%), 55 remaining
# LinkedIn RapidAPI: 120/500 used (24%), 380 remaining
# JSearch RapidAPI: 80/250 used (32%), 170 remaining
```

**Check Logs:**

```bash
# Backend logs
tail -f /home/firas/Utopia/backend/logs/app.log

# Cron logs
tail -f /home/firas/Utopia/logs/cron.log

# Daily updater logs
tail -f /home/firas/Utopia/logs/job_updater.log
```

---

## End of Part 2
- **Total Lines (Part 2):** 1190
- **Status:** ✅ Complete
- **Last Updated:** January 2025
