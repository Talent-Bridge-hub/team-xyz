"""
Interview Simulator API
Endpoints for AI-powered interview simulation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
import sys
import os

# Add project root to path for utils access
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from backend.app.models.interview import (
    InterviewStartRequest,
    InterviewStartResponse,
    AnswerSubmitRequest,
    AnswerResponse,
    QuestionResponse,
    SessionCompletionResponse,
    SessionListResponse,
    SessionListItem,
    SessionDetailResponse,
    QuestionAnswerPair,
    SessionStatsResponse,
    AnswerScores,
    AnswerFeedback,
    SessionRatings,
    SessionFeedbackDetail,
    SessionAverageScores
)
from backend.app.models.user import UserResponse
from backend.app.api.deps import get_current_user
from backend.app.core.database import DatabaseWrapper
from utils.interview_simulator import InterviewSimulator
from config.database import execute_query, insert_one, update_one
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/interview", tags=["Interview Simulator"])


def fetch_one(query: str, params: tuple = None):
    """Helper to fetch a single row"""
    try:
        results = execute_query(query, params, fetch=True)
        if not results or len(results) == 0:
            return None
        result_dict = results[0]
        result_tuple = tuple(result_dict.values())
        logger.debug(f"fetch_one: dict keys={list(result_dict.keys())}, tuple length={len(result_tuple)}")
        return result_tuple
    except Exception as e:
        logger.error(f"fetch_one error: {e}, query: {query}, params: {params}")
        return None


def fetch_all(query: str, params: tuple = None):
    """Helper to fetch all rows"""
    try:
        results = execute_query(query, params, fetch=True)
        if not results:
            return []
        return [tuple(row.values()) for row in results]
    except Exception as e:
        logger.error(f"fetch_all error: {e}, query: {query}, params: {params}")
        return []


@router.post("/start", response_model=InterviewStartResponse)
async def start_interview(
    request: InterviewStartRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Start a new interview session
    
    Creates a new interview session and returns the first question.
    Questions are selected from the question bank based on:
    - Session type (technical/behavioral/mixed)
    - Job role
    - Difficulty level
    - Resume context (if provided)
    """
    try:
        # Initialize simulator
        simulator = InterviewSimulator(user_id=current_user.id)
        
        # Start session - handle both enum and string values
        session_type_value = request.session_type.value if hasattr(request.session_type, 'value') else request.session_type
        difficulty_value = request.difficulty_level.value if hasattr(request.difficulty_level, 'value') else request.difficulty_level
        
        session_result = simulator.start_session(
            session_type=session_type_value,
            job_role=request.job_role,
            difficulty_level=difficulty_value,
            num_questions=request.num_questions,
            resume_id=request.resume_id
        )
        
        # Extract first question
        question_data = session_result.get('first_question', {})
        
        # Build response
        response = InterviewStartResponse(
            session_id=session_result['session_id'],
            session_type=request.session_type,
            job_role=request.job_role,
            difficulty_level=request.difficulty_level,
            total_questions=request.num_questions,
            first_question=QuestionResponse(
                question_id=question_data.get('id', 0),
                question_number=1,
                total_questions=request.num_questions,
                question_text=question_data.get('question_text', ''),
                question_type=question_data.get('question_type', 'technical'),
                category=question_data.get('category'),
                difficulty=question_data.get('difficulty_level', request.difficulty_level.value)
            ),
            message=f"Interview session started! You have {request.num_questions} questions to answer. Good luck!"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to start interview: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start interview: {str(e)}"
        )


