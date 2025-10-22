"""
Professional Footprint Calculator for UtopiaHire Module 4
Combines data from GitHub, Stack Overflow, and LinkedIn to calculate overall career footprint
Stores results in database and provides actionable insights
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json

from utils.github_analyzer import GitHubAnalyzer
from utils.stackoverflow_scanner import StackOverflowScanner
from config.database import execute_query, insert_one, update_one, get_one


class FootprintCalculator:
    """
    Calculates comprehensive professional footprint score
    
    Scoring weights:
    - LinkedIn: 25% (professional network and presence)
    - GitHub: 45% (code and technical contributions)
    - Stack Overflow: 30% (community engagement and expertise)
    
    Overall score: 0-100
    Performance levels: excellent (85-100), good (70-84), average (55-69), needs_improvement (0-54)
    """
    
    def __init__(self, user_id: int):
        """
        Initialize footprint calculator for a user
        
        Args:
            user_id: Database user ID
        """
        self.user_id = user_id
        self.github_analyzer = GitHubAnalyzer()
        self.stackoverflow_scanner = StackOverflowScanner()
        
    def scan_github(self, username: str) -> Dict:
        """
        Scan and store GitHub profile data
        
        Args:
            username: GitHub username
            
        Returns:
            Analysis results dictionary
        """
        print(f"\n🔍 Scanning GitHub: @{username}")
        
        try:
            result = self.github_analyzer.analyze_user(username)
            
            # Get or create user profile
            profile_id = self._get_or_create_profile()
            
            # Store GitHub data
            github_data = {
                'profile_id': profile_id,
                'username': username,
                'name': result['profile']['name'],
                'bio': result['profile']['bio'],
                'location': result['profile']['location'],
                'company': result['profile']['company'],
                'blog_url': result['profile']['blog_url'],
                'email': result['profile']['email'],
                'public_repos': result['profile']['public_repos'],
                'total_stars': result['repositories']['total_stars'],
                'total_forks': result['repositories']['total_forks'],
                'followers': result['profile']['followers'],
                'following': result['profile']['following'],
                'total_commits_last_year': result['activity']['commits'],
                'total_pull_requests': result['activity']['pull_requests'],
                'total_issues': result['activity']['issues'],
                'contribution_streak_days': result['activity']['activity_streak'],
                'top_repositories': json.dumps(result['repositories']['top_repos']),
                'languages_used': json.dumps(result['repositories']['languages']),
                'code_quality_score': result['scores']['code_quality_score'],
                'activity_score': result['scores']['activity_score'],
                'impact_score': result['scores']['impact_score'],
                'account_created_at': result['profile']['account_created_at']
            }
            
            # Delete old data if exists
            execute_query(
                "DELETE FROM github_data WHERE profile_id = %s",
                (profile_id,),
                fetch=False
            )
            
            insert_one('github_data', github_data)
            
            print(f"  ✓ GitHub data saved (score: {result['scores']['overall_github_score']}/100)")
            
            return result
            
        except Exception as e:
            print(f"  ✗ GitHub scan failed: {e}")
            raise
    
    def scan_stackoverflow(self, user_id: int) -> Dict:
        """
        Scan and store Stack Overflow profile data
        
        Args:
            user_id: Stack Overflow numeric user ID
            
        Returns:
            Analysis results dictionary
        """
        print(f"\n🔍 Scanning Stack Overflow: User {user_id}")
        
        try:
            result = self.stackoverflow_scanner.analyze_user(user_id)
            
            # Get or create user profile
            profile_id = self._get_or_create_profile()
            
            # Store Stack Overflow data
            stackoverflow_data = {
                'profile_id': profile_id,
                'user_id': user_id,
                'display_name': result['profile']['display_name'],
                'reputation': result['profile']['reputation'],
                'location': result['profile']['location'],
                'about_me': result['profile']['about_me'],
                'website_url': result['profile']['website_url'],
                'gold_badges': result['profile']['gold_badges'],
                'silver_badges': result['profile']['silver_badges'],
                'bronze_badges': result['profile']['bronze_badges'],
                'question_count': result['questions']['total_questions'],
                'answer_count': result['answers']['total_answers'],
                'accepted_answers': result['answers']['accepted_answers'],
                'total_views': result['answers']['total_views'] + result['questions']['total_views'],
                'top_tags': json.dumps(result['top_tags']),
                'member_since': result['profile']['creation_date'],
                'last_access_date': result['profile']['last_access_date'],
                'expertise_score': result['scores']['expertise_score'],
                'helpfulness_score': result['scores']['helpfulness_score'],
                'community_score': result['scores']['community_score']
            }
            
            # Delete old data if exists
            execute_query(
                "DELETE FROM stackoverflow_data WHERE profile_id = %s",
                (profile_id,),
                fetch=False
            )
            
            insert_one('stackoverflow_data', stackoverflow_data)
            
            print(f"  ✓ Stack Overflow data saved (score: {result['scores']['overall_stackoverflow_score']}/100)")
            
            return result
            
        except Exception as e:
            print(f"  ✗ Stack Overflow scan failed: {e}")
            raise
    
    def calculate_footprint(self) -> Dict:
        """
        Calculate overall professional footprint score from all platforms
        
        Returns:
            Dictionary with scores and recommendations
        """
        print(f"\n📊 Calculating professional footprint...")
        
        profile_id = self._get_or_create_profile()
        
        # Get platform data
        github_data = get_one('github_data', {'profile_id': profile_id})
        stackoverflow_data = get_one('stackoverflow_data', {'profile_id': profile_id})
        
        # Calculate individual platform scores
        github_score = 0
        stackoverflow_score = 0
        platforms_used = []
        
        if github_data:
            github_score = self._calculate_github_overall_score(github_data)
            platforms_used.append('github')
        
        if stackoverflow_data:
            stackoverflow_score = self._calculate_stackoverflow_overall_score(stackoverflow_data)
            platforms_used.append('stackoverflow')
        
        # LinkedIn not implemented yet (requires web scraping or API access)
        linkedin_score = 0
        
        # Calculate weighted overall score
        if not platforms_used:
            overall_score = 0
        elif len(platforms_used) == 1:
            # Only one platform
            overall_score = github_score if 'github' in platforms_used else stackoverflow_score
        else:
            # Multiple platforms - use weighted average
            # GitHub: 45%, Stack Overflow: 30%, LinkedIn: 25%
            overall_score = int(
                github_score * 0.60 +  # Increase weight since LinkedIn not available
                stackoverflow_score * 0.40
            )
        
        # Calculate component scores
        visibility_score = self._calculate_visibility_score(github_data, stackoverflow_data)
        activity_score = self._calculate_activity_score(github_data, stackoverflow_data)
        impact_score = self._calculate_impact_score(github_data, stackoverflow_data)
        expertise_score = self._calculate_expertise_score(github_data, stackoverflow_data)
        
        # Determine performance level
        if overall_score >= 85:
            performance_level = 'excellent'
        elif overall_score >= 70:
            performance_level = 'good'
        elif overall_score >= 55:
            performance_level = 'average'
        else:
            performance_level = 'needs_improvement'
        
        # Generate insights
        strengths, weaknesses, recommendations = self._generate_insights(
            github_data, stackoverflow_data, overall_score
        )
        
        # Calculate percentile (simplified - would need peer data for real calculation)
        percentile = min(99, int(overall_score * 0.9))  # Rough estimate
        peer_comparison = 'above_average' if percentile >= 60 else 'average' if percentile >= 40 else 'below_average'
        
        # Save scores to database
        footprint_data = {
            'profile_id': profile_id,
            'linkedin_score': linkedin_score,
            'github_score': github_score,
            'stackoverflow_score': stackoverflow_score,
            'overall_score': overall_score,
            'visibility_score': visibility_score,
            'activity_score': activity_score,
            'impact_score': impact_score,
            'expertise_score': expertise_score,
            'performance_level': performance_level,
            'strengths': json.dumps(strengths),
            'weaknesses': json.dumps(weaknesses),
            'recommendations': json.dumps(recommendations),
            'percentile': percentile,
            'peer_comparison': peer_comparison
        }
        
        # Delete old scores
        execute_query(
            "DELETE FROM footprint_scores WHERE profile_id = %s",
            (profile_id,),
            fetch=False
        )
        
        score_id = insert_one('footprint_scores', footprint_data)
        
        # Save to history
        history_data = {
            'profile_id': profile_id,
            'overall_score': overall_score,
            'linkedin_score': linkedin_score,
            'github_score': github_score,
            'stackoverflow_score': stackoverflow_score,
            'score_change': 0,  # Would need previous score to calculate
            'improvement_percentage': 0.0,
            'events': json.dumps([])
        }
        
        insert_one('footprint_history', history_data)
        
        print(f"  ✓ Footprint calculated: {overall_score}/100 ({performance_level})")
        
        return {
            'overall_score': overall_score,
            'linkedin_score': linkedin_score,
            'github_score': github_score,
            'stackoverflow_score': stackoverflow_score,
            'visibility_score': visibility_score,
            'activity_score': activity_score,
            'impact_score': impact_score,
            'expertise_score': expertise_score,
            'performance_level': performance_level,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'recommendations': recommendations,
            'percentile': percentile,
            'peer_comparison': peer_comparison,
            'platforms_used': platforms_used
        }
    
    def _get_or_create_profile(self) -> int:
        """Get or create user profile, return profile_id"""
        profile = get_one('user_profiles', {'user_id': self.user_id})
        
        if profile:
            return profile['id']
        
        # Create new profile
        return insert_one('user_profiles', {
            'user_id': self.user_id,
            'scan_status': 'scanning'
        })
    
    def _calculate_github_overall_score(self, data: Dict) -> int:
        """Calculate GitHub overall score from database data"""
        return int(
            data['code_quality_score'] * 0.3 +
            data['activity_score'] * 0.4 +
            data['impact_score'] * 0.3
        )
    
    def _calculate_stackoverflow_overall_score(self, data: Dict) -> int:
        """Calculate Stack Overflow overall score from database data"""
        return int(
            data['expertise_score'] * 0.40 +
            data['helpfulness_score'] * 0.35 +
            data['community_score'] * 0.25
        )
    
    def _calculate_visibility_score(self, github_data: Optional[Dict], 
                                   stackoverflow_data: Optional[Dict]) -> int:
        """Calculate how visible the user is in the tech community"""
        scores = []
        
        if github_data:
            followers_score = min(100, github_data['followers'] * 2)
            stars_score = min(100, github_data['total_stars'] * 2)
            scores.extend([followers_score, stars_score])
        
        if stackoverflow_data:
            rep_score = min(100, stackoverflow_data['reputation'] / 1000)
            scores.append(rep_score)
        
        return int(sum(scores) / len(scores)) if scores else 0
    
    def _calculate_activity_score(self, github_data: Optional[Dict],
                                 stackoverflow_data: Optional[Dict]) -> int:
        """Calculate how active the user is"""
        scores = []
        
        if github_data:
            scores.append(github_data['activity_score'])
        
        if stackoverflow_data:
            scores.append(stackoverflow_data['community_score'])
        
        return int(sum(scores) / len(scores)) if scores else 0
    
    def _calculate_impact_score(self, github_data: Optional[Dict],
                               stackoverflow_data: Optional[Dict]) -> int:
        """Calculate the user's impact on the community"""
        scores = []
        
        if github_data:
            scores.append(github_data['impact_score'])
        
        if stackoverflow_data:
            scores.append(stackoverflow_data['helpfulness_score'])
        
        return int(sum(scores) / len(scores)) if scores else 0
    
    def _calculate_expertise_score(self, github_data: Optional[Dict],
                                  stackoverflow_data: Optional[Dict]) -> int:
        """Calculate technical expertise level"""
        scores = []
        
        if github_data:
            scores.append(github_data['code_quality_score'])
        
        if stackoverflow_data:
            scores.append(stackoverflow_data['expertise_score'])
        
        return int(sum(scores) / len(scores)) if scores else 0
    
    def _generate_insights(self, github_data: Optional[Dict],
                          stackoverflow_data: Optional[Dict],
                          overall_score: int) -> Tuple[List[str], List[str], List[str]]:
        """Generate strengths, weaknesses, and recommendations"""
        strengths = []
        weaknesses = []
        recommendations = []
        
        # GitHub insights
        if github_data:
            if github_data['total_stars'] > 50:
                strengths.append(f"Strong GitHub presence with {github_data['total_stars']} stars")
            elif github_data['total_stars'] < 10:
                weaknesses.append("Limited GitHub stars - projects may need more visibility")
                recommendations.append("Share your projects on social media and dev communities")
            
            if github_data['public_repos'] > 20:
                strengths.append(f"Active developer with {github_data['public_repos']} repositories")
            elif github_data['public_repos'] < 5:
                weaknesses.append("Few public repositories")
                recommendations.append("Create more public projects to showcase your skills")
            
            if github_data['contribution_streak_days'] > 7:
                strengths.append(f"Consistent contributor ({github_data['contribution_streak_days']} day streak)")
            else:
                recommendations.append("Build a consistent contribution streak to show dedication")
        
        # Stack Overflow insights
        if stackoverflow_data:
            if stackoverflow_data['reputation'] > 1000:
                strengths.append(f"Strong Stack Overflow reputation: {stackoverflow_data['reputation']:,}")
            elif stackoverflow_data['reputation'] < 500:
                weaknesses.append("Low Stack Overflow reputation")
                recommendations.append("Answer questions in your areas of expertise to build reputation")
            
            if stackoverflow_data['accepted_answers'] > 10:
                strengths.append(f"{stackoverflow_data['accepted_answers']} accepted answers - helping the community")
            else:
                recommendations.append("Focus on providing quality answers that get accepted")
        
        # Overall recommendations
        if overall_score < 70:
            if not github_data:
                recommendations.append("Create a GitHub account and start building projects")
            if not stackoverflow_data:
                recommendations.append("Join Stack Overflow and contribute to discussions")
        
        if not strengths:
            strengths.append("You're just getting started - keep building!")
        
        return strengths, weaknesses, recommendations


