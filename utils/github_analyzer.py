"""
GitHub Portfolio Analyzer for UtopiaHire Module 4
Analyzes GitHub profiles and calculates contribution scores
Uses GitHub API to fetch public profile data and repository information
"""

import requests
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import Counter
from dotenv import load_dotenv
from pathlib import Path
import time

# Load environment variables from project root
project_root = Path(__file__).parent.parent
load_dotenv(project_root / '.env')

class GitHubAnalyzer:
    """
    Analyzes GitHub profiles to assess developer activity and impact
    
    Features:
    - Profile information extraction
    - Repository analysis (stars, forks, languages)
    - Contribution metrics (commits, PRs, issues)
    - Code quality assessment
    - Impact scoring (0-100)
    """
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize GitHub analyzer
        
        Args:
            github_token: Optional GitHub personal access token (increases rate limit)
                         If None, tries to load from GITHUB_TOKEN env var
                         Falls back to unauthenticated requests (60 requests/hour)
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'UtopiaHire-Footprint-Scanner'
        }
        
        # Use provided token, or try to load from environment
        token = github_token or os.getenv('GITHUB_TOKEN')
        
        if token:
            self.headers['Authorization'] = f'token {token}'
            self.rate_limit = 5000  # Authenticated rate limit per hour
            # Show partial token for verification (last 4 chars only)
            token_preview = f"...{token[-4:]}" if len(token) > 4 else "****"
            print(f"✅ GitHub API: Authenticated with token {token_preview} (5000 req/hour)")
        else:
            self.rate_limit = 60  # Unauthenticated rate limit per hour
            print(f"⚠️  GitHub API: Unauthenticated (60 req/hour) - Add GITHUB_TOKEN to .env for higher limits")
            
        self.requests_made = 0
        self.last_request_time = None
        
    def _make_request(self, endpoint: str, retries: int = 3) -> Optional[Dict]:
        """
        Make API request with rate limiting, retry logic and error handling
        
        Args:
            endpoint: API endpoint (e.g., '/users/username')
            retries: Number of retries on timeout (default 3)
            
        Returns:
            Response JSON or None if error
        """
        # Rate limiting: simple sleep to avoid hitting limits
        if self.last_request_time:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < 0.1:  # Max 10 requests per second
                time.sleep(0.1 - time_since_last)
        
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                self.requests_made += 1
                self.last_request_time = time.time()
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                elif response.status_code == 403:
                    # Rate limit exceeded
                    reset_time = response.headers.get('X-RateLimit-Reset')
                    if reset_time:
                        reset_dt = datetime.fromtimestamp(int(reset_time))
                        wait_seconds = (reset_dt - datetime.now()).total_seconds()
                        print(f"⚠️  Rate limit exceeded. Resets at {reset_dt} (wait {int(wait_seconds)}s)")
                    return None
                else:
                    print(f"⚠️  GitHub API error: {response.status_code}")
                    return None
                    
            except requests.exceptions.Timeout as e:
                if attempt < retries - 1:
                    print(f"⚠️  Request timeout, retrying ({attempt + 1}/{retries})...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    print(f"❌ Request timeout after {retries} attempts: {url}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Network error: {e}")
                return None
        
        return None
    
    def get_user_profile(self, username: str) -> Optional[Dict]:
        """
        Get GitHub user profile information
        
        Args:
            username: GitHub username
            
        Returns:
            Dictionary with profile data or None if user not found
        """
        profile = self._make_request(f'/users/{username}')
        
        if not profile:
            return None
            
        return {
            'username': profile.get('login'),
            'name': profile.get('name'),
            'bio': profile.get('bio'),
            'location': profile.get('location'),
            'company': profile.get('company'),
            'blog_url': profile.get('blog'),
            'email': profile.get('email'),
            'public_repos': profile.get('public_repos', 0),
            'followers': profile.get('followers', 0),
            'following': profile.get('following', 0),
            'account_created_at': profile.get('created_at'),
            'updated_at': profile.get('updated_at')
        }
    
    def get_repositories(self, username: str, max_repos: int = 100) -> List[Dict]:
        """
        Get user's public repositories with detailed language stats
        
        Args:
            username: GitHub username
            max_repos: Maximum number of repos to fetch
            
        Returns:
            List of repository dictionaries with language details
        """
        repos = []
        page = 1
        per_page = min(100, max_repos)  # GitHub max is 100 per page
        
        while len(repos) < max_repos:
            endpoint = f'/users/{username}/repos?page={page}&per_page={per_page}&sort=updated'
            page_repos = self._make_request(endpoint)
            
            if not page_repos:
                break
                
            repos.extend(page_repos)
            
            if len(page_repos) < per_page:
                break
                
            page += 1
        
        return repos[:max_repos]
    
    def get_repository_languages(self, owner: str, repo_name: str) -> Dict[str, int]:
        """
        Get detailed language breakdown for a specific repository
        Returns bytes of code written in each language
        
        Args:
            owner: Repository owner username
            repo_name: Repository name
            
        Returns:
            Dictionary mapping language to bytes of code
        """
        try:
            endpoint = f'/repos/{owner}/{repo_name}/languages'
            languages = self._make_request(endpoint)
            return languages if languages else {}
        except:
            return {}
    
    def _extract_skills_from_repos(self, repos: List[Dict]) -> Dict:
        """
        Extract programming languages, frameworks, and tools from repositories
        
        Args:
            repos: List of repository dictionaries
            
        Returns:
            Dictionary with categorized skills
        """
        # Technology keywords to detect from repo names, descriptions, and topics
        frameworks = {
            'React': ['react', 'reactjs', 'react-native'],
            'Vue': ['vue', 'vuejs', 'nuxt'],
            'Angular': ['angular', 'angularjs'],
            'Django': ['django'],
            'Flask': ['flask'],
            'Express': ['express', 'expressjs'],
            'FastAPI': ['fastapi'],
            'Spring': ['spring', 'springboot', 'spring-boot'],
            'Laravel': ['laravel'],
            'Ruby on Rails': ['rails', 'ruby-on-rails'],
            'Next.js': ['nextjs', 'next-js', 'next.js'],
            'Svelte': ['svelte', 'sveltekit'],
            'Node.js': ['nodejs', 'node-js', 'node.js'],
            '.NET': ['dotnet', '.net', 'asp.net'],
            'TensorFlow': ['tensorflow'],
            'PyTorch': ['pytorch'],
            'Keras': ['keras']
        }
        
        databases = {
            'PostgreSQL': ['postgres', 'postgresql'],
            'MySQL': ['mysql'],
            'MongoDB': ['mongodb', 'mongo'],
            'Redis': ['redis'],
            'SQLite': ['sqlite'],
            'Cassandra': ['cassandra'],
            'DynamoDB': ['dynamodb'],
            'Elasticsearch': ['elasticsearch', 'elastic'],
            'Firebase': ['firebase']
        }
        
        tools = {
            'Docker': ['docker', 'dockerfile'],
            'Kubernetes': ['kubernetes', 'k8s'],
            'AWS': ['aws', 'amazon-web-services'],
            'Azure': ['azure'],
            'GCP': ['gcp', 'google-cloud'],
            'Git': ['git', 'github-actions'],
            'CI/CD': ['ci-cd', 'jenkins', 'travis', 'circleci'],
            'Terraform': ['terraform'],
            'Ansible': ['ansible'],
            'GraphQL': ['graphql'],
            'REST API': ['rest-api', 'restful', 'api'],
            'WebSocket': ['websocket', 'socket.io'],
            'Microservices': ['microservices', 'microservice']
        }
        
        detected_frameworks = Counter()
        detected_databases = Counter()
        detected_tools = Counter()
        
        for repo in repos:
            # Defensive: repository fields may exist but be None
            name = (repo.get('name') or '').lower()
            description = (repo.get('description') or '').lower()
            topics_list = repo.get('topics') or []
            # topics may be a list of strings
            topics_text = ' '.join(topics_list)
            text_to_search = ' '.join([
                name,
                description,
                topics_text
            ])
            
            # Check frameworks
            for framework, keywords in frameworks.items():
                if any(keyword in text_to_search for keyword in keywords):
                    detected_frameworks[framework] += 1
            
            # Check databases
            for db, keywords in databases.items():
                if any(keyword in text_to_search for keyword in keywords):
                    detected_databases[db] += 1
            
            # Check tools
            for tool, keywords in tools.items():
                if any(keyword in text_to_search for keyword in keywords):
                    detected_tools[tool] += 1
        
        return {
            'frameworks': dict(detected_frameworks.most_common(10)),
            'databases': dict(detected_databases.most_common(5)),
            'tools': dict(detected_tools.most_common(10))
        }
    
    def analyze_repositories(self, repos: List[Dict]) -> Dict:
        """
        Analyze repository data to extract metrics with detailed language statistics
        
        Args:
            repos: List of repository dictionaries from GitHub API
            
        Returns:
            Dictionary with analysis results including accurate language breakdown
        """
        if not repos:
            return {
                'total_repos': 0,
                'total_stars': 0,
                'total_forks': 0,
                'total_watchers': 0,
                'languages': {},
                'language_bytes': {},
                'top_repos': [],
                'repo_quality_score': 0,
                'skills': {'frameworks': {}, 'databases': {}, 'tools': {}}
            }
        
        total_stars = sum(r.get('stargazers_count', 0) for r in repos)
        total_forks = sum(r.get('forks_count', 0) for r in repos)
        total_watchers = sum(r.get('watchers_count', 0) for r in repos)
        
        # Fetch detailed language statistics for repositories
        print(f"  📊 Fetching detailed language stats for {len(repos)} repositories...")
        language_bytes = Counter()
        repos_analyzed = 0
        
        for repo in repos[:30]:  # Analyze top 30 repos to avoid too many API calls
            owner = repo.get('owner', {}).get('login')
            repo_name = repo.get('name')
            
            if owner and repo_name:
                repo_langs = self.get_repository_languages(owner, repo_name)
                for lang, bytes_count in repo_langs.items():
                    language_bytes[lang] += bytes_count
                repos_analyzed += 1
        
        print(f"  ✓ Analyzed language stats for {repos_analyzed} repositories")
        
        # Convert bytes to percentage and repository count
        total_bytes = sum(language_bytes.values())
        language_percentages = {}
        if total_bytes > 0:
            for lang, bytes_count in language_bytes.items():
                percentage = (bytes_count / total_bytes) * 100
                language_percentages[lang] = round(percentage, 2)
        
        # Also count by repository (old method for comparison)
        language_counter = Counter()
        for repo in repos:
            lang = repo.get('language')
            if lang:
                language_counter[lang] += 1
        
        # Extract skills from repositories
        skills = self._extract_skills_from_repos(repos)
        
        # Get top repos by stars
        top_repos = sorted(
            repos,
            key=lambda r: (r.get('stargazers_count', 0), r.get('forks_count', 0)),
            reverse=True
        )[:10]
        
        top_repos_data = [{
            'name': r['name'],
            'description': r.get('description', ''),
            'language': r.get('language'),
            'stars': r.get('stargazers_count', 0),
            'forks': r.get('forks_count', 0),
            'url': r['html_url'],
            'updated_at': r.get('updated_at'),
            'has_readme': True,  # Assume true, can check separately
            'has_license': r.get('license') is not None
        } for r in top_repos]
        
        # Calculate repository quality score
        quality_metrics = {
            'has_description': sum(1 for r in repos if r.get('description')),
            'has_topics': sum(1 for r in repos if r.get('topics')),
            'has_license': sum(1 for r in repos if r.get('license')),
            'has_homepage': sum(1 for r in repos if r.get('homepage')),
            'not_forked': sum(1 for r in repos if not r.get('fork')),
            'recently_updated': sum(1 for r in repos if self._is_recently_updated(r.get('updated_at')))
        }
        
        total_possible = len(repos) * 6
        total_score = sum(quality_metrics.values())
        repo_quality_score = int((total_score / total_possible * 100)) if total_possible > 0 else 0
        
        return {
            'total_repos': len(repos),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'total_watchers': total_watchers,
            'languages': dict(language_counter),  # Count by repository
            'language_bytes': dict(language_bytes),  # Actual bytes of code
            'language_percentages': language_percentages,  # Percentage breakdown
            'skills': skills,
            'top_repos': top_repos_data,
            'repo_quality_score': repo_quality_score,
            'quality_metrics': quality_metrics
        }
    
    def _is_recently_updated(self, updated_at_str: Optional[str], days: int = 180) -> bool:
        """Check if repo was updated within last N days"""
        if not updated_at_str:
            return False
        try:
            updated_at = datetime.strptime(updated_at_str, '%Y-%m-%dT%H:%M:%SZ')
            return (datetime.now() - updated_at).days <= days
        except:
            return False
    
    def get_user_events(self, username: str, max_events: int = 300) -> List[Dict]:
        """
        Get user's recent activity events
        
        Args:
            username: GitHub username
            max_events: Maximum events to fetch
            
        Returns:
            List of event dictionaries
        """
        events = []
        page = 1
        per_page = min(100, max_events)
        
        while len(events) < max_events:
            endpoint = f'/users/{username}/events?page={page}&per_page={per_page}'
            page_events = self._make_request(endpoint)
            
            if not page_events:
                break
                
            events.extend(page_events)
            
            if len(page_events) < per_page:
                break
                
            page += 1
            
            # GitHub only returns last 90 days of events
            if page > 3:  # Max 300 events
                break
        
        return events[:max_events]
    
    def get_profile_readme(self, username: str) -> Optional[str]:
        """
        Fetch user's GitHub profile README content
        
        GitHub profile READMEs are stored in a special repository named the same as the username.
        For example, user 'johndoe' would have their README at github.com/johndoe/johndoe
        
        Args:
            username: GitHub username
            
        Returns:
            README content as string, or None if not found
        """
        try:
            # Try to get README from username/username repository
            endpoint = f'/repos/{username}/{username}/readme'
            readme_data = self._make_request(endpoint)
            
            if not readme_data:
                print(f"  ⚠️  No profile README found for {username}")
                return None
            
            # GitHub API returns README content in base64
            import base64
            content = readme_data.get('content', '')
            if content:
                # Decode base64 content
                decoded_content = base64.b64decode(content).decode('utf-8')
                print(f"  ✓ Profile README retrieved ({len(decoded_content)} characters)")
                return decoded_content
            
            return None
        except Exception as e:
            print(f"  ⚠️  Error fetching profile README: {e}")
            return None
    
    def analyze_activity(self, events: List[Dict]) -> Dict:
        """
        Analyze user activity from events
        
        Args:
            events: List of GitHub event dictionaries
            
        Returns:
            Dictionary with activity metrics
        """
        if not events:
            return {
                'total_events': 0,
                'commits': 0,
                'pull_requests': 0,
                'issues': 0,
                'reviews': 0,
                'event_types': {},
                'activity_streak': 0,
                'active_days': 0
            }
        
        event_type_counter = Counter(e['type'] for e in events)
        
        # Count specific activities
        commits = event_type_counter.get('PushEvent', 0)
        pull_requests = event_type_counter.get('PullRequestEvent', 0)
        issues = event_type_counter.get('IssuesEvent', 0)
        reviews = event_type_counter.get('PullRequestReviewEvent', 0)
        
        # Calculate activity streak and active days
        event_dates = []
        for event in events:
            try:
                created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                event_dates.append(created_at.date())
            except:
                continue
        
        unique_dates = sorted(set(event_dates), reverse=True)
        active_days = len(unique_dates)
        
        # Calculate current streak
        streak = 0
        if unique_dates:
            current_date = datetime.now().date()
            for date in unique_dates:
                if (current_date - date).days <= 1:
                    streak += 1
                    current_date = date
                else:
                    break
        
        return {
            'total_events': len(events),
            'commits': commits,
            'pull_requests': pull_requests,
            'issues': issues,
            'reviews': reviews,
            'event_types': dict(event_type_counter),
            'activity_streak': streak,
            'active_days': active_days
        }
    
    def calculate_scores(self, profile: Dict, repo_analysis: Dict, activity_analysis: Dict) -> Dict:
        """
        Calculate GitHub scores (0-100) based on various metrics
        
        Scoring breakdown:
        - Code Quality (0-100): Repository quality, README, licenses
        - Activity Score (0-100): Commits, PRs, issues, streak
        - Impact Score (0-100): Stars, forks, followers
        
        Args:
            profile: User profile data
            repo_analysis: Repository analysis results
            activity_analysis: Activity analysis results
            
        Returns:
            Dictionary with scores and overall GitHub score
        """
        # 1. Code Quality Score (30%)
        code_quality = repo_analysis['repo_quality_score']
        
        # 2. Activity Score (40%)
        # Components: commits, PRs, issues, active days, streak
        activity_components = {
            'commits': min(100, activity_analysis['commits'] * 5),  # Max at 20 commits
            'pull_requests': min(100, activity_analysis['pull_requests'] * 10),  # Max at 10 PRs
            'issues': min(100, activity_analysis['issues'] * 10),  # Max at 10 issues
            'active_days': min(100, activity_analysis['active_days'] * 2),  # Max at 50 days
            'streak': min(100, activity_analysis['activity_streak'] * 5)  # Max at 20 days streak
        }
        activity_score = int(sum(activity_components.values()) / len(activity_components))
        
        # 3. Impact Score (30%)
        # Components: stars, forks, followers
        stars_score = min(100, repo_analysis['total_stars'] * 2)  # Max at 50 stars
        forks_score = min(100, repo_analysis['total_forks'] * 5)  # Max at 20 forks
        followers_score = min(100, profile['followers'] * 2)  # Max at 50 followers
        
        impact_score = int((stars_score + forks_score + followers_score) / 3)
        
        # Overall GitHub score (weighted average)
        overall_score = int(
            code_quality * 0.3 +
            activity_score * 0.4 +
            impact_score * 0.3
        )
        
        return {
            'code_quality_score': code_quality,
            'activity_score': activity_score,
            'impact_score': impact_score,
            'overall_github_score': overall_score,
            'activity_breakdown': activity_components
        }
    
    def analyze_user(self, username: str) -> Dict:
        """
        Complete GitHub profile analysis
        
        Args:
            username: GitHub username
            
        Returns:
            Complete analysis dictionary with all metrics and scores
        """
        print(f"🔍 Analyzing GitHub profile: {username}")
        
        # Get profile
        profile = self.get_user_profile(username)
        if not profile:
            raise ValueError(f"GitHub user '{username}' not found")
        
        print(f"  ✓ Profile retrieved: {profile['name'] or username}")
        
        # Get repositories
        repos = self.get_repositories(username)
        print(f"  ✓ Found {len(repos)} public repositories")
        
        # Analyze repositories
        repo_analysis = self.analyze_repositories(repos)
        print(f"  ✓ Repository analysis complete ({repo_analysis['total_stars']} stars)")
        
        # Get activity events
        events = self.get_user_events(username)
        print(f"  ✓ Found {len(events)} recent events")
        
        # Get profile README
        profile_readme = self.get_profile_readme(username)
        
        # Analyze activity
        activity_analysis = self.analyze_activity(events)
        print(f"  ✓ Activity analysis complete ({activity_analysis['commits']} commits)")
        
        # Calculate scores
        scores = self.calculate_scores(profile, repo_analysis, activity_analysis)
        print(f"  ✓ Overall GitHub score: {scores['overall_github_score']}/100")
        
        # Compile complete result
        return {
            'profile': profile,
            'repositories': repo_analysis,
            'activity': activity_analysis,
            'profile_readme': profile_readme,  # Add README to results
            'scores': scores,
            'analyzed_at': datetime.now().isoformat(),
            'api_requests_made': self.requests_made
        }


# Example usage and testing
if __name__ == '__main__':
    import sys
    
    # Test with a well-known GitHub user
    test_username = sys.argv[1] if len(sys.argv) > 1 else 'torvalds'
    
    analyzer = GitHubAnalyzer()
    
    try:
        result = analyzer.analyze_user(test_username)
        
        print("\n" + "="*70)
        print("GitHub Analysis Results")
        print("="*70)
        
        profile = result['profile']
        print(f"\nProfile: {profile['name']} (@{profile['username']})")
        print(f"Location: {profile['location']}")
        print(f"Bio: {profile['bio']}")
        print(f"Public Repos: {profile['public_repos']}")
        print(f"Followers: {profile['followers']}")
        
        repos = result['repositories']
        print(f"\nRepositories:")
        print(f"  Total: {repos['total_repos']}")
        print(f"  Total Stars: {repos['total_stars']}")
        print(f"  Total Forks: {repos['total_forks']}")
        print(f"  Languages: {', '.join(repos['languages'].keys())}")
        
        activity = result['activity']
        print(f"\nActivity (last 90 days):")
        print(f"  Commits: {activity['commits']}")
        print(f"  Pull Requests: {activity['pull_requests']}")
        print(f"  Issues: {activity['issues']}")
        print(f"  Active Days: {activity['active_days']}")
        print(f"  Current Streak: {activity['activity_streak']} days")
        
        scores = result['scores']
        print(f"\nScores:")
        print(f"  Code Quality: {scores['code_quality_score']}/100")
        print(f"  Activity: {scores['activity_score']}/100")
        print(f"  Impact: {scores['impact_score']}/100")
        print(f"  Overall: {scores['overall_github_score']}/100")
        
        print(f"\nAPI Requests Made: {result['api_requests_made']}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
