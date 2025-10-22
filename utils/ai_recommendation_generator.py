"""
AI-Powered Recommendation Generator for GitHub Profiles
Analyzes profile README and generates personalized career recommendations

Uses Hugging Face Inference API for intelligent analysis
"""

import logging
import json
import re
from typing import Dict, List, Optional
from huggingface_hub import InferenceClient
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIRecommendationGenerator:
    """
    Generate AI-powered personalized recommendations based on GitHub profile analysis
    """
    
    def __init__(self, hf_token: str = None):
        """
        Initialize the AI recommendation generator
        
        Args:
            hf_token: Hugging Face API token (optional, can use env var)
        """
        self.hf_token = hf_token or os.getenv('HUGGINGFACE_TOKEN')
        
        if not self.hf_token:
            logger.warning("No HuggingFace token provided. Using public models with rate limits.")
            logger.warning("Get a free token at: https://huggingface.co/settings/tokens")
        
        self.client = InferenceClient(token=self.hf_token)
        # Use a reliable model for chat/text generation
        # These models are free and work well with HuggingFace Inference API
        self.model = "HuggingFaceH4/zephyr-7b-beta"
        
        logger.info(f"AI Recommendation Generator initialized with model: {self.model}")
    
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
        logger.info("Generating AI-powered recommendations...")
        
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
        
        # Generate recommendations using AI
        recommendations = self._generate_ai_recommendations(context)
        
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
        
        languages = repos.get('languages', {})
        if languages:
            context_parts.append("\nProgramming Languages:")
            for lang, count in list(languages.items())[:5]:
                context_parts.append(f"  - {lang}: {count} repos")
        
        skills = repos.get('skills', {})
        for category, items in skills.items():
            if items:
                context_parts.append(f"\n{category.title()}:")
                for item, count in list(items.items())[:5]:
                    context_parts.append(f"  - {item}: {count} repos")
        
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
        
        # README content (most important!)
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
            context_parts.append(f"Questions: {so_profile.get('question_count', 0)}")
            context_parts.append(f"Answers: {so_profile.get('answer_count', 0)}")
            
            tags = stackoverflow_data.get('top_tags', [])
            if tags:
                context_parts.append("Top Tags:")
                for tag in tags[:5]:
                    context_parts.append(f"  - {tag.get('name')}: {tag.get('count')} posts")
        
        return "\n".join(context_parts)
    
    def _generate_ai_recommendations(self, context: str) -> Dict[str, List[Dict]]:
        """
        Generate recommendations using AI based on profile context
        """
        prompt = f"""You are an expert career advisor for software developers. Analyze the following developer's GitHub profile and provide personalized recommendations.

{context}

Based on the above information, provide:

1. **Profile Recommendations** (3-5 recommendations):
   - Focus on improving GitHub presence, portfolio, and visibility
   - Consider README content, project descriptions, and profile completeness
   - Prioritize based on current weaknesses (high/medium/low priority)

2. **Career Insights** (2-3 insights):
   - Identify technical strengths based on languages, frameworks, and projects
   - Highlight unique skills or expertise areas
   - Note career trajectory and potential paths

3. **Skill Gaps** (3-5 skills):
   - Identify in-demand technologies not currently in their stack
   - Consider industry trends and complementary skills
   - Suggest skills that align with their existing expertise

Format your response as JSON with this structure:
{{
  "profile_recommendations": [
    {{
      "category": "GitHub Activity|Portfolio|Profile Optimization|Community Engagement",
      "priority": "high|medium|low",
      "title": "Short recommendation title",
      "description": "Detailed explanation of why this matters",
      "action_items": ["Specific action 1", "Specific action 2", "Specific action 3"]
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

Make recommendations SPECIFIC and ACTIONABLE based on the actual profile data, not generic advice.
If there's a README, reference specific content from it in your recommendations.
"""

        try:
            # Call AI model using chat completion
            logger.info("Calling AI model for recommendations...")
            
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = self.client.chat_completion(
                messages=messages,
                model=self.model,
                max_tokens=2000,
                temperature=0.7
            )
            
            # Extract the assistant's response
            ai_response = response.choices[0].message.content
            logger.info("AI response received")
            
            # Parse JSON from response
            recommendations = self._parse_ai_response(ai_response)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {e}")
            # Fallback to rule-based recommendations
            return self._fallback_recommendations(context)
    
    def _parse_ai_response(self, response: str) -> Dict[str, List[Dict]]:
        """
        Parse AI response and extract recommendations
        """
        try:
            # Try to find JSON in response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                recommendations = json.loads(json_str)
                
                # Validate structure
                if 'profile_recommendations' in recommendations:
                    return recommendations
            
            logger.warning("Could not parse AI response as JSON, using fallback")
            return self._create_default_recommendations()
            
        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            return self._create_default_recommendations()
    
    def _fallback_recommendations(self, context: str) -> Dict[str, List[Dict]]:
        """
        Generate rule-based recommendations as fallback with README analysis
        """
        logger.info("Using fallback rule-based recommendations with README analysis")
        
        recommendations = {
            "profile_recommendations": [],
            "career_insights": [],
            "skill_gaps": []
        }
        
        # Parse context for basic metrics
        has_readme = "No profile README found" not in context
        readme_content = ""
        if has_readme and "=== PROFILE README ===" in context:
            # Extract README content
            parts = context.split("=== PROFILE README ===")
            if len(parts) > 1:
                readme_parts = parts[1].split("===")
                if readme_parts:
                    readme_content = readme_parts[0].strip()
        
        # Analyze README content for personalization
        readme_mentions_cloud = any(word in readme_content.lower() for word in ['aws', 'azure', 'gcp', 'cloud', 'kubernetes', 'docker'])
        readme_mentions_web = any(word in readme_content.lower() for word in ['react', 'vue', 'angular', 'frontend', 'web'])
        readme_mentions_backend = any(word in readme_content.lower() for word in ['backend', 'api', 'server', 'django', 'flask', 'express'])
        readme_mentions_learning = any(word in readme_content.lower() for word in ['learning', 'studying', 'exploring', 'currently working on'])
        
        if not has_readme:
            recommendations["profile_recommendations"].append({
                "category": "Profile Optimization",
                "priority": "high",
                "title": "Create a GitHub Profile README",
                "description": "A profile README is your digital portfolio's homepage. It's the first thing visitors see and significantly increases profile engagement by 10x.",
                "action_items": [
                    "Create a repository with the same name as your username",
                    "Add a README.md showcasing your skills, projects, and interests",
                    "Include sections: About Me, Tech Stack, Featured Projects, and Contact Info",
                    "Add dynamic elements like GitHub stats, contribution graphs, or tech icons"
                ],
                "impact": "Significantly increases profile visibility and engagement with recruiters"
            })
        else:
            # README exists - provide specific improvement suggestions
            recommendations["career_insights"].append({
                "insight_type": "strengths",
                "title": "Strong Profile Presentation",
                "description": "You have a profile README which demonstrates professionalism and attention to detail",
                "evidence": ["Profile README created", "Public repositories", "Active engagement"]
            })
            
            # Personalized recommendations based on README content
            if readme_mentions_cloud:
                recommendations["profile_recommendations"].append({
                    "category": "Portfolio",
                    "priority": "high",
                    "title": "Expand Your Cloud Portfolio",
                    "description": "Your README shows interest in cloud technologies. Build projects that demonstrate hands-on cloud experience.",
                    "action_items": [
                        "Deploy a full-stack application on AWS/Azure/GCP",
                        "Create infrastructure-as-code with Terraform or CloudFormation",
                        "Document cloud architecture and cost optimization in README",
                        "Add CI/CD pipeline using GitHub Actions or similar"
                    ],
                    "impact": "Demonstrates practical cloud skills that employers actively seek"
                })
                recommendations["skill_gaps"].extend(["AWS Certified Solutions Architect", "Kubernetes Administration", "Terraform"])
            
            if readme_mentions_web and not readme_mentions_backend:
                recommendations["profile_recommendations"].append({
                    "category": "Skills Development",
                    "priority": "medium",
                    "title": "Build Full-Stack Experience",
                    "description": "Your README shows frontend focus. Adding backend skills makes you more versatile.",
                    "action_items": [
                        "Create a RESTful API using Node.js/Express or Python/FastAPI",
                        "Integrate your frontend projects with a custom backend",
                        "Learn database design (PostgreSQL, MongoDB)",
                        "Deploy full-stack applications"
                    ],
                    "impact": "Increases marketability as a full-stack developer (30-40% higher salary range)"
                })
                recommendations["skill_gaps"].extend(["Backend Development", "API Design", "Database Management"])
            
            if readme_mentions_learning:
                recommendations["career_insights"].append({
                    "insight_type": "growth",
                    "title": "Growth Mindset",
                    "description": "Your README mentions ongoing learning, which is highly valued by employers",
                    "evidence": ["Mentions current learning projects", "Shows curiosity", "Continuous improvement"]
                })
        
        # Check activity level
        if "Commits: 0" in context or "Activity Score: 0" in context or "Commits: 1" in context or "Commits: 2" in context:
            recommendations["profile_recommendations"].append({
                "category": "GitHub Activity",
                "priority": "high",
                "title": "Increase Your GitHub Activity",
                "description": "Regular contributions demonstrate commitment and keep your profile visible to recruiters and the developer community.",
                "action_items": [
                    "Commit code at least 3-4 times per week",
                    "Contribute to open source projects in your area of expertise",
                    "Document your learning journey through code commits",
                    "Build a consistent contribution streak (aim for 30+ days)"
                ],
                "impact": "Higher visibility in GitHub trends and improved profile ranking"
            })
        
        # Check repository count  
        total_repos = 0
        if "Total Repos:" in context:
            try:
                import re
                match = re.search(r'Total Repos: (\d+)', context)
                if match:
                    total_repos = int(match.group(1))
            except:
                pass
        
        if total_repos < 5:
            recommendations["profile_recommendations"].append({
                "category": "Portfolio",
                "priority": "high",
                "title": "Build Your Project Portfolio",
                "description": "A diverse portfolio of projects demonstrates your skills and problem-solving abilities to potential employers.",
                "action_items": [
                    "Create 5-10 public repositories showcasing different skills",
                    "Include full-stack projects, algorithms, and tools",
                    "Write comprehensive README files for each project",
                    "Deploy projects and include live demo links"
                ],
                "impact": "Stronger technical portfolio that showcases versatile skills to employers"
            })
        
        # Add generic career insights if none exist
        if not recommendations["career_insights"]:
            recommendations["career_insights"].append({
                "insight_type": "growth",
                "title": "Focus on Consistent Growth",
                "description": "Building a strong developer profile takes time. Focus on consistent, quality contributions over quantity.",
                "evidence": [
                    "Regular commits show dedication",
                    "Quality documentation demonstrates professionalism",
                    "Diverse projects show versatility"
                ]
            })
        
        # Add skill gaps if not already populated
        if not recommendations["skill_gaps"]:
            recommendations["skill_gaps"] = [
                "Docker & Containerization",
                "Cloud Services (AWS/Azure/GCP)",
                "CI/CD Pipelines",
                "TypeScript",
                "System Design"
            ]
        
        # Limit to top recommendations
        recommendations["profile_recommendations"] = recommendations["profile_recommendations"][:5]
        recommendations["career_insights"] = recommendations["career_insights"][:3]
        recommendations["skill_gaps"] = recommendations["skill_gaps"][:5]
        
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
                    "impact": "Improved profile visibility and professional networking opportunities"
                }
            ],
            "career_insights": [
                {
                    "insight_type": "growth",
                    "title": "Continue Building Your Portfolio",
                    "description": "Focus on creating quality projects that showcase your skills",
                    "evidence": ["Active development", "Project diversity", "Code quality"]
                }
            ],
            "skill_gaps": ["Cloud Technologies", "DevOps Tools", "Modern Frameworks"]
        }


# Example usage
if __name__ == '__main__':
    # Test with sample data
    generator = AIRecommendationGenerator()
    
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
            'languages': {'Python': 8, 'JavaScript': 5, 'TypeScript': 2}
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
    
    recommendations = generator.analyze_readme_and_generate_recommendations(
        readme_content=sample_readme,
        github_data=sample_github_data
    )
    
    print(json.dumps(recommendations, indent=2))
