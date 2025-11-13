"""
Pydantic models for Resume API
Request/response schemas for resume review endpoints
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========== Request Models ==========

class ResumeUploadResponse(BaseModel):
    """Response after uploading a resume"""
    resume_id: int
    filename: str
    file_size: int
    file_type: str
    parsed_text_length: int
    word_count: int
    uploaded_at: datetime
    message: str = "Resume uploaded and parsed successfully"


class ResumeAnalysisRequest(BaseModel):
    """Request for resume analysis"""
    resume_id: int = Field(..., description="ID of uploaded resume")
    job_title: Optional[str] = Field(None, description="Target job title for optimization")
    job_description: Optional[str] = Field(None, description="Job description to match against")


class ResumeEnhancementRequest(BaseModel):
    """Request for resume enhancement suggestions"""
    resume_id: int = Field(..., description="ID of uploaded resume")
    enhancement_type: str = Field(
        "full", 
        description="Type of enhancement: 'full', 'grammar', 'action_verbs', 'quantify'"
    )
    target_job: Optional[str] = Field(None, description="Target job for tailored enhancements")
    
    @validator('enhancement_type')
    def validate_enhancement_type(cls, v):
        """Validate enhancement type"""
        allowed = ['full', 'grammar', 'action_verbs', 'quantify', 'ats_optimize']
        if v not in allowed:
            raise ValueError(f'Enhancement type must be one of: {", ".join(allowed)}')
        return v


class ResumeEnhancementDownloadRequest(BaseModel):
    """Request for downloading enhanced resume (resume_id in URL path)"""
    enhancement_type: str = Field("full", description="Type of enhancement: full, grammar, action_verbs, quantify, ats_optimize")
    target_job: Optional[str] = Field(None, description="Optional target job for tailored improvements")
    selected_improvements: Optional[List[str]] = Field(None, description="Optional list of specific improvement IDs to apply")


class CoverLetterRequest(BaseModel):
    """Request for generating a cover letter"""
    resume_id: int = Field(..., description="ID of the resume to use")
    job_title: str = Field(..., description="Job title/position")
    company: str = Field(..., description="Company name")
    job_description: str = Field(..., description="Job description text")
    tone: str = Field("professional", description="Tone: professional, enthusiastic, formal, conversational")
    length: str = Field("medium", description="Length: short, medium, long")
    highlights: Optional[List[str]] = Field(None, description="Specific achievements to emphasize")
    
    @validator('tone')
    def validate_tone(cls, v):
        allowed = ['professional', 'enthusiastic', 'formal', 'conversational']
        if v not in allowed:
            raise ValueError(f'Tone must be one of: {", ".join(allowed)}')
        return v
    
    @validator('length')
    def validate_length(cls, v):
        allowed = ['short', 'medium', 'long']
        if v not in allowed:
            raise ValueError(f'Length must be one of: {", ".join(allowed)}')
        return v


class CoverLetterResponse(BaseModel):
    """Response containing generated cover letter"""
    cover_letter: str
    word_count: int
    sections: Dict[str, str]
    suggestions: List[str]
    metadata: Dict[str, Any]
    enhancement_type: str = Field(
        "full", 
        description="Type of enhancement: 'full', 'grammar', 'action_verbs', 'quantify'"
    )
    target_job: Optional[str] = Field(None, description="Target job for tailored enhancements")
    selected_improvements: Optional[List[str]] = Field(None, description="List of specific improvements to apply")
    
    @validator('enhancement_type')
    def validate_enhancement_type(cls, v):
        """Validate enhancement type"""
        allowed = ['full', 'grammar', 'action_verbs', 'quantify', 'ats_optimize']
        if v not in allowed:
            raise ValueError(f'Enhancement type must be one of: {", ".join(allowed)}')
        return v


# ========== Response Models ==========

class SectionScore(BaseModel):
    """Score for a resume section"""
    section_name: str
    score: float = Field(..., ge=0, le=100)
    feedback: str
    issues: List[str] = []
    suggestions: List[str] = []


class ATSScore(BaseModel):
    """ATS (Applicant Tracking System) compatibility score"""
    overall_score: float = Field(..., ge=0, le=100)
    keyword_score: float = Field(..., ge=0, le=100)
    format_score: float = Field(..., ge=0, le=100)
    content_score: float = Field(..., ge=0, le=100)
    matched_keywords: List[str] = []
    missing_keywords: List[str] = []
    strengths: List[str] = []
    weaknesses: List[str] = []


class ResumeAnalysisResponse(BaseModel):
    """Complete resume analysis response"""
    resume_id: int
    overall_score: float = Field(..., ge=0, le=100)
    skill_match_score: float = Field(default=75.0, ge=0, le=100)
    experience_score: float = Field(default=75.0, ge=0, le=100)
    education_score: float = Field(default=75.0, ge=0, le=100)
    grade: str  # A+, A, B+, B, C+, C, D, F
    ats_score: ATSScore
    section_scores: List[SectionScore]
    
    # Key findings
    strengths: List[str]
    weaknesses: List[str]
    critical_issues: List[str]
    recommendations: List[str]
    improvement_suggestions: List[str] = []  # Alias for recommendations
    
    # Detailed metrics
    word_count: int
    action_verb_count: int
    quantified_achievements: int
    spelling_errors: int
    formatting_issues: int
    
    # Metadata
    analyzed_at: datetime
    analysis_duration_ms: int


class EnhancementSuggestion(BaseModel):
    """A single enhancement suggestion"""
    section: str
    original_text: str
    enhanced_text: str
    improvement_type: str  # 'action_verb', 'quantification', 'grammar', 'tone', 'ats'
    impact: str  # 'high', 'medium', 'low'
    explanation: str


class ResumeEnhancementResponse(BaseModel):
    """Resume enhancement suggestions response"""
    resume_id: int
    enhancement_type: str
    suggestions: List[EnhancementSuggestion]
    
    # Summary
    total_suggestions: int
    high_impact_count: int
    medium_impact_count: int
    low_impact_count: int
    
    # Estimated improvement
    estimated_score_improvement: float = Field(..., description="Estimated score increase if applied")
    
    # Metadata
    enhanced_at: datetime


class ResumeListItem(BaseModel):
    """Resume item in list view"""
    resume_id: int
    filename: str
    uploaded_at: datetime
    last_analyzed: Optional[datetime]
    last_score: Optional[float]
    word_count: int
    file_type: str


class ResumeListResponse(BaseModel):
    """List of user's resumes"""
    resumes: List[ResumeListItem]
    total: int
    page: int
    page_size: int


class ResumeDeleteResponse(BaseModel):
    """Response after deleting a resume"""
    message: str
    success: bool = True
    resume_id: int


# ========== Database Models (Internal) ==========

class ResumeInDB(BaseModel):
    """Resume as stored in database"""
    id: int
    user_id: int
    filename: str
    file_path: str
    file_size: int
    file_type: str
    parsed_text: str
    parsed_data: Optional[Dict[str, Any]]  # JSON field with sections, metadata
    word_count: int
    uploaded_at: datetime
    last_analyzed: Optional[datetime]
    last_score: Optional[float]
    
    class Config:
        from_attributes = True
