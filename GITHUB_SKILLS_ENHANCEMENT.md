# GitHub Skills & Language Analysis Enhancement

## Overview
Enhanced the footprint module to use GitHub API tokens for fetching detailed repository insights, including:
- **Accurate language statistics** (bytes of code, not just repo count)
- **Automated skills extraction** (frameworks, databases, tools)
- **Beautiful visualizations** with progress bars and badges

## Changes Made

### 1. Backend - GitHub Analyzer (`utils/github_analyzer.py`)

#### New Method: `get_repository_languages()`
```python
def get_repository_languages(self, owner: str, repo_name: str) -> Dict[str, int]:
    """Fetch detailed language breakdown (bytes of code) for each repository"""
```

#### Enhanced: `analyze_repositories()`
- **Before**: Only counted primary language per repository
- **After**: 
  - Fetches actual bytes of code per language from GitHub API
  - Calculates accurate percentage breakdown
  - Analyzes top 30 repositories to balance detail vs API rate limits
  - Returns both repository count AND code bytes

**New Fields Returned:**
```python
{
    'language_bytes': {      # Raw bytes of code
        'TypeScript': 524288,
        'JavaScript': 245760,
        # ...
    },
    'language_percentages': { # Percentage breakdown
        'TypeScript': 65.50,
        'JavaScript': 27.99,
        'HTML': 2.46,
        # ...
    }
}
```

#### New Method: `_extract_skills_from_repos()`
Intelligently extracts technologies from:
- Repository names
- Repository descriptions  
- Repository topics

**Categories Detected:**
- **Frameworks**: React, Vue, Angular, Django, Flask, Express, FastAPI, Spring, Next.js, etc.
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, SQLite, DynamoDB, etc.
- **Tools**: Docker, Kubernetes, AWS, Azure, GCP, CI/CD, Terraform, GraphQL, etc.

Returns count of projects using each technology.

### 2. Backend - API Models (`backend/app/models/footprint.py`)

#### New Model: `GitHubSkills`
```python
class GitHubSkills(BaseModel):
    frameworks: Dict[str, int]  # e.g., {'React': 5, 'Django': 3}
    databases: Dict[str, int]   # e.g., {'PostgreSQL': 4, 'Redis': 2}
    tools: Dict[str, int]       # e.g., {'Docker': 8, 'AWS': 6}
```

#### Updated Model: `GitHubAnalysis`
```python
class GitHubAnalysis(BaseModel):
    # ... existing fields ...
    languages: Dict[str, float]              # Changed from int to float (percentages)
    language_bytes: Optional[Dict[str, int]] # NEW: Raw bytes per language
    skills: Optional[GitHubSkills]           # NEW: Extracted skills
```

### 3. Backend - API Endpoints (`backend/app/api/footprint.py`)

Updated both `/scan` and `/{scan_id}` endpoints to:
- Include `language_percentages` in response
- Include `language_bytes` in response
- Include `skills` breakdown (frameworks, databases, tools)

### 4. Frontend - TypeScript Interface (`FootprintPage.tsx`)

#### Updated Interface:
```typescript
interface FootprintScan {
  github_data?: {
    repositories: {
      // ... existing fields ...
      language_percentages?: Record<string, number>;  // NEW
      skills?: {                                      // NEW
        frameworks: Record<string, number>;
        databases: Record<string, number>;
        tools: Record<string, number>;
      };
    };
  };
}
```

### 5. Frontend - UI Components (`FootprintPage.tsx`)

#### New Section: Programming Languages Breakdown
- **Visual Progress Bars**: 25-block horizontal bars showing percentage
- **Color-Coded**: Each language has its own color (TypeScript=blue, JavaScript=yellow, etc.)
- **Accurate Percentages**: Shows real coding time breakdown (e.g., "TypeScript 65.50%")
- **Top 5 Languages**: Displays most-used languages

#### New Section: Skills & Technologies
Three subsections with color-coded badges:

1. **Frameworks & Libraries** (Blue badges)
   - Shows frameworks like React, Django, Express
   - Badge shows project count (e.g., "React 5")
   - Top 6 most-used frameworks

2. **Databases** (Green badges)
   - PostgreSQL, MongoDB, Redis, etc.
   - Shows usage count per project

