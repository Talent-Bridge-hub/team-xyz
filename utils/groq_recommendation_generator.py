"""
AI-Powered Recommendation Generator using Groq API
Analyzes GitHub profile README and generates personalized career recommendations

Uses Groq's fast LLM inference for intelligent analysis
"""

import logging
import json
import re
from typing import Dict, List, Optional
from groq import Groq
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqRecommendationGenerator:
    """
    Generate AI-powered personalized recommendations based on GitHub profile analysis
    Uses Groq API for ultra-fast inference
    """
    
    def __init__(self, groq_api_key: str = None):
        """
        Initialize the Groq recommendation generator
        
        Args:
            groq_api_key: Groq API key (optional, can use env var GROQ_API_KEY)
        """
        self.api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass groq_api_key parameter.")
        
        self.client = Groq(api_key=self.api_key)
        
        # Use Groq's fastest models
        # llama-3.3-70b-versatile: Best for complex reasoning
        # llama-3.1-8b-instant: Fastest, good for quick tasks
        self.model = "llama-3.3-70b-versatile"
        
        logger.info(f"✅ Groq AI Recommendation Generator initialized with model: {self.model}")
    
    def analyze_readme_and_generate_recommendations(
        self,
        readme_content: Optional[str],
        github_data: Dict,
        stackoverflow_data: Optional[Dict] = None
    ) -> Dict[str, List[Dict]]:
        """
        Analyze README content and GitHub data to generate personalized recommendations
        
        Args:
            readme_content: User's GitHub profile README content
            github_data: GitHub analysis data (repos, languages, activity, scores)
            stackoverflow_data: Optional StackOverflow data
            
        Returns:
            Dictionary with profile_recommendations, career_insights, and skill_gaps
        """
        logger.info("🤖 Generating AI-powered recommendations using Groq...")
        
        # Extract key information
        profile = github_data.get('profile', {})
        repos = github_data.get('repositories', {})
        activity = github_data.get('activity', {})
        scores = github_data.get('scores', {})
        
        # Build context for AI
        context = self._build_context(
            profile=profile,
            repos=repos,
            activity=activity,
            scores=scores,
            readme_content=readme_content,
            stackoverflow_data=stackoverflow_data
        )
        
        # Generate recommendations using Groq AI
        recommendations = self._generate_ai_recommendations(context)
        
        logger.info(f"✅ Generated {len(recommendations.get('profile_recommendations', []))} recommendations")
        
        return recommendations
    
    def _build_context(
        self,
        profile: Dict,
        repos: Dict,
        activity: Dict,
        scores: Dict,
        readme_content: Optional[str],
        stackoverflow_data: Optional[Dict]
    ) -> str:
        """
        Build comprehensive context for AI analysis
        """
        context_parts = []
        
        # Profile information
        context_parts.append("=== GITHUB PROFILE ===")
        context_parts.append(f"Username: {profile.get('username', 'N/A')}")
        context_parts.append(f"Name: {profile.get('name', 'N/A')}")
        context_parts.append(f"Location: {profile.get('location', 'N/A')}")
        context_parts.append(f"Bio: {profile.get('bio', 'N/A')}")
        context_parts.append(f"Public Repos: {profile.get('public_repos', 0)}")
        context_parts.append(f"Followers: {profile.get('followers', 0)}")
        
        # Repository analysis
        context_parts.append("\n=== REPOSITORIES ===")
        context_parts.append(f"Total Repos: {repos.get('total_repos', 0)}")
        context_parts.append(f"Total Stars: {repos.get('total_stars', 0)}")
        context_parts.append(f"Total Forks: {repos.get('total_forks', 0)}")
        
        # Languages
        languages = repos.get('language_percentages', repos.get('languages', {}))
        if languages:
            context_parts.append("\nProgramming Languages:")
            for lang, percentage in list(languages.items())[:5]:
                context_parts.append(f"  - {lang}: {percentage}%")
        
        # Skills (frameworks, databases, tools)
        skills = repos.get('skills', {})
        for category, items in skills.items():
            if items:
                context_parts.append(f"\n{category.title()}:")
                for item, count in list(items.items())[:5]:
                    context_parts.append(f"  - {item}: {count} repos")
        
        # Top repositories
        top_repos = repos.get('top_repos', [])
        if top_repos:
            context_parts.append("\nTop Repositories:")
            for repo in top_repos[:3]:
                context_parts.append(f"  - {repo.get('name')}: {repo.get('description', 'No description')}")
                context_parts.append(f"    Stars: {repo.get('stars', 0)}, Language: {repo.get('language', 'N/A')}")
        
        # Activity metrics
        context_parts.append("\n=== ACTIVITY (Last 90 Days) ===")
        context_parts.append(f"Commits: {activity.get('commits', 0)}")
        context_parts.append(f"Pull Requests: {activity.get('pull_requests', 0)}")
        context_parts.append(f"Issues: {activity.get('issues', 0)}")
        context_parts.append(f"Active Days: {activity.get('active_days', 0)}")
        context_parts.append(f"Current Streak: {activity.get('activity_streak', 0)} days")
        
        # Scores
        context_parts.append("\n=== SCORES ===")
        context_parts.append(f"Overall GitHub Score: {scores.get('overall_github_score', 0)}/100")
        context_parts.append(f"Code Quality: {scores.get('code_quality_score', 0)}/100")
        context_parts.append(f"Activity: {scores.get('activity_score', 0)}/100")
        context_parts.append(f"Impact: {scores.get('impact_score', 0)}/100")
        
        # README content (most important for personalization!)
        if readme_content:
            context_parts.append("\n=== PROFILE README ===")
            # Limit README to 2000 chars to avoid token limits
            truncated_readme = readme_content[:2000]
            if len(readme_content) > 2000:
                truncated_readme += "\n... (truncated)"
            context_parts.append(truncated_readme)
        else:
            context_parts.append("\n=== PROFILE README ===")
            context_parts.append("No profile README found")
        
        # StackOverflow data
        if stackoverflow_data:
            so_profile = stackoverflow_data.get('profile', {})
            context_parts.append("\n=== STACKOVERFLOW ===")
            context_parts.append(f"Reputation: {so_profile.get('reputation', 0)}")
            
            so_scores = stackoverflow_data.get('scores', {})
            context_parts.append(f"Overall SO Score: {so_scores.get('overall_stackoverflow_score', 0)}/100")
            
            tags = stackoverflow_data.get('top_tags', [])
            if tags:
                context_parts.append("Top Tags:")
                for tag in tags[:5]:
                    tag_name = tag.get('name') or tag.get('tag_name', 'unknown')
                    tag_count = tag.get('count') or tag.get('answer_count', 0)
                    context_parts.append(f"  - {tag_name}: {tag_count} posts")
        
        return "\n".join(context_parts)
    
    def _generate_ai_recommendations(self, context: str) -> Dict[str, List[Dict]]:
        """
        Generate recommendations using Groq AI based on profile context
        """
        prompt = f"""You are an expert career advisor for software developers. Analyze the following developer's GitHub profile and provide personalized recommendations.

{context}

Based on the above information, provide:

1. **Profile Recommendations** (3-5 recommendations):
   - Focus on improving GitHub presence, portfolio, and visibility
   - Consider README content, project descriptions, and profile completeness
   - Prioritize based on current weaknesses (high/medium/low priority)
   - Make recommendations SPECIFIC to this developer's situation

2. **Career Insights** (2-3 insights):
   - Identify technical strengths based on languages, frameworks, and projects
   - Highlight unique skills or expertise areas
   - Note career trajectory and potential paths
   - Reference specific evidence from their profile

3. **Skill Gaps** (3-5 skills):
   - Identify in-demand technologies not currently in their stack
   - Consider industry trends and complementary skills
   - Suggest skills that align with their existing expertise

**IMPORTANT**: 
- If there's a README, reference specific content from it in your recommendations
- Be SPECIFIC and ACTIONABLE based on the actual profile data, not generic advice
- Consider the developer's current level (scores) when making recommendations

Format your response as JSON with this exact structure:
{{
  "profile_recommendations": [
    {{
      "category": "GitHub Activity|Portfolio|Profile Optimization|Community Engagement",
      "priority": "high|medium|low",
      "title": "Short recommendation title",
      "description": "Detailed explanation of why this matters",
      "action_items": ["Specific action 1", "Specific action 2", "Specific action 3"],
      "impact": "Expected impact or benefit"
    }}
  ],
  "career_insights": [
    {{
      "insight_type": "skills|expertise|growth|strengths",
      "title": "Insight title",
      "description": "Detailed insight",
      "evidence": ["Evidence 1", "Evidence 2"]
    }}
  ],
  "skill_gaps": ["Skill 1", "Skill 2", "Skill 3"]
}}

Respond ONLY with the JSON, no other text."""

        try:
            # Call Groq API
            logger.info("📡 Calling Groq API for recommendations...")
            
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career advisor for software developers. Provide specific, actionable recommendations in JSON format only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=2500,
                temperature=0.7,
                top_p=1,
                stream=False
            )
            
            # Extract response
            ai_response = chat_completion.choices[0].message.content
            logger.info(f"✅ Groq API response received ({len(ai_response)} chars)")
            
            # Parse JSON from response
            recommendations = self._parse_ai_response(ai_response)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Error generating AI recommendations: {e}")
            # Fallback to rule-based recommendations
            return self._fallback_recommendations(context)
    
    def _parse_ai_response(self, response: str) -> Dict[str, List[Dict]]:
        """
        Parse AI response and extract recommendations
        """
        try:
            # Clean response - remove markdown code blocks if present
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Parse JSON
            recommendations = json.loads(cleaned_response)
            
            # Validate structure
            if 'profile_recommendations' in recommendations:
                logger.info("✅ Successfully parsed AI recommendations")
                return recommendations
            else:
                logger.warning("⚠️  AI response missing expected fields, using fallback")
                return self._create_default_recommendations()
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error: {e}")
            logger.error(f"Response was: {response[:200]}...")
            return self._create_default_recommendations()
        except Exception as e:
            logger.error(f"❌ Error parsing AI response: {e}")
            return self._create_default_recommendations()
    
    def _fallback_recommendations(self, context: str) -> Dict[str, List[Dict]]:
        """
        Generate rule-based recommendations as fallback with README analysis
        """
        logger.info("⚠️  Using fallback rule-based recommendations")
        
        recommendations = {
            "profile_recommendations": [],
            "career_insights": [],
            "skill_gaps": []
        }
        
        # Parse context for basic metrics
        has_readme = "No profile README found" not in context
        
        if not has_readme:
            recommendations["profile_recommendations"].append({
                "category": "Profile Optimization",
                "priority": "high",
                "title": "Create a GitHub Profile README",
                "description": "A profile README is your digital portfolio's homepage and significantly increases engagement.",
                "action_items": [
                    "Create a repository with the same name as your username",
                    "Add a README.md showcasing your skills, projects, and interests",
                    "Include sections: About Me, Tech Stack, Featured Projects",
                    "Add dynamic elements like GitHub stats or contribution graphs"
                ],
                "impact": "10x increase in profile visibility and recruiter engagement"
            })
        
        # Check activity level
        if "Commits: 0" in context or "Activity Score: 0" in context:
            recommendations["profile_recommendations"].append({
                "category": "GitHub Activity",
                "priority": "high",
                "title": "Increase Your GitHub Activity",
                "description": "Regular contributions demonstrate commitment and keep your profile visible.",
                "action_items": [
                    "Commit code at least 3-4 times per week",
                    "Contribute to open source projects",
                    "Build a consistent contribution streak (30+ days)",
                    "Document your learning journey through commits"
                ],
                "impact": "Higher visibility in GitHub trends and improved profile ranking"
            })
        
        # Generic insights
        recommendations["career_insights"].append({
            "insight_type": "growth",
            "title": "Building Your Developer Profile",
            "description": "Focus on consistent growth and quality contributions",
            "evidence": ["Regular commits show dedication", "Quality documentation demonstrates professionalism"]
        })
        
        # Default skill gaps
        recommendations["skill_gaps"] = [
            "Cloud Technologies (AWS/Azure/GCP)",
            "Docker & Kubernetes",
            "TypeScript",
            "CI/CD Pipelines",
            "System Design"
        ]
        
        return recommendations
    
    def _create_default_recommendations(self) -> Dict[str, List[Dict]]:
        """
        Create minimal default recommendations
        """
        return {
            "profile_recommendations": [
                {
                    "category": "Profile Optimization",
                    "priority": "medium",
                    "title": "Enhance Your GitHub Presence",
                    "description": "Improve your GitHub profile to increase visibility and opportunities",
                    "action_items": [
                        "Update your profile README",
                        "Add detailed project descriptions",
                        "Engage with the developer community"
                    ],
                    "impact": "Improved profile visibility and networking opportunities"
                }
            ],
            "career_insights": [
                {
                    "insight_type": "growth",
                    "title": "Continue Building Your Portfolio",
                    "description": "Focus on creating quality projects that showcase your skills",
                    "evidence": ["Active development", "Project diversity"]
                }
            ],
            "skill_gaps": ["Cloud Technologies", "DevOps Tools", "Modern Frameworks"]
        }


