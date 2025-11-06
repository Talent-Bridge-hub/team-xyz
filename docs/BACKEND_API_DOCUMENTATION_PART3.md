# UtopiaHire Backend API Documentation - Part 3
## Interview & Footprint API Reference

> **Generated:** November 6, 2025  
> **Version:** 1.0.0  
> **Base URL:** `http://localhost:8000/api/v1`

---

## Table of Contents (Part 3)

9. [Interview API](#interview-api)
10. [Footprint API](#footprint-api)
11. [Rate Limiting](#rate-limiting)
12. [Webhooks](#webhooks)
13. [Best Practices](#best-practices)

---

## 9. Interview API

**Base Path:** `/api/v1/interview`  
**Tag:** `Interview Simulator`  
**Authentication:** Required for all endpoints

### Overview

The Interview Simulator provides AI-powered mock interviews with:
- **Question Bank:** 200+ curated technical and behavioral questions
- **AI Analysis:** Groq-powered answer evaluation using llama-3.3-70b-versatile
- **Multi-dimensional Scoring:** Relevance, completeness, clarity, technical accuracy, communication
- **Detailed Feedback:** Strengths, weaknesses, missing points, and suggestions
- **Session History:** Track progress over multiple interviews

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/start` | Start new interview session |
| GET | `/{session_id}/question` | Get next question |
| POST | `/answer` | Submit answer to question |
| POST | `/{session_id}/complete` | Complete interview session |
| GET | `/sessions` | List interview sessions |
| GET | `/{session_id}` | Get session details |
| GET | `/stats/overview` | Get user statistics |
| DELETE | `/{session_id}` | Delete interview session |

---

### POST /api/v1/interview/start

**Start a new interview session**

Creates an interview session with questions tailored to job role and difficulty.

**Authentication:** Required

**Request Body:**
```json
{
  "session_type": "technical",
  "job_role": "Backend Developer",
  "difficulty_level": "intermediate",
  "num_questions": 5,
  "resume_id": 1
}
```

**Fields:**
- `session_type` (required): Type of interview
  - `technical`: Technical/coding questions
  - `behavioral`: Behavioral/situational questions
  - `mixed`: Combination of both
- `job_role` (required): Target job role
- `difficulty_level` (required): Question difficulty
  - `junior`: Entry-level questions
  - `intermediate`: Mid-level questions
  - `senior`: Advanced questions
- `num_questions` (optional, default: 5, max: 10): Number of questions
- `resume_id` (optional): Resume for context-aware questions

**Response (200 OK):**
```json
{
  "session_id": 1,
  "session_type": "technical",
  "job_role": "Backend Developer",
  "difficulty_level": "intermediate",
  "total_questions": 5,
  "first_question": {
    "question_id": 42,
    "question_number": 1,
    "total_questions": 5,
    "question_text": "Explain the difference between REST and GraphQL APIs. When would you choose one over the other?",
    "question_type": "technical",
    "category": "API Design",
    "difficulty": "intermediate"
  },
  "message": "Interview session started! You have 5 questions to answer. Good luck!"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/interview/start" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "session_type": "technical",
    "job_role": "Backend Developer",
    "difficulty_level": "intermediate",
    "num_questions": 5
  }'
```

---

### POST /api/v1/interview/answer

**Submit answer to interview question**

Analyzes answer using Groq AI and provides detailed feedback.

**Authentication:** Required

**Request Body:**
```json
{
  "session_id": 1,
  "question_id": 42,
  "answer": "REST uses HTTP methods and multiple endpoints for different resources, while GraphQL uses a single endpoint with queries. REST is better for simple CRUD operations and caching, while GraphQL excels when you need flexible data fetching and want to avoid over-fetching or under-fetching data. I would choose REST for public APIs with well-defined resources, and GraphQL for complex internal APIs where clients need different data shapes.",
  "time_taken_seconds": 180
}
```

**Fields:**
- `session_id` (required): Active interview session ID
- `question_id` (required): Question being answered
- `answer` (required): User's answer text
- `time_taken_seconds` (optional): Time spent on answer

**Response (200 OK):**
```json
{
  "answer_id": 1,
  "question_number": 1,
  "question_text": "Explain the difference between REST and GraphQL APIs...",
  "your_answer": "REST uses HTTP methods and multiple endpoints...",
  "time_taken_seconds": 180,
  "scores": {
    "overall": 85,
    "relevance": 90,
    "completeness": 82,
    "clarity": 88,
    "technical_accuracy": 85,
    "communication": 80
  },
  "feedback": {
    "strengths": [
      "Clear comparison between REST and GraphQL",
      "Good use cases for each technology",
      "Mentions important concepts like over-fetching",
      "Well-structured answer"
    ],
    "weaknesses": [
      "Could mention versioning differences",
      "GraphQL subscription feature not discussed"
    ],
    "missing_points": [
      "Real-time capabilities with GraphQL subscriptions",
      "REST API versioning strategies",
      "Performance considerations for complex queries"
    ],
    "suggestions": [
      "Add example of when GraphQL subscriptions are useful",
      "Mention caching strategies for GraphQL",
      "Discuss N+1 query problem in GraphQL"
    ],
    "narrative": "Excellent answer demonstrating strong understanding of both REST and GraphQL. You clearly articulated the key differences and appropriate use cases. To elevate this to a perfect answer, consider discussing real-time capabilities (GraphQL subscriptions) and caching strategies. Your explanation was well-structured and easy to follow."
  },
  "sentiment": "positive",
  "has_more_questions": true
}
```

**Scoring Breakdown:**

| Score Type | Weight | Description |
|------------|--------|-------------|
| **Relevance** | 25% | How well answer addresses the question |
| **Completeness** | 25% | Coverage of key points |
| **Clarity** | 20% | Communication effectiveness |
| **Technical Accuracy** | 20% | Correctness of information |
| **Communication** | 10% | Professional presentation |

**Overall Score = Weighted average of all dimensions**

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/interview/answer" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": 1,
    "question_id": 42,
    "answer": "REST uses HTTP methods...",
    "time_taken_seconds": 180
  }'
```

---

### POST /api/v1/interview/{session_id}/complete

**Complete interview session and get final feedback**

Finalizes session and provides comprehensive performance report.

**Authentication:** Required

**Path Parameters:**
- `session_id`: Interview session to complete

**Response (200 OK):**
```json
{
  "session_id": 1,
  "completed": true,
  "questions_answered": 5,
  "total_time_seconds": 900,
  "average_scores": {
    "overall": 82.4,
    "relevance": 85.2,
    "completeness": 78.6,
    "clarity": 84.0,
    "technical_accuracy": 82.0,
    "communication": 79.0
  },
  "performance": "good",
  "ratings": {
    "technical": 4,
    "communication": 4,
    "confidence": 4
  },
  "feedback": {
    "strengths": [
      "Strong technical knowledge",
      "Clear communication style",
      "Good use of examples",
      "Well-structured answers"
    ],
    "areas_to_improve": [
      "Add more quantified examples",
      "Discuss trade-offs more explicitly",
      "Practice system design scenarios"
    ],
    "recommended_resources": [
      "System Design Interview – An Insider's Guide",
      "LeetCode for technical practice",
      "Mock interview practice sessions"
    ],
    "preparation_tips": "Focus on Backend Developer questions and practice the STAR method for behavioral questions.",
    "practice_recommendations": "Your performance was good. Continue practicing similar questions at intermediate level."
  },
  "message": "Interview completed! You answered 5 questions with an average score of 82.4%"
}
```

**Performance Levels:**

| Score Range | Performance | Description |
|-------------|-------------|-------------|
| 85-100 | Excellent | Outstanding performance |
| 75-84 | Good | Strong performance |
| 60-74 | Average | Acceptable performance |
| 0-59 | Needs Improvement | Requires practice |

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/interview/1/complete" \
  -H "Authorization: Bearer <token>"
```

---

### GET /api/v1/interview/sessions

**List user's interview sessions**

Returns paginated list of all interview sessions.

**Authentication:** Required

**Query Parameters:**
- `skip` (optional, default: 0): Number of records to skip
- `limit` (optional, default: 20): Max records to return
- `session_type` (optional): Filter by type (technical/behavioral/mixed)
- `session_status` (optional): Filter by status (in_progress/completed)

**Response (200 OK):**
```json
{
  "sessions": [
    {
      "id": 1,
      "session_type": "technical",
      "job_role": "Backend Developer",
      "difficulty_level": "intermediate",
      "total_questions": 5,
      "questions_answered": 5,
      "status": "completed",
      "average_score": 82.4,
      "duration_seconds": 900,
      "started_at": "2025-11-06T10:00:00Z",
      "completed_at": "2025-11-06T10:15:00Z",
      "overall_performance": "good",
      "technical_rating": 4,
      "communication_rating": 4,
      "confidence_rating": 4
    },
    {
      "id": 2,
      "session_type": "behavioral",
      "job_role": "Software Engineer",
      "difficulty_level": "junior",
      "total_questions": 5,
      "questions_answered": 3,
      "status": "in_progress",
      "average_score": null,
      "duration_seconds": null,
      "started_at": "2025-11-06T11:00:00Z",
      "completed_at": null,
      "overall_performance": null,
      "technical_rating": null,
      "communication_rating": null,
      "confidence_rating": null
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/interview/sessions?session_type=technical&session_status=completed" \
  -H "Authorization: Bearer <token>"
```

---

### GET /api/v1/interview/{session_id}

**Get detailed session information**

Returns complete session data with all questions and answers.

**Authentication:** Required

**Path Parameters:**
- `session_id`: Session to retrieve

**Response (200 OK):**
```json
{
  "session_id": 1,
  "session_type": "technical",
  "job_role": "Backend Developer",
  "difficulty_level": "intermediate",
  "total_questions": 5,
  "questions_answered": 5,
  "status": "completed",
  "average_scores": {
    "overall": 82.4,
    "relevance": 85.2,
    "completeness": 78.6,
    "clarity": 84.0,
    "technical_accuracy": 82.0,
    "communication": 79.0
  },
  "questions_and_answers": [
    {
      "question_number": 1,
      "question_text": "Explain the difference between REST and GraphQL APIs...",
      "question_type": "technical",
      "user_answer": "REST uses HTTP methods and multiple endpoints...",
      "time_taken_seconds": 180,
      "scores": {
        "overall": 85,
        "relevance": 90,
        "completeness": 82,
        "clarity": 88,
        "technical_accuracy": 85,
        "communication": 80
      },
      "feedback": {
        "strengths": ["Clear comparison", "Good use cases"],
        "weaknesses": ["Could mention versioning"],
        "missing_points": ["Real-time capabilities"],
        "suggestions": ["Add GraphQL subscription example"],
        "narrative": "Excellent answer demonstrating strong understanding..."
      },
      "sentiment": "positive"
    }
  ],
  "feedback": {
    "strengths": ["Strong technical knowledge", "Clear communication"],
    "areas_to_improve": ["Add more examples", "Discuss trade-offs"],
    "recommended_resources": ["System Design Interview book", "LeetCode"],
    "preparation_tips": "Focus on Backend Developer questions...",
    "practice_recommendations": "Continue practicing at intermediate level..."
  },
  "duration_seconds": 900,
  "started_at": "2025-11-06T10:00:00Z",
  "completed_at": "2025-11-06T10:15:00Z"
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/interview/1" \
  -H "Authorization: Bearer <token>"
```

---

### GET /api/v1/interview/stats/overview

**Get user's overall interview statistics**

Returns comprehensive statistics across all completed interviews.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "total_sessions": 10,
  "total_questions_answered": 50,
  "average_overall_score": 78.5,
  "average_session_duration_minutes": 18.5,
  "performance_distribution": {
    "excellent": 2,
    "good": 5,
    "average": 2,
    "needs_improvement": 1
  },
  "favorite_job_role": "Backend Developer",
  "improvement_trend": "improving"
}
```

**Improvement Trends:**
- `improving`: Recent scores higher than older scores
- `stable`: Consistent performance
- `declining`: Recent scores lower than older scores

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/interview/stats/overview" \
  -H "Authorization: Bearer <token>"
```

---

## 10. Footprint API

**Base Path:** `/api/v1/footprint`  
**Tag:** `Footprint Scanner`  
**Authentication:** Required for all endpoints

### Overview

The Digital Footprint Scanner analyzes your online presence across:
- **GitHub:** Profile, repositories, contributions, activity, skills
- **StackOverflow:** Reputation, answers, questions, badges, tags
- **Privacy Analysis:** Exposed information and risk assessment
- **AI Recommendations:** Groq-powered personalized suggestions using README analysis

### Key Features

1. **Multi-Platform Analysis**: Scan GitHub and StackOverflow simultaneously
2. **Comprehensive Scoring**: Overall visibility + 4 dimensional scores
3. **AI-Powered Insights**: Groq llama-3.3-70b-versatile analyzes your GitHub README
4. **Privacy Assessment**: Identifies exposed information and provides risk ratings
5. **Progress Tracking**: Compare scans over time to track improvements
6. **Career Recommendations**: Actionable suggestions based on your digital footprint

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/scan` | Scan digital footprint |
| GET | `/recommendations/{scan_id}` | Get AI recommendations |
| GET | `/history` | Get scan history |
| GET | `/compare/{scan_id_1}/{scan_id_2}` | Compare two scans |
| GET | `/{scan_id}` | Get scan details |

---

### POST /api/v1/footprint/scan

**Scan digital footprint across platforms**

Analyzes GitHub and/or StackOverflow profiles with comprehensive scoring.

**Authentication:** Required

**Request Body:**
```json
{
  "github_username": "johndoe",
  "stackoverflow_id": 12345,
  "stackoverflow_name": "John Doe",
  "include_privacy_analysis": true
}
```

**Fields:**
- `github_username` (optional): GitHub username to analyze
- `stackoverflow_id` (optional): StackOverflow user ID
- `stackoverflow_name` (optional): StackOverflow display name (alternative to ID)
- `include_privacy_analysis` (optional, default: false): Include privacy report

**Note:** At least one of `github_username` or `stackoverflow_id`/`stackoverflow_name` is required.

**Response (200 OK):**
```json
{
  "scan_id": 1,
  "user_id": 1,
  "github_analysis": {
    "profile": {
      "username": "johndoe",
      "name": "John Doe",
      "bio": "Full-stack developer passionate about open source",
      "location": "Tunisia",
      "company": "TechCorp",
      "email": "john@example.com",
      "followers": 150,
      "following": 80,
      "public_repos": 25,
      "public_gists": 5,
      "created_at": "2020-01-15T10:00:00Z",
      "profile_url": "https://github.com/johndoe",
      "avatar_url": "https://avatars.githubusercontent.com/u/12345"
    },
    "top_repositories": [
      {
        "name": "awesome-project",
        "description": "A full-stack web application",
        "language": "Python",
        "stars": 42,
        "forks": 8,
        "watchers": 10,
        "open_issues": 2,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2025-11-01T00:00:00Z",
        "url": "https://github.com/johndoe/awesome-project"
      }
    ],
    "total_stars": 120,
    "total_forks": 35,
    "languages": {
      "Python": 45.5,
      "JavaScript": 30.2,
      "TypeScript": 15.8,
      "HTML": 5.5,
      "CSS": 3.0
    },
    "language_bytes": {
      "Python": 145234,
      "JavaScript": 96543,
      "TypeScript": 50123
    },
    "skills": {
      "frameworks": ["Django", "FastAPI", "React", "Next.js"],
      "databases": ["PostgreSQL", "MongoDB", "Redis"],
      "tools": ["Docker", "Git", "CI/CD", "AWS"]
    },
    "activity": {
      "total_commits": 1250,
      "total_prs": 45,
      "total_issues": 30,
      "contributions_last_year": 850,
      "activity_streak": 30,
      "most_active_repo": "awesome-project"
    },
    "scores": {
      "overall_github_score": 82,
      "code_quality_score": 85,
      "activity_score": 80,
      "impact_score": 78,
      "visibility_score": 82
    },
    "visibility_level": "high",
    "analyzed_at": "2025-11-06T12:00:00Z"
  },
  "stackoverflow_analysis": {
    "profile": {
      "user_id": 12345,
      "display_name": "John Doe",
      "reputation": 5420,
      "badges": {
        "gold": 2,
        "silver": 15,
        "bronze": 45,
        "total": 62
      },
      "location": "Tunisia",
      "website_url": "https://johndoe.dev",
      "profile_url": "https://stackoverflow.com/users/12345/john-doe",
      "creation_date": "2021-03-15T00:00:00Z"
    },
    "top_tags": [
      {
        "name": "python",
        "count": 85,
        "score": 420
      },
      {
        "name": "django",
        "count": 42,
        "score": 280
      },
      {
        "name": "javascript",
        "count": 38,
        "score": 195
      }
    ],
    "activity": {
      "total_answers": 120,
      "accepted_answers": 48,
      "total_questions": 15,
      "answer_score": 1250,
      "question_score": 180,
      "total_views": 45000
    },
    "scores": {
      "overall_stackoverflow_score": 75,
      "expertise_score": 78,
      "helpfulness_score": 72,
      "community_score": 70,
      "visibility_score": 75,
      "activity_score": 70,
      "impact_score": 80
    },
    "visibility_level": "high",
    "analyzed_at": "2025-11-06T12:00:00Z"
  },
  "privacy_report": {
    "overall_risk_level": "medium",
    "issues_found": [
      {
        "severity": "medium",
        "category": "Personal Information",
        "description": "Email address is publicly visible on GitHub profile",
        "recommendation": "Consider removing public email or using a professional email",
        "platform": "github"
      }
    ],
    "exposed_information": [
      "Public email address",
      "Location information",
      "Company affiliation"
    ],
    "visibility_score": 30,
    "recommendations": [
      "Review privacy settings on all platforms",
      "Use professional email addresses for public profiles",
      "Be mindful of location sharing"
    ]
  },
  "overall_visibility_score": 78,
  "professional_score": 78,
  "visibility_score": 78,
  "activity_score": 75,
  "impact_score": 79,
  "expertise_score": 78,
  "scanned_at": "2025-11-06T12:00:00Z",
  "message": "Successfully scanned 2 platform(s)"
}
```

**Scoring System:**

**Overall Score Calculation:**
```
Overall = (GitHub Score × 0.6) + (StackOverflow Score × 0.4)
```

**GitHub Score Formula:**
```
GitHub Score = (Code Quality × 0.3) + (Activity × 0.4) + (Impact × 0.3)

Code Quality = f(repo_quality, documentation, best_practices)
Activity = f(commits, PRs, issues, contribution_streak)
Impact = f(stars, forks, followers)
```

**StackOverflow Score Formula:**
```
StackOverflow Score = (Expertise × 0.4) + (Helpfulness × 0.35) + (Community × 0.25)

Expertise = f(reputation, tag_scores, answer_quality)
Helpfulness = f(accepted_answers, upvotes, answer_count)
Community = f(badges, engagement, views)
```

**4 Dimensional Scores:**
1. **Visibility Score**: Public presence and profile completeness
2. **Activity Score**: Contribution frequency and consistency
3. **Impact Score**: Influence measured by stars, followers, reputation
4. **Expertise Score**: Technical depth and skill diversity

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/footprint/scan" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "github_username": "johndoe",
    "stackoverflow_id": 12345,
    "include_privacy_analysis": true
  }'
```

---

### GET /api/v1/footprint/recommendations/{scan_id}

**Get AI-powered personalized recommendations**

Uses Groq AI (llama-3.3-70b-versatile) to analyze GitHub README and generate intelligent recommendations.

**Authentication:** Required

**Path Parameters:**
- `scan_id`: Scan to generate recommendations for

**Response (200 OK):**
```json
{
  "scan_id": 1,
  "profile_recommendations": [
    {
      "category": "GitHub Activity",
      "priority": "high",
      "title": "Increase Open Source Contributions",
      "description": "Your contribution activity has decreased in the last 6 months",
      "action_items": [
        "Contribute to 2-3 popular open source projects in your domain",
        "Set aside 2 hours weekly for open source work",
        "Document your contributions in your README"
      ],
      "impact": "Higher visibility to recruiters and stronger portfolio"
    },
    {
      "category": "Portfolio",
      "priority": "medium",
      "title": "Showcase Projects with Better Documentation",
      "description": "Several repositories lack comprehensive README files",
      "action_items": [
        "Add detailed README to top 5 repositories",
        "Include setup instructions and usage examples",
        "Add screenshots and demo links"
      ],
      "impact": "Demonstrates professionalism and makes projects more accessible"
    },
    {
      "category": "Skills Development",
      "priority": "medium",
      "title": "Expand Cloud Platform Experience",
      "description": "Limited evidence of cloud platform usage",
      "action_items": [
        "Build and deploy a project on AWS/Azure",
        "Obtain cloud certification (AWS/Azure)",
        "Document cloud architecture in portfolio"
      ],
      "impact": "Meets requirements for senior backend positions"
    }
  ],
  "career_insights": [
    {
      "insight_type": "skills",
      "title": "Primary Language: Python",
      "description": "You primarily work with Python, accounting for 45% of your code",
      "evidence": [
        "25 Python repositories",
        "Django and FastAPI frameworks",
        "5+ years of Python experience"
      ]
    },
    {
      "insight_type": "expertise",
      "title": "Backend Development Specialization",
      "description": "Your skills align strongly with backend development roles",
      "evidence": [
        "API development expertise",
        "Database design experience",
        "Microservices architecture"
      ]
    }
  ],
  "skill_gaps": [
    "Kubernetes",
    "Docker",
    "CI/CD",
    "Cloud Platforms (AWS/Azure)",
    "System Design"
  ],
  "competitive_analysis": {
    "github_percentile": "Top 30% based on activity and repositories",
    "stackoverflow_percentile": "Top 40% based on reputation",
    "overall_ranking": "Above average among developers with similar experience"
  },
  "generated_at": "2025-11-06T12:15:00Z"
}
```

**AI Recommendation Process:**

1. **Context Building**: Aggregates profile data, repositories, skills, activity
2. **README Analysis**: Parses GitHub README content (first 2000 chars)
3. **Groq AI Analysis**: Uses llama-3.3-70b-versatile with structured prompt
4. **JSON Parsing**: Extracts recommendations, insights, skill gaps
5. **Fallback**: Rule-based recommendations if AI fails

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/footprint/recommendations/1" \
  -H "Authorization: Bearer <token>"
```

---

### GET /api/v1/footprint/history

**Get scan history**

Returns paginated list of previous footprint scans.

**Authentication:** Required

**Query Parameters:**
- `skip` (optional, default: 0): Records to skip
- `limit` (optional, default: 20): Max records

**Response (200 OK):**
```json
{
  "scans": [
    {
      "scan_id": 1,
      "scanned_at": "2025-11-06T12:00:00Z",
      "platforms_scanned": ["github", "stackoverflow"],
      "overall_visibility_score": 78,
      "professional_score": 78,
      "github_score": 82,
      "stackoverflow_score": 75,
      "visibility_score": 78,
      "activity_score": 75,
      "impact_score": 79,
      "expertise_score": 78
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 20
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/footprint/history?limit=10" \
  -H "Authorization: Bearer <token>"
```

---

### GET /api/v1/footprint/compare/{scan_id_1}/{scan_id_2}

**Compare two scans to track progress**

Shows improvements, declines, and new achievements between scans.

**Authentication:** Required

**Path Parameters:**
- `scan_id_1`: Earlier scan ID
- `scan_id_2`: Later scan ID

**Response (200 OK):**
```json
{
  "previous_scan_id": 1,
  "current_scan_id": 2,
  "time_between_scans": "30 days",
  "visibility_change": 8,
  "professional_change": 5,
  "improvements": [
    "Overall visibility increased by 8 points",
    "GitHub score improved by 10 points",
    "StackOverflow score improved by 5 points"
  ],
  "declines": [],
  "new_achievements": [
    "Increased GitHub activity and contributions",
    "Enhanced StackOverflow reputation",
    "Added 5 new public repositories"
  ],
  "summary": "Great progress! Your online visibility has significantly improved over 30 days."
}
```

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/footprint/compare/1/2" \
  -H "Authorization: Bearer <token>"
```

---

## 11. Rate Limiting

### Rate Limit Configuration

| Endpoint Category | Rate Limit | Window |
|------------------|------------|--------|
| **Authentication** | 5 requests | 1 minute |
| **Resume Operations** | 10 requests | 1 hour |
| **Job Scraping** | 5 requests | 1 hour |
| **Job Matching** | 20 requests | 1 hour |
| **Interview** | 20 requests | 1 hour |
| **Footprint Scanning** | 10 requests | 1 hour |

### Rate Limit Headers

All responses include rate limit information:

```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1730804400
```

### Rate Limit Exceeded Response (429)

```json
{
  "error": "Rate limit exceeded. Try again in 3420 seconds."
}
```

---

## 12. Webhooks

**Status:** Coming Soon

Planned webhook events:
- `resume.analyzed` - Resume analysis completed
- `job.matched` - New job matches found
- `interview.completed` - Interview session finished
- `footprint.scanned` - Footprint scan completed

---

## 13. Best Practices

### API Integration Tips

**1. Token Management:**
```javascript
// Refresh token before expiry
const isTokenExpired = (token) => {
  const payload = JSON.parse(atob(token.split('.')[1]));
  return Date.now() >= payload.exp * 1000;
};

if (isTokenExpired(token)) {
  token = await refreshToken();
}
```

**2. Error Handling:**
```javascript
try {
  const response = await api.post('/resumes/upload', formData);
  return response.data;
} catch (error) {
  if (error.response) {
    // Server responded with error
    if (error.response.status === 401) {
      // Redirect to login
    } else if (error.response.status === 429) {
      // Handle rate limit
      const retryAfter = error.response.headers['retry-after'];
    } else {
      // Show error message
      showError(error.response.data.detail);
    }
  } else if (error.request) {
    // Request made but no response
    showError('Network error. Please check your connection.');
  } else {
    // Request setup error
    showError('An unexpected error occurred.');
  }
}
```

**3. File Uploads:**
```javascript
const uploadResume = async (file) => {
  // Validate file size
  if (file.size > 10 * 1024 * 1024) {
    throw new Error('File too large (max 10MB)');
  }
  
  // Validate file type
  const allowedTypes = ['.pdf', '.docx', '.doc'];
  const ext = file.name.substring(file.name.lastIndexOf('.'));
  if (!allowedTypes.includes(ext.toLowerCase())) {
    throw new Error('Invalid file type');
  }
  
  // Upload with progress
  const formData = new FormData();
  formData.append('file', file);
  
  return axios.post('/resumes/upload', formData, {
    onUploadProgress: (progressEvent) => {
      const percent = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total
      );
      updateProgress(percent);
    }
  });
};
```

**4. Pagination:**
```javascript
const fetchAllJobs = async () => {
  let allJobs = [];
  let page = 1;
  let hasMore = true;
  
  while (hasMore) {
    const response = await api.get(`/jobs/list?page=${page}&page_size=50`);
    allJobs = allJobs.concat(response.data.jobs);
    hasMore = page < response.data.total_pages;
    page++;
  }
  
  return allJobs;
};
```

### Performance Optimization

**1. Batch Requests:**
```javascript
// Instead of multiple sequential requests
const resume = await api.get(`/resumes/${id}`);
const analysis = await api.post(`/resumes/analyze`, { resume_id: id });

// Use Promise.all for parallel requests
const [resume, analysis] = await Promise.all([
  api.get(`/resumes/${id}`),
  api.post(`/resumes/analyze`, { resume_id: id })
]);
```

**2. Caching:**
```javascript
const cache = new Map();

const getCachedData = async (key, fetchFn, ttl = 5 * 60 * 1000) => {
  const cached = cache.get(key);
  
  if (cached && Date.now() - cached.timestamp < ttl) {
    return cached.data;
  }
  
  const data = await fetchFn();
  cache.set(key, { data, timestamp: Date.now() });
  return data;
};
```

**3. Debouncing:**
```javascript
const debounce = (fn, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
};

const searchJobs = debounce(async (keywords) => {
  const results = await api.post('/jobs/search', { keywords });
  displayResults(results);
}, 500);
```

### Security Best Practices

1. **Never log tokens**: Avoid logging JWT tokens or sensitive data
2. **Use HTTPS**: Always use HTTPS in production
3. **Validate input**: Validate all user input on frontend before sending
4. **Handle errors gracefully**: Don't expose internal errors to users
5. **Implement CORS**: Configure CORS properly for production domains
6. **Rate limiting**: Respect rate limits and implement exponential backoff
7. **Token storage**: Use localStorage or sessionStorage, not cookies (unless httpOnly)

---

**End of Part 3**

This completes the comprehensive UtopiaHire Backend API Documentation covering all endpoints, authentication, data models, error handling, and best practices.

For questions or support, contact the development team or open an issue on GitHub.

**Version:** 1.0.0  
**Last Updated:** November 6, 2025  
**API Status:** ✅ Production Ready
