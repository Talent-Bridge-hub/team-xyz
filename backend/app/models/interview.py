"""
Interview Simulator Pydantic Models
Data validation schemas for interview session, questions, answers, and feedback
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class SessionType(str, Enum):
    """Interview session types"""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    MIXED = "mixed"
    JOB_SPECIFIC = "job-specific"


class DifficultyLevel(str, Enum):
    """Difficulty levels"""
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"


class QuestionType(str, Enum):
    """Question types"""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SITUATIONAL = "situational"
    PROBLEM_SOLVING = "problem-solving"


class SessionStatus(str, Enum):
    """Session status"""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class Performance(str, Enum):
    """Overall performance rating"""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    NEEDS_IMPROVEMENT = "needs_improvement"


# Request Models

class InterviewStartRequest(BaseModel):
    """Request to start a new interview session"""
    session_type: SessionType = Field(
        default=SessionType.MIXED,
        description="Type of interview session"
    )
    job_role: str = Field(
        default="Software Engineer",
        description="Target job role"
    )
    difficulty_level: DifficultyLevel = Field(
        default=DifficultyLevel.MID,
        description="Interview difficulty level"
    )
    num_questions: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of questions (1-20)"
    )
    resume_id: Optional[int] = Field(
        None,
        description="Optional resume ID to tailor questions"
    )


class AnswerSubmitRequest(BaseModel):
    """Request to submit an answer"""
    session_id: int = Field(..., description="Interview session ID")
    question_id: int = Field(..., description="Question ID from question bank")
    answer: str = Field(..., min_length=10, description="The candidate's answer (min 10 chars)")
    time_taken_seconds: Optional[int] = Field(None, description="Time taken to answer in seconds")


# Response Models

class QuestionResponse(BaseModel):
    """Interview question details"""
    question_number: int = Field(..., description="Question number in session")
    total_questions: int = Field(..., description="Total questions in session")
    question_id: int = Field(..., description="Question ID from database")
    question_text: str = Field(..., description="The question text")
    question_type: str = Field(..., description="Type of question")
    category: Optional[str] = Field(None, description="Question category")
    difficulty: str = Field(..., description="Difficulty level")


class AnswerScores(BaseModel):
    """Scoring breakdown for an answer"""
    overall: float = Field(..., ge=0, le=100, description="Overall score (0-100)")
    relevance: float = Field(..., ge=0, le=100, description="Relevance to question")
    completeness: float = Field(..., ge=0, le=100, description="Answer completeness")
    clarity: float = Field(..., ge=0, le=100, description="Communication clarity")
    technical_accuracy: float = Field(..., ge=0, le=100, description="Technical correctness")
    communication: float = Field(..., ge=0, le=100, description="Communication quality")


class AnswerFeedback(BaseModel):
    """Detailed feedback for an answer"""
    strengths: List[str] = Field(..., description="What was done well")
    weaknesses: List[str] = Field(..., description="Areas that need improvement")
    missing_points: List[str] = Field(..., description="Key points that were missed")
    suggestions: List[str] = Field(..., description="Actionable improvement suggestions")
    narrative: str = Field(..., description="Narrative feedback summary")


class AnswerResponse(BaseModel):
    """Response after submitting an answer"""
    answer_id: int = Field(..., description="Answer record ID")
    question_number: int = Field(..., description="Question number answered")
    question_text: str = Field(..., description="The question that was answered")
    your_answer: str = Field(..., description="The submitted answer")
    time_taken_seconds: int = Field(..., description="Time taken to answer")
    scores: AnswerScores = Field(..., description="Scoring breakdown")
    feedback: AnswerFeedback = Field(..., description="Detailed feedback")
    sentiment: str = Field(..., description="Detected sentiment (confident/hesitant/neutral)")
    has_more_questions: bool = Field(..., description="Whether there are more questions")


class InterviewStartResponse(BaseModel):
    """Response when starting a new interview session"""
    session_id: int = Field(..., description="New session ID")
    session_type: str = Field(..., description="Type of session")
    job_role: str = Field(..., description="Target job role")
    difficulty_level: str = Field(..., description="Difficulty level")
    total_questions: int = Field(..., description="Total questions in session")
    first_question: Optional[QuestionResponse] = Field(None, description="The first question")
    message: str = Field(..., description="Welcome message")


class SessionRatings(BaseModel):
    """Session performance ratings"""
    technical: int = Field(..., ge=1, le=5, description="Technical skill rating (1-5)")
    communication: int = Field(..., ge=1, le=5, description="Communication rating (1-5)")
    confidence: int = Field(..., ge=1, le=5, description="Confidence rating (1-5)")


class SessionFeedbackDetail(BaseModel):
    """Detailed session feedback"""
    strengths: List[str] = Field(..., description="Overall session strengths")
    areas_to_improve: List[str] = Field(..., description="Areas needing improvement")
    recommended_resources: List[str] = Field(..., description="Learning resources")
    preparation_tips: str = Field(..., description="Personalized preparation tips")
    practice_recommendations: str = Field(..., description="Practice recommendations")


class SessionAverageScores(BaseModel):
    """Average scores across all answers"""
    overall: float = Field(..., ge=0, le=100)
    relevance: float = Field(..., ge=0, le=100)
    completeness: float = Field(..., ge=0, le=100)
    clarity: float = Field(..., ge=0, le=100)
    technical_accuracy: float = Field(..., ge=0, le=100)
    communication: float = Field(..., ge=0, le=100)


class SessionCompletionResponse(BaseModel):
    """Response when completing a session"""
    session_id: int = Field(..., description="Session ID")
    completed: bool = Field(True, description="Whether session is completed")
    questions_answered: int = Field(..., description="Number of questions answered")
    total_time_seconds: int = Field(..., description="Total time for session")
    average_scores: SessionAverageScores = Field(..., description="Average scores")
    performance: str = Field(..., description="Overall performance rating")
    ratings: SessionRatings = Field(..., description="Performance ratings")
    feedback: SessionFeedbackDetail = Field(..., description="Detailed feedback")
    message: str = Field(..., description="Completion message")


class SessionListItem(BaseModel):
    """Summary of an interview session for list view"""
    id: int = Field(..., description="Session ID")
    session_type: str = Field(..., description="Type of session")
    job_role: str = Field(..., description="Target job role")
    difficulty_level: str = Field(..., description="Difficulty level")
    total_questions: int = Field(..., description="Total questions")
    questions_answered: int = Field(..., description="Questions answered")
    average_score: Optional[float] = Field(None, description="Average score")
    status: str = Field(..., description="Session status")
    duration_seconds: Optional[int] = Field(None, description="Session duration")
    started_at: str = Field(..., description="Start timestamp")
    completed_at: Optional[str] = Field(None, description="Completion timestamp")
    overall_performance: Optional[str] = Field(None, description="Performance rating")
    technical_rating: Optional[int] = Field(None, description="Technical rating (1-5)")
    communication_rating: Optional[int] = Field(None, description="Communication rating (1-5)")
    confidence_rating: Optional[int] = Field(None, description="Confidence rating (1-5)")


class SessionListResponse(BaseModel):
    """Paginated list of interview sessions"""
    sessions: List[SessionListItem] = Field(..., description="List of sessions")
    total: int = Field(..., description="Total number of sessions")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Results per page")


class QuestionAnswerPair(BaseModel):
    """A question with its answer for session details"""
    question_number: int = Field(..., description="Question number")
    question_text: str = Field(..., description="The question")
    question_type: str = Field(..., description="Question type")
    user_answer: Optional[str] = Field(None, description="User's answer")
    time_taken_seconds: Optional[int] = Field(None, description="Time taken")
    scores: Optional[AnswerScores] = Field(None, description="Scoring breakdown")
    feedback: Optional[AnswerFeedback] = Field(None, description="Answer feedback")
    sentiment: Optional[str] = Field(None, description="Answer sentiment")


class SessionDetailResponse(BaseModel):
    """Detailed session information with all Q&A"""
    session_id: int = Field(..., description="Session ID")
    session_type: str = Field(..., description="Type of session")
    job_role: str = Field(..., description="Target job role")
    difficulty_level: str = Field(..., description="Difficulty level")
    status: str = Field(..., description="Session status")
    started_at: str = Field(..., description="Start timestamp")
    completed_at: Optional[str] = Field(None, description="Completion timestamp")
    total_questions: int = Field(..., description="Total questions")
    questions_answered: int = Field(..., description="Questions answered")
    duration_seconds: Optional[int] = Field(None, description="Total duration")
    average_scores: Optional[SessionAverageScores] = Field(None, description="Average scores")
    performance: Optional[str] = Field(None, description="Performance rating")
    ratings: Optional[SessionRatings] = Field(None, description="Performance ratings")
    feedback: Optional[SessionFeedbackDetail] = Field(None, description="Session feedback")
    questions_and_answers: List[QuestionAnswerPair] = Field(..., description="All Q&A pairs")


class SessionStatsResponse(BaseModel):
    """User's interview statistics"""
    total_sessions: int = Field(..., description="Total sessions completed")
    total_questions_answered: int = Field(..., description="Total questions answered")
    average_overall_score: float = Field(..., description="Average score across all sessions")
    average_session_duration_minutes: float = Field(..., description="Average session duration")
    performance_distribution: Dict[str, int] = Field(
        ...,
        description="Count of sessions by performance level"
    )
    favorite_job_role: Optional[str] = Field(None, description="Most practiced job role")
    improvement_trend: str = Field(..., description="Score improvement trend (improving/stable/declining)")