# Example usage
if __name__ == '__main__':
    # Test with sample data
    import sys
    
    generator = GroqRecommendationGenerator()
    
    sample_github_data = {
        'profile': {
            'username': 'testuser',
            'name': 'Test Developer',
            'bio': 'Full-stack developer',
            'public_repos': 15,
            'followers': 50
        },
        'repositories': {
            'total_repos': 15,
            'total_stars': 30,
            'language_percentages': {'Python': 53.5, 'JavaScript': 30.2, 'TypeScript': 16.3}
        },
        'activity': {
            'commits': 25,
            'pull_requests': 5,
            'active_days': 15,
            'activity_streak': 7
        },
        'scores': {
            'overall_github_score': 65,
            'code_quality_score': 70,
            'activity_score': 60,
            'impact_score': 65
        }
    }
    
    sample_readme = """
    # Hi, I'm Test Developer! 👋
    
    I'm a full-stack developer passionate about building web applications.
    
    ## 🛠️ Tech Stack
    - Frontend: React, Vue.js
    - Backend: Python, Node.js
    - Database: PostgreSQL, MongoDB
    
    ## 🚀 Current Focus
    Learning cloud technologies and DevOps practices.
    """
    
    try:
        recommendations = generator.analyze_readme_and_generate_recommendations(
            readme_content=sample_readme,
            github_data=sample_github_data
        )
        
        print("\n" + "="*70)
        print("AI RECOMMENDATIONS (Groq-Powered)")
        print("="*70)
        print(json.dumps(recommendations, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
