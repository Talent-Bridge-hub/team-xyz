"""
StackOverflow Reputation Scanner for UtopiaHire Module 4
Analyzes Stack Overflow profiles using Stack Exchange API
No API key required for basic public data
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import time

class StackOverflowScanner:
    """
    Scans Stack Overflow profiles to assess technical expertise and community engagement
    
    Features:
    - Profile information extraction
    - Reputation and badge analysis
    - Question/answer metrics
    - Top tags (expertise areas)
    - Community impact assessment
    """
    
    def __init__(self):
        """Initialize Stack Overflow scanner"""
        self.base_url = "https://api.stackexchange.com/2.3"
        self.site = "stackoverflow"
        self.requests_made = 0
        self.last_request_time = None
        
        # Stack Exchange API has quota of ~300 requests/day without key
        # With key: 10,000 requests/day (but we'll work without key first)
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Make API request with rate limiting
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Response JSON or None if error
        """
        # Rate limiting: 1 request per second
        if self.last_request_time:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < 1.0:
                time.sleep(1.0 - time_since_last)
        
        url = f"{self.base_url}{endpoint}"
        
        # Default params
        if params is None:
            params = {}
        
        params['site'] = self.site
        params['filter'] = 'default'  # Can use custom filters for more data
        
        try:
            response = requests.get(url, params=params, timeout=10)
            self.requests_made += 1
            self.last_request_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for API errors
                if 'error_id' in data:
                    raise Exception(f"Stack Exchange API error: {data.get('error_message')}")
                
                # Check quota
                quota_remaining = data.get('quota_remaining', 0)
                if quota_remaining < 10:
                    print(f"⚠️  Warning: Only {quota_remaining} API requests remaining today")
                
                return data
            else:
                raise Exception(f"Stack Exchange API error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {e}")
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Get user profile by Stack Overflow user ID
        
        Args:
            user_id: Stack Overflow user ID (numeric)
            
        Returns:
            Dictionary with user data or None if not found
        """
        response = self._make_request(f'/users/{user_id}')
        
        if not response or not response.get('items'):
            return None
        
        user = response['items'][0]
        
        return {
            'user_id': user['user_id'],
            'display_name': user.get('display_name'),
            'reputation': user.get('reputation', 0),
            'location': user.get('location'),
            'about_me': user.get('about_me'),
            'website_url': user.get('website_url'),
            'profile_image': user.get('profile_image'),
            
            # Badge counts
            'gold_badges': user.get('badge_counts', {}).get('gold', 0),
            'silver_badges': user.get('badge_counts', {}).get('silver', 0),
            'bronze_badges': user.get('badge_counts', {}).get('bronze', 0),
            
            # Activity dates
            'creation_date': datetime.fromtimestamp(user.get('creation_date', 0)).isoformat(),
            'last_access_date': datetime.fromtimestamp(user.get('last_access_date', 0)).isoformat(),
            
            # Links
            'profile_link': user.get('link')
        }
    
    def search_user_by_name(self, display_name: str) -> List[Dict]:
        """
        Search for users by display name
        
        Args:
            display_name: User's display name on Stack Overflow
            
        Returns:
            List of matching users (may be multiple)
        """
        response = self._make_request('/users', {
            'inname': display_name,
            'pagesize': 10,
            'sort': 'reputation',
            'order': 'desc'
        })
        
        if not response or not response.get('items'):
            return []
        
        users = []
        for user in response['items']:
            users.append({
                'user_id': user['user_id'],
                'display_name': user.get('display_name'),
                'reputation': user.get('reputation', 0),
                'profile_link': user.get('link')
            })
        
        return users
    
    def get_user_tags(self, user_id: int, top_n: int = 10) -> List[Dict]:
        """
        Get user's top tags (expertise areas)
        
        Args:
            user_id: Stack Overflow user ID
            top_n: Number of top tags to return
            
        Returns:
            List of tag dictionaries with scores
        """
        response = self._make_request(f'/users/{user_id}/top-tags', {
            'pagesize': top_n
        })
        
        if not response or not response.get('items'):
            return []
        
        tags = []
        for tag in response['items']:
            tags.append({
                'tag_name': tag['tag_name'],
                'answer_count': tag['answer_count'],
                'answer_score': tag['answer_score'],
                'question_count': tag['question_count'],
                'question_score': tag['question_score']
            })
        
        return tags
    
    def get_user_answers(self, user_id: int, max_answers: int = 100) -> Dict:
        """
        Get user's answers statistics
        
        Args:
            user_id: Stack Overflow user ID
            max_answers: Maximum answers to fetch
            
        Returns:
            Dictionary with answer statistics
        """
        response = self._make_request(f'/users/{user_id}/answers', {
            'pagesize': min(100, max_answers),
            'sort': 'votes',
            'order': 'desc'
        })
        
        if not response or not response.get('items'):
            return {
                'total_answers': 0,
                'accepted_answers': 0,
                'total_score': 0,
                'average_score': 0,
                'total_views': 0
            }
        
        answers = response['items']
        total_answers = response.get('total', len(answers))
        
        accepted_answers = sum(1 for a in answers if a.get('is_accepted', False))
        total_score = sum(a.get('score', 0) for a in answers)
        total_views = sum(a.get('view_count', 0) for a in answers)
        
        return {
            'total_answers': total_answers,
            'accepted_answers': accepted_answers,
            'total_score': total_score,
            'average_score': total_score / total_answers if total_answers > 0 else 0,
            'total_views': total_views,
            'top_answers': [{
                'answer_id': a['answer_id'],
                'score': a.get('score', 0),
                'is_accepted': a.get('is_accepted', False),
                'title': a.get('title', 'N/A'),
                'link': a.get('link')
            } for a in answers[:5]]  # Top 5 answers
        }
    
    def get_user_questions(self, user_id: int, max_questions: int = 100) -> Dict:
        """
        Get user's questions statistics
        
        Args:
            user_id: Stack Overflow user ID
            max_questions: Maximum questions to fetch
            
        Returns:
            Dictionary with question statistics
        """
        response = self._make_request(f'/users/{user_id}/questions', {
            'pagesize': min(100, max_questions),
            'sort': 'votes',
            'order': 'desc'
        })
        
        if not response or not response.get('items'):
            return {
                'total_questions': 0,
                'total_score': 0,
                'total_views': 0,
                'average_score': 0
            }
        
        questions = response['items']
        total_questions = response.get('total', len(questions))
        
        total_score = sum(q.get('score', 0) for q in questions)
        total_views = sum(q.get('view_count', 0) for q in questions)
        
        return {
            'total_questions': total_questions,
            'total_score': total_score,
            'total_views': total_views,
            'average_score': total_score / total_questions if total_questions > 0 else 0
        }
    
    def calculate_scores(self, profile: Dict, tags: List[Dict], 
                        answers_stats: Dict, questions_stats: Dict) -> Dict:
        """
        Calculate Stack Overflow scores (0-100)
        
        Scoring breakdown:
        - Expertise Score (0-100): Based on reputation, badges, top tags
        - Helpfulness Score (0-100): Based on answer quality and acceptance rate
        - Community Score (0-100): Based on overall engagement and impact
        
        Args:
            profile: User profile data
            tags: Top tags data
            answers_stats: Answer statistics
            questions_stats: Question statistics
            
        Returns:
            Dictionary with scores
        """
        # 1. Expertise Score (based on reputation and badges)
        reputation = profile['reputation']
        
        # Reputation scoring (logarithmic scale)
        if reputation == 0:
            rep_score = 0
        elif reputation < 100:
            rep_score = 20
        elif reputation < 500:
            rep_score = 40
        elif reputation < 1000:
            rep_score = 50
        elif reputation < 5000:
            rep_score = 70
        elif reputation < 10000:
            rep_score = 85
        else:
            rep_score = min(100, 85 + (reputation - 10000) / 1000)
        
        # Badge score
        gold_score = profile['gold_badges'] * 20
        silver_score = profile['silver_badges'] * 5
        bronze_score = profile['bronze_badges'] * 1
        badge_score = min(100, gold_score + silver_score + bronze_score)
        
        expertise_score = int((rep_score * 0.7 + badge_score * 0.3))
        
        # 2. Helpfulness Score (based on answers)
        total_answers = answers_stats['total_answers']
        accepted_answers = answers_stats['accepted_answers']
        
        if total_answers == 0:
            helpfulness_score = 0
        else:
            acceptance_rate = (accepted_answers / total_answers) * 100
            answer_volume_score = min(100, total_answers * 2)  # Max at 50 answers
            avg_score_normalized = min(100, answers_stats['average_score'] * 10)  # Max at 10 avg score
            
            helpfulness_score = int(
                acceptance_rate * 0.4 +
                answer_volume_score * 0.3 +
                avg_score_normalized * 0.3
            )
        
        # 3. Community Score (overall engagement)
        total_activity = total_answers + questions_stats['total_questions']
        total_views = answers_stats['total_views'] + questions_stats['total_views']
        num_tags = len(tags)
        
        activity_score = min(100, total_activity * 1)  # Max at 100 posts
        visibility_score = min(100, total_views / 1000)  # Max at 100k views
        expertise_breadth = min(100, num_tags * 10)  # Max at 10 tags
        
        community_score = int(
            activity_score * 0.4 +
            visibility_score * 0.3 +
            expertise_breadth * 0.3
        )
        
        # Overall Stack Overflow score (weighted average)
        overall_score = int(
            expertise_score * 0.40 +
            helpfulness_score * 0.35 +
            community_score * 0.25
        )
        
        return {
            'expertise_score': expertise_score,
            'helpfulness_score': helpfulness_score,
            'community_score': community_score,
            'overall_stackoverflow_score': overall_score,
            'breakdown': {
                'reputation_score': int(rep_score),
                'badge_score': int(badge_score),
                'acceptance_rate': int(acceptance_rate) if total_answers > 0 else 0
            }
        }
    
    def analyze_user(self, user_id: int) -> Dict:
        """
        Complete Stack Overflow profile analysis
        
        Args:
            user_id: Stack Overflow user ID
            
        Returns:
            Complete analysis dictionary with all metrics and scores
        """
        print(f"🔍 Analyzing Stack Overflow profile: {user_id}")
        
        # Get profile
        profile = self.get_user_by_id(user_id)
        if not profile:
            raise ValueError(f"Stack Overflow user {user_id} not found")
        
        print(f"  ✓ Profile retrieved: {profile['display_name']}")
        print(f"  ✓ Reputation: {profile['reputation']:,}")
        
        # Get top tags
        tags = self.get_user_tags(user_id)
        print(f"  ✓ Found {len(tags)} top tags")
        
        # Get answer statistics
        answers_stats = self.get_user_answers(user_id)
        print(f"  ✓ Answer stats: {answers_stats['total_answers']} answers, {answers_stats['accepted_answers']} accepted")
        
        # Get question statistics
        questions_stats = self.get_user_questions(user_id)
        print(f"  ✓ Question stats: {questions_stats['total_questions']} questions")
        
        # Calculate scores
        scores = self.calculate_scores(profile, tags, answers_stats, questions_stats)
        print(f"  ✓ Overall Stack Overflow score: {scores['overall_stackoverflow_score']}/100")
        
        # Compile complete result
        return {
            'profile': profile,
            'top_tags': tags,
            'answers': answers_stats,
            'questions': questions_stats,
            'scores': scores,
            'analyzed_at': datetime.now().isoformat(),
            'api_requests_made': self.requests_made
        }


# Example usage and testing
if __name__ == '__main__':
    import sys
    
    # Test with Jon Skeet (user ID: 22656) - one of the most famous SO users
    test_user_id = int(sys.argv[1]) if len(sys.argv) > 1 else 22656
    
    scanner = StackOverflowScanner()
    
    try:
        result = scanner.analyze_user(test_user_id)
        
        print("\n" + "="*70)
        print("Stack Overflow Analysis Results")
        print("="*70)
        
        profile = result['profile']
        print(f"\nProfile: {profile['display_name']}")
        print(f"Reputation: {profile['reputation']:,}")
        print(f"Badges: 🥇 {profile['gold_badges']} | 🥈 {profile['silver_badges']} | 🥉 {profile['bronze_badges']}")
        print(f"Member since: {profile['creation_date']}")
        print(f"Profile: {profile['profile_link']}")
        
        tags = result['top_tags']
        print(f"\nTop Tags ({len(tags)}):")
        for i, tag in enumerate(tags[:5], 1):
            print(f"  {i}. {tag['tag_name']}: {tag['answer_score']} score ({tag['answer_count']} answers)")
        
        answers = result['answers']
        print(f"\nAnswers:")
        print(f"  Total: {answers['total_answers']}")
        print(f"  Accepted: {answers['accepted_answers']}")
        print(f"  Average Score: {answers['average_score']:.1f}")
        print(f"  Total Views: {answers['total_views']:,}")
        
        questions = result['questions']
        print(f"\nQuestions:")
        print(f"  Total: {questions['total_questions']}")
        print(f"  Total Score: {questions['total_score']}")
        print(f"  Total Views: {questions['total_views']:,}")
        
        scores = result['scores']
        print(f"\nScores:")
        print(f"  Expertise: {scores['expertise_score']}/100")
        print(f"  Helpfulness: {scores['helpfulness_score']}/100")
        print(f"  Community: {scores['community_score']}/100")
        print(f"  Overall: {scores['overall_stackoverflow_score']}/100")
        
        print(f"\nAPI Requests Made: {result['api_requests_made']}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