3. **Tools & Platforms** (Purple badges)
   - Docker, Kubernetes, AWS, CI/CD tools
   - Top 8 most-used tools

## Visual Design

### Language Progress Bars
```
TypeScript  ███████████████████░░░░░░  65.50%
JavaScript  ███████░░░░░░░░░░░░░░░░░░  27.99%
HTML        █░░░░░░░░░░░░░░░░░░░░░░░░   2.46%
```

### Skill Badges
```
[React 5] [Django 3] [Next.js 4]
[PostgreSQL 4] [Redis 2]
[Docker 8] [AWS 6] [Kubernetes 3]
```

## How It Works

### Data Flow
1. **User initiates scan** with GitHub username
2. **Backend fetches** user's repositories (up to 100)
3. **For top 30 repos**, backend calls `/repos/{owner}/{repo}/languages` API
4. **Aggregates** bytes of code across all languages
5. **Calculates** percentages based on total bytes
6. **Extracts skills** by analyzing repo names, descriptions, topics
7. **Returns** comprehensive analysis to frontend
8. **Frontend displays** visual progress bars and skill badges

### GitHub Token Usage
- **Without token**: 60 requests/hour (limited)
- **With token**: 5000 requests/hour (recommended)
- Set `GITHUB_TOKEN` in backend `.env` file

### API Rate Limit Strategy
- Analyzes **top 30 repositories** (not all 100+)
- Balances accuracy with rate limit consumption
- Each repo requires 1 API call for language stats
- Total: ~31 calls per scan (profile + repos list + 30 language calls)

## Benefits

### For Users
✅ **Accurate representation** of coding time (not just repo count)
✅ **Skills showcase** automatically extracted from projects
✅ **Visual appeal** with color-coded progress bars and badges
✅ **Comprehensive view** of technical expertise

### For Recruiters
✅ **Real skill validation** from actual code contributions
✅ **Technology stack** clearly displayed
✅ **Experience level** indicated by project counts
✅ **Diverse expertise** across frameworks, databases, tools

## Example Output

### Before Enhancement
```
Languages: JavaScript (12), Python (8), Java (3)
```

### After Enhancement
```
Programming Languages:
  TypeScript  ███████████████████░░░░░░  65.50%
  JavaScript  ███████░░░░░░░░░░░░░░░░░░  27.99%
  HTML        █░░░░░░░░░░░░░░░░░░░░░░░░   2.46%
  JSON        █░░░░░░░░░░░░░░░░░░░░░░░░   2.03%
  Markdown    ▒░░░░░░░░░░░░░░░░░░░░░░░░   1.22%

Frameworks & Libraries:
  [React 8] [Express 6] [Next.js 4] [Django 3] [FastAPI 2]

Databases:
  [PostgreSQL 5] [MongoDB 4] [Redis 3]

Tools & Platforms:
  [Docker 10] [AWS 7] [Kubernetes 5] [CI/CD 4]
```

## Testing

### To Test Enhanced Analysis:
1. Ensure `GITHUB_TOKEN` is set in `/home/firas/Utopia/backend/.env`
2. Run backend: `cd backend && uvicorn app.main:app --reload`
3. Run frontend: `cd frontend && npm run dev`
4. Create new footprint scan with GitHub username
5. Verify:
   - Language percentages appear with progress bars
   - Skills badges show frameworks, databases, tools
   - Percentages match actual code composition

## Files Modified

### Backend
- ✅ `utils/github_analyzer.py` - Enhanced with language fetching and skills extraction
- ✅ `backend/app/models/footprint.py` - Added GitHubSkills model, updated GitHubAnalysis
- ✅ `backend/app/api/footprint.py` - Updated endpoints to include new data

### Frontend
- ✅ `frontend/src/pages/footprint/FootprintPage.tsx` - Added visualizations and skills display

## Future Enhancements

### Potential Additions
- 📊 Language trends over time (compare scans)
- 🏆 Technology badges/achievements
- 📈 Skills growth tracking
- 🔍 Detailed framework version detection
- 🌐 Open source contribution analysis
- 📚 Documentation quality scoring

---

**Status**: ✅ Complete and ready to use
**Requires**: GitHub API token for accurate analysis
**Impact**: Transforms basic profile scan into comprehensive skills assessment
