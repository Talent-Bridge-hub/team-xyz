"""
Footprint Scanner Models
Pydantic models for digital footprint analysis (GitHub, StackOverflow, etc.)
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class VisibilityLevel(str, Enum):
    """Online visibility level"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class PrivacyRisk(str, Enum):
    """Privacy risk level"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SAFE = "safe"


class PlatformType(str, Enum):
    """Social/professional platform type"""
    GITHUB = "github"
    STACKOVERFLOW = "stackoverflow"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    OTHER = "other"


# ==================== REQUEST MODELS ====================

class FootprintScanRequest(BaseModel):
    """Request to scan digital footprint"""
    github_username: Optional[str] = Field(None, description="GitHub username")
    stackoverflow_id: Optional[int] = Field(None, description="StackOverflow user ID")
    stackoverflow_name: Optional[str] = Field(None, description="StackOverflow display name")
    linkedin_url: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL")
    include_privacy_analysis: bool = Field(True, description="Include privacy risk assessment")


# ==================== GITHUB MODELS ====================

class GitHubRepository(BaseModel):
    """GitHub repository details"""
    name: str = Field(..., description="Repository name")
    description: Optional[str] = Field(None, description="Repository description")
    language: Optional[str] = Field(None, description="Primary programming language")
    stars: int = Field(..., description="Number of stars")
    forks: int = Field(..., description="Number of forks")
    url: str = Field(..., description="Repository URL")
    updated_at: str = Field(..., description="Last update timestamp")
    has_readme: bool = Field(..., description="Has README file")
    has_license: bool = Field(..., description="Has license")


class GitHubProfile(BaseModel):
    """GitHub profile information"""
    username: str = Field(..., description="GitHub username")
    name: Optional[str] = Field(None, description="Full name")
    bio: Optional[str] = Field(None, description="Biography")
    location: Optional[str] = Field(None, description="Location")
    company: Optional[str] = Field(None, description="Company")
    blog_url: Optional[str] = Field(None, description="Blog/website URL")
    email: Optional[str] = Field(None, description="Public email")
    public_repos: int = Field(..., description="Number of public repositories")
    followers: int = Field(..., description="Number of followers")
    following: int = Field(..., description="Number following")
    account_created_at: str = Field(..., description="Account creation date")


class GitHubActivity(BaseModel):
    """GitHub activity metrics"""
    total_events: int = Field(..., description="Total public events")
    commits: int = Field(..., description="Number of commits")
    pull_requests: int = Field(..., description="Number of pull requests")
    issues: int = Field(..., description="Number of issues")
    reviews: int = Field(..., description="Number of code reviews")
    activity_streak: int = Field(..., description="Current activity streak (days)")
    active_days: int = Field(..., description="Total active days in period")


class GitHubScores(BaseModel):
    """GitHub scoring metrics"""
    code_quality_score: int = Field(..., ge=0, le=100, description="Code quality score (0-100)")
    activity_score: int = Field(..., ge=0, le=100, description="Activity score (0-100)")
    impact_score: int = Field(..., ge=0, le=100, description="Impact score (0-100)")
    overall_github_score: int = Field(..., ge=0, le=100, description="Overall GitHub score (0-100)")


class GitHubSkills(BaseModel):
    """Extracted skills from GitHub repositories"""
    frameworks: Dict[str, int] = Field(default_factory=dict, description="Frameworks and libraries used")
    databases: Dict[str, int] = Field(default_factory=dict, description="Database technologies")
    tools: Dict[str, int] = Field(default_factory=dict, description="Development tools and platforms")


class GitHubAnalysis(BaseModel):
    """Complete GitHub analysis"""
    profile: GitHubProfile
    top_repositories: List[GitHubRepository]
    total_stars: int = Field(..., description="Total stars across all repos")
    total_forks: int = Field(..., description="Total forks across all repos")
    languages: Dict[str, float] = Field(..., description="Programming languages by percentage")
    language_bytes: Optional[Dict[str, int]] = Field(None, description="Languages by bytes of code")
    skills: Optional[GitHubSkills] = Field(None, description="Extracted skills and technologies")
    activity: GitHubActivity
    scores: GitHubScores
    visibility_level: VisibilityLevel
    analyzed_at: str = Field(..., description="Analysis timestamp")


# ==================== STACKOVERFLOW MODELS ====================

class StackOverflowBadges(BaseModel):
    """StackOverflow badge counts"""
    gold: int = Field(..., description="Gold badges")
    silver: int = Field(..., description="Silver badges")
    bronze: int = Field(..., description="Bronze badges")
    total: int = Field(..., description="Total badges")


class StackOverflowTag(BaseModel):
    """StackOverflow expertise tag"""
    name: str = Field(..., description="Tag name")
    count: int = Field(..., description="Number of posts with this tag")
    score: int = Field(..., description="Total score for this tag")


class StackOverflowProfile(BaseModel):
    """StackOverflow profile information"""
    user_id: int = Field(..., description="StackOverflow user ID")
    display_name: str = Field(..., description="Display name")
    reputation: int = Field(..., description="Reputation score")
    location: Optional[str] = Field(None, description="Location")
    website_url: Optional[str] = Field(None, description="Website URL")
    profile_link: str = Field(..., description="StackOverflow profile link")
    badges: StackOverflowBadges
    creation_date: str = Field(..., description="Account creation date")
    last_access_date: str = Field(..., description="Last access date")


class StackOverflowActivity(BaseModel):
    """StackOverflow activity metrics"""
    total_answers: int = Field(..., description="Total answers posted")
    accepted_answers: int = Field(..., description="Accepted answers")
    total_questions: int = Field(..., description="Total questions asked")
    answer_score: int = Field(..., description="Total answer score")
    question_score: int = Field(..., description="Total question score")
    total_views: int = Field(..., description="Total post views")


class StackOverflowScores(BaseModel):
    """StackOverflow scoring metrics"""
    expertise_score: int = Field(..., ge=0, le=100, description="Expertise score (0-100)")
    helpfulness_score: int = Field(..., ge=0, le=100, description="Helpfulness score (0-100)")
    community_score: int = Field(..., ge=0, le=100, description="Community engagement (0-100)")
    overall_stackoverflow_score: int = Field(..., ge=0, le=100, description="Overall SO score (0-100)")


class StackOverflowAnalysis(BaseModel):
    """Complete StackOverflow analysis"""
    profile: StackOverflowProfile
    top_tags: List[StackOverflowTag]
    activity: StackOverflowActivity
    scores: StackOverflowScores
    visibility_level: VisibilityLevel
    analyzed_at: str = Field(..., description="Analysis timestamp")


# ==================== PRIVACY MODELS ====================

class PrivacyIssue(BaseModel):
    """Privacy concern or issue"""
    severity: PrivacyRisk = Field(..., description="Risk severity level")
    category: str = Field(..., description="Issue category")
    description: str = Field(..., description="Issue description")
    recommendation: str = Field(..., description="How to address this issue")
    platform: PlatformType = Field(..., description="Platform where issue was found")


class PrivacyReport(BaseModel):
    """Privacy analysis report"""
    overall_risk_level: PrivacyRisk = Field(..., description="Overall privacy risk")
    issues_found: List[PrivacyIssue] = Field(..., description="Privacy issues identified")
    exposed_information: List[str] = Field(..., description="Publicly exposed information")
    visibility_score: int = Field(..., ge=0, le=100, description="Online visibility (0-100)")
    recommendations: List[str] = Field(..., description="Privacy recommendations")


# ==================== RECOMMENDATIONS MODELS ====================

class ProfileRecommendation(BaseModel):
    """Profile improvement recommendation"""
    category: str = Field(..., description="Recommendation category")
    priority: str = Field(..., description="Priority: high/medium/low")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed description")
    action_items: List[str] = Field(..., description="Specific action items")
    impact: str = Field(..., description="Expected impact")


class CareerInsight(BaseModel):
    """Career-related insight"""
    insight_type: str = Field(..., description="Type of insight")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Insight description")
    evidence: List[str] = Field(..., description="Supporting evidence")


# ==================== RESPONSE MODELS ====================

class FootprintScanResponse(BaseModel):
    """Complete footprint scan results"""
    scan_id: int = Field(..., description="Scan ID")
    user_id: int = Field(..., description="User who performed the scan")
    github_analysis: Optional[GitHubAnalysis] = Field(None, description="GitHub analysis")
    stackoverflow_analysis: Optional[StackOverflowAnalysis] = Field(None, description="StackOverflow analysis")
    privacy_report: Optional[PrivacyReport] = Field(None, description="Privacy assessment")
    overall_visibility_score: int = Field(..., ge=0, le=100, description="Overall visibility (0-100)")
    professional_score: int = Field(..., ge=0, le=100, description="Professional presence (0-100)")
    visibility_score: int = Field(0, ge=0, le=100, description="Visibility dimension score (0-100)")
    activity_score: int = Field(0, ge=0, le=100, description="Activity dimension score (0-100)")
    impact_score: int = Field(0, ge=0, le=100, description="Impact dimension score (0-100)")
    expertise_score: int = Field(0, ge=0, le=100, description="Expertise dimension score (0-100)")
    scanned_at: str = Field(..., description="Scan timestamp")
    message: str = Field(..., description="Status message")


class FootprintRecommendationsResponse(BaseModel):
    """Personalized recommendations"""
    scan_id: int = Field(..., description="Related scan ID")
    profile_recommendations: List[ProfileRecommendation] = Field(..., description="Profile improvements")
    career_insights: List[CareerInsight] = Field(..., description="Career insights")
    skill_gaps: List[str] = Field(..., description="Identified skill gaps")
    competitive_analysis: Dict[str, str] = Field(..., description="How you compare to peers")
    generated_at: str = Field(..., description="Generation timestamp")


class ScanHistoryItem(BaseModel):
    """Footprint scan history item"""
    scan_id: int = Field(..., description="Scan ID")
    scanned_at: str = Field(..., description="Scan timestamp")
    platforms_scanned: List[str] = Field(..., description="Platforms included")
    overall_visibility_score: int = Field(..., description="Overall visibility score")
    professional_score: int = Field(..., description="Professional score")
    github_score: Optional[int] = Field(None, description="GitHub score")
    stackoverflow_score: Optional[int] = Field(None, description="StackOverflow score")
    visibility_score: int = Field(0, description="Visibility dimension score")
    activity_score: int = Field(0, description="Activity dimension score")
    impact_score: int = Field(0, description="Impact dimension score")
    expertise_score: int = Field(0, description="Expertise dimension score")


class ScanHistoryResponse(BaseModel):
    """List of footprint scans"""
    scans: List[ScanHistoryItem] = Field(..., description="Scan history")
    total: int = Field(..., description="Total number of scans")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Results per page")


class FootprintComparisonResponse(BaseModel):
    """Compare two scans"""
    previous_scan_id: int = Field(..., description="Earlier scan ID")
    current_scan_id: int = Field(..., description="Later scan ID")
    time_between_scans: str = Field(..., description="Time elapsed between scans")
    visibility_change: int = Field(..., description="Change in visibility score")
    professional_change: int = Field(..., description="Change in professional score")
    improvements: List[str] = Field(..., description="Areas that improved")
    declines: List[str] = Field(..., description="Areas that declined")
    new_achievements: List[str] = Field(..., description="New achievements")
    summary: str = Field(..., description="Overall comparison summary")
