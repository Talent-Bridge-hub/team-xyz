"""
Resume Module

Handles resume upload, parsing, analysis, and enhancement.

Features:
- Resume upload (PDF/DOCX)
- Resume parsing and text extraction
- AI-powered resume analysis
- ATS compatibility scoring
- Enhancement suggestions
- Template generation
"""

from .router import router
from .service import ResumeService
from .schemas import (
    # Request schemas
    ResumeAnalysisRequest,
    ResumeEnhancementRequest,
    
    # Response schemas
    ResumeUploadResponse,
    ResumeAnalysisResponse,
    ResumeEnhancementResponse,
    ResumeListResponse,
    ResumeListItem,
    ResumeDeleteResponse,
    
    # Nested schemas
    SectionScore,
    ATSScore,
    EnhancementSuggestion,
    
    # Internal schemas
    ResumeInDB
)
from .models import (
    ResumeQueries,
    resume_row_to_dict,
    resume_row_to_list_item,
    prepare_resume_data,
    prepare_analysis_update
)
from .utils import (
    ResumeParser,
    ResumeAnalyzer,
    ResumeEnhancer,
    ResumeTemplateGenerator,
    calculate_word_count,
    sanitize_filename,
    validate_file_extension
)

__all__ = [
    # Router
    "router",
    
    # Service
    "ResumeService",
    
    # Request schemas
    "ResumeAnalysisRequest",
    "ResumeEnhancementRequest",
    
    # Response schemas
    "ResumeUploadResponse",
    "ResumeAnalysisResponse",
    "ResumeEnhancementResponse",
    "ResumeListResponse",
    "ResumeListItem",
    "ResumeDeleteResponse",
    
    # Nested schemas
    "SectionScore",
    "ATSScore",
    "EnhancementSuggestion",
    
    # Internal schemas
    "ResumeInDB",
    
    # Database functions
    "ResumeQueries",
    "resume_row_to_dict",
    "resume_row_to_list_item",
    "prepare_resume_data",
    "prepare_analysis_update",
    
    # Utility classes
    "ResumeParser",
    "ResumeAnalyzer",
    "ResumeEnhancer",
    "ResumeTemplateGenerator",
    
    # Utility functions
    "calculate_word_count",
    "sanitize_filename",
    "validate_file_extension",
]