@router.get("/{session_id}/question", response_model=QuestionResponse)
async def get_next_question(
    session_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get the next question in the interview session
    
    Returns the next unanswered question or indicates if the session is complete.
    """
    try:
        # Verify session belongs to user
        session_query = "SELECT * FROM interview_sessions WHERE id = %s AND user_id = %s"
        session = fetch_one(session_query, (session_id, current_user.id))
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found"
            )
        
        # Check if session is complete
        if session[7] >= session[6]:  # questions_answered >= total_questions
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Interview session is already complete"
            )
        
        # Get next unanswered question
        question_query = """
            SELECT 
                iq.id as interview_question_id,
                iq.question_order,
                qb.id as question_id,
                qb.question_text,
                qb.question_type,
                qb.difficulty_level
            FROM interview_questions iq
            JOIN interview_question_bank qb ON iq.question_id = qb.id
            LEFT JOIN interview_answers ia ON ia.interview_question_id = iq.id
            WHERE iq.session_id = %s AND ia.id IS NULL
            ORDER BY iq.question_order
            LIMIT 1
        """
        question = fetch_one(question_query, (session_id,))
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No more questions available"
            )
        
        response = QuestionResponse(
            question_id=question[2],  # question_id from interview_question_bank
            question_number=question[1],  # question_order
            total_questions=session[6],  # total_questions from session
            question_text=question[3],  # question_text
            question_type=question[4],  # question_type
            category=None,
            difficulty=question[5]  # difficulty_level
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get next question: {str(e)}"
        )


@router.post("/answer", response_model=AnswerResponse)
async def submit_answer(
    request: AnswerSubmitRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Submit an answer to a question
    
    Analyzes the answer using AI and provides:
    - Multi-dimensional scores (relevance, completeness, clarity, etc.)
    - Detailed feedback with strengths and weaknesses
    - Specific suggestions for improvement
    - Indication if more questions remain
    """
    try:
        # Verify session belongs to user
        session_query = "SELECT * FROM interview_sessions WHERE id = %s AND user_id = %s"
        session = fetch_one(session_query, (request.session_id, current_user.id))
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found"
            )
        
        # Verify question exists in session and get interview_question_id
        question_query = """
            SELECT iq.id, iq.question_order, qb.question_text, qb.key_points
            FROM interview_questions iq
            JOIN interview_question_bank qb ON iq.question_id = qb.id
            WHERE qb.id = %s AND iq.session_id = %s
        """
        question = fetch_one(question_query, (request.question_id, request.session_id))
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found in this session"
            )
        
        interview_question_id = question[0]  # iq.id
        
        # Check if already answered
        answer_check = "SELECT id FROM interview_answers WHERE interview_question_id = %s"
        existing = fetch_one(answer_check, (interview_question_id,))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This question has already been answered"
            )
        
        # Get AI analyzer for answer analysis
        from utils.ai_answer_analyzer import AIAnswerAnalyzer
        import os
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
        ai_analyzer = AIAnswerAnalyzer(hf_token=hf_token)
        
        # Analyze the answer
        try:
            logger.info(f"Analyzing answer with AI (token present: {bool(hf_token)})")
            analysis = ai_analyzer.analyze_answer(
                user_answer=request.answer,
                question_text=question[2],  # question_text
                question_data={'key_points': question[3] if question[3] else {}},  # Changed from list to dict
                difficulty_level=session[5],  # difficulty_level (fixed column index!)
                job_role=session[4]  # job_role (fixed column index!)
            )
            logger.info(f"AI analysis complete. Overall score: {analysis.get('overall_score')}, AI generated: {analysis.get('ai_generated', False)}")
        except Exception as e:
            logger.error(f"AI analysis failed: {e}", exc_info=True)
            # Fallback to basic scores
            analysis = {
                'overall_score': 70,
                'relevance_score': 70,
                'completeness_score': 70,
                'clarity_score': 70,
                'technical_accuracy_score': 70,
                'communication_score': 70,
                'strengths': ['Answer provided'],
                'weaknesses': [],
                'missing_points': [],
                'suggestions': ['Consider providing more details'],
                'ai_feedback': 'Answer received and recorded.',
                'sentiment': 'neutral'
            }
        
        # Save answer to database
        from config.database import insert_one
        answer_data = {
            'interview_question_id': interview_question_id,
            'session_id': request.session_id,  # ✅ Add session_id
            'user_answer': request.answer,
            'time_taken_seconds': request.time_taken_seconds if request.time_taken_seconds else 0,
            'overall_score': analysis.get('overall_score', 70),
            'relevance_score': analysis.get('relevance_score', 70),
            'completeness_score': analysis.get('completeness_score', 70),
            'clarity_score': analysis.get('clarity_score', 70),
            'technical_accuracy_score': analysis.get('technical_accuracy_score', 70),
            'communication_score': analysis.get('communication_score', 70),
            'strengths': '|'.join(analysis.get('strengths', [])),
            'weaknesses': '|'.join(analysis.get('weaknesses', [])),
            'missing_points': '|'.join(analysis.get('missing_points', [])),
            'suggestions': '|'.join(analysis.get('suggestions', [])),
            'ai_feedback': analysis.get('ai_feedback', ''),
            'sentiment': analysis.get('sentiment', 'neutral')
        }
        answer_id = insert_one('interview_answers', answer_data)
        
        # Update session progress - don't fetch results (UPDATE doesn't return rows)
        update_query = """
            UPDATE interview_sessions 
            SET questions_answered = questions_answered + 1,
                average_score = (
                    SELECT COALESCE(AVG(overall_score), 0)
                    FROM interview_answers ia
                    JOIN interview_questions iq ON ia.interview_question_id = iq.id
                    WHERE iq.session_id = %s
                )
            WHERE id = %s
        """
        execute_query(update_query, (request.session_id, request.session_id), fetch=False)
        
        # Check if there are more questions
        has_more = (session[7] + 1) < session[6]  # (questions_answered + 1) < total_questions
        
        # Build response with all required fields
        response = AnswerResponse(
            answer_id=answer_id,
            question_number=question[1],
            question_text=question[2],  # question_text from query (index 2, not 3!)
            your_answer=request.answer,  # The submitted answer
            time_taken_seconds=request.time_taken_seconds or 0,  # Time taken (default 0 if not provided)
            scores=AnswerScores(
                overall=analysis.get('overall_score', 70),
                relevance=analysis.get('relevance_score', 70),
                completeness=analysis.get('completeness_score', 70),
                clarity=analysis.get('clarity_score', 70),
                technical_accuracy=analysis.get('technical_accuracy_score', 70),
                communication=analysis.get('communication_score', 70)
            ),
            feedback=AnswerFeedback(
                strengths=analysis.get('strengths', []),
                weaknesses=analysis.get('weaknesses', []),
                missing_points=analysis.get('missing_points', []),
                suggestions=analysis.get('suggestions', []),
                narrative=analysis.get('ai_feedback', '')
            ),
            sentiment=analysis.get('sentiment', 'neutral'),
            has_more_questions=has_more
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit answer: {str(e)}"
        )


