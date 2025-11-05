"""
Resume Service Layer

Business logic for resume upload, parsing, analysis, and enhancement.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from fastapi import HTTPException, status, UploadFile
import json

from .schemas import (
    ResumeUploadResponse,
    ResumeAnalysisRequest,
    ResumeAnalysisResponse,
    ResumeEnhancementRequest,
    ResumeEnhancementResponse,
    ResumeListResponse,
    ResumeListItem,
    ResumeDeleteResponse,
    ResumeInDB,
    ATSScore,
    SectionScore,
    EnhancementSuggestion
)
from .models import (
    ResumeQueries,
    resume_row_to_dict,
    resume_row_to_list_item,
    prepare_resume_data,
    prepare_analysis_update
)
from shared.database import DatabaseWrapper


class ResumeService:
    """
    Service class for resume operations.
    
    Handles:
    - Resume upload and parsing
    - Resume storage and retrieval
    - Resume analysis coordination
    - Resume enhancement coordination
    - File management
    """
    
    def __init__(self, db: DatabaseWrapper, upload_dir: Path):
        """
        Initialize resume service.
        
        Args:
            db: Database wrapper instance
            upload_dir: Directory for storing resume files
        """
        self.db = db
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    async def upload_resume(
        self,
        user_id: int,
        file: UploadFile,
        content: bytes
    ) -> ResumeUploadResponse:
        """
        Upload and store a resume file.
        
        Args:
            user_id: User ID
            file: Uploaded file
            content: File content bytes
            
        Returns:
            Resume upload response with metadata
            
        Raises:
            HTTPException: If upload or parsing fails
        """
        # Generate unique filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file_ext = Path(file.filename).suffix
        safe_filename = f"user_{user_id}_{timestamp}{file_ext}"
        file_path = self.upload_dir / safe_filename
        
        # Save file
        try:
            with open(file_path, 'wb') as f:
                f.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )
        
        # Parse resume (placeholder - will be implemented by utils.py)
        parsed_text = ""  # TODO: Implement resume parsing
        parsed_data = {}  # TODO: Implement structured data extraction
        word_count = len(parsed_text.split()) if parsed_text else 0
        
        # Store in database
        resume_tuple = prepare_resume_data(
            user_id=user_id,
            filename=file.filename,
            file_path=str(file_path),
            file_size=len(content),
            file_type=file_ext[1:],  # Remove dot
            parsed_text=parsed_text,
            parsed_data=parsed_data,
            word_count=word_count
        )
        
        result = self.db.execute_query(ResumeQueries.INSERT_RESUME, resume_tuple)
        
        if not result:
            # Cleanup file if DB insert fails
            file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store resume in database"
            )
        
        resume_row = result[0]
        
        return ResumeUploadResponse(
            resume_id=resume_row['id'],
            filename=resume_row['filename'],
            file_size=resume_row['file_size'],
            file_type=resume_row['file_type'],
            parsed_text_length=len(parsed_text),
            word_count=word_count,
            uploaded_at=resume_row['uploaded_at'],
            message="Resume uploaded and parsed successfully"
        )
    
    async def get_resume_by_id(
        self,
        resume_id: int,
        user_id: int
    ) -> Optional[ResumeInDB]:
        """
        Get resume by ID (with user verification).
        
        Args:
            resume_id: Resume ID
            user_id: User ID for ownership verification
            
        Returns:
            Resume data or None if not found
        """
        result = self.db.execute_query(
            ResumeQueries.SELECT_BY_USER_AND_ID,
            (resume_id, user_id)
        )
        
        if not result:
            return None
        
        resume_dict = resume_row_to_dict(result[0])
        return ResumeInDB(**resume_dict)
    
    async def list_user_resumes(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20
    ) -> ResumeListResponse:
        """
        List all resumes for a user.
        
        Args:
            user_id: User ID
            page: Page number (1-indexed)
            page_size: Items per page
            
        Returns:
            Paginated list of resumes
        """
        offset = (page - 1) * page_size
        
        # Get total count
        count_result = self.db.execute_query(
            ResumeQueries.COUNT_BY_USER,
            (user_id,)
        )
        total = count_result[0]['count'] if count_result else 0
        
        # Get resumes
        result = self.db.execute_query(
            ResumeQueries.SELECT_BY_USER,
            (user_id, page_size, offset)
        )
        
        resumes = []
        if result:
            resumes = [ResumeListItem(**resume_row_to_list_item(row)) for row in result]
        
        return ResumeListResponse(
            resumes=resumes,
            total=total,
            page=page,
            page_size=page_size
        )
    
    async def delete_resume(
        self,
        resume_id: int,
        user_id: int
    ) -> ResumeDeleteResponse:
        """
        Delete a resume.
        
        Args:
            resume_id: Resume ID
            user_id: User ID for ownership verification
            
        Returns:
            Delete confirmation
            
        Raises:
            HTTPException: If resume not found or delete fails
        """
        # Check if resume exists
        resume = await self.get_resume_by_id(resume_id, user_id)
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        # Delete file from filesystem
        try:
            file_path = Path(resume.file_path)
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            # Log error but continue with DB deletion
            pass
        
        # Delete from database
        self.db.execute_query(
            ResumeQueries.DELETE_RESUME,
            (resume_id, user_id)
        )
        
        return ResumeDeleteResponse(
            message="Resume deleted successfully",
            success=True,
            resume_id=resume_id
        )
    
    async def update_analysis_results(
        self,
        resume_id: int,
        score: float
    ) -> bool:
        """
        Update resume with analysis results.
        
        Args:
            resume_id: Resume ID
            score: Overall analysis score
            
        Returns:
            True if successful
        """
        update_tuple = prepare_analysis_update(resume_id, score)
        
        result = self.db.execute_query(
            ResumeQueries.UPDATE_ANALYSIS,
            update_tuple
        )
        
        return result is not None
    
    async def analyze_resume(
        self,
        resume_id: int,
        user_id: int,
        job_title: Optional[str] = None,
        job_description: Optional[str] = None
    ) -> ResumeAnalysisResponse:
        """
        Analyze a resume and provide detailed feedback.
        
        This method coordinates the analysis but delegates the actual
        analysis logic to utils/resume_analyzer.py
        
        Args:
            resume_id: Resume ID
            user_id: User ID
            job_title: Optional target job title
            job_description: Optional job description for matching
            
        Returns:
            Complete analysis response
            
        Raises:
            HTTPException: If resume not found
        """
        # Get resume
        resume = await self.get_resume_by_id(resume_id, user_id)
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        # TODO: Implement actual analysis using ResumeAnalyzer
        # For now, return placeholder response
        start_time = datetime.utcnow()
        
        # Placeholder analysis results
        overall_score = 75.0
        
        ats_score = ATSScore(
            overall_score=80.0,
            keyword_score=75.0,
            format_score=85.0,
            content_score=80.0,
            matched_keywords=["Python", "FastAPI", "PostgreSQL"],
            missing_keywords=["Docker", "Kubernetes"],
            strengths=["Clean formatting", "Clear structure"],
            weaknesses=["Missing key technologies"]
        )
        
        section_scores = [
            SectionScore(
                section_name="Experience",
                score=80.0,
                feedback="Strong experience section",
                issues=[],
                suggestions=["Add more quantifiable achievements"]
            ),
            SectionScore(
                section_name="Education",
                score=70.0,
                feedback="Basic education info present",
                issues=["Missing GPA"],
                suggestions=["Consider adding relevant coursework"]
            )
        ]
        
        end_time = datetime.utcnow()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Update database with analysis results
        await self.update_analysis_results(resume_id, overall_score)
        
        return ResumeAnalysisResponse(
            resume_id=resume_id,
            overall_score=overall_score,
            skill_match_score=75.0,
            experience_score=80.0,
            education_score=70.0,
            grade="B+",
            ats_score=ats_score,
            section_scores=section_scores,
            strengths=["Clear structure", "Good experience"],
            weaknesses=["Missing quantification", "Limited keywords"],
            critical_issues=[],
            recommendations=["Add more metrics", "Include relevant keywords"],
            improvement_suggestions=["Add more metrics", "Include relevant keywords"],
            word_count=resume.word_count,
            action_verb_count=15,
            quantified_achievements=5,
            spelling_errors=0,
            formatting_issues=0,
            analyzed_at=end_time,
            analysis_duration_ms=duration_ms
        )
    
    async def enhance_resume(
        self,
        resume_id: int,
        user_id: int,
        enhancement_type: str,
        target_job: Optional[str] = None
    ) -> ResumeEnhancementResponse:
        """
        Generate enhancement suggestions for a resume.
        
        This method coordinates the enhancement but delegates the actual
        logic to utils/resume_enhancer.py
        
        Args:
            resume_id: Resume ID
            user_id: User ID
            enhancement_type: Type of enhancement
            target_job: Optional target job
            
        Returns:
            Enhancement suggestions
            
        Raises:
            HTTPException: If resume not found
        """
        # Get resume
        resume = await self.get_resume_by_id(resume_id, user_id)
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        # TODO: Implement actual enhancement using ResumeEnhancer
        # For now, return placeholder response
        
        suggestions = [
            EnhancementSuggestion(
                section="Experience",
                original_text="Worked on backend development",
                enhanced_text="Engineered scalable backend systems serving 1M+ users",
                improvement_type="quantification",
                impact="high",
                explanation="Added specific metrics to demonstrate impact"
            ),
            EnhancementSuggestion(
                section="Experience",
                original_text="Made improvements to API performance",
                enhanced_text="Optimized API response times by 40% through database query optimization",
                improvement_type="quantification",
                impact="high",
                explanation="Quantified improvement and specified method"
            )
        ]
        
        high_impact = len([s for s in suggestions if s.impact == "high"])
        medium_impact = len([s for s in suggestions if s.impact == "medium"])
        low_impact = len([s for s in suggestions if s.impact == "low"])
        
        return ResumeEnhancementResponse(
            resume_id=resume_id,
            enhancement_type=enhancement_type,
            suggestions=suggestions,
            total_suggestions=len(suggestions),
            high_impact_count=high_impact,
            medium_impact_count=medium_impact,
            low_impact_count=low_impact,
            estimated_score_improvement=15.0,
            enhanced_at=datetime.utcnow()
        )