# Example usage
if __name__ == '__main__':
    # Test with user_id=1, GitHub username, Stack Overflow ID
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python footprint_calculator.py <github_username> <stackoverflow_user_id>")
        print("Example: python footprint_calculator.py octocat 22656")
        sys.exit(1)
    
    github_username = sys.argv[1]
    stackoverflow_id = int(sys.argv[2])
    
    calculator = FootprintCalculator(user_id=1)
    
    try:
        # Scan platforms
        calculator.scan_github(github_username)
        calculator.scan_stackoverflow(stackoverflow_id)
        
        # Calculate footprint
        result = calculator.calculate_footprint()
        
        print("\n" + "="*70)
        print("Professional Footprint Report")
        print("="*70)
        
        print(f"\nOverall Score: {result['overall_score']}/100 ({result['performance_level'].upper()})")
        print(f"Percentile: Top {100 - result['percentile']}%")
        
        print(f"\nPlatform Scores:")
        print(f"  GitHub: {result['github_score']}/100")
        print(f"  Stack Overflow: {result['stackoverflow_score']}/100")
        
        print(f"\nDimension Scores:")
        print(f"  Visibility: {result['visibility_score']}/100")
        print(f"  Activity: {result['activity_score']}/100")
        print(f"  Impact: {result['impact_score']}/100")
        print(f"  Expertise: {result['expertise_score']}/100")
        
        print(f"\n✅ Strengths ({len(result['strengths'])}):")
        for strength in result['strengths']:
            print(f"  • {strength}")
        
        if result['weaknesses']:
            print(f"\n⚠️  Areas to Improve ({len(result['weaknesses'])}):")
            for weakness in result['weaknesses']:
                print(f"  • {weakness}")
        
        print(f"\n💡 Recommendations ({len(result['recommendations'])}):")
        for rec in result['recommendations']:
            print(f"  • {rec}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