@router.post("/{session_id}/complete", response_model=SessionCompletionResponse)
async def complete_session(
    session_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Complete an interview session
    
    Finalizes the session and provides:
    - Overall performance summary
    - Average scores across all dimensions
    - Detailed feedback and recommendations
    - Resources for improvement
    """
    try:
        # Verify session belongs to user
        session_query = "SELECT * FROM interview_sessions WHERE id = %s AND user_id = %s"
        session = fetch_one(session_query, (session_id, current_user.id))
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found"
            )
        
        # Check if already completed
        if session[8] == 'completed':  # status column
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is already completed"
            )
        
        # Calculate average scores from all answers
        scores_query = """
            SELECT 
                AVG(ia.overall_score) as overall_score,
                AVG(ia.relevance_score) as relevance_score,
                AVG(ia.completeness_score) as completeness_score,
                AVG(ia.clarity_score) as clarity_score,
                AVG(ia.technical_accuracy_score) as technical_accuracy_score,
                AVG(ia.communication_score) as communication_score
            FROM interview_answers ia
            JOIN interview_questions iq ON ia.interview_question_id = iq.id
            WHERE iq.session_id = %s
        """
        avg_scores = fetch_one(scores_query, (session_id,))
        
        # Get all answers for analysis
        answers_query = """
            SELECT ia.*, qb.question_type
            FROM interview_answers ia
            JOIN interview_questions iq ON ia.interview_question_id = iq.id
            JOIN interview_question_bank qb ON iq.question_id = qb.id
            WHERE iq.session_id = %s
        """
        answers = fetch_all(answers_query, (session_id,))
        
        # Calculate performance rating
        overall_avg = float(avg_scores[0] or 75)
        if overall_avg >= 85:
            performance = 'excellent'
        elif overall_avg >= 75:
            performance = 'good'
        elif overall_avg >= 60:
            performance = 'average'
        else:
            performance = 'needs_improvement'
        
        # Generate ratings (1-5 scale)
        technical_rating = min(5, max(1, int((float(avg_scores[4] or 70) / 20))))
        communication_rating = min(5, max(1, int((float(avg_scores[5] or 70) / 20))))
        confidence_rating = min(5, max(1, int((overall_avg / 20))))
        
        # Helper function for safe string splitting
        def safe_split(value):
            if value is None:
                return []
            if isinstance(value, list):
                return value
            if isinstance(value, str):
                return [s.strip() for s in value.split('|') if s.strip()]
            return []
        
        # Collect strengths and weaknesses from all answers
        all_strengths = []
        all_weaknesses = []
        for answer in answers:
            strengths_str = answer[11]  # strengths column (index 11)
            weaknesses_str = answer[12]  # weaknesses column (index 12)
            all_strengths.extend(safe_split(strengths_str))
            all_weaknesses.extend(safe_split(weaknesses_str))
        
        # Get unique top items
        key_strengths = list(set(all_strengths))[:5] if all_strengths else ['Completed the interview']
        areas_to_improve = list(set(all_weaknesses))[:5] if all_weaknesses else ['Continue practicing']
        
        # Generic recommendations
        recommended_resources = [
            'LeetCode for technical practice',
            'Cracking the Coding Interview book',
            'System Design Interview resources'
        ]
        
        preparation_tips = f"Focus on {session[4]} questions and practice the STAR method for behavioral questions."  # session[4] = job_role
        practice_recommendations = f"Your performance was {performance}. Continue practicing similar questions at {session[5]} level."  # session[5] = difficulty_level
        
        # Calculate duration
        from datetime import datetime
        started_at = session[11]  # started_at is at index 11, not 5!
        # Handle both datetime objects and string timestamps
        if started_at:
            if isinstance(started_at, str):
                started_at = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            duration_seconds = int((datetime.utcnow() - started_at).total_seconds())
        else:
            duration_seconds = 0
        
        # Update session status
        update_query = """
            UPDATE interview_sessions 
            SET status = 'completed',
                completed_at = NOW(),
                average_score = %s
            WHERE id = %s
        """
        execute_query(update_query, (overall_avg, session_id), fetch=False)
        
        # Build response
        response = SessionCompletionResponse(
            session_id=session_id,
            completed=True,
            questions_answered=session[7],  # questions_answered from session tuple
            total_time_seconds=duration_seconds,
            average_scores=SessionAverageScores(
                overall=overall_avg,
                relevance=float(avg_scores[1] or 70),
                completeness=float(avg_scores[2] or 70),
                clarity=float(avg_scores[3] or 70),
                technical_accuracy=float(avg_scores[4] or 70),
                communication=float(avg_scores[5] or 70)
            ),
            performance=performance,
            ratings=SessionRatings(
                technical=technical_rating,
                communication=communication_rating,
                confidence=confidence_rating
            ),
            feedback=SessionFeedbackDetail(
                strengths=key_strengths,
                areas_to_improve=areas_to_improve,
                recommended_resources=recommended_resources,
                preparation_tips=preparation_tips,
                practice_recommendations=practice_recommendations
            ),
            message=f"Interview completed! You answered {session[7]} questions with an average score of {overall_avg:.1f}%"
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete session: {str(e)}"
        )


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(
    skip: int = 0,
    limit: int = 20,
    session_type: Optional[str] = None,
    session_status: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    List user's interview sessions
    
    Returns paginated list of sessions with:
    - Session metadata
    - Performance scores
    - Completion status
    - Timestamps
    
    Filters:
    - session_type: Filter by type (technical/behavioral/mixed)
    - session_status: Filter by status (in_progress/completed)
    """
    try:
        # Build query with filters
        query = """
            SELECT 
                id, session_type, job_role, difficulty_level,
                total_questions, questions_answered, status,
                average_score, started_at, completed_at
            FROM interview_sessions
            WHERE user_id = %s
        """
        params = [current_user.id]
        
        if session_type:
            query += " AND session_type = %s"
            params.append(session_type)
        
        if session_status:
            query += " AND status = %s"
            params.append(session_status)
        
        query += " ORDER BY started_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, skip])
        
        sessions = fetch_all(query, tuple(params))
        
        # Get total count
        count_query = "SELECT COUNT(*) FROM interview_sessions WHERE user_id = %s"
        count_params = [current_user.id]
        
        if session_type:
            count_query += " AND session_type = %s"
            count_params.append(session_type)
        
        if session_status:
            count_query += " AND status = %s"
            count_params.append(session_status)
        
        total_result = fetch_one(count_query, tuple(count_params))
        total = total_result[0] if total_result else 0
        
        # Build response
        session_items = []
        for session in sessions:
            # Get feedback ratings if completed
            feedback_ratings = None
            if session[6] == 'completed':  # status
                feedback_query = """
                    SELECT overall_performance, technical_rating, 
                           communication_rating, confidence_rating
                    FROM interview_feedback
                    WHERE session_id = %s
                """
                feedback_ratings = fetch_one(feedback_query, (session[0],))
            
            item = SessionListItem(
                id=session[0],
                session_type=session[1],
                job_role=session[2],
                difficulty_level=session[3],
                total_questions=session[4],
                questions_answered=session[5],
                status=session[6],
                average_score=session[7] if session[7] else None,
                duration_seconds=None,  # Not in current query
                started_at=session[8].isoformat() if session[8] else None,
                completed_at=session[9].isoformat() if session[9] else None,
                overall_performance=feedback_ratings[0] if feedback_ratings else None,
                technical_rating=feedback_ratings[1] if feedback_ratings else None,
                communication_rating=feedback_ratings[2] if feedback_ratings else None,
                confidence_rating=feedback_ratings[3] if feedback_ratings else None
            )
            session_items.append(item)
        
        response = SessionListResponse(
            sessions=session_items,
            total=total,
            page=skip // limit + 1 if limit > 0 else 1,
            page_size=limit
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}"
        )


