"""
Footprint Scanner API
Endpoints for analyzing digital footprint across GitHub, StackOverflow, etc.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import sys
import os
from datetime import datetime
import json

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from backend.app.models.footprint import (
    FootprintScanRequest,
    FootprintScanResponse,
    GitHubAnalysis,
    GitHubProfile,
    GitHubRepository,
    GitHubActivity,
    GitHubScores,
    GitHubSkills,
    StackOverflowAnalysis,
    StackOverflowProfile,
    StackOverflowBadges,
    StackOverflowTag,
    StackOverflowActivity,
    StackOverflowScores,
    PrivacyReport,
    PrivacyIssue,
    FootprintRecommendationsResponse,
    ProfileRecommendation,
    CareerInsight,
    ScanHistoryResponse,
    ScanHistoryItem,
    FootprintComparisonResponse,
    VisibilityLevel,
    PrivacyRisk,
    PlatformType
)
from backend.app.models.user import UserResponse
from backend.app.api.auth import get_current_user
from utils.github_analyzer import GitHubAnalyzer
from utils.stackoverflow_scanner import StackOverflowScanner
from config.database import insert_one, execute_query

router = APIRouter(prefix="/api/v1/footprint", tags=["Footprint Scanner"])


def calculate_visibility_level(score: int) -> VisibilityLevel:
    """Calculate visibility level from score"""
    if score >= 75:
        return VisibilityLevel.HIGH
    elif score >= 50:
        return VisibilityLevel.MEDIUM
    elif score >= 25:
        return VisibilityLevel.LOW
    else:
        return VisibilityLevel.NONE


def generate_privacy_report(
    github_data: Optional[dict],
    stackoverflow_data: Optional[dict]
) -> PrivacyReport:
    """Generate privacy assessment report"""
    issues = []
    exposed_info = []
    
    # Check GitHub privacy
    if github_data:
        profile = github_data.get('profile', {})
        
        if profile.get('email'):
            issues.append(PrivacyIssue(
                severity=PrivacyRisk.MEDIUM,
                category="Personal Information",
                description="Email address is publicly visible on GitHub profile",
                recommendation="Consider removing public email or using a professional email",
                platform=PlatformType.GITHUB
            ))
            exposed_info.append("Public email address")
        
        if profile.get('location'):
            exposed_info.append("Location information")
        
        if profile.get('company'):
            exposed_info.append("Company affiliation")
    
    # Check StackOverflow privacy
    if stackoverflow_data:
        profile = stackoverflow_data.get('profile', {})
        
        if profile.get('location'):
            exposed_info.append("StackOverflow location")
        
        if profile.get('website_url'):
            exposed_info.append("Personal website URL")
    
    # Determine overall risk
    if len(issues) >= 3:
        overall_risk = PrivacyRisk.HIGH
    elif len(issues) >= 1:
        overall_risk = PrivacyRisk.MEDIUM
    else:
        overall_risk = PrivacyRisk.LOW
    
    # Generate recommendations
    recommendations = [
        "Review privacy settings on all platforms",
        "Use professional email addresses for public profiles",
        "Be mindful of location sharing",
        "Regularly audit exposed information",
        "Consider separating personal and professional accounts"
    ]
    
    visibility_score = len(exposed_info) * 10
    
    return PrivacyReport(
        overall_risk_level=overall_risk,
        issues_found=issues,
        exposed_information=exposed_info,
        visibility_score=min(100, visibility_score),
        recommendations=recommendations[:3]
    )


def generate_recommendations(
    github_data: Optional[dict],
    stackoverflow_data: Optional[dict]
) -> tuple:
    """Generate personalized recommendations"""
    profile_recs = []
    career_insights = []
    skill_gaps = []
    
    # GitHub recommendations
    if github_data:
        gh_score = github_data.get('scores', {}).get('overall_github_score', 0)
        
        if gh_score < 50:
            profile_recs.append(ProfileRecommendation(
                category="GitHub Activity",
                priority="high",
                title="Increase GitHub Activity",
                description="Your GitHub activity is below average for developers",
                action_items=[
                    "Contribute to open source projects",
                    "Create more public repositories",
                    "Participate in code reviews"
                ],
                impact="Higher visibility to recruiters and better portfolio"
            ))
        
        repos = github_data.get('repositories', {}).get('total_repos', 0)
        if repos < 5:
            profile_recs.append(ProfileRecommendation(
                category="Portfolio",
                priority="medium",
                title="Build Your Portfolio",
                description="More projects demonstrate diverse skills",
                action_items=[
                    "Create 5-10 showcase projects",
                    "Add detailed README files",
                    "Include project documentation"
                ],
                impact="Stronger technical portfolio"
            ))
        
        languages = github_data.get('repositories', {}).get('languages', {})
        if languages:
            top_lang = max(languages.items(), key=lambda x: x[1])[0]
            career_insights.append(CareerInsight(
                insight_type="skills",
                title=f"Primary Language: {top_lang}",
                description=f"You primarily work with {top_lang}",
                evidence=[f"{count} repositories" for lang, count in list(languages.items())[:3]]
            ))
    
    # StackOverflow recommendations
    if stackoverflow_data:
        so_score = stackoverflow_data.get('scores', {}).get('overall_stackoverflow_score', 0)
        reputation = stackoverflow_data.get('profile', {}).get('reputation', 0)
        
        if reputation < 500:
            profile_recs.append(ProfileRecommendation(
                category="Community Engagement",
                priority="medium",
                title="Build StackOverflow Reputation",
                description="Higher reputation demonstrates expertise",
                action_items=[
                    "Answer questions in your expertise areas",
                    "Ask well-researched questions",
                    "Earn badges through contributions"
                ],
                impact="Recognized technical authority"
            ))
        
        tags = stackoverflow_data.get('top_tags', [])
        if tags:
            career_insights.append(CareerInsight(
                insight_type="expertise",
                title="Technical Expertise Areas",
                description="Your primary areas of technical expertise",
                evidence=[f"{tag['name']}: {tag['count']} posts" for tag in tags[:5]]
            ))
    
    # Skill gaps analysis
    if github_data and stackoverflow_data:
        gh_langs = set(github_data.get('repositories', {}).get('languages', {}).keys())
        so_tags = set(tag['name'] for tag in stackoverflow_data.get('top_tags', []))
        
        # Common in-demand skills
        in_demand = {'Python', 'JavaScript', 'TypeScript', 'React', 'Node.js', 'Docker', 'Kubernetes'}
        missing_skills = in_demand - gh_langs - so_tags
        
        skill_gaps = list(missing_skills)[:5]
    
    competitive_analysis = {
        "github_percentile": "Top 30% based on activity and repositories",
        "stackoverflow_percentile": "Top 50% based on reputation",
        "overall_ranking": "Above average among developers with similar experience"
    }
    
    return profile_recs, career_insights, skill_gaps, competitive_analysis


@router.post("/scan", response_model=FootprintScanResponse)
async def scan_footprint(
    request: FootprintScanRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Scan digital footprint across platforms
    
    Analyzes:
    - GitHub: Profile, repositories, activity, contributions
    - StackOverflow: Reputation, answers, questions, tags
    - Privacy: Exposed information and risks
    
    Returns comprehensive analysis with scores and recommendations.
    """
    try:
        platforms_scanned = []
        github_data = None
        stackoverflow_data = None
        github_score = None
        stackoverflow_score = None
        
        # GitHub Analysis
        if request.github_username:
            print(f"Analyzing GitHub: {request.github_username}")
            platforms_scanned.append("github")
            
            try:
                analyzer = GitHubAnalyzer()
                gh_result = analyzer.analyze_user(request.github_username)
                
                if gh_result:
                    github_data = gh_result
                    github_score = gh_result.get('scores', {}).get('overall_github_score', 0)
            except ValueError as e:
                # User not found
                print(f"GitHub user not found: {e}")
                raise HTTPException(
                    status_code=404,
                    detail=f"GitHub user '{request.github_username}' not found. Please check the username and try again."
                )
            except Exception as e:
                print(f"GitHub analysis error: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to analyze GitHub profile: {str(e)}"
                )
        
        # StackOverflow Analysis
        if request.stackoverflow_id or request.stackoverflow_name:
            print(f"Analyzing StackOverflow")
            platforms_scanned.append("stackoverflow")
            
            try:
                scanner = StackOverflowScanner()
                
                if request.stackoverflow_id:
                    so_result = scanner.analyze_user(user_id=request.stackoverflow_id)
                else:
                    so_result = scanner.analyze_user(display_name=request.stackoverflow_name)
                
                if so_result:
                    stackoverflow_data = so_result
                    stackoverflow_score = so_result.get('scores', {}).get('overall_stackoverflow_score', 0)
            except Exception as e:
                print(f"StackOverflow analysis error: {e}")
        
        # Calculate overall scores
        scores = [s for s in [github_score, stackoverflow_score] if s is not None]
        overall_visibility = int(sum(scores) / len(scores)) if scores else 0
        professional_score = overall_visibility  # Simplified for now
        
        # Calculate dimension scores from GitHub and StackOverflow data
        visibility_score = 0
        activity_score = 0
        impact_score = 0
        expertise_score = 0
        
        if github_data:
            gh_scores = github_data.get('scores', {})
            # Visibility: Based on profile completeness and public presence
            visibility_score += gh_scores.get('visibility_score', 0)
            # Activity: Based on commits, PRs, issues
            activity_score += gh_scores.get('activity_score', 0)
            # Impact: Based on stars, forks, followers
            impact_score += gh_scores.get('impact_score', 0)
            # Expertise: Based on code quality and repo quality
            expertise_score += gh_scores.get('code_quality_score', 0)
        
        if stackoverflow_data:
            so_scores = stackoverflow_data.get('scores', {})
            # Add StackOverflow contribution to scores
            visibility_score += so_scores.get('visibility_score', 0)
            activity_score += so_scores.get('activity_score', 0)
            impact_score += so_scores.get('impact_score', 0)
            expertise_score += so_scores.get('expertise_score', 0)
        
        # Average the scores if we have multiple platforms
        platform_count = len([p for p in [github_data, stackoverflow_data] if p])
        if platform_count > 0:
            visibility_score = int(visibility_score / platform_count)
            activity_score = int(activity_score / platform_count)
            impact_score = int(impact_score / platform_count)
            expertise_score = int(expertise_score / platform_count)
        
        # Generate privacy report
        privacy_report_data = None
        privacy_risk = None
        if request.include_privacy_analysis:
            privacy_report_obj = generate_privacy_report(github_data, stackoverflow_data)
            privacy_report_data = privacy_report_obj.dict()
            privacy_risk = privacy_report_obj.overall_risk_level.value
        
        # Store in database
        scan_record = {
            'user_id': current_user.id,
            'platforms_scanned': platforms_scanned,
            'github_username': request.github_username,
            'github_data': json.dumps(github_data) if github_data else None,
            'github_score': github_score,
            'stackoverflow_user_id': request.stackoverflow_id,
            'stackoverflow_name': request.stackoverflow_name,
            'stackoverflow_data': json.dumps(stackoverflow_data) if stackoverflow_data else None,
            'stackoverflow_score': stackoverflow_score,
            'overall_visibility_score': overall_visibility,
            'professional_score': professional_score,
            'visibility_score': visibility_score,
            'activity_score': activity_score,
            'impact_score': impact_score,
            'expertise_score': expertise_score,
            'privacy_report': json.dumps(privacy_report_data) if privacy_report_data else None,
            'privacy_risk_level': privacy_risk
        }
        
        scan_id = insert_one('footprint_scans', scan_record)
        
        # Build response
        github_analysis = None
        if github_data:
            profile = github_data.get('profile', {})
            repos = github_data.get('repositories', {})
            activity = github_data.get('activity', {})
            scores_data = github_data.get('scores', {})
            skills_data = repos.get('skills', {})
            
            github_analysis = GitHubAnalysis(
                profile=GitHubProfile(**profile),
                top_repositories=[GitHubRepository(**r) for r in repos.get('top_repos', [])[:5]],
                total_stars=repos.get('total_stars', 0),
                total_forks=repos.get('total_forks', 0),
                languages=repos.get('language_percentages', repos.get('languages', {})),
                language_bytes=repos.get('language_bytes'),
                skills=GitHubSkills(**skills_data) if skills_data else None,
                activity=GitHubActivity(**activity),
                scores=GitHubScores(**scores_data),
                visibility_level=calculate_visibility_level(github_score),
                analyzed_at=datetime.now().isoformat()
            )
        
        stackoverflow_analysis = None
        if stackoverflow_data:
            profile = stackoverflow_data.get('profile', {})
            
            # Build badges object from individual fields
            badges = {
                'gold': profile.get('gold_badges', 0),
                'silver': profile.get('silver_badges', 0),
                'bronze': profile.get('bronze_badges', 0),
                'total': profile.get('gold_badges', 0) + profile.get('silver_badges', 0) + profile.get('bronze_badges', 0)
            }
            
            # Remove badge fields from profile dict
            profile_without_badges = {k: v for k, v in profile.items() if k not in ['gold_badges', 'silver_badges', 'bronze_badges']}
            
            # Map tag fields to model
            mapped_tags = []
            for tag in stackoverflow_data.get('top_tags', [])[:10]:
                mapped_tags.append(StackOverflowTag(
                    name=tag.get('tag_name', ''),
                    count=tag.get('answer_count', 0),
                    score=tag.get('answer_score', 0)
                ))
            
            # Combine answer and question stats for activity
            answers = stackoverflow_data.get('answers', {})
            questions = stackoverflow_data.get('questions', {})
            activity_data = {
                'total_answers': answers.get('total_answers', 0),
                'accepted_answers': answers.get('accepted_answers', 0),
                'total_questions': questions.get('total_questions', 0),
                'answer_score': answers.get('total_score', 0),
                'question_score': questions.get('total_score', 0),
                'total_views': answers.get('total_views', 0) + questions.get('total_views', 0)
            }
            
            stackoverflow_analysis = StackOverflowAnalysis(
                profile=StackOverflowProfile(
                    **profile_without_badges,
                    badges=StackOverflowBadges(**badges)
                ),
                top_tags=mapped_tags,
                activity=StackOverflowActivity(**activity_data),
                scores=StackOverflowScores(**stackoverflow_data.get('scores', {})),
                visibility_level=calculate_visibility_level(stackoverflow_score),
                analyzed_at=stackoverflow_data.get('analyzed_at', datetime.now().isoformat())
            )
        
        response = FootprintScanResponse(
            scan_id=scan_id,
            user_id=current_user.id,
            github_analysis=github_analysis,
            stackoverflow_analysis=stackoverflow_analysis,
            privacy_report=privacy_report_obj if request.include_privacy_analysis else None,
            overall_visibility_score=overall_visibility,
            professional_score=professional_score,
            visibility_score=visibility_score,
            activity_score=activity_score,
            impact_score=impact_score,
            expertise_score=expertise_score,
            scanned_at=datetime.now().isoformat(),
            message=f"Successfully scanned {len(platforms_scanned)} platform(s)"
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to scan footprint: {str(e)}"
        )


