# Footprint Module Documentation - PART 2
---

## Table of Contents - Part 2

7. [AI Recommendations System](#7-ai-recommendations-system)
8. [Frontend Components](#8-frontend-components)
9. [Integration Flows](#9-integration-flows)
10. [Configuration & Environment](#10-configuration--environment)
11. [Testing Guide](#11-testing-guide)
12. [Deployment](#12-deployment)
13. [Troubleshooting](#13-troubleshooting)

---

## 7. AI Recommendations System

### 7.1 Groq API Integration

**File:** `/utils/groq_recommendation_generator.py` (500+ lines)

#### 7.1.1 Overview

The AI Recommendations System uses **Groq's llama-3.3-70b-versatile** model to generate:
- **Profile Recommendations:** 3-5 actionable suggestions per platform
- **Career Insights:** 2-3 strategic career guidance items
- **Skill Gaps:** 3-5 missing skills to learn

**Key Features:**
- Context-aware analysis (profile, repos, README, activity, scores)
- Structured JSON output
- Rule-based fallback if AI fails
- README analysis (truncated to 2000 chars)
- Temperature 0.7 for balanced creativity

#### 7.1.2 Groq Configuration

**API Endpoint:** `https://api.groq.com/openai/v1/chat/completions`

**Supported Models:**
- `llama-3.3-70b-versatile` (default, best performance)
- `llama-3.1-70b-versatile` (alternative)
- `llama-3.1-8b-instant` (faster, less accurate)
- `mixtral-8x7b-32768` (alternative)

**Environment Variables:**

```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile  # Optional, defaults to this
```

**Rate Limits:**
- Varies by subscription tier
- Recommended: Add retry logic with exponential backoff

#### 7.1.3 GroqRecommendationGenerator Class

**Initialization:**

```python
class GroqRecommendationGenerator:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Groq recommendation generator.
        
        Args:
            api_key: Groq API key (falls back to GROQ_API_KEY env var)
            model: Model name (defaults to llama-3.3-70b-versatile)
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        self.model = model or os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
        self.base_url = 'https://api.groq.com/openai/v1'
```

**Main Method:**

```python
async def analyze_readme_and_generate_recommendations(
    self,
    readme_content: Optional[str],
    github_data: Optional[Dict],
    stackoverflow_data: Optional[Dict]
) -> Dict[str, Any]:
    """
    Generate AI-powered recommendations using Groq API.
    
    Args:
        readme_content: GitHub profile README (max 2000 chars)
        github_data: GitHub analysis results
        stackoverflow_data: StackOverflow analysis results
        
    Returns:
        {
            "profile_recommendations": [
                {
                    "platform": "GitHub",
                    "priority": "high|medium|low",
                    "title": "Recommendation Title",
                    "description": "Detailed description",
                    "action_items": ["Action 1", "Action 2"]
                }
            ],
            "career_insights": [
                {
                    "insight_type": "Growth Potential|Skill Development|Career Path",
                    "description": "Insight description",
                    "recommendations": ["Rec 1", "Rec 2"]
                }
            ],
            "skill_gaps": ["Skill 1", "Skill 2", "Skill 3"],
            "generated_at": "2025-11-06T10:00:00Z",
            "ai_generated": true
        }
    """
```

#### 7.1.4 Context Building

**Method:** `_build_context()`

**Context Components:**

1. **Profile Information:**
   - Name, bio, location
   - Account age, followers
   - Public repositories count

2. **Repository Analysis:**
   - Top repositories (name, stars, description)
   - Total stars, forks
   - Languages used (with percentages)

3. **Skills Extracted:**
   - Frameworks (React, Django, etc.)
   - Databases (PostgreSQL, MongoDB, etc.)
   - Tools (Docker, Kubernetes, etc.)

4. **Activity Metrics:**
   - Commits, PRs, issues
   - Activity streak
   - Recent contributions

5. **Scores:**
   - Overall visibility score
   - GitHub/StackOverflow scores
   - Dimension scores

6. **README Content:**
   - Truncated to 2000 characters
   - Used for understanding developer's presentation

7. **StackOverflow Data (if available):**
   - Reputation, badges
   - Top tags
   - Answer/question stats

**Example Context:**

```python
context = f"""
Profile: {profile.get('name')} (@{profile.get('login')})
Bio: {profile.get('bio', 'No bio')}
Location: {profile.get('location', 'Not specified')}
Followers: {profile.get('followers', 0)}
Public Repos: {profile.get('public_repos', 0)}

Top Repositories:
- awesome-project (150 ⭐): An awesome Python project
- react-dashboard (80 ⭐): Modern React dashboard
- api-service (50 ⭐): RESTful API with FastAPI

Languages: Python (45%), JavaScript (30%), TypeScript (15%)

Skills Detected:
- Frameworks: React, Django, FastAPI
- Databases: PostgreSQL, MongoDB, Redis
- Tools: Docker, Kubernetes, AWS

Activity (Last 90 Days):
- Commits: 150
- Pull Requests: 45
- Issues: 35
- Activity Streak: 12 days

Scores:
- Overall: 78.5/100
- GitHub: 79.8/100
- StackOverflow: 76.5/100

README Content:
{readme_content[:2000]}

StackOverflow:
- Reputation: 15,000
- Badges: 5 gold, 20 silver, 50 bronze
- Top Tags: python, javascript, react
- Answers: 150 (80 accepted)
"""
```

#### 7.1.5 Prompt Engineering

**System Prompt:**

```python
system_prompt = """You are an expert career advisor and technical mentor for software developers. 
Analyze the developer's profile and provide personalized, actionable recommendations to improve 
their online presence and career prospects.

Focus on:
1. Profile optimization (README, bio, project descriptions)
2. Skill development (based on current skills and market trends)
3. Community engagement (contributions, networking)
4. Career growth opportunities

Provide specific, actionable advice with clear next steps."""
```

**User Prompt:**

```python
user_prompt = f"""Analyze this developer's profile and provide recommendations:

{context}

Please provide:
1. Profile Recommendations (3-5 items):
   - Platform (GitHub/StackOverflow)
   - Priority (high/medium/low)
   - Title (short, actionable)
   - Description (why this matters)
   - Action Items (2-4 specific steps)

2. Career Insights (2-3 items):
   - Insight Type (Growth Potential, Skill Development, Career Path)
   - Description (what you observed)
   - Recommendations (how to leverage or improve)

3. Skill Gaps (3-5 skills):
   - Based on current skills and market demand
   - Consider the developer's focus area

Return ONLY valid JSON in this exact format:
{{
  "profile_recommendations": [...],
  "career_insights": [...],
  "skill_gaps": [...]
}}"""
```

**API Request:**

```python
response = requests.post(
    f"{self.base_url}/chat/completions",
    headers={
        "Authorization": f"Bearer {self.api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": self.model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2500,
        "response_format": {"type": "json_object"}
    },
    timeout=30
)
```

#### 7.1.6 Response Parsing

**Method:** `_parse_ai_response()`

**Parsing Logic:**

1. **Extract Content:**
   ```python
   content = response['choices'][0]['message']['content']
   ```

2. **Handle Markdown Code Blocks:**
   ```python
   if '```json' in content:
       # Extract JSON from markdown code block
       json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
       if json_match:
           content = json_match.group(1)
   ```

3. **Parse JSON:**
   ```python
   recommendations = json.loads(content)
   ```

4. **Validate Structure:**
   ```python
   required_keys = ['profile_recommendations', 'career_insights', 'skill_gaps']
   if not all(key in recommendations for key in required_keys):
       raise ValueError("Missing required keys in AI response")
   ```

5. **Add Metadata:**
   ```python
   recommendations['generated_at'] = datetime.utcnow().isoformat()
   recommendations['ai_generated'] = True
   ```

#### 7.1.7 Fallback System

**Method:** `_fallback_recommendations()`

**Rule-Based Logic:**

```python
def _fallback_recommendations(self, context: str) -> Dict[str, Any]:
    """Generate rule-based recommendations if AI fails."""
    
    recommendations = {
        "profile_recommendations": [],
        "career_insights": [],
        "skill_gaps": [],
        "generated_at": datetime.utcnow().isoformat(),
        "ai_generated": False
    }
    
    # Check for README
    if 'README Content:\nNone' in context or 'README Content:\n\n' in context:
        recommendations['profile_recommendations'].append({
            "platform": "GitHub",
            "priority": "high",
            "title": "Create Profile README",
            "description": "Add a profile README to introduce yourself",
            "action_items": [
                "Create username/username repository",
                "Add README.md with introduction",
                "Include skills, projects, and contact info"
            ]
        })
    
    # Check activity level
    if 'Commits: 0' in context or 'Activity Streak: 0' in context:
        recommendations['profile_recommendations'].append({
            "platform": "GitHub",
            "priority": "high",
            "title": "Increase Activity",
            "description": "Regular contributions improve visibility",
            "action_items": [
                "Commit code regularly (aim for 3-5 days/week)",
                "Contribute to open source projects",
                "Open PRs and issues on projects you use"
            ]
        })
    
    # Generic career insights
    recommendations['career_insights'].append({
        "insight_type": "General Growth",
        "description": "Continue building your developer profile",
        "recommendations": [
            "Keep learning new technologies",
            "Build projects that solve real problems",
            "Engage with the developer community"
        ]
    })
    
    # Common skill gaps
    recommendations['skill_gaps'] = [
        "Cloud Platforms (AWS, Azure, GCP)",
        "Containerization (Docker, Kubernetes)",
        "CI/CD Pipelines",
        "Microservices Architecture",
        "Testing Frameworks"
    ]
    
    return recommendations
```

#### 7.1.8 Error Handling

**Comprehensive Error Handling:**

```python
try:
    # Attempt AI generation
    recommendations = await self._generate_ai_recommendations(context)
    return recommendations
    
except requests.exceptions.Timeout:
    logger.warning("Groq API timeout, using fallback")
    return self._fallback_recommendations(context)
    
except requests.exceptions.RequestException as e:
    logger.error(f"Groq API error: {e}, using fallback")
    return self._fallback_recommendations(context)
    
except json.JSONDecodeError as e:
    logger.error(f"Failed to parse AI response: {e}, using fallback")
    return self._fallback_recommendations(context)
    
except Exception as e:
    logger.error(f"Unexpected error: {e}, using fallback")
    return self._fallback_recommendations(context)
```

#### 7.1.9 Example AI Response

```json
{
  "profile_recommendations": [
    {
      "platform": "GitHub",
      "priority": "high",
      "title": "Enhance Profile README with Dynamic Stats",
      "description": "Your README is basic. Adding dynamic badges and stats will make your profile stand out and show your activity at a glance.",
      "action_items": [
        "Add GitHub stats card using github-readme-stats",
        "Include language usage graph",
        "Add badges for top skills and certifications",
        "Link to your best projects with descriptions"
      ]
    },
    {
      "platform": "GitHub",
      "priority": "medium",
      "title": "Improve Repository Descriptions",
      "description": "Many repos lack detailed descriptions. Clear descriptions help recruiters understand your work.",
      "action_items": [
        "Add comprehensive README to each project",
        "Include setup instructions and dependencies",
        "Add screenshots or demo links",
        "Document architecture decisions"
      ]
    },
    {
      "platform": "StackOverflow",
      "priority": "medium",
      "title": "Increase Answer Quality",
      "description": "Your acceptance rate is 53%. Focus on comprehensive answers with code examples.",
      "action_items": [
        "Include working code examples",
        "Explain the 'why' not just the 'how'",
        "Format answers with proper markdown",
        "Follow up on comments and questions"
      ]
    }
  ],
  "career_insights": [
    {
      "insight_type": "Skill Development",
      "description": "You have strong backend skills (Python, FastAPI, PostgreSQL) but limited frontend presence. Full-stack developers are in high demand.",
      "recommendations": [
        "Learn React or Vue.js to complement your backend skills",
        "Build a full-stack project showcasing both skills",
        "Consider Next.js for full-stack TypeScript development",
        "Add frontend projects to your GitHub"
      ]
    },
    {
      "insight_type": "Growth Potential",
      "description": "Your DevOps/cloud skills are limited. Cloud technologies are essential for modern development.",
      "recommendations": [
        "Learn Docker and containerization basics",
        "Get AWS or Azure certification",
        "Deploy your projects to cloud platforms",
        "Learn Kubernetes for container orchestration",
        "Set up CI/CD pipelines for your projects"
      ]
    }
  ],
  "skill_gaps": [
    "React or Vue.js (Frontend Framework)",
    "Docker & Kubernetes (Containerization)",
    "AWS or Azure (Cloud Platform)",
    "CI/CD Pipelines (GitHub Actions, Jenkins)",
    "GraphQL (Modern API Technology)"
  ],
  "generated_at": "2025-11-06T10:35:00Z",
  "ai_generated": true
}
```

---

## 8. Frontend Components

### 8.1 FootprintPage Component

**File:** `/frontend/src/pages/footprint/FootprintPage.tsx` (600+ lines)

#### 8.1.1 Overview

Main page component that displays:
- Overall visibility score gauge
- Four dimension score gauges
- GitHub profile section (8 stats)
- Programming languages breakdown
- Skills & technologies
- StackOverflow badges
- Contribution graph
- Activity chart
- AI recommendations

#### 8.1.2 Component Structure

```typescript
interface FootprintScan {
  scan_id: number;
  scanned_at: string;
  overall_score: number;
  github_score: number | null;
  stackoverflow_score: number | null;
  visibility_score: number;
  activity_score: number;
  impact_score: number;
  expertise_score: number;
  visibility_level: string;
  performance_level: string;
  github_analysis?: GitHubAnalysis;
  stackoverflow_analysis?: StackOverflowAnalysis;
}

export default function FootprintPage() {
  const [latestScan, setLatestScan] = useState<FootprintScan | null>(null);
  const [scanHistory, setScanHistory] = useState<FootprintScan[]>([]);
  const [loading, setLoading] = useState(true);
  const [showScanForm, setShowScanForm] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // ... component logic
}
```

#### 8.1.3 Key Features

**1. Score Gauges:**
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
  {/* Overall Score - Large */}
  <div className="lg:col-span-2">
    <ScoreGauge score={latestScan.overall_score} size={240} />
    <div className="text-center mt-4">
      <h3 className="text-2xl font-bold">Overall Visibility</h3>
      <p className="text-gray-600">Performance: {latestScan.performance_level}</p>
    </div>
  </div>
  
  {/* Dimension Scores - Small */}
  <DimensionCard title="Visibility" score={latestScan.visibility_score} />
  <DimensionCard title="Activity" score={latestScan.activity_score} />
  <DimensionCard title="Impact" score={latestScan.impact_score} />
  <DimensionCard title="Expertise" score={latestScan.expertise_score} />
</div>
```

**2. GitHub Stats:**
```typescript
<div className="grid grid-cols-2 md:grid-cols-4 gap-4">
  <StatCard icon={<Package />} label="Repositories" value={profile.public_repos} />
  <StatCard icon={<Star />} label="Total Stars" value={repos.total_stars} />
  <StatCard icon={<GitFork />} label="Total Forks" value={repos.total_forks} />
  <StatCard icon={<Users />} label="Followers" value={profile.followers} />
  <StatCard icon={<GitCommit />} label="Commits" value={activity.commits} />
  <StatCard icon={<GitPullRequest />} label="Pull Requests" value={activity.pull_requests} />
  <StatCard icon={<UserPlus />} label="Following" value={profile.following} />
  <StatCard icon={<Zap />} label="Day Streak" value={activity.activity_streak} />
</div>
```

**3. Language Breakdown:**
```typescript
{Object.entries(languages)
  .sort(([, a], [, b]) => b - a)
  .slice(0, 5)
  .map(([lang, bytes]) => {
    const percentage = (bytes / totalBytes * 100).toFixed(1);
    return (
      <div key={lang}>
        <div className="flex justify-between mb-2">
          <span className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${getLanguageColor(lang)}`} />
            {lang}
          </span>
          <span className="font-semibold">{percentage}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${percentage}%` }}
            transition={{ duration: 1, delay: index * 0.1 }}
            className={`h-2 rounded-full ${getLanguageColor(lang)}`}
          />
        </div>
      </div>
    );
  })}
```

**4. Skills Display:**
```typescript
<div className="space-y-4">
  {/* Frameworks */}
  <div>
    <h4 className="text-sm font-semibold text-gray-700 mb-2">Frameworks</h4>
    <div className="flex flex-wrap gap-2">
      {skills.frameworks.map(fw => (
        <span key={fw} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full">
          {fw}
        </span>
      ))}
    </div>
  </div>
  
  {/* Databases */}
  <div>
    <h4 className="text-sm font-semibold text-gray-700 mb-2">Databases</h4>
    <div className="flex flex-wrap gap-2">
      {skills.databases.map(db => (
        <span key={db} className="px-3 py-1 bg-green-100 text-green-700 rounded-full">
          {db}
        </span>
      ))}
    </div>
  </div>
  
  {/* Tools */}
  <div>
    <h4 className="text-sm font-semibold text-gray-700 mb-2">Tools & Technologies</h4>
    <div className="flex flex-wrap gap-2">
      {skills.tools.map(tool => (
        <span key={tool} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full">
          {tool}
        </span>
      ))}
    </div>
  </div>
</div>
```

**5. StackOverflow Badges:**
```typescript
<div className="flex items-center gap-6">
  <div className="flex items-center gap-2">
    <Award className="w-6 h-6 text-yellow-500" />
    <div>
      <div className="text-2xl font-bold">{badges.gold}</div>
      <div className="text-sm text-gray-600">Gold</div>
    </div>
  </div>
  <div className="flex items-center gap-2">
    <Award className="w-6 h-6 text-gray-400" />
    <div>
      <div className="text-2xl font-bold">{badges.silver}</div>
      <div className="text-sm text-gray-600">Silver</div>
    </div>
  </div>
  <div className="flex items-center gap-2">
    <Award className="w-6 h-6 text-orange-600" />
    <div>
      <div className="text-2xl font-bold">{badges.bronze}</div>
      <div className="text-sm text-gray-600">Bronze</div>
    </div>
  </div>
</div>
```

#### 8.1.4 API Integration

```typescript
useEffect(() => {
  fetchScanHistory();
}, []);

const fetchScanHistory = async () => {
  try {
    const token = localStorage.getItem('access_token');
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
    
    const response = await fetch(`${API_BASE_URL}/footprint/history?limit=10`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      setScanHistory(data.scans);
      
      // Fetch full details for latest scan
      if (data.scans.length > 0) {
        await fetchScanDetails(data.scans[0].scan_id);
      }
    }
  } catch (error) {
    console.error('Failed to fetch scan history:', error);
    setError('Failed to load scan history');
  } finally {
    setLoading(false);
  }
};

const fetchScanDetails = async (scanId: number) => {
  try {
    const token = localStorage.getItem('access_token');
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
    
    const response = await fetch(`${API_BASE_URL}/footprint/${scanId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      setLatestScan(data);
    }
  } catch (error) {
    console.error('Failed to fetch scan details:', error);
  }
};
```

### 8.2 FootprintScanForm Component

**File:** `/frontend/src/components/footprint/FootprintScanForm.tsx` (200+ lines)

#### 8.2.1 Component Structure

```typescript
interface FootprintScanFormProps {
  onClose: () => void;
  onScanComplete: () => void;
}

export default function FootprintScanForm({ onClose, onScanComplete }: FootprintScanFormProps) {
  const [githubUsername, setGithubUsername] = useState('');
  const [stackoverflowUserId, setStackoverflowUserId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // ... component logic
}
```

#### 8.2.2 Form Validation

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  
  // Validation
  if (!githubUsername.trim()) {
    setError('GitHub username is required');
    return;
  }
  
  // ... submit logic
};
```

#### 8.2.3 API Call

```typescript
const submitScan = async () => {
  try {
    setLoading(true);
    setError('');
    
    const token = localStorage.getItem('access_token');
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
    
    const response = await fetch(`${API_BASE_URL}/footprint/scan`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        github_username: githubUsername,
        stackoverflow_user_id: stackoverflowUserId || null,
        include_privacy_analysis: true
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      onScanComplete();
      onClose();
    } else {
      const errorData = await response.json();
      handleError(response.status, errorData);
    }
  } catch (error) {
    setError('Network error. Please check your connection.');
  } finally {
    setLoading(false);
  }
};
```

#### 8.2.4 Error Handling

```typescript
const handleError = (status: number, errorData: any) => {
  switch (status) {
    case 404:
      setError('GitHub user not found. Please check the username.');
      break;
    case 401:
      setError('Session expired. Please log in again.');
      break;
    case 429:
      setError('Too many requests. Please try again later.');
      break;
    case 500:
      setError('Server error. Please try again later.');
      break;
    default:
      setError(errorData.detail || 'Failed to scan profile. Please try again.');
  }
};
```

### 8.3 ScoreGauge Component

**File:** `/frontend/src/components/footprint/ScoreGauge.tsx`

**Features:**
- Animated circular progress bar
- Color-coded by score (green: 85+, blue: 70-84, orange: 55-69, red: <55)
- Gradient fill
- Glow effect
- Smooth animation (1.5s ease-out)

### 8.4 RecommendationsList Component

**File:** `/frontend/src/components/footprint/RecommendationsList.tsx`

**Features:**
- Fetches AI recommendations from `/footprint/recommendations/{scan_id}`
- Priority-based icons (high: red alert, medium: yellow trend, low: green check)
- Priority badges with color coding
- Platform badges
- Action items with checkmarks
- Framer Motion animations (staggered)

### 8.5 GitHubContributionGraph Component

**File:** `/frontend/src/components/footprint/GitHubContributionGraph.tsx`

**Features:**
- 365-day contribution heatmap (52 weeks)
- 5 activity levels (0-4) with colors
- Month labels
- Day of week labels
- Total contributions and longest streak stats
- Hover tooltips with date and count
- Animated square appearance

### 8.6 ActivityChart Component

**File:** `/frontend/src/components/footprint/ActivityChart.tsx`

**Features:**
- Recharts line chart
- 5 lines: Overall, Visibility, Activity, Impact, Expertise
- Color-coded lines
- Custom tooltip
- Responsive container
- Trend visualization over time

---

## 9. Integration Flows

### 9.1 End-to-End Scan Flow

```
1. User clicks "New Scan" button
   ↓
2. FootprintScanForm modal opens
   ↓
3. User enters:
   - GitHub username (required)
   - StackOverflow user ID (optional)
   ↓
4. Form validates input
   ↓
5. POST /api/v1/footprint/scan
   ↓
6. Backend validates JWT token
   ↓
7. Check if user has exceeded scan rate limits
   ↓
8. Parallel execution:
   ├── GitHubAnalyzer.analyze()
   │   ├── Fetch profile
   │   ├── Fetch repositories (max 100)
   │   ├── Fetch language stats
   │   ├── Fetch activity events (90 days)
   │   ├── Fetch profile README
   │   ├── Extract skills
   │   └── Calculate GitHub scores
   │
   └── StackOverflowScanner.analyze()
       ├── Fetch profile by ID
       ├── Fetch top tags
       ├── Fetch answers stats
       ├── Fetch questions stats
       └── Calculate SO scores
   ↓
9. FootprintCalculator combines results
   ↓
10. Calculate 4 dimension scores
   ↓
11. Determine visibility level and performance level
   ↓
12. Optional: Generate privacy report
   ↓
13. Store in footprint_scans table (PostgreSQL)
   ↓
14. Return FootprintScanResponse to frontend
   ↓
15. Frontend displays results:
    - Score gauges animate
    - Charts populate with data
    - Stats cards show metrics
   ↓
16. User clicks "View Recommendations"
   ↓
17. GET /api/v1/footprint/recommendations/{scan_id}
   ↓
18. Backend checks if recommendations exist in DB
   ↓
19. If not, trigger GroqRecommendationGenerator
   ↓
20. Build context from scan data
   ↓
21. Call Groq API with context
   ↓
22. Parse JSON response
   ↓
23. If AI fails, use fallback recommendations
   ↓
24. Update footprint_scans.recommendations (JSONB)
   ↓
25. Return recommendations to frontend
   ↓
26. RecommendationsList displays AI-powered suggestions
```

### 9.2 Recommendation Generation Flow

```
1. GET /footprint/recommendations/{scan_id}
   ↓
2. Fetch scan from database
   ↓
3. Check if recommendations already exist
   ↓
4. If exists and recent (< 24 hours):
   └→ Return cached recommendations
   ↓
5. If not exists or outdated:
   ↓
6. GroqRecommendationGenerator.analyze_readme_and_generate_recommendations()
   ↓
7. Build comprehensive context:
   - Profile info
   - Repositories
   - Languages
   - Skills
   - Activity
   - Scores
   - README content (max 2000 chars)
   - StackOverflow data
   ↓
8. Prepare Groq API request:
   - Model: llama-3.3-70b-versatile
   - Temperature: 0.7
   - Max tokens: 2500
   - System prompt: Expert career advisor
   - User prompt: Context + instructions
   ↓
9. POST to Groq API
   ↓
10. Handle response:
    ├── Success:
    │   ├── Extract content
    │   ├── Parse JSON (handle markdown)
    │   ├── Validate structure
    │   └── Add metadata
    │
    └── Failure (timeout, error, invalid JSON):
        └→ Use rule-based fallback
   ↓
11. Update database:
    UPDATE footprint_scans
    SET recommendations = {...}::jsonb
    WHERE id = scan_id
   ↓
12. Return recommendations to API endpoint
   ↓
13. API returns to frontend
   ↓
14. Frontend displays:
    - Profile recommendations (3-5)
    - Career insights (2-3)
    - Skill gaps (3-5)
```

### 9.3 History & Comparison Flow

```
1. User views FootprintPage
   ↓
2. GET /footprint/history?limit=10
   ↓
3. Return list of scans with basic info
   ↓
4. Display scan history in ActivityChart
   ↓
5. User selects two scans to compare
   ↓
6. GET /footprint/compare/{scan_id_1}/{scan_id_2}
   ↓
7. Backend fetches both scans
   ↓
8. Calculate deltas:
   - Overall score change
   - Dimension score changes
   - Improvement percentage
   ↓
9. Return comparison data
   ↓
10. Frontend displays:
    - Side-by-side scores
    - Change indicators (↑ ↓)
    - Improvement percentage
    - Timeline of changes
```

---

## 10. Configuration & Environment

### 10.1 Backend Environment Variables

**File:** `/backend/.env`

```bash
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=utopiahire
DB_USER=utopia_user
DB_PASSWORD=utopia_secure_2025

# JWT Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# GitHub API (Optional but recommended)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# StackOverflow API (Optional, increases rate limit)
STACKOVERFLOW_API_KEY=your_stackoverflow_key

# Groq AI API (Required for AI recommendations)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile  # Optional, defaults to this

# Application
DEBUG=true
LOG_LEVEL=INFO
```

### 10.2 Frontend Environment Variables

**File:** `/frontend/.env`

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 10.3 Rate Limiting Configuration

**GitHub:**
- Authenticated: 5,000 requests/hour
- Unauthenticated: 60 requests/hour
- Recommendation: Always use GITHUB_TOKEN

**StackOverflow:**
- With key: 10,000 requests/day
- Without key: 300 requests/day
- Throttle: 1 request/second

**Groq:**
- Varies by subscription tier
- Implement retry logic with exponential backoff

---

## 11. Testing Guide

### 11.1 Manual Testing

**Test File:** `/tests/test_footprint.py`

**1. Test GitHub Analyzer:**

```python
from utils.github_analyzer import GitHubAnalyzer

analyzer = GitHubAnalyzer(github_token='your_token')

# Test profile fetch
profile = analyzer.get_user_profile('octocat')
print(f"Name: {profile['name']}")
print(f"Followers: {profile['followers']}")

# Test repository analysis
repos = analyzer.get_repositories('octocat', max_repos=10)
print(f"Found {len(repos)} repositories")

# Test skills extraction
repo_analysis = analyzer.analyze_repositories(repos)
print(f"Skills: {repo_analysis['skills']}")
```

**2. Test StackOverflow Scanner:**

```python
from utils.stackoverflow_scanner import StackOverflowScanner

scanner = StackOverflowScanner(api_key='your_key')

# Test user fetch
user = scanner.get_user_by_id(123456)
print(f"Name: {user['display_name']}")
print(f"Reputation: {user['reputation']}")

# Test tags
tags = scanner.get_user_tags(123456, top_n=5)
for tag in tags:
    print(f"Tag: {tag['tag_name']} ({tag['count']} posts)")
```

**3. Test Footprint Calculator:**

```python
from utils.footprint_calculator import FootprintCalculator

calculator = FootprintCalculator(user_id=1, db_connection=conn)

# Test full scan
result = calculator.calculate_footprint(
    github_username='octocat',
    stackoverflow_id='123456'
)

print(f"Overall Score: {result['overall_score']}")
print(f"Visibility: {result['visibility_score']}")
print(f"Activity: {result['activity_score']}")
print(f"Impact: {result['impact_score']}")
print(f"Expertise: {result['expertise_score']}")
```

**4. Test Groq Recommendations:**

```python
from utils.groq_recommendation_generator import GroqRecommendationGenerator

generator = GroqRecommendationGenerator(api_key='your_groq_key')

# Test recommendation generation
recommendations = await generator.analyze_readme_and_generate_recommendations(
    readme_content="# My Profile\nFull stack developer...",
    github_data={'profile': {...}, 'repositories': {...}},
    stackoverflow_data={'profile': {...}}
)

print(f"Profile Recs: {len(recommendations['profile_recommendations'])}")
print(f"Career Insights: {len(recommendations['career_insights'])}")
print(f"Skill Gaps: {recommendations['skill_gaps']}")
```

### 11.2 API Endpoint Testing

**Using curl:**

```bash
# Get JWT token first
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' \
  | jq -r '.access_token')

# Test scan endpoint
curl -X POST http://localhost:8000/api/v1/footprint/scan \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "github_username": "octocat",
    "stackoverflow_user_id": "123456",
    "include_privacy_analysis": true
  }'

# Test recommendations
curl -X GET http://localhost:8000/api/v1/footprint/recommendations/1 \
  -H "Authorization: Bearer $TOKEN"

# Test history
curl -X GET "http://localhost:8000/api/v1/footprint/history?limit=5" \
  -H "Authorization: Bearer $TOKEN"

# Test comparison
curl -X GET http://localhost:8000/api/v1/footprint/compare/1/2 \
  -H "Authorization: Bearer $TOKEN"
```

### 11.3 Frontend Testing

**Manual UI Testing:**

1. **Login Flow:**
   - Navigate to `/login`
   - Enter credentials
   - Verify redirect to `/dashboard`

2. **Footprint Page:**
   - Navigate to `/footprint`
   - Verify loading state
   - Check if scan history loads
   - Verify score gauges render

3. **Scan Form:**
   - Click "New Scan" button
   - Enter GitHub username
   - (Optional) Enter StackOverflow ID
   - Submit form
   - Verify loading spinner
   - Check for success/error messages

4. **Results Display:**
   - Verify score gauges animate
   - Check GitHub stats cards
   - Verify language breakdown
   - Check skills display
   - Verify StackOverflow section (if data exists)

5. **Recommendations:**
   - Click "View Recommendations"
   - Verify AI recommendations load
   - Check action items display
   - Verify priority badges

6. **Charts:**
   - Verify contribution graph renders
   - Check activity chart with historical data
   - Verify tooltips work on hover

---

## 12. Deployment

### 12.1 Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL database
createdb utopiahire

# Run migrations
python backend/migrations/create_footprint_tables.py

# Set environment variables
export GITHUB_TOKEN=ghp_xxxxx
export GROQ_API_KEY=gsk_xxxxx
export STACKOVERFLOW_API_KEY=xxxxx  # Optional
```

### 12.2 Production Configuration

**1. Database Connection Pool:**

```python
# backend/app/core/database.py
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    dsn=DATABASE_URL
)
```

**2. API Rate Limiting:**

```python
# backend/app/api/footprint.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/scan")
@limiter.limit("5/hour")  # 5 scans per hour per user
async def scan_footprint(...):
    ...
```

**3. Caching Recommendations:**

```python
# Cache recommendations for 24 hours
RECOMMENDATION_CACHE_DURATION = 86400  # seconds

# Check cache before calling Groq API
if recommendations and recommendations.get('generated_at'):
    generated_at = datetime.fromisoformat(recommendations['generated_at'])
    if (datetime.utcnow() - generated_at).total_seconds() < RECOMMENDATION_CACHE_DURATION:
        return recommendations  # Return cached
```

## 13. Troubleshooting

### 13.1 Common Issues

#### Issue 1: GitHub API Rate Limit Exceeded

**Error:** `403 Forbidden - Rate limit exceeded`

**Solution:**
```bash
# Add GITHUB_TOKEN to .env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Verify token
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
```

#### Issue 2: StackOverflow API Not Returning Data

**Error:** `User not found` or empty results

**Solution:**
- Verify user ID is correct (numeric ID, not display name)
- Use `search_user_by_name()` to find correct ID
- Check API key is valid (if using one)

#### Issue 3: Groq API Timeout

**Error:** `Timeout error when calling Groq API`

**Solution:**
```python
# Increase timeout
response = requests.post(
    url,
    json=payload,
    timeout=60  # Increase from 30 to 60 seconds
)

# Implement retry logic
for attempt in range(3):
    try:
        response = call_groq_api()
        break
    except requests.exceptions.Timeout:
        if attempt < 2:
            time.sleep(2 ** attempt)  # Exponential backoff
        else:
            # Use fallback
            return fallback_recommendations()
```

#### Issue 4: Frontend Not Loading Scan Results

**Error:** Network error or empty state

**Solution:**
```typescript
// Check API URL configuration
console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL);

// Verify JWT token
const token = localStorage.getItem('access_token');
if (!token) {
  console.error('No access token found');
  // Redirect to login
}

// Check CORS configuration in backend
// backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Issue 5: Database Connection Errors

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
psql -U utopia_user -d utopiahire -c "\dt"

# Verify credentials in .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=utopiahire
DB_USER=utopia_user
DB_PASSWORD=utopia_secure_2025

# Test connection
psql -h localhost -U utopia_user -d utopiahire
```

### 13.2 Debug Mode

**Enable Debug Logging:**

```python
# backend/app/core/config.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# In utils files
logger.debug(f"Fetching GitHub profile for: {username}")
logger.debug(f"API Response: {response.json()}")
logger.error(f"Error occurred: {str(e)}")
```

### 13.3 Performance Optimization

**1. Database Query Optimization:**

```sql
-- Add indexes if missing
CREATE INDEX CONCURRENTLY idx_footprint_user_created 
ON footprint_scans(user_id, created_at DESC);

-- Analyze query performance
EXPLAIN ANALYZE 
SELECT * FROM footprint_scans 
WHERE user_id = 1 
ORDER BY created_at DESC 
LIMIT 10;
```

**2. API Response Caching:**

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def get_github_profile_cached(username: str, timestamp: int):
    """Cache GitHub profile for 1 hour"""
    return GitHubAnalyzer().get_user_profile(username)

# Use timestamp to invalidate cache every hour
timestamp = int(datetime.now().timestamp() / 3600)
profile = get_github_profile_cached('octocat', timestamp)
```

**3. Frontend Performance:**

```typescript
// Lazy load components
const RecommendationsList = lazy(() => import('./RecommendationsList'));
const ActivityChart = lazy(() => import('./ActivityChart'));

// Memoize expensive computations
const languagePercentages = useMemo(() => {
  return calculateLanguagePercentages(languages);
}, [languages]);

// Debounce API calls
const debouncedFetch = useMemo(
  () => debounce(fetchScanDetails, 300),
  []
);
```

---

## 14. Future Enhancements

### 14.1 Planned Features

1. **LinkedIn Integration:**
   - Add LinkedIn profile analysis
   - Extract work experience, education, skills
   - Adjust scoring weights: GitHub (40%), StackOverflow (30%), LinkedIn (30%)

2. **Twitter/X Integration:**
   - Analyze developer Twitter presence
   - Track tech discussions, engagement
   - Add social influence score

3. **LeetCode/HackerRank Integration:**
   - Track competitive programming stats
   - Add problem-solving score dimension

4. **Portfolio Website Analysis:**
   - Crawl personal website/blog
   - Analyze content quality
   - Check SEO optimization

5. **Scheduled Scans:**
   - Auto-scan profiles weekly/monthly
   - Send email reports on changes
   - Track long-term progress

6. **Team Analytics:**
   - Compare team members
   - Identify skill gaps in team
   - Recommend training resources

### 14.2 Known Limitations

1. **GitHub README Analysis:**
   - Limited to 2000 characters for AI context
   - Does not analyze images/diagrams

2. **StackOverflow Search:**
   - Display name search may return multiple users
   - Requires manual ID verification

3. **AI Recommendations:**
   - Quality depends on Groq API availability
   - Fallback recommendations are generic

4. **Rate Limiting:**
   - GitHub unauthenticated: only 60 req/hour
   - StackOverflow without key: only 300 req/day

5. **Historical Data:**
   - GitHub events limited to last 90 days
   - Cannot analyze contribution history beyond 90 days

---

**End of Part 2**