@router.get("/{session_id}", response_model=SessionDetailResponse)
async def get_session_details(
    session_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get detailed information about a specific session
    
    Returns:
    - Session metadata
    - All questions and answers
    - Individual scores for each answer
    - Overall feedback and recommendations
    """
    try:
        # Get session info
        session_query = """
            SELECT 
                id, session_type, job_role, difficulty_level,
                total_questions, questions_answered, status,
                average_score, started_at, completed_at
            FROM interview_sessions
            WHERE id = %s AND user_id = %s
        """
        logger.info(f"[GET_SESSION_DETAILS] Fetching session {session_id} for user {current_user.id}")
        session = fetch_one(session_query, (session_id, current_user.id))
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found"
            )
        
        logger.info(f"[GET_SESSION_DETAILS] Session fetched. Tuple length: {len(session)}, Data: {session}")
        
        # Get questions and answers
        qa_query = """
            SELECT 
                iq.question_order,
                qb.question_text,
                qb.question_type,
                ia.user_answer,
                ia.overall_score,
                ia.relevance_score,
                ia.completeness_score,
                ia.clarity_score,
                ia.technical_accuracy_score,
                ia.communication_score,
                ia.strengths,
                ia.weaknesses,
                ia.missing_points,
                ia.suggestions,
                ia.ai_feedback,
                ia.sentiment,
                ia.time_taken_seconds
            FROM interview_questions iq
            JOIN interview_question_bank qb ON iq.question_id = qb.id
            LEFT JOIN interview_answers ia ON ia.interview_question_id = iq.id
            WHERE iq.session_id = %s
            ORDER BY iq.question_order
        """
        logger.info(f"[GET_SESSION_DETAILS] Fetching Q&A records for session {session_id}")
        qa_records = fetch_all(qa_query, (session_id,))
        logger.info(f"[GET_SESSION_DETAILS] Fetched {len(qa_records)} Q&A records")
        
        # Build Q&A pairs
        qa_pairs = []
        for idx, record in enumerate(qa_records):
            try:
                logger.info(f"[GET_SESSION_DETAILS] Processing Q&A record {idx+1}/{len(qa_records)}, Record length: {len(record)}")
                if record[3]:  # Has answer (user_answer is at index 3 now)
                    # Safely handle string/list conversions
                    def safe_split(value):
                        if value is None:
                            return []
                        if isinstance(value, list):
                            return value
                        if isinstance(value, str):
                            return [s.strip() for s in value.split('|') if s.strip()]
                        return []
                    
                    # Safe index access with defaults
                    def safe_get(index, default=None):
                        return record[index] if len(record) > index else default
                    
                    pair = QuestionAnswerPair(
                        question_number=safe_get(0, 0),
                        question_text=safe_get(1, ''),
                        question_type=safe_get(2, 'general'),
                        user_answer=safe_get(3, ''),
                        time_taken_seconds=safe_get(16, 0),
                        scores=AnswerScores(
                            overall=float(safe_get(4, 70)),
                            relevance=float(safe_get(5, 70)),
                            completeness=float(safe_get(6, 70)),
                            clarity=float(safe_get(7, 70)),
                            technical_accuracy=float(safe_get(8, 70)),
                            communication=float(safe_get(9, 70))
                        ),
                        feedback=AnswerFeedback(
                            strengths=safe_split(safe_get(10)),
                            weaknesses=safe_split(safe_get(11)),
                            missing_points=safe_split(safe_get(12)),
                            suggestions=safe_split(safe_get(13)),
                            narrative=safe_get(14, '') or ''
                        ),
                        sentiment=safe_get(15, 'neutral') or 'neutral'
                    )
                else:
                    # Unanswered question
                    pair = QuestionAnswerPair(
                        question_number=safe_get(0, 0),
                        question_text=safe_get(1, ''),
                        question_type=safe_get(2, 'general'),
                        user_answer=None,
                        time_taken_seconds=None,
                        scores=None,
                        feedback=None,
                        sentiment=None
                    )
                qa_pairs.append(pair)
            except Exception as e:
                logger.error(f"Error building QA pair from record: {e}. Record length: {len(record)}")
                continue  # Skip this record and continue with others
        
        # Get overall feedback if session is completed
        overall_feedback = None
        if session[6] == 'completed':
            feedback_query = """
                SELECT 
                    overall_performance, technical_rating, communication_rating,
                    confidence_rating, key_strengths, areas_to_improve,
                    recommended_resources, preparation_tips, practice_recommendations
                FROM interview_feedback
                WHERE session_id = %s
            """
            feedback_record = fetch_one(feedback_query, (session_id,))
            
            if feedback_record:
                def safe_split(value):
                    if value is None:
                        return []
                    if isinstance(value, list):
                        return value
                    if isinstance(value, str):
                        return [s.strip() for s in value.split('|') if s.strip()]
                    return []
                
                overall_feedback = SessionFeedbackDetail(
                    strengths=safe_split(feedback_record[4]),
                    areas_to_improve=safe_split(feedback_record[5]),
                    recommended_resources=safe_split(feedback_record[6]),
                    preparation_tips=feedback_record[7] if feedback_record[7] else "",
                    practice_recommendations=feedback_record[8] if feedback_record[8] else ""
                )
        
        # Build average scores if available
        avg_scores = None
        if session[7]:
            # Calculate averages from all answers
            avg_query = """
                SELECT 
                    AVG(overall_score),
                    AVG(relevance_score),
                    AVG(completeness_score),
                    AVG(clarity_score),
                    AVG(technical_accuracy_score),
                    AVG(communication_score)
                FROM interview_answers
                WHERE session_id = %s
            """
            avg_record = fetch_one(avg_query, (session_id,))
            logger.info(f"[GET_SESSION_DETAILS] avg_record type: {type(avg_record)}, length: {len(avg_record) if avg_record else 0}, data: {avg_record}")
            
            if avg_record and len(avg_record) >= 6 and avg_record[0]:
                avg_scores = SessionAverageScores(
                    overall=float(avg_record[0]),
                    relevance=float(avg_record[1]),
                    completeness=float(avg_record[2]),
                    clarity=float(avg_record[3]),
                    technical_accuracy=float(avg_record[4]),
                    communication=float(avg_record[5])
                )
        
        # Build response
        try:
            logger.info(f"Building session detail response. Session tuple length: {len(session)}")
            logger.info(f"Questions and answers count: {len(qa_pairs)}")
            
            # Calculate duration from timestamps
            duration_seconds = 0
            if session[8] and session[9]:  # started_at and completed_at
                from datetime import datetime
                started = session[8] if isinstance(session[8], datetime) else datetime.fromisoformat(session[8].replace('Z', '+00:00'))
                completed = session[9] if isinstance(session[9], datetime) else datetime.fromisoformat(session[9].replace('Z', '+00:00'))
                duration_seconds = int((completed - started).total_seconds())
            
            response = SessionDetailResponse(
                session_id=session[0],
                session_type=session[1],
                job_role=session[2],
                difficulty_level=session[3],
                total_questions=session[4],
                questions_answered=session[5],
                status=session[6],
                average_scores=avg_scores,
                questions_and_answers=qa_pairs,
                feedback=overall_feedback,  # Changed from overall_feedback to feedback
                duration_seconds=duration_seconds,
                started_at=session[8].isoformat() if session[8] else None,
                completed_at=session[9].isoformat() if session[9] else None
            )
            
            logger.info(f"Session detail response built successfully for session {session_id}")
        except IndexError as ie:
            logger.error(f"Index error building response. Session length: {len(session)}, Session data: {session}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Session data structure mismatch: {str(ie)}"
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_session_details: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session details: {str(e)}"
        )


@router.get("/stats/overview", response_model=SessionStatsResponse)
async def get_user_stats(
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get user's overall interview statistics
    
    Returns:
    - Total sessions completed
    - Average scores across all sessions
    - Performance distribution
    - Most practiced job roles
    """
    try:
        # Get basic stats
        stats_query = """
            SELECT 
                COUNT(*) as total_sessions,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_sessions,
                COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_sessions,
                AVG(CASE WHEN status = 'completed' THEN average_score END) as avg_score
            FROM interview_sessions
            WHERE user_id = %s
        """
        stats = fetch_one(stats_query, (current_user.id,))
        
        # Get performance distribution
        perf_query = """
            SELECT overall_performance, COUNT(*) 
            FROM interview_feedback
            WHERE session_id IN (
                SELECT id FROM interview_sessions WHERE user_id = %s
            )
            GROUP BY overall_performance
        """
        perf_records = fetch_all(perf_query, (current_user.id,))
        performance_distribution = {record[0]: record[1] for record in perf_records}
        
        # Get top job roles
        roles_query = """
            SELECT job_role, COUNT(*) as count
            FROM interview_sessions
            WHERE user_id = %s AND status = 'completed'
            GROUP BY job_role
            ORDER BY count DESC
            LIMIT 5
        """
        roles_records = fetch_all(roles_query, (current_user.id,))
        top_job_roles = {record[0]: record[1] for record in roles_records}
        
        # Calculate total questions answered
        answered_query = """
            SELECT SUM(questions_answered)
            FROM interview_sessions
            WHERE user_id = %s AND status = 'completed'
        """
        answered_result = fetch_one(answered_query, (current_user.id,))
        total_answered = int(answered_result[0]) if answered_result and answered_result[0] else 0
        
        # Calculate average duration
        duration_query = """
            SELECT AVG(duration_seconds)
            FROM interview_sessions
            WHERE user_id = %s AND status = 'completed' AND duration_seconds IS NOT NULL
        """
        duration_result = fetch_one(duration_query, (current_user.id,))
        avg_duration_minutes = float(duration_result[0] / 60) if duration_result and duration_result[0] else 0.0
        
        # Determine trend (simple: compare last 3 vs previous 3)
        trend_query = """
            SELECT average_score
            FROM interview_sessions
            WHERE user_id = %s AND status = 'completed' AND average_score IS NOT NULL
            ORDER BY completed_at DESC
            LIMIT 6
        """
        trend_scores = fetch_all(trend_query, (current_user.id,))
        
        improvement_trend = "stable"
        if len(trend_scores) >= 4:
            recent_avg = sum([s[0] for s in trend_scores[:3]]) / 3
            older_avg = sum([s[0] for s in trend_scores[3:6]]) / min(3, len(trend_scores[3:6]))
            if recent_avg > older_avg + 5:
                improvement_trend = "improving"
            elif recent_avg < older_avg - 5:
                improvement_trend = "declining"
        
        # Get favorite job role
        favorite_role = list(top_job_roles.keys())[0] if top_job_roles else None
        
        # Build response
        response = SessionStatsResponse(
            total_sessions=stats[0] if stats else 0,
            total_questions_answered=total_answered,
            average_overall_score=float(stats[3]) if stats and stats[3] else 0.0,
            average_session_duration_minutes=avg_duration_minutes,
            performance_distribution=performance_distribution,
            favorite_job_role=favorite_role,
            improvement_trend=improvement_trend
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user stats: {str(e)}"
        )


@router.delete("/{session_id}")
async def delete_session(
    session_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Delete an interview session
    
    Removes the session and all related data:
    - Interview questions
    - Interview answers
    - Interview feedback
    """
    try:
        # Verify session belongs to user
        session_query = "SELECT id FROM interview_sessions WHERE id = %s AND user_id = %s"
        session = fetch_one(session_query, (session_id, current_user.id))
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found"
            )
        
        logger.info(f"Deleting session {session_id} for user {current_user.id}")
        
        # Delete in reverse order of foreign key dependencies
        # 1. Delete answers
        delete_answers = "DELETE FROM interview_answers WHERE interview_question_id IN (SELECT id FROM interview_questions WHERE session_id = %s)"
        execute_query(delete_answers, (session_id,), fetch=False)
        logger.info(f"Deleted answers for session {session_id}")
        
        # 2. Delete questions
        delete_questions = "DELETE FROM interview_questions WHERE session_id = %s"
        execute_query(delete_questions, (session_id,), fetch=False)
        logger.info(f"Deleted questions for session {session_id}")
        
        # 3. Delete feedback
        delete_feedback = "DELETE FROM interview_feedback WHERE session_id = %s"
        execute_query(delete_feedback, (session_id,), fetch=False)
        logger.info(f"Deleted feedback for session {session_id}")
        
        # 4. Delete session
        delete_session_query = "DELETE FROM interview_sessions WHERE id = %s"
        execute_query(delete_session_query, (session_id,), fetch=False)
        logger.info(f"Deleted session {session_id} successfully")
        
        return {"message": "Interview session deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )
