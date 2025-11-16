# Footprint Module Documentation - PART 1

---

## Table of Contents - Part 1

1. [Module Overview](#1-module-overview)
2. [System Architecture](#2-system-architecture)
3. [Platform Integrations](#3-platform-integrations)
4. [Scoring System](#4-scoring-system)
5. [Database Schema](#5-database-schema)
6. [Backend API Reference](#6-backend-api-reference)

---

## 1. Module Overview

### 1.1 Purpose

The **Digital Footprint Scanner** analyzes a developer's online presence across multiple platforms to provide:
- **Comprehensive visibility scoring** (0-100 scale)
- **Platform-specific analysis** (GitHub, StackOverflow)
- **AI-powered personalized recommendations** (Groq API)
- **Career insights and skill gap analysis**
- **Privacy assessment and risk evaluation**
- **Progress tracking over time**

### 1.2 Key Features

✅ **Multi-Platform Scanning:**
- GitHub profile, repositories, activity, README analysis
- StackOverflow reputation, badges, tags, contributions
- Support for additional platforms (LinkedIn, Twitter - future)(Soon)

✅ **Advanced Scoring:**
- Overall visibility score (0-100)
- 4 dimension scores: Visibility, Activity, Impact, Expertise
- Performance levels: Excellent (85-100), Good (70-84), Average (55-69), Needs Improvement (0-54)

✅ **AI Recommendations:**
- Groq API integration (llama-3.3-70b-versatile)
- Profile recommendations (3-5 items)
- Career insights (2-3 items)
- Skill gap identification (3-5 skills)
- Rule-based fallback system

✅ **Privacy Analysis:**
- Identifies exposed personal information
- Risk assessment (Critical, High, Medium, Low, Safe)
- Privacy recommendations

✅ **Progress Tracking:**
- Scan history with pagination
- Compare two scans for improvement analysis
- Historical score trends

### 1.3 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend Framework** | FastAPI | Latest |
| **Language** | Python | 3.12+ |
| **Database** | PostgreSQL | 14+ |
| **Data Storage** | JSONB (PostgreSQL) | - |
| **GitHub API** | REST API v3 | v3 |
| **StackOverflow API** | Stack Exchange API | 2.3 |
| **AI Model** | Groq (llama-3.3-70b-versatile) | Latest |
| **Frontend** | React 18 + TypeScript | 18.x |
| **UI Library** | TailwindCSS + Framer Motion | Latest |
| **Charts** | Recharts | Latest |

### 1.4 Module Files

**Backend (5 files):**
- `/backend/app/api/footprint.py` (850+ lines) - API endpoints
- `/backend/app/models/footprint.py` (400+ lines) - Pydantic models
- `/backend/migrations/create_footprint_tables.py` - Migration script
- `/config/footprint_schema.sql` (300+ lines) - Database schema

**Utilities (4 files):**
- `/utils/footprint_calculator.py` (500+ lines) - Overall scoring engine
- `/utils/github_analyzer.py` (700+ lines) - GitHub integration
- `/utils/stackoverflow_scanner.py` (500+ lines) - StackOverflow integration
- `/utils/groq_recommendation_generator.py` (500+ lines) - AI recommendations

**Frontend (6 files):**
- `/frontend/src/pages/footprint/FootprintPage.tsx` (600+ lines) - Main page
- `/frontend/src/components/footprint/FootprintScanForm.tsx` (200+ lines) - Scan form
- `/frontend/src/components/footprint/ScoreGauge.tsx` - Score visualization
- `/frontend/src/components/footprint/RecommendationsList.tsx` - AI recommendations UI
- `/frontend/src/components/footprint/GitHubContributionGraph.tsx` - Contribution heatmap
- `/frontend/src/components/footprint/ActivityChart.tsx` - Activity chart

**Total:** 15 files, ~5000+ lines of code

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │ FootprintPage  │  │ ScanForm       │  │ Charts & Gauges │  │
│  │ (Main Display) │  │ (Initiate Scan)│  │ (Visualization) │  │
│  └────────┬───────┘  └────────┬───────┘  └────────┬────────┘  │
└───────────┼──────────────────────┼──────────────────────┼────────┘
            │                      │                      │
            │    API Calls (JWT Auth)                     │
            └──────────────────────┼──────────────────────┘
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND API (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              /api/v1/footprint/* Endpoints               │  │
│  │  • POST /scan           • GET /recommendations/{id}      │  │
│  │  • GET /history         • GET /compare/{id1}/{id2}       │  │
│  │  • GET /{scan_id}                                        │  │
│  └───────────┬──────────────────────────────────────────────┘  │
└──────────────┼─────────────────────────────────────────────────┘
               │
      ┌────────┼────────┐
      │        │        │
      ▼        ▼        ▼
┌───────────┐ ┌────────────┐ ┌──────────────────┐
│  GitHub   │ │StackOverfl.│ │ Groq AI          │
│  Analyzer │ │  Scanner   │ │ Recommendation   │
│  (API v3) │ │  (API 2.3) │ │ Generator        │
└─────┬─────┘ └──────┬─────┘ └────────┬─────────┘
      │              │                 │
      │              │                 │
      └──────────────┼─────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Footprint Calculator  │
        │  (Scoring Engine)      │
        └────────────┬───────────┘
                     │
                     ▼
          ┌─────────────────────┐
          │  PostgreSQL DB      │
          │  (footprint_scans)  │
          └─────────────────────┘
```

### 2.2 Data Flow

**1. Scan Initiation:**
```
User Input (GitHub username, SO ID)
    → POST /api/v1/footprint/scan
    → Validate authentication (JWT)
    → Check scan rate limits
```

**2. Platform Analysis (Parallel):**
```
GitHub Analysis:                    StackOverflow Analysis:
→ Fetch profile                     → Fetch profile by ID/name
→ Get repositories (max 100)        → Get top tags (max 10)
→ Analyze languages (bytes)         → Get answers (max 100)
→ Get activity events (90 days)     → Get questions (max 100)
→ Fetch profile README              → Calculate scores
→ Extract skills                    → Return analysis
→ Calculate GitHub score
→ Return analysis
```

**3. Score Calculation:**
```
FootprintCalculator
    → Combine GitHub + StackOverflow data
    → Apply weights: GitHub (60%), StackOverflow (40%)
    → Calculate 4 dimensions:
        • Visibility: followers, stars, reputation
        • Activity: commits, PRs, answers, questions
        • Impact: stars, forks, accepted answers
        • Expertise: code quality, badges, reputation
    → Determine performance level
    → Generate insights (strengths, weaknesses, recommendations)
```

**4. AI Recommendations (Optional):**
```
Groq API Integration
    → Build context (profile, repos, skills, README, scores)
    → Send to Groq llama-3.3-70b-versatile
    → Parse JSON response
    → Extract profile_recommendations, career_insights, skill_gaps
    → Fallback to rule-based if AI fails
```

**5. Database Storage:**
```
Store in footprint_scans table
    → user_id, platforms_scanned[]
    → github_data (JSONB), stackoverflow_data (JSONB)
    → scores (overall, dimensions)
    → privacy_report (JSONB)
    → recommendations (JSONB)
    → Created/updated timestamps
```

**6. Response to Frontend:**
```
Return FootprintScanResponse
    → scan_id, scanned_at
    → github_analysis, stackoverflow_analysis
    → overall_score, dimension_scores
    → visibility_level, performance_level
    → privacy_report (if requested)
    → recommendations
```

### 2.3 Component Responsibilities

| Component | Responsibility | Lines of Code |
|-----------|---------------|---------------|
| **footprint.py (API)** | Endpoint handlers, request validation, response formatting | 850+ |
| **footprint_calculator.py** | Overall score calculation, insights generation | 500+ |
| **github_analyzer.py** | GitHub API integration, profile/repo/activity analysis | 700+ |
| **stackoverflow_scanner.py** | StackOverflow API integration, reputation/badge analysis | 500+ |
| **groq_recommendation_generator.py** | AI recommendations, context building, fallback logic | 500+ |
| **FootprintPage.tsx** | UI display, score gauges, charts, recommendations | 600+ |
| **FootprintScanForm.tsx** | User input, validation, error handling | 200+ |

---

## 3. Platform Integrations

### 3.1 GitHub Integration

**File:** `/utils/github_analyzer.py` (700+ lines)

#### 3.1.1 GitHub REST API v3

**Base URL:** `https://api.github.com`

**Authentication:**
```python
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',  # Optional but recommended
    'Accept': 'application/vnd.github.v3+json'
}
```

**Rate Limits:**
- **Authenticated:** 5,000 requests/hour
- **Unauthenticated:** 60 requests/hour

**Environment Variable:**
```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 3.1.2 API Endpoints Used

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `GET /users/{username}` | User profile | name, bio, location, followers, repos, created_at |
| `GET /users/{username}/repos?per_page=100` | Repositories | name, description, stars, forks, language, topics |
| `GET /repos/{owner}/{repo}/languages` | Language stats | `{ "Python": 12345, "JavaScript": 5678 }` (bytes) |
| `GET /users/{username}/events?per_page=300` | Activity events | PushEvent, PullRequestEvent, IssuesEvent (last 90 days) |
| `GET /repos/{username}/{username}/contents/README.md` | Profile README | Base64 encoded content |

#### 3.1.3 GitHubAnalyzer Class

**Key Methods:**

```python
class GitHubAnalyzer:
    def __init__(self, github_token: Optional[str] = None):
        """Initialize with optional GitHub token for higher rate limits"""
        
    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """
        Fetch basic user profile information.
        
        Returns:
            {
                'login': 'username',
                'name': 'Full Name',
                'bio': 'Developer bio',
                'location': 'City, Country',
                'public_repos': 50,
                'followers': 100,
                'following': 50,
                'created_at': '2020-01-01T00:00:00Z'
            }
        """
        
    def get_repositories(self, username: str, max_repos: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch user's public repositories (up to max_repos).
        
        Returns: List of repositories with name, description, stars, forks, language, topics
        """
        
    def get_repository_languages(self, owner: str, repo_name: str) -> Dict[str, int]:
        """
        Get detailed language breakdown by bytes of code.
        
        Returns: {'Python': 15234, 'JavaScript': 8901, 'HTML': 2345}
        """
        
    def get_user_events(self, username: str, max_events: int = 300) -> List[Dict[str, Any]]:
        """
        Fetch recent activity events (last 90 days).
        
        Returns: List of events (PushEvent, PullRequestEvent, IssuesEvent, etc.)
        """
        
    def get_profile_readme(self, username: str) -> Optional[str]:
        """
        Fetch profile README from username/username repository.
        
        Returns: Decoded README content or None if not found
        """
        
    def analyze_repositories(self, repos: List[Dict]) -> Dict[str, Any]:
        """
        Analyze repositories to extract:
        - Total stars, forks
        - Languages used (with bytes)
        - Skills (frameworks, databases, tools)
        - Top repositories
        
        Returns:
            {
                'total_repos': 50,
                'total_stars': 500,
                'total_forks': 100,
                'languages': {'Python': 50000, 'JavaScript': 30000},
                'skills': {
                    'frameworks': ['React', 'Django', 'FastAPI'],
                    'databases': ['PostgreSQL', 'MongoDB'],
                    'tools': ['Docker', 'Kubernetes', 'AWS']
                },
                'top_repositories': [...]
            }
        """
        
    def analyze_activity(self, events: List[Dict]) -> Dict[str, Any]:
        """
        Analyze activity events to calculate:
        - Total events count
        - Commits count
        - Pull requests count
        - Issues count
        - Activity streak (consecutive days)
        
        Returns:
            {
                'total_events': 150,
                'commits': 80,
                'pull_requests': 30,
                'issues': 20,
                'activity_streak': 15,
                'active_days': 45
            }
        """
        
    def calculate_scores(self, profile: Dict, repo_analysis: Dict, activity_analysis: Dict) -> Dict[str, float]:
        """
        Calculate GitHub scores (0-100 scale).
        
        Scoring Formula:
        - Code Quality (30%): Stars/repo, followers, repo activity
        - Activity (40%): Commits, PRs, issues, streak
        - Impact (30%): Total stars, forks, followers
        
        Returns:
            {
                'code_quality_score': 75.5,
                'activity_score': 82.3,
                'impact_score': 68.9,
                'overall_score': 76.2
            }
        """
```

#### 3.1.4 Skills Detection

**Frameworks Detected (17):**
- React, Vue, Angular, Svelte
- Django, Flask, FastAPI, Express
- Spring Boot, Laravel, Ruby on Rails
- Next.js, Nuxt.js, Gatsby
- TensorFlow, PyTorch, Keras

**Databases Detected (9):**
- PostgreSQL, MySQL, MongoDB, Redis
- SQLite, Cassandra, DynamoDB, Firebase, Elasticsearch

**Tools Detected (13):**
- Docker, Kubernetes, Jenkins, GitLab CI
- AWS, Azure, GCP
- Terraform, Ansible
- GraphQL, REST API
- Microservices, CI/CD

**Detection Logic:**
```python
def _extract_skills_from_repos(self, repos: List[Dict]) -> Dict[str, List[str]]:
    """
    Extract skills from:
    - Repository names
    - Repository descriptions
    - Repository topics
    
    Uses case-insensitive matching against predefined skill lists.
    """
```

#### 3.1.5 Example Response

```json
{
  "profile": {
    "login": "johndoe",
    "name": "John Doe",
    "bio": "Full Stack Developer | Python | React",
    "location": "San Francisco, CA",
    "public_repos": 42,
    "followers": 150,
    "following": 80,
    "created_at": "2018-05-15T12:00:00Z"
  },
  "repositories": {
    "total_repos": 42,
    "total_stars": 850,
    "total_forks": 120,
    "languages": {
      "Python": 125000,
      "JavaScript": 85000,
      "TypeScript": 45000,
      "HTML": 12000
    },
    "skills": {
      "frameworks": ["React", "Django", "FastAPI", "Express"],
      "databases": ["PostgreSQL", "MongoDB", "Redis"],
      "tools": ["Docker", "Kubernetes", "AWS", "CI/CD"]
    }
  },
  "activity": {
    "total_events": 280,
    "commits": 150,
    "pull_requests": 45,
    "issues": 35,
    "activity_streak": 12,
    "active_days": 65
  },
  "scores": {
    "code_quality_score": 78.5,
    "activity_score": 85.2,
    "impact_score": 72.8,
    "overall_score": 79.8
  }
}
```

### 3.2 StackOverflow Integration

**File:** `/utils/stackoverflow_scanner.py` (500+ lines)

#### 3.2.1 Stack Exchange API 2.3

**Base URL:** `https://api.stackexchange.com/2.3`

**Authentication:**
```python
params = {
    'site': 'stackoverflow',
    'key': STACKOVERFLOW_API_KEY  # Optional, increases quota
}
```

**Rate Limits:**
- **With API Key:** 10,000 requests/day
- **Without API Key:** 300 requests/day
- **Throttle:** 1 request/second

**Environment Variable:**
```bash
STACKOVERFLOW_API_KEY=your_stack_exchange_key_here  # Optional
```

#### 3.2.2 API Endpoints Used

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `GET /users/{id}` | User profile | reputation, badges, questions, answers |
| `GET /users?inname={name}` | Search by name | List of matching users |
| `GET /users/{id}/tags` | Top tags | Tags with score, count |
| `GET /users/{id}/answers` | User answers | Answer stats, acceptance rate |
| `GET /users/{id}/questions` | User questions | Question stats, views |

#### 3.2.3 StackOverflowScanner Class

**Key Methods:**

```python
class StackOverflowScanner:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with optional API key for higher rate limits"""
        
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch user profile by numeric ID.
        
        Returns:
            {
                'user_id': 123456,
                'display_name': 'John Doe',
                'reputation': 15000,
                'badge_counts': {'gold': 5, 'silver': 20, 'bronze': 50},
                'question_count': 30,
                'answer_count': 150,
                'profile_image': 'url',
                'link': 'stackoverflow_profile_url'
            }
        """
        
    def search_user_by_name(self, display_name: str) -> List[Dict[str, Any]]:
        """
        Search users by display name (may return multiple matches).
        
        Returns: List of users matching the name
        """
        
    def get_user_tags(self, user_id: int, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Get user's top expertise tags.
        
        Returns:
            [
                {'tag_name': 'python', 'count': 50, 'score': 500},
                {'tag_name': 'javascript', 'count': 30, 'score': 300}
            ]
        """
        
    def get_user_answers(self, user_id: int, max_answers: int = 100) -> Dict[str, Any]:
        """
        Get user's answer statistics.
        
        Returns:
            {
                'total_answers': 150,
                'accepted_answers': 80,
                'total_score': 1500,
                'total_views': 50000,
                'acceptance_rate': 53.3
            }
        """
        
    def get_user_questions(self, user_id: int, max_questions: int = 100) -> Dict[str, Any]:
        """
        Get user's question statistics.
        
        Returns:
            {
                'total_questions': 30,
                'total_score': 200,
                'total_views': 15000,
                'answered_questions': 25
            }
        """
        
    def calculate_scores(self, profile: Dict, tags: List[Dict], 
                        answers_stats: Dict, questions_stats: Dict) -> Dict[str, float]:
        """
        Calculate StackOverflow scores (0-100 scale).
        
        Scoring Formula:
        - Expertise (40%): Reputation, badges, top tags
        - Helpfulness (35%): Accepted answers, answer score
        - Community (25%): Question quality, views, engagement
        
        Returns:
            {
                'expertise_score': 75.0,
                'helpfulness_score': 80.5,
                'community_score': 70.2,
                'overall_score': 75.9
            }
        """
```

#### 3.2.4 Reputation Scoring

**Logarithmic Scale:**

| Reputation Range | Score |
|-----------------|-------|
| 0 - 100 | 20 |
| 100 - 500 | 40 |
| 500 - 1,000 | 50 |
| 1,000 - 5,000 | 70 |
| 5,000 - 10,000 | 85 |
| 10,000+ | 90-100 (capped at 100) |

**Badge Scoring:**
- Gold badge: 20 points each
- Silver badge: 5 points each
- Bronze badge: 1 point each
- Capped at 100 points

#### 3.2.5 Example Response

```json
{
  "profile": {
    "user_id": 123456,
    "display_name": "John Doe",
    "reputation": 15000,
    "badge_counts": {
      "gold": 5,
      "silver": 20,
      "bronze": 50
    },
    "question_count": 30,
    "answer_count": 150
  },
  "tags": [
    {"tag_name": "python", "count": 50, "score": 500},
    {"tag_name": "javascript", "count": 30, "score": 300},
    {"tag_name": "react", "count": 25, "score": 250}
  ],
  "answers": {
    "total_answers": 150,
    "accepted_answers": 80,
    "total_score": 1500,
    "acceptance_rate": 53.3
  },
  "questions": {
    "total_questions": 30,
    "total_score": 200,
    "answered_questions": 25
  },
  "scores": {
    "expertise_score": 78.5,
    "helpfulness_score": 82.0,
    "community_score": 74.5,
    "overall_score": 78.7
  }
}
```

---

## 4. Scoring System

### 4.1 Overall Visibility Score

**Formula:**
```
Overall Score = (GitHub Score × 0.60) + (StackOverflow Score × 0.40)
```

**Rationale:**
- GitHub shows coding activity and project contributions (60% weight)
- StackOverflow shows expertise and community engagement (40% weight)
- LinkedIn not yet integrated (would adjust weights to 40-30-30)

**Range:** 0-100

**Performance Levels:**
- **Excellent:** 85-100 (Top 10% of developers)
- **Good:** 70-84 (Above average)
- **Average:** 55-69 (Typical developer)
- **Needs Improvement:** 0-54 (Below average)

### 4.2 GitHub Scoring

**Overall GitHub Score = Code Quality (30%) + Activity (40%) + Impact (30%)**

#### 4.2.1 Code Quality Score (30%)

**Factors:**
- Average stars per repository
- Code organization (multiple languages, topics)
- Repository freshness (recent updates)
- Profile completeness (bio, location, README)

**Calculation:**
```python
avg_stars_per_repo = total_stars / max(total_repos, 1)
stars_score = min(avg_stars_per_repo * 10, 100)  # 10 stars/repo = 100 points

follower_score = min(followers / 10, 50)  # 1 follower = 0.1 points, max 50

quality_score = (stars_score * 0.6) + (follower_score * 0.4)
```

#### 4.2.2 Activity Score (40%)

**Factors:**
- Recent commits (last 90 days)
- Pull requests opened/reviewed
- Issues created/commented
- Activity streak (consecutive days)
- Active days in last 90 days

**Calculation:**
```python
commits_score = min(commits / 5, 40)  # 1 commit = 0.2 points, max 40
pr_score = min(pull_requests / 2, 30)  # 1 PR = 0.5 points, max 30
issues_score = min(issues / 2, 20)  # 1 issue = 0.5 points, max 20
streak_score = min(activity_streak * 2, 10)  # 1 day streak = 2 points, max 10

activity_score = commits_score + pr_score + issues_score + streak_score
```

#### 4.2.3 Impact Score (30%)

**Factors:**
- Total stars across all repositories
- Total forks (code reuse)
- Total followers
- Top repository stars

**Calculation:**
```python
stars_impact = min(total_stars / 10, 50)  # 10 stars = 1 point, max 50
forks_impact = min(total_forks / 5, 30)  # 5 forks = 1 point, max 30
followers_impact = min(followers / 5, 20)  # 5 followers = 1 point, max 20

impact_score = stars_impact + forks_impact + followers_impact
```

### 4.3 StackOverflow Scoring

**Overall SO Score = Expertise (40%) + Helpfulness (35%) + Community (25%)**

#### 4.3.1 Expertise Score (40%)

**Factors:**
- Reputation points (logarithmic scale)
- Badge counts (gold, silver, bronze)
- Top tags (number and scores)

**Calculation:**
```python
# Reputation scoring (logarithmic)
if reputation < 100: rep_score = 20
elif reputation < 500: rep_score = 40
elif reputation < 1000: rep_score = 50
elif reputation < 5000: rep_score = 70
elif reputation < 10000: rep_score = 85
else: rep_score = min(85 + (reputation - 10000) / 1000, 100)

# Badge scoring
badge_score = min(
    (gold_badges * 20) + (silver_badges * 5) + (bronze_badges * 1),
    100
)

expertise_score = (rep_score * 0.6) + (badge_score * 0.4)
```

#### 4.3.2 Helpfulness Score (35%)

**Factors:**
- Answer acceptance rate
- Total answer score
- Positive feedback ratio

**Calculation:**
```python
acceptance_rate = (accepted_answers / total_answers) * 100

# Acceptance rate scoring
if acceptance_rate >= 60: acceptance_score = 100
elif acceptance_rate >= 50: acceptance_score = 85
elif acceptance_rate >= 40: acceptance_score = 70
elif acceptance_rate >= 30: acceptance_score = 50
else: acceptance_score = acceptance_rate

# Answer score
answer_score = min(total_answer_score / 10, 100)  # 10 score = 1 point

helpfulness_score = (acceptance_score * 0.7) + (answer_score * 0.3)
```

#### 4.3.3 Community Score (25%)

**Factors:**
- Question quality (score, views)
- Engagement (comments, edits)
- Consistency (account age, activity)

**Calculation:**
```python
question_quality = min(total_question_score / 5, 50)  # 5 score = 1 point
question_views = min(total_views / 1000, 50)  # 1000 views = 1 point

community_score = (question_quality * 0.5) + (question_views * 0.5)
```

### 4.4 Four Dimension Scores

**Calculated from combined GitHub + StackOverflow data:**

#### 4.4.1 Visibility Score

**Definition:** How discoverable you are online

**Factors:**
- GitHub followers
- Total stars on repositories
- StackOverflow reputation
- Profile completeness

**Weight Distribution:**
- GitHub followers: 30%
- Repository stars: 30%
- SO reputation: 30%
- Profile completeness: 10%

#### 4.4.2 Activity Score

**Definition:** How actively you contribute

**Factors:**
- GitHub commits, PRs, issues (last 90 days)
- Activity streak
- StackOverflow answers/questions
- Recent activity

**Weight Distribution:**
- GitHub activity: 60%
- SO contributions: 30%
- Consistency: 10%

#### 4.4.3 Impact Score

**Definition:** How much influence you have

**Factors:**
- Repository stars and forks
- Followers
- StackOverflow answer score
- Accepted answers

**Weight Distribution:**
- GitHub impact: 50%
- SO helpfulness: 40%
- Follower base: 10%

#### 4.4.4 Expertise Score

**Definition:** Your technical skill level

**Factors:**
- Code quality metrics
- StackOverflow badges and reputation
- Top tags
- Skills extracted from repositories

**Weight Distribution:**
- SO expertise: 50%
- GitHub code quality: 30%
- Skills diversity: 20%

---

## 5. Database Schema

### 5.1 Primary Table: footprint_scans

**File:** `/backend/migrations/create_footprint_tables.py`

**Table Structure:**

```sql
CREATE TABLE footprint_scans (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Scan Metadata
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    platforms_scanned TEXT[] NOT NULL,  -- ['github', 'stackoverflow']
    
    -- Platform Data (JSONB for flexibility)
    github_data JSONB,
    stackoverflow_data JSONB,
    
    -- Scores (0-100 scale)
    overall_score FLOAT CHECK (overall_score >= 0 AND overall_score <= 100),
    github_score FLOAT CHECK (github_score >= 0 AND github_score <= 100),
    stackoverflow_score FLOAT CHECK (stackoverflow_score >= 0 AND stackoverflow_score <= 100),
    
    -- Dimension Scores (0-100 scale)
    visibility_score FLOAT CHECK (visibility_score >= 0 AND visibility_score <= 100),
    activity_score FLOAT CHECK (activity_score >= 0 AND activity_score <= 100),
    impact_score FLOAT CHECK (impact_score >= 0 AND impact_score <= 100),
    expertise_score FLOAT CHECK (expertise_score >= 0 AND expertise_score <= 100),
    
    -- Identifiers for re-scanning
    github_username TEXT,
    stackoverflow_user_id TEXT,
    
    -- Analysis Results (JSONB)
    privacy_report JSONB,
    recommendations JSONB,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**

```sql
-- Performance indexes
CREATE INDEX idx_footprint_user_id ON footprint_scans(user_id);
CREATE INDEX idx_footprint_scanned_at ON footprint_scans(scanned_at DESC);
CREATE INDEX idx_footprint_github_username ON footprint_scans(github_username);
CREATE INDEX idx_footprint_stackoverflow_id ON footprint_scans(stackoverflow_user_id);
CREATE INDEX idx_footprint_visibility ON footprint_scans(overall_score DESC);

-- JSONB index for fast queries
CREATE INDEX idx_footprint_platforms_gin ON footprint_scans USING GIN(platforms_scanned);
```

### 5.2 JSONB Field Structures

#### 5.2.1 github_data

```json
{
  "profile": {
    "login": "username",
    "name": "Full Name",
    "bio": "Developer bio",
    "location": "City, Country",
    "public_repos": 50,
    "followers": 100,
    "following": 50,
    "created_at": "2020-01-01T00:00:00Z",
    "profile_readme": "# My Profile\n..."
  },
  "repositories": {
    "total_repos": 50,
    "total_stars": 500,
    "total_forks": 100,
    "languages": {
      "Python": 125000,
      "JavaScript": 85000
    },
    "skills": {
      "frameworks": ["React", "Django"],
      "databases": ["PostgreSQL", "MongoDB"],
      "tools": ["Docker", "Kubernetes"]
    },
    "top_repositories": [
      {
        "name": "awesome-project",
        "description": "An awesome project",
        "stars": 150,
        "forks": 30,
        "language": "Python"
      }
    ]
  },
  "activity": {
    "total_events": 280,
    "commits": 150,
    "pull_requests": 45,
    "issues": 35,
    "activity_streak": 12,
    "active_days": 65
  },
  "scores": {
    "code_quality_score": 78.5,
    "activity_score": 85.2,
    "impact_score": 72.8,
    "overall_score": 79.8
  }
}
```

#### 5.2.2 stackoverflow_data

```json
{
  "profile": {
    "user_id": 123456,
    "display_name": "John Doe",
    "reputation": 15000,
    "badge_counts": {
      "gold": 5,
      "silver": 20,
      "bronze": 50
    },
    "question_count": 30,
    "answer_count": 150
  },
  "tags": [
    {"tag_name": "python", "count": 50, "score": 500}
  ],
  "answers": {
    "total_answers": 150,
    "accepted_answers": 80,
    "acceptance_rate": 53.3
  },
  "questions": {
    "total_questions": 30,
    "total_score": 200
  },
  "scores": {
    "expertise_score": 78.5,
    "helpfulness_score": 82.0,
    "community_score": 74.5,
    "overall_score": 78.7
  }
}
```

#### 5.2.3 privacy_report

```json
{
  "email_exposed": false,
  "phone_exposed": false,
  "location_exposed": true,
  "risks": [
    {
      "category": "Personal Information",
      "risk_level": "medium",
      "description": "Location is publicly visible",
      "recommendation": "Consider removing location if not needed"
    }
  ],
  "overall_risk": "low",
  "timestamp": "2025-11-06T10:00:00Z"
}
```

#### 5.2.4 recommendations

```json
{
  "profile_recommendations": [
    {
      "platform": "GitHub",
      "priority": "high",
      "title": "Add Profile README",
      "description": "Create a username/username repository with README.md",
      "action_items": [
        "Create repository with your username",
        "Add README.md with introduction",
        "Include skills, projects, contact"
      ]
    }
  ],
  "career_insights": [
    {
      "insight_type": "Growth Potential",
      "description": "Strong backend skills, consider frontend",
      "recommendations": [
        "Learn React or Vue.js",
        "Build full-stack projects"
      ]
    }
  ],
  "skill_gaps": ["React", "Docker", "AWS"],
  "generated_at": "2025-11-06T10:00:00Z",
  "ai_generated": true
}
```

---

## 6. Backend API Reference

**Base URL:** `http://localhost:8000/api/v1/footprint`

**Authentication:** JWT Bearer Token (all endpoints protected)

### 6.1 POST /scan

**Description:** Initiate a new footprint scan

**Request:**

```json
{
  "github_username": "johndoe",
  "stackoverflow_user_id": "123456",  // Optional
  "stackoverflow_display_name": "John Doe",  // Alternative to ID
  "include_privacy_analysis": true  // Optional, default false
}
```

**Response (200 OK):**

```json
{
  "scan_id": 42,
  "scanned_at": "2025-11-06T10:30:00Z",
  "platforms_scanned": ["github", "stackoverflow"],
  "github_analysis": { /* GitHub data */ },
  "stackoverflow_analysis": { /* SO data */ },
  "overall_score": 78.5,
  "github_score": 79.8,
  "stackoverflow_score": 76.5,
  "visibility_score": 75.2,
  "activity_score": 82.5,
  "impact_score": 76.8,
  "expertise_score": 79.3,
  "visibility_level": "high",
  "performance_level": "good",
  "privacy_report": { /* Privacy data */ },
  "message": "Footprint scan completed successfully"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid input (missing github_username)
- `401 Unauthorized`: Invalid or missing JWT token
- `404 Not Found`: GitHub user not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: API failure or database error

### 6.2 GET /recommendations/{scan_id}

**Description:** Get AI-powered recommendations for a scan

**Path Parameters:**
- `scan_id` (integer): Scan ID

**Response (200 OK):**

```json
{
  "scan_id": 42,
  "profile_recommendations": [
    {
      "platform": "GitHub",
      "priority": "high",
      "title": "Enhance Profile README",
      "description": "Your README is basic, add more details",
      "action_items": [
        "Add skills section with badges",
        "Include top projects with links",
        "Add contact information"
      ]
    }
  ],
  "career_insights": [
    {
      "insight_type": "Skill Development",
      "description": "Focus on cloud technologies",
      "recommendations": [
        "Learn AWS or Azure",
        "Get cloud certification",
        "Build cloud-native projects"
      ]
    }
  ],
  "skill_gaps": ["Docker", "Kubernetes", "AWS", "CI/CD", "Microservices"],
  "generated_at": "2025-11-06T10:35:00Z",
  "ai_generated": true
}
```

### 6.3 GET /history

**Description:** Get user's scan history with pagination

**Query Parameters:**
- `limit` (integer, optional): Number of scans (default 10, max 50)
- `skip` (integer, optional): Number of scans to skip (default 0)

**Response (200 OK):**

```json
{
  "scans": [
    {
      "scan_id": 42,
      "scanned_at": "2025-11-06T10:30:00Z",
      "platforms_scanned": ["github", "stackoverflow"],
      "overall_score": 78.5,
      "visibility_level": "high"
    }
  ],
  "total": 5,
  "limit": 10,
  "skip": 0
}
```

### 6.4 GET /compare/{scan_id_1}/{scan_id_2}

**Description:** Compare two scans to track progress

**Path Parameters:**
- `scan_id_1` (integer): First scan ID (older)
- `scan_id_2` (integer): Second scan ID (newer)

**Response (200 OK):**

```json
{
  "scan_1": {
    "scan_id": 40,
    "scanned_at": "2025-11-01T10:00:00Z",
    "overall_score": 75.0
  },
  "scan_2": {
    "scan_id": 42,
    "scanned_at": "2025-11-06T10:30:00Z",
    "overall_score": 78.5
  },
  "changes": {
    "overall_score_change": 3.5,
    "visibility_change": 2.5,
    "activity_change": 5.0,
    "impact_change": 1.5,
    "expertise_change": 4.0
  },
  "improvement_percentage": 4.67
}
```

### 6.5 GET /{scan_id}

**Description:** Get full details of a specific scan

**Path Parameters:**
- `scan_id` (integer): Scan ID

**Response (200 OK):**

```json
{
  "scan_id": 42,
  "scanned_at": "2025-11-06T10:30:00Z",
  "platforms_scanned": ["github", "stackoverflow"],
  "github_analysis": { /* Complete GitHub data */ },
  "stackoverflow_analysis": { /* Complete SO data */ },
  "overall_score": 78.5,
  "dimension_scores": {
    "visibility": 75.2,
    "activity": 82.5,
    "impact": 76.8,
    "expertise": 79.3
  },
  "privacy_report": { /* Privacy analysis */ },
  "recommendations": { /* AI recommendations */ }
}
```

---

**End of Part 1**

**Continue to [FOOTPRINT_MODULE_PART2.md](./FOOTPRINT_MODULE_PART2.md) for:**
- AI Recommendations System (Groq Integration)
- Utility Deep Dives (GitHub Analyzer, StackOverflow Scanner)
- Frontend Components
- Troubleshooting