@router.get("/recommendations/{scan_id}", response_model=FootprintRecommendationsResponse)
async def get_recommendations(
    scan_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get AI-powered personalized recommendations based on footprint scan
    
    Provides:
    - Profile improvement suggestions (AI-analyzed from README)
    - Career insights based on skills and projects
    - Skill gap analysis with industry trends
    - Competitive positioning
    """
    try:
        # Get scan data
        query = """
            SELECT github_data, stackoverflow_data, recommendations, career_insights
            FROM footprint_scans
            WHERE id = %s AND user_id = %s
        """
        results = execute_query(query, (scan_id, current_user.id))
        
        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan not found"
            )
        
        scan = results[0]
        github_data = json.loads(scan['github_data']) if isinstance(scan['github_data'], str) else scan['github_data']
        stackoverflow_data = json.loads(scan['stackoverflow_data']) if isinstance(scan['stackoverflow_data'], str) else scan['stackoverflow_data']
        
        # Generate AI-powered recommendations
        try:
            from utils.ai_recommendation_generator import AIRecommendationGenerator
            
            # Initialize AI generator
            hf_token = os.getenv('HUGGINGFACE_TOKEN')
            ai_generator = AIRecommendationGenerator(hf_token=hf_token)
            
            # Get README content from github_data
            readme_content = github_data.get('profile_readme') if github_data else None
            
            # Generate AI recommendations
            print(f"🤖 Generating AI-powered recommendations for scan {scan_id}...")
            ai_recommendations = ai_generator.analyze_readme_and_generate_recommendations(
                readme_content=readme_content,
                github_data=github_data,
                stackoverflow_data=stackoverflow_data
            )
            
            # Transform AI recommendations to API format
            profile_recs = [
                ProfileRecommendation(**rec) 
                for rec in ai_recommendations.get('profile_recommendations', [])
            ]
            
            career_insights = [
                CareerInsight(**insight)
                for insight in ai_recommendations.get('career_insights', [])
            ]
            
            skill_gaps = ai_recommendations.get('skill_gaps', [])
            
            print(f"✓ Generated {len(profile_recs)} recommendations, {len(career_insights)} insights")
            
        except Exception as e:
            print(f"⚠️  AI recommendation generation failed: {e}")
            print(f"   Falling back to rule-based recommendations")
            # Fallback to rule-based recommendations
            profile_recs, career_insights, skill_gaps, _ = generate_recommendations(
                github_data,
                stackoverflow_data
            )
        
        # If we still don't have recommendations, check cache as last resort
        if not profile_recs and scan['recommendations']:
            print("  Using cached recommendations as fallback")
            recs_data = scan['recommendations']
            if isinstance(recs_data, str):
                profile_recs_data = json.loads(recs_data)
            else:
                profile_recs_data = recs_data
            
            profile_recs = [ProfileRecommendation(**rec) for rec in profile_recs_data]
            
        if not career_insights and scan['career_insights']:
            insights_data = scan['career_insights']
            if insights_data:
                career_insights_data = json.loads(insights_data) if isinstance(insights_data, str) else insights_data
                career_insights = [CareerInsight(**ins) for ins in career_insights_data]
        
        # Set default competitive analysis if not provided
        competitive_analysis = {
            "github_percentile": "Analyzing your competitive position",
            "stackoverflow_percentile": "Analyzing your competitive position",
            "overall_ranking": "Evaluation in progress"
        }
        
        response = FootprintRecommendationsResponse(
            scan_id=scan_id,
            profile_recommendations=profile_recs,
            career_insights=career_insights,
            skill_gaps=skill_gaps,
            competitive_analysis=competitive_analysis,
            generated_at=datetime.now().isoformat()
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.get("/history", response_model=ScanHistoryResponse)
async def get_scan_history(
    skip: int = 0,
    limit: int = 20,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get user's footprint scan history
    
    Returns paginated list of previous scans with scores and platforms.
    """
    try:
        # Get scans
        query = """
            SELECT 
                id, scanned_at, platforms_scanned,
                overall_visibility_score, professional_score,
                github_score, stackoverflow_score,
                visibility_score, activity_score, impact_score, expertise_score
            FROM footprint_scans
            WHERE user_id = %s
            ORDER BY scanned_at DESC
            LIMIT %s OFFSET %s
        """
        results = execute_query(query, (current_user.id, limit, skip))
        
        # Get total count
        count_query = "SELECT COUNT(*) as count FROM footprint_scans WHERE user_id = %s"
        count_result = execute_query(count_query, (current_user.id,))
        total = count_result[0]['count'] if count_result else 0
        
        # Build response
        scan_items = []
        for scan in results:
            item = ScanHistoryItem(
                scan_id=scan['id'],
                scanned_at=scan['scanned_at'].isoformat() if scan['scanned_at'] else None,
                platforms_scanned=scan['platforms_scanned'] or [],
                overall_visibility_score=scan['overall_visibility_score'],
                professional_score=scan['professional_score'],
                github_score=scan['github_score'],
                stackoverflow_score=scan['stackoverflow_score'],
                visibility_score=scan.get('visibility_score', 0),
                activity_score=scan.get('activity_score', 0),
                impact_score=scan.get('impact_score', 0),
                expertise_score=scan.get('expertise_score', 0)
            )
            scan_items.append(item)
        
        response = ScanHistoryResponse(
            scans=scan_items,
            total=total,
            page=skip // limit + 1 if limit > 0 else 1,
            page_size=limit
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve scan history: {str(e)}"
        )


@router.get("/compare/{scan_id_1}/{scan_id_2}", response_model=FootprintComparisonResponse)
async def compare_scans(
    scan_id_1: int,
    scan_id_2: int,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Compare two footprint scans
    
    Shows progress, improvements, and changes between scans.
    """
    try:
        # Get both scans
        query = """
            SELECT 
                id, scanned_at, overall_visibility_score, professional_score,
                github_score, stackoverflow_score, github_data, stackoverflow_data
            FROM footprint_scans
            WHERE id IN (%s, %s) AND user_id = %s
            ORDER BY scanned_at ASC
        """
        results = execute_query(query, (scan_id_1, scan_id_2, current_user.id))
        
        if len(results) < 2:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or both scans not found"
            )
        
        earlier = results[0]
        later = results[1]
        
        # Calculate time difference
        time_diff = later['scanned_at'] - earlier['scanned_at']
        days = time_diff.days
        
        # Calculate changes
        visibility_change = later['overall_visibility_score'] - earlier['overall_visibility_score']
        professional_change = later['professional_score'] - earlier['professional_score']
        
        # Identify improvements and declines
        improvements = []
        declines = []
        new_achievements = []
        
        if visibility_change > 0:
            improvements.append(f"Overall visibility increased by {visibility_change} points")
        elif visibility_change < 0:
            declines.append(f"Overall visibility decreased by {abs(visibility_change)} points")
        
        if later['github_score'] and earlier['github_score']:
            gh_change = later['github_score'] - earlier['github_score']
            if gh_change > 0:
                improvements.append(f"GitHub score improved by {gh_change} points")
                new_achievements.append("Increased GitHub activity and contributions")
        
        if later['stackoverflow_score'] and earlier['stackoverflow_score']:
            so_change = later['stackoverflow_score'] - earlier['stackoverflow_score']
            if so_change > 0:
                improvements.append(f"StackOverflow score improved by {so_change} points")
                new_achievements.append("Enhanced StackOverflow reputation")
        
        # Generate summary
        if visibility_change > 10:
            summary = f"Great progress! Your online visibility has significantly improved over {days} days."
        elif visibility_change > 0:
            summary = f"Positive trend! Your profile visibility has improved slightly over {days} days."
        elif visibility_change < -10:
            summary = f"Attention needed. Your visibility has declined over {days} days."
        else:
            summary = f"Stable profile. No major changes detected over {days} days."
        
        response = FootprintComparisonResponse(
            previous_scan_id=earlier['id'],
            current_scan_id=later['id'],
            time_between_scans=f"{days} days",
            visibility_change=visibility_change,
            professional_change=professional_change,
            improvements=improvements,
            declines=declines,
            new_achievements=new_achievements,
            summary=summary
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compare scans: {str(e)}"
        )


@router.get("/{scan_id}", response_model=FootprintScanResponse)
async def get_scan_details(
    scan_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get detailed results of a specific footprint scan
    """
    try:
        query = """
            SELECT *
            FROM footprint_scans
            WHERE id = %s AND user_id = %s
        """
        results = execute_query(query, (scan_id, current_user.id))
        
        if not results:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan not found"
            )
        
        scan = results[0]
        
        # Parse stored data (handle JSONB which may already be dicts)
        github_data = scan['github_data'] if isinstance(scan['github_data'], dict) else (json.loads(scan['github_data']) if scan['github_data'] else None)
        stackoverflow_data = scan['stackoverflow_data'] if isinstance(scan['stackoverflow_data'], dict) else (json.loads(scan['stackoverflow_data']) if scan['stackoverflow_data'] else None)
        privacy_data = scan['privacy_report'] if isinstance(scan['privacy_report'], dict) else (json.loads(scan['privacy_report']) if scan['privacy_report'] else None)
        
        # Build GitHub analysis
        github_analysis = None
        if github_data:
            profile = github_data.get('profile', {})
            repos = github_data.get('repositories', {})
            activity = github_data.get('activity', {})
            scores_data = github_data.get('scores', {})
            skills_data = repos.get('skills', {})
            
            github_analysis = GitHubAnalysis(
                profile=GitHubProfile(**profile),
                top_repositories=[GitHubRepository(**r) for r in repos.get('top_repos', [])[:5]],
                total_stars=repos.get('total_stars', 0),
                total_forks=repos.get('total_forks', 0),
                languages=repos.get('language_percentages', repos.get('languages', {})),
                language_bytes=repos.get('language_bytes'),
                skills=GitHubSkills(**skills_data) if skills_data else None,
                activity=GitHubActivity(**activity),
                scores=GitHubScores(**scores_data),
                visibility_level=calculate_visibility_level(scan['github_score']),
                analyzed_at=scan['scanned_at'].isoformat()
            )
        
        # Build StackOverflow analysis
        stackoverflow_analysis = None
        if stackoverflow_data:
            profile = stackoverflow_data.get('profile', {})
            
            # Build badges object from individual fields
            badges = {
                'gold': profile.get('gold_badges', 0),
                'silver': profile.get('silver_badges', 0),
                'bronze': profile.get('bronze_badges', 0),
                'total': profile.get('gold_badges', 0) + profile.get('silver_badges', 0) + profile.get('bronze_badges', 0)
            }
            
            # Remove badge fields from profile dict
            profile_without_badges = {k: v for k, v in profile.items() if k not in ['gold_badges', 'silver_badges', 'bronze_badges']}
            
            # Map tag fields to model
            mapped_tags = []
            for tag in stackoverflow_data.get('top_tags', [])[:10]:
                mapped_tags.append(StackOverflowTag(
                    name=tag.get('tag_name', ''),
                    count=tag.get('answer_count', 0),
                    score=tag.get('answer_score', 0)
                ))
            
            # Combine answer and question stats for activity
            answers = stackoverflow_data.get('answers', {})
            questions = stackoverflow_data.get('questions', {})
            activity_data = {
                'total_answers': answers.get('total_answers', 0),
                'accepted_answers': answers.get('accepted_answers', 0),
                'total_questions': questions.get('total_questions', 0),
                'answer_score': answers.get('total_score', 0),
                'question_score': questions.get('total_score', 0),
                'total_views': answers.get('total_views', 0) + questions.get('total_views', 0)
            }
            
            stackoverflow_analysis = StackOverflowAnalysis(
                profile=StackOverflowProfile(
                    **profile_without_badges,
                    badges=StackOverflowBadges(**badges)
                ),
                top_tags=mapped_tags,
                activity=StackOverflowActivity(**activity_data),
                scores=StackOverflowScores(**stackoverflow_data.get('scores', {})),
                visibility_level=calculate_visibility_level(scan['stackoverflow_score']) if scan['stackoverflow_score'] else VisibilityLevel.NONE,
                analyzed_at=stackoverflow_data.get('analyzed_at', scan['scanned_at'].isoformat())
            )
        
        # Build privacy report
        privacy_report = None
        if privacy_data:
            privacy_report = PrivacyReport(**privacy_data)
        
        response = FootprintScanResponse(
            scan_id=scan['id'],
            user_id=scan['user_id'],
            github_analysis=github_analysis,
            stackoverflow_analysis=stackoverflow_analysis,
            privacy_report=privacy_report,
            overall_visibility_score=scan['overall_visibility_score'],
            professional_score=scan['professional_score'],
            visibility_score=scan.get('visibility_score', 0),
            activity_score=scan.get('activity_score', 0),
            impact_score=scan.get('impact_score', 0),
            expertise_score=scan.get('expertise_score', 0),
            scanned_at=scan['scanned_at'].isoformat(),
            message="Scan details retrieved successfully"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve scan details: {str(e)}"
        )
