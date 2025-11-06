# UtopiaHire Database Documentation - Part 4
## Digital Footprint Scanner Tables

> **Generated:** November 6, 2025  
> **Version:** 1.0.0  
> **Database:** PostgreSQL 14+

---

## Table of Contents (Part 4)

1. [Footprint Module Overview](#footprint-module-overview)
2. [Footprint Scans Table](#footprint-scans-table)
3. [JSONB Data Structures](#jsonb-data-structures)
4. [Scoring Algorithms](#scoring-algorithms)
5. [Privacy & Security](#privacy--security)

---

## 1. Footprint Module Overview

### Purpose & Architecture

The **Digital Footprint Scanner** analyzes users' online professional presence across multiple platforms:
- ✅ **GitHub**: Repository analysis, contribution activity, code quality
- ✅ **LinkedIn**: Profile completeness, network strength, engagement
- ✅ **StackOverflow**: Reputation, expertise areas, community contributions
- ✅ **Comprehensive Scoring**: Multi-dimensional evaluation (visibility, activity, impact, expertise)
- ✅ **Privacy Analysis**: Identifies potential privacy risks
- ✅ **Career Insights**: Actionable recommendations for improvement

### Module Architecture

```
┌────────────────────────────────────────────────────┐
│         DIGITAL FOOTPRINT SCANNER                   │
├────────────────────────────────────────────────────┤
│                                                     │
│   User Initiates Scan                              │
│           │                                         │
│           ▼                                         │
│   ┌───────────────┐                                │
│   │ Input Handles │                                │
│   │ - GitHub      │                                │
│   │ - LinkedIn    │                                │
│   │ - StackOverflow│                               │
│   └───────┬───────┘                                │
│           │                                         │
│           ▼                                         │
│   ┌───────────────┐                                │
│   │   API Calls   │                                │
│   │ - GitHub API  │                                │
│   │ - LinkedIn    │                                │
│   │ - Stack API   │                                │
│   └───────┬───────┘                                │
│           │                                         │
│           ▼                                         │
│   ┌───────────────┐                                │
│   │Data Aggregation│                               │
│   │  & Analysis   │                                │
│   └───────┬───────┘                                │
│           │                                         │
│           ▼                                         │
│   ┌───────────────┐                                │
│   │Score Calculation│                              │
│   │ - Platform    │                                │
│   │ - Overall     │                                │
│   │ - Dimensions  │                                │
│   └───────┬───────┘                                │
│           │                                         │
│           ▼                                         │
│   ┌───────────────┐                                │
│   │footprint_scans│                                │
│   │  (Database)   │                                │
│   └───────────────┘                                │
│                                                     │
└────────────────────────────────────────────────────┘
```

### Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Visibility** | 25% | How easily you're found online |
| **Activity** | 30% | Recent contributions & engagement |
| **Impact** | 25% | Influence & reach of your work |
| **Expertise** | 20% | Demonstrated knowledge & skills |

**Overall Score Calculation:**
```
Overall = (Visibility × 0.25) + (Activity × 0.30) + (Impact × 0.25) + (Expertise × 0.20)
```

---

## 2. Footprint Scans Table

**Purpose:** Store comprehensive digital footprint analysis results

**Schema:**
```sql
CREATE TABLE IF NOT EXISTS footprint_scans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    scan_type VARCHAR(50) DEFAULT 'comprehensive',
    platforms_scanned TEXT[],
    
    -- GitHub Data
    github_username VARCHAR(255),
    github_data JSONB,
    github_score INTEGER CHECK (github_score >= 0 AND github_score <= 100),
    
    -- StackOverflow Data
    stackoverflow_user_id VARCHAR(255),
    stackoverflow_name VARCHAR(255),
    stackoverflow_data JSONB,
    stackoverflow_score INTEGER CHECK (stackoverflow_score >= 0 AND stackoverflow_score <= 100),
    
    -- LinkedIn Data
    linkedin_url TEXT,
    linkedin_data JSONB,
    linkedin_score INTEGER CHECK (linkedin_score >= 0 AND linkedin_score <= 100),
    
    -- Aggregate Scores
    overall_visibility_score INTEGER CHECK (overall_visibility_score >= 0 AND overall_visibility_score <= 100),
    professional_score INTEGER CHECK (professional_score >= 0 AND professional_score <= 100),
    visibility_score INTEGER CHECK (visibility_score >= 0 AND visibility_score <= 100),
    activity_score INTEGER CHECK (activity_score >= 0 AND activity_score <= 100),
    impact_score INTEGER CHECK (impact_score >= 0 AND impact_score <= 100),
    expertise_score INTEGER CHECK (expertise_score >= 0 AND expertise_score <= 100),
    
    -- Analysis Results
    privacy_report JSONB,
    privacy_risk_level VARCHAR(20) DEFAULT 'low',
    recommendations JSONB,
    career_insights JSONB,
    
    -- Timestamps
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Scan identifier |
| `user_id` | INTEGER | FK → users(id), CASCADE | Scan owner |
| `scan_type` | VARCHAR(50) | DEFAULT 'comprehensive' | Type of scan performed |
| `platforms_scanned` | TEXT[] | NULL | Array of scanned platforms |
| **GitHub** ||||
| `github_username` | VARCHAR(255) | NULL | GitHub username |
| `github_data` | JSONB | NULL | Complete GitHub profile data |
| `github_score` | INTEGER | 0-100 CHECK | GitHub presence score |
| **StackOverflow** ||||
| `stackoverflow_user_id` | VARCHAR(255) | NULL | StackOverflow user ID |
| `stackoverflow_name` | VARCHAR(255) | NULL | StackOverflow display name |
| `stackoverflow_data` | JSONB | NULL | Complete SO profile data |
| `stackoverflow_score` | INTEGER | 0-100 CHECK | StackOverflow presence score |
| **LinkedIn** ||||
| `linkedin_url` | TEXT | NULL | LinkedIn profile URL |
| `linkedin_data` | JSONB | NULL | LinkedIn profile data |
| `linkedin_score` | INTEGER | 0-100 CHECK | LinkedIn presence score |
| **Aggregate Scores** ||||
| `overall_visibility_score` | INTEGER | 0-100 CHECK | Combined visibility |
| `professional_score` | INTEGER | 0-100 CHECK | Overall professionalism |
| `visibility_score` | INTEGER | 0-100 CHECK | Online discoverability |
| `activity_score` | INTEGER | 0-100 CHECK | Recent engagement |
| `impact_score` | INTEGER | 0-100 CHECK | Influence & reach |
| `expertise_score` | INTEGER | 0-100 CHECK | Demonstrated knowledge |
| **Analysis** ||||
| `privacy_report` | JSONB | NULL | Privacy risk assessment |
| `privacy_risk_level` | VARCHAR(20) | DEFAULT 'low' | low/medium/high/critical |
| `recommendations` | JSONB | NULL | Improvement suggestions |
| `career_insights` | JSONB | NULL | Career advice & opportunities |
| **Timestamps** ||||
| `scanned_at` | TIMESTAMP | AUTO | Scan execution time |
| `created_at` | TIMESTAMP | AUTO | Record creation time |

**Scan Types:**
- **comprehensive** - Full analysis of all available platforms
- **quick** - Basic profile check
- **privacy_focused** - Emphasis on privacy & security
- **career_optimization** - Focus on career development
- **comparison** - Benchmark against peers/industry

**Indexes:**
```sql
CREATE INDEX idx_footprint_user_id ON footprint_scans(user_id);
CREATE INDEX idx_footprint_scanned_at ON footprint_scans(scanned_at DESC);
CREATE INDEX idx_footprint_github_username ON footprint_scans(github_username);
CREATE INDEX idx_footprint_stackoverflow_id ON footprint_scans(stackoverflow_user_id);
CREATE INDEX idx_footprint_visibility ON footprint_scans(overall_visibility_score DESC);
CREATE INDEX idx_footprint_platforms ON footprint_scans USING GIN(platforms_scanned);
```

---

## 3. JSONB Data Structures

### 3.1 GitHub Data Structure

```json
{
  "profile": {
    "username": "johndoe",
    "name": "John Doe",
    "bio": "Senior Backend Engineer | Python & Go enthusiast",
    "avatar_url": "https://avatars.githubusercontent.com/u/12345",
    "location": "Tunis, Tunisia",
    "email": "john@example.com",
    "blog": "https://johndoe.dev",
    "twitter_username": "johndoe_dev",
    "company": "TechCorp",
    "hireable": true,
    "public_repos": 42,
    "public_gists": 15,
    "followers": 385,
    "following": 125,
    "account_created": "2018-05-12",
    "account_age_days": 2735
  },
  "activity": {
    "total_commits_last_year": 1245,
    "contribution_streak_days": 87,
    "longest_streak_days": 156,
    "commits_by_month": {
      "2025-11": 98,
      "2025-10": 112,
      "2025-09": 95
    },
    "pull_requests_merged": 67,
    "issues_opened": 34,
    "code_reviews": 89
  },
  "repositories": {
    "total_stars": 2340,
    "total_forks": 456,
    "total_watchers": 189,
    "top_repositories": [
      {
        "name": "microservices-framework",
        "description": "Lightweight microservices framework in Python",
        "stars": 1200,
        "forks": 234,
        "language": "Python",
        "url": "https://github.com/johndoe/microservices-framework",
        "topics": ["microservices", "python", "fastapi", "docker"],
        "last_updated": "2025-11-03",
        "is_fork": false,
        "has_wiki": true,
        "has_issues": true,
        "open_issues_count": 12
      },
      {
        "name": "auth-service",
        "description": "OAuth2 authentication service",
        "stars": 678,
        "forks": 123,
        "language": "Go",
        "url": "https://github.com/johndoe/auth-service",
        "topics": ["oauth2", "authentication", "go", "jwt"],
        "last_updated": "2025-10-28"
      }
    ]
  },
  "languages": {
    "Python": 45.2,
    "Go": 28.5,
    "JavaScript": 15.8,
    "Shell": 6.3,
    "Dockerfile": 4.2
  },
  "contributions": {
    "total_contributions": 1567,
    "contributions_last_year": 1245,
    "most_active_repos": [
      "microservices-framework",
      "auth-service",
      "devops-tools"
    ]
  },
  "code_quality_indicators": {
    "documentation_score": 85,
    "test_coverage_estimate": 78,
    "ci_cd_usage": true,
    "has_readme": 95,
    "has_license": 88,
    "average_repo_size_kb": 1250
  },
  "community_engagement": {
    "starred_repositories": 456,
    "organizations": ["opensource-tunisia", "techcorp"],
    "sponsor_count": 12,
    "sponsoring_count": 5
  }
}
```

### 3.2 StackOverflow Data Structure

```json
{
  "profile": {
    "user_id": "12345678",
    "display_name": "John Doe",
    "reputation": 15234,
    "profile_image": "https://i.stack.imgur.com/abc123.jpg",
    "website_url": "https://johndoe.dev",
    "location": "Tunis, Tunisia",
    "about_me": "Senior Backend Engineer passionate about Python and distributed systems",
    "member_since": "2019-03-15",
    "last_access_date": "2025-11-06",
    "account_age_days": 2428
  },
  "reputation": {
    "total": 15234,
    "change_week": 125,
    "change_month": 487,
    "change_quarter": 1234,
    "change_year": 3456,
    "reputation_history": {
      "2025": 3456,
      "2024": 4567,
      "2023": 3890,
      "2022": 2321
    }
  },
  "badges": {
    "total": 78,
    "gold": 4,
    "silver": 23,
    "bronze": 51,
    "badge_list": [
      {
        "name": "Famous Question",
        "type": "gold",
        "description": "Asked a question with 10,000 views"
      },
      {
        "name": "Great Answer",
        "type": "gold",
        "description": "Answer score of 100 or more"
      }
    ]
  },
  "activity": {
    "questions_asked": 89,
    "answers_given": 234,
    "accepted_answers": 156,
    "acceptance_rate": 66.67,
    "total_votes_cast": 1234,
    "helpful_flags": 45,
    "posts_edited": 67
  },
  "engagement": {
    "question_views": 245678,
    "answer_views": 567890,
    "profile_views": 12345,
    "reached_people": 813568,
    "average_question_score": 8.5,
    "average_answer_score": 12.3
  },
  "expertise": {
    "top_tags": [
      {
        "tag": "python",
        "score": 4567,
        "post_count": 156,
        "percentile": 95
      },
      {
        "tag": "django",
        "score": 2345,
        "post_count": 89,
        "percentile": 88
      },
      {
        "tag": "postgresql",
        "score": 1234,
        "post_count": 67,
        "percentile": 82
      },
      {
        "tag": "docker",
        "score": 987,
        "post_count": 45,
        "percentile": 78
      }
    ],
    "tag_categories": {
      "languages": ["python", "javascript", "go"],
      "frameworks": ["django", "fastapi", "react"],
      "databases": ["postgresql", "mongodb", "redis"],
      "devops": ["docker", "kubernetes", "aws"]
    }
  },
  "quality_metrics": {
    "answer_acceptance_rate": 66.67,
    "upvote_ratio": 0.92,
    "helpful_percentage": 78.5,
    "avg_time_to_answer_minutes": 45,
    "consistency_score": 85
  }
}
```

### 3.3 LinkedIn Data Structure

```json
{
  "profile": {
    "name": "John Doe",
    "headline": "Senior Backend Engineer | Building scalable systems",
    "location": "Tunis, Tunisia",
    "profile_url": "https://linkedin.com/in/johndoe",
    "profile_image": "https://media.licdn.com/profile.jpg",
    "industry": "Information Technology",
    "current_position": "Senior Backend Engineer at TechCorp",
    "summary": "Experienced engineer with 7+ years building distributed systems..."
  },
  "experience": [
    {
      "title": "Senior Backend Engineer",
      "company": "TechCorp",
      "location": "Tunis, Tunisia",
      "start_date": "2020-01",
      "end_date": null,
      "is_current": true,
      "duration_months": 58,
      "description": "Leading backend architecture for microservices platform serving 1M+ users..."
    },
    {
      "title": "Backend Developer",
      "company": "StartupXYZ",
      "location": "Remote",
      "start_date": "2018-03",
      "end_date": "2019-12",
      "is_current": false,
      "duration_months": 22,
      "description": "Developed RESTful APIs and database schemas..."
    }
  ],
  "education": [
    {
      "institution": "University of Tunis",
      "degree": "Bachelor of Science",
      "field_of_study": "Computer Science",
      "start_year": 2014,
      "end_year": 2018,
      "grade": "3.8/4.0"
    }
  ],
  "skills": [
    {
      "name": "Python",
      "endorsements": 67,
      "proficiency": "expert"
    },
    {
      "name": "System Design",
      "endorsements": 45,
      "proficiency": "advanced"
    },
    {
      "name": "PostgreSQL",
      "endorsements": 52,
      "proficiency": "advanced"
    }
  ],
  "certifications": [
    {
      "name": "AWS Certified Solutions Architect",
      "issuer": "Amazon Web Services",
      "issue_date": "2023-06",
      "expiry_date": "2026-06",
      "credential_id": "AWS-SAA-12345"
    }
  ],
  "network": {
    "connections": 1245,
    "followers": 2340,
    "following": 456
  },
  "activity": {
    "posts_last_month": 12,
    "comments_last_month": 34,
    "shares_last_month": 8,
    "engagement_rate": 4.5,
    "profile_views_last_90_days": 234,
    "search_appearances_last_90_days": 456
  },
  "completeness": {
    "profile_strength": "All-Star",
    "profile_completeness": 95,
    "missing_sections": ["Volunteer Experience"],
    "recommendations_received": 8,
    "recommendations_given": 12
  }
}
```

### 3.4 Privacy Report Structure

```json
{
  "risk_level": "medium",
  "overall_risk_score": 45,
  "identified_risks": [
    {
      "category": "personal_information",
      "severity": "medium",
      "risk": "Email address publicly visible on GitHub",
      "platform": "GitHub",
      "recommendation": "Consider using GitHub's email privacy feature",
      "impact": "Increased spam, potential phishing attacks",
      "fix_url": "https://github.com/settings/emails"
    },
    {
      "category": "location_data",
      "severity": "low",
      "risk": "Precise location shared on LinkedIn",
      "platform": "LinkedIn",
      "recommendation": "Consider showing only city/region instead of full address",
      "impact": "Minor privacy concern",
      "fix_url": "https://linkedin.com/settings/privacy"
    },
    {
      "category": "professional_history",
      "severity": "low",
      "risk": "Complete employment history visible",
      "platform": "LinkedIn",
      "recommendation": "Review visibility settings for older positions",
      "impact": "Low - standard professional practice"
    }
  ],
  "visibility_analysis": {
    "github": {
      "public_repos": 42,
      "public_email": true,
      "public_location": true,
      "searchable": true
    },
    "linkedin": {
      "profile_visibility": "public",
      "connections_visible": true,
      "activity_broadcasts": true
    },
    "stackoverflow": {
      "profile_public": true,
      "real_name_used": true,
      "location_visible": true
    }
  },
  "sensitive_data_found": {
    "api_keys": false,
    "passwords": false,
    "personal_documents": false,
    "financial_info": false,
    "phone_numbers": false,
    "home_address": false
  },
  "recommendations": [
    "Enable GitHub email privacy",
    "Review LinkedIn connection visibility",
    "Set up Google Alerts for your name",
    "Regular audit of public information"
  ]
}
```

### 3.5 Recommendations Structure

```json
{
  "quick_wins": [
    {
      "action": "Update GitHub README files",
      "impact": "high",
      "effort": "low",
      "timeframe": "1-2 hours",
      "reason": "Improves project discoverability and professionalism",
      "priority": 1
    },
    {
      "action": "Add project descriptions",
      "impact": "medium",
      "effort": "low",
      "timeframe": "30 minutes",
      "reason": "Helps recruiters understand your work",
      "priority": 2
    }
  ],
  "platform_specific": {
    "github": [
      {
        "category": "activity",
        "recommendation": "Contribute to open source projects",
        "current_score": 65,
        "potential_score": 85,
        "improvement": 20,
        "steps": [
          "Find projects aligned with your skills",
          "Start with documentation contributions",
          "Submit 1-2 PRs per month"
        ]
      },
      {
        "category": "visibility",
        "recommendation": "Pin your best repositories",
        "current_score": 70,
        "potential_score": 90,
        "improvement": 20
      }
    ],
    "stackoverflow": [
      {
        "category": "expertise",
        "recommendation": "Answer questions in your expertise areas",
        "current_score": 78,
        "potential_score": 90,
        "improvement": 12,
        "focus_tags": ["python", "django", "postgresql"]
      }
    ],
    "linkedin": [
      {
        "category": "network",
        "recommendation": "Expand your network in target industries",
        "current_score": 60,
        "potential_score": 80,
        "improvement": 20
      },
      {
        "category": "content",
        "recommendation": "Share technical insights weekly",
        "current_score": 45,
        "potential_score": 75,
        "improvement": 30
      }
    ]
  },
  "skill_development": [
    {
      "skill": "System Design",
      "current_evidence": "Limited in portfolio",
      "recommendation": "Create system design blog posts or diagrams",
      "resources": [
        "System Design Primer (GitHub)",
        "Designing Data-Intensive Applications (Book)"
      ]
    }
  ],
  "career_positioning": {
    "current_perception": "Mid-level Backend Developer",
    "target_perception": "Senior Backend Engineer / Tech Lead",
    "gap_analysis": [
      "Limited evidence of leadership",
      "Need to showcase system design skills",
      "More thought leadership content needed"
    ],
    "action_plan": [
      "Write technical blog posts (2 per month)",
      "Lead an open source project",
      "Present at local meetups",
      "Mentor junior developers publicly"
    ]
  }
}
```

### 3.6 Career Insights Structure

```json
{
  "market_position": {
    "compared_to_peers": {
      "percentile": 78,
      "score": 82,
      "peer_group": "Backend Engineers, 5-7 years experience, Tunisia",
      "strengths": ["Technical skills", "Code quality"],
      "gaps": ["Thought leadership", "Community involvement"]
    },
    "industry_benchmarks": {
      "github_activity": "Above average",
      "stackoverflow_reputation": "Top 15%",
      "linkedin_engagement": "Below average"
    }
  },
  "opportunities": [
    {
      "type": "job_match",
      "title": "Senior Backend Engineer",
      "company": "GlobalTech",
      "match_score": 92,
      "reasoning": "Strong alignment with required skills (Python, PostgreSQL, Microservices)",
      "salary_range": "$80K-$120K",
      "url": "https://careers.globaltech.com/123"
    },
    {
      "type": "freelance",
      "platform": "Upwork",
      "opportunity": "Python consulting projects",
      "estimated_rate": "$50-75/hour",
      "demand": "high"
    }
  ],
  "growth_trajectory": {
    "current_level": "Mid-Senior Engineer",
    "next_level": "Senior/Lead Engineer",
    "time_to_next_level": "12-18 months",
    "required_improvements": [
      "Increase technical visibility (blog, talks)",
      "Demonstrate leadership skills",
      "Build stronger professional network"
    ]
  },
  "trending_skills_gap": [
    {
      "skill": "Kubernetes",
      "demand": "very high",
      "your_proficiency": "beginner",
      "market_requirement": "intermediate",
      "learning_priority": "high"
    },
    {
      "skill": "GraphQL",
      "demand": "high",
      "your_proficiency": "none",
      "market_requirement": "basic",
      "learning_priority": "medium"
    }
  ]
}
```

---

## 4. Scoring Algorithms

### 4.1 GitHub Score (0-100)

```python
def calculate_github_score(github_data):
    """
    Calculate GitHub presence score based on multiple factors
    """
    weights = {
        'activity': 0.30,    # Recent contributions
        'impact': 0.25,      # Stars, forks, followers
        'quality': 0.25,     # Code quality indicators
        'consistency': 0.20  # Regular contributions
    }
    
    # Activity Score (0-100)
    commits_last_year = github_data['activity']['total_commits_last_year']
    activity_score = min(100, (commits_last_year / 500) * 100)
    
    # Impact Score (0-100)
    total_stars = github_data['repositories']['total_stars']
    followers = github_data['profile']['followers']
    impact_score = min(100, ((total_stars / 1000) * 60) + ((followers / 500) * 40))
    
    # Quality Score (0-100)
    doc_score = github_data['code_quality_indicators']['documentation_score']
    test_coverage = github_data['code_quality_indicators']['test_coverage_estimate']
    quality_score = (doc_score + test_coverage) / 2
    
    # Consistency Score (0-100)
    streak = github_data['activity']['contribution_streak_days']
    consistency_score = min(100, (streak / 180) * 100)
    
    # Weighted average
    github_score = (
        activity_score * weights['activity'] +
        impact_score * weights['impact'] +
        quality_score * weights['quality'] +
        consistency_score * weights['consistency']
    )
    
    return round(github_score, 2)
```

### 4.2 StackOverflow Score (0-100)

```python
def calculate_stackoverflow_score(so_data):
    """
    Calculate StackOverflow presence score
    """
    weights = {
        'reputation': 0.40,  # Total reputation
        'expertise': 0.30,   # Tag scores & badges
        'engagement': 0.20,  # Activity & helpfulness
        'reach': 0.10        # Views & people reached
    }
    
    # Reputation Score (0-100)
    reputation = so_data['profile']['reputation']
    reputation_score = min(100, (reputation / 20000) * 100)
    
    # Expertise Score (0-100)
    gold_badges = so_data['badges']['gold']
    silver_badges = so_data['badges']['silver']
    top_tag_percentile = so_data['expertise']['top_tags'][0]['percentile']
    expertise_score = min(100, 
        (gold_badges * 10) + (silver_badges * 3) + top_tag_percentile * 0.5
    )
    
    # Engagement Score (0-100)
    answers = so_data['activity']['answers_given']
    acceptance_rate = so_data['activity']['acceptance_rate']
    engagement_score = min(100, (answers / 200) * 70 + acceptance_rate * 0.3)
    
    # Reach Score (0-100)
    reached_people = so_data['engagement']['reached_people']
    reach_score = min(100, (reached_people / 1000000) * 100)
    
    # Weighted average
    so_score = (
        reputation_score * weights['reputation'] +
        expertise_score * weights['expertise'] +
        engagement_score * weights['engagement'] +
        reach_score * weights['reach']
    )
    
    return round(so_score, 2)
```

### 4.3 Overall Score Calculation

```python
def calculate_overall_scores(github_score, stackoverflow_score, linkedin_score):
    """
    Calculate comprehensive digital footprint scores
    """
    # Platform weights (GitHub emphasized for developers)
    platform_weights = {
        'github': 0.45,
        'stackoverflow': 0.35,
        'linkedin': 0.20
    }
    
    # Overall visibility score
    overall_score = (
        github_score * platform_weights['github'] +
        stackoverflow_score * platform_weights['stackoverflow'] +
        linkedin_score * platform_weights['linkedin']
    )
    
    # Dimension scores
    visibility_score = calculate_visibility(github_score, stackoverflow_score, linkedin_score)
    activity_score = calculate_activity(github_score, stackoverflow_score)
    impact_score = calculate_impact(github_score, stackoverflow_score)
    expertise_score = calculate_expertise(stackoverflow_score, github_score)
    
    return {
        'overall': round(overall_score, 2),
        'visibility': round(visibility_score, 2),
        'activity': round(activity_score, 2),
        'impact': round(impact_score, 2),
        'expertise': round(expertise_score, 2)
    }
```

---

## 5. Privacy & Security

### Privacy Risk Levels

| Level | Score Range | Description | Action Required |
|-------|-------------|-------------|-----------------|
| **Low** | 0-30 | Minimal exposure | Monitor regularly |
| **Medium** | 31-60 | Some concerns | Review & optimize |
| **High** | 61-85 | Significant risks | Immediate action needed |
| **Critical** | 86-100 | Severe vulnerabilities | Urgent remediation |

### Example Queries

```sql
-- Perform footprint scan
INSERT INTO footprint_scans (
    user_id, scan_type, platforms_scanned,
    github_username, github_data, github_score,
    stackoverflow_user_id, stackoverflow_name, stackoverflow_data, stackoverflow_score,
    overall_visibility_score, professional_score,
    visibility_score, activity_score, impact_score, expertise_score,
    privacy_report, privacy_risk_level,
    recommendations, career_insights
)
VALUES (
    1, 'comprehensive', ARRAY['GitHub', 'StackOverflow'],
    'johndoe', '{"profile": {...}}'::jsonb, 82,
    '12345678', 'John Doe', '{"profile": {...}}'::jsonb, 78,
    80, 85,
    75, 85, 78, 80,
    '{"risk_level": "medium", ...}'::jsonb, 'medium',
    '{"quick_wins": [...]}'::jsonb, '{"market_position": {...}}'::jsonb
)
RETURNING id;

-- Get latest scan for user
SELECT *
FROM footprint_scans
WHERE user_id = 1
ORDER BY scanned_at DESC
LIMIT 1;

-- Compare scans over time
SELECT 
    scanned_at::date,
    overall_visibility_score,
    github_score,
    stackoverflow_score,
    activity_score
FROM footprint_scans
WHERE user_id = 1
ORDER BY scanned_at DESC
LIMIT 12;

-- Users with high-risk privacy issues
SELECT 
    fs.user_id,
    u.name,
    u.email,
    fs.privacy_risk_level,
    fs.privacy_report->>'overall_risk_score' as risk_score,
    fs.scanned_at
FROM footprint_scans fs
JOIN users u ON fs.user_id = u.id
WHERE fs.privacy_risk_level IN ('high', 'critical')
ORDER BY fs.scanned_at DESC;

-- Platform usage statistics
SELECT 
    UNNEST(platforms_scanned) as platform,
    COUNT(*) as scan_count,
    AVG(overall_visibility_score) as avg_visibility
FROM footprint_scans
WHERE scanned_at >= NOW() - INTERVAL '30 days'
GROUP BY platform
ORDER BY scan_count DESC;
```

---

**End of Part 4**

**Next:** [Part 5 - Indexes, Migrations & Best Practices](./DATABASE_DOCUMENTATION_PART5.md)

---

**Documentation Navigation:**
- [Part 1](./DATABASE_DOCUMENTATION_PART1.md): Overview, Architecture, Users, Resumes
- [Part 2](./DATABASE_DOCUMENTATION_PART2.md): Resume Enhancements, Skills, Jobs
- [Part 3](./DATABASE_DOCUMENTATION_PART3.md): Interview Module
- **Part 4** (Current): Footprint Scanner
- **Part 5**: Indexes, Migrations & Best Practices
