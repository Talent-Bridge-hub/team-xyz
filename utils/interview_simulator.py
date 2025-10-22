"""
AI Interview Simulator Module for UtopiaHire
Simulates job interviews with AI-powered question selection and answer analysis

WHY THIS MODULE:
- Help job seekers practice interviews in a safe environment
- Build confidence before real interviews
- Get instant feedback on answers
- Identify strengths and areas for improvement
- Track progress over time
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random
import json

from config.database import execute_query, insert_one, update_one
from utils.answer_analyzer import AnswerAnalyzer
from utils.ai_answer_analyzer import AIAnswerAnalyzer
from utils.resume_parser import ResumeParser

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InterviewSimulator:
    """
    Simulate job interviews with AI-powered analysis
    """
    
    def __init__(self, user_id: Optional[int] = None, use_ai: bool = True):
        """
        Initialize the interview simulator
        
        Args:
            user_id: Optional user ID for session tracking
            use_ai: Whether to use AI-powered analysis (default: True)
        """
        self.user_id = user_id
        self.use_ai = use_ai
        
        # Initialize analyzers
        if use_ai:
            try:
                self.ai_analyzer = AIAnswerAnalyzer()
                logger.info("AI analyzer initialized successfully")
            except Exception as e:
                logger.warning(f"AI analyzer failed to initialize: {e}. Falling back to basic analyzer.")
                self.use_ai = False
                self.analyzer = AnswerAnalyzer()
        else:
            self.analyzer = AnswerAnalyzer()
        
        self.current_session = None
        logger.info(f"Interview simulator initialized (AI: {self.use_ai})")
    
    def start_session(
        self,
        session_type: str = 'mixed',
        job_role: str = 'Software Engineer',
        difficulty_level: str = 'mid',
        num_questions: int = 5,
        resume_id: Optional[int] = None
    ) -> Dict:
        """
        Start a new interview session
        
        Args:
            session_type: 'technical', 'behavioral', 'mixed', or 'job-specific'
            job_role: Target job role (e.g., 'Software Engineer')
            difficulty_level: 'junior', 'mid', or 'senior'
            num_questions: Number of questions to ask
            resume_id: Optional resume ID to tailor questions
        
        Returns:
            Session information dictionary
        """
        logger.info(f"Starting {session_type} interview session for {job_role} ({difficulty_level})")
        
        # Create session record
        session_data = {
            'user_id': self.user_id,
            'resume_id': resume_id,
            'session_type': session_type,
            'job_role': job_role,
            'difficulty_level': difficulty_level,
            'total_questions': num_questions,
            'questions_answered': 0,
            'status': 'in_progress'
        }
        
        session_id = insert_one('interview_sessions', session_data)
        
        # Select questions
        questions = self._select_questions(
            session_type=session_type,
            job_role=job_role,
            difficulty_level=difficulty_level,
            num_questions=num_questions,
            resume_id=resume_id
        )
        
        # Record questions in database
        for idx, question in enumerate(questions, 1):
            insert_one('interview_questions', {
                'session_id': session_id,
                'question_id': question['id'],
                'question_order': idx
            })
        
        self.current_session = {
            'session_id': session_id,
            'questions': questions,
            'current_question_index': 0,
            'start_time': datetime.now()
        }
        
        return {
            'session_id': session_id,
            'session_type': session_type,
            'job_role': job_role,
            'difficulty_level': difficulty_level,
            'total_questions': num_questions,
            'first_question': questions[0] if questions else None
        }
    
    def get_next_question(self) -> Optional[Dict]:
        """
        Get the next question in the current session
        
        Returns:
            Question dictionary or None if session complete
        """
        if not self.current_session:
            logger.warning("No active session")
            return None
        
        idx = self.current_session['current_question_index']
        questions = self.current_session['questions']
        
        if idx >= len(questions):
            logger.info("All questions answered")
            return None
        
        question = questions[idx]
        self.current_session['question_start_time'] = datetime.now()
        
        return {
            'question_number': idx + 1,
            'total_questions': len(questions),
            'question_id': question['id'],
            'question_text': question['question_text'],
            'question_type': question['question_type'],
            'category': question.get('category', ''),
            'difficulty': question.get('difficulty_level', 'mid')
        }
    
    def submit_answer(self, answer: str) -> Dict:
        """
        Submit answer to current question and get feedback
        
        Args:
            answer: The user's answer text
        
        Returns:
            Analysis results with feedback
        """
        if not self.current_session:
            raise ValueError("No active session")
        
        idx = self.current_session['current_question_index']
        questions = self.current_session['questions']
        
        if idx >= len(questions):
            raise ValueError("All questions already answered")
        
        question = questions[idx]
        
        # Calculate time taken
        question_start = self.current_session.get('question_start_time', datetime.now())
        time_taken = int((datetime.now() - question_start).total_seconds())
        
        # Analyze the answer using AI or basic analyzer
        if self.use_ai:
            try:
                analysis = self.ai_analyzer.analyze_answer(
                    user_answer=answer,
                    question_text=question.get('question_text', ''),
                    question_data=question,
                    difficulty_level=self.current_session.get('difficulty_level', 'mid'),
                    job_role=self.current_session.get('job_role', 'Software Engineer')
                )
                logger.info(f"AI analysis complete (score: {analysis['overall_score']})")
            except Exception as e:
                logger.error(f"AI analysis failed: {e}. Using fallback analyzer.")
                analysis = self.analyzer.analyze_answer(
                    user_answer=answer,
                    question_data=question,
                    difficulty_level=self.current_session.get('difficulty_level', 'mid')
                )
        else:
            analysis = self.analyzer.analyze_answer(
                user_answer=answer,
                question_data=question,
                difficulty_level=self.current_session.get('difficulty_level', 'mid')
            )
        
        # Get the interview_question record ID
        interview_question = execute_query(
            """
            SELECT id FROM interview_questions 
            WHERE session_id = %s AND question_order = %s
            """,
            (self.current_session['session_id'], idx + 1)
        )
        
        if not interview_question:
            raise ValueError("Interview question record not found")
        
        interview_question_id = interview_question[0]['id']
        
        # Store answer and analysis
        answer_data = {
            'interview_question_id': interview_question_id,
            'session_id': self.current_session['session_id'],
            'user_answer': answer,
            'time_taken_seconds': time_taken,
            'relevance_score': analysis['relevance_score'],
            'completeness_score': analysis['completeness_score'],
            'clarity_score': analysis['clarity_score'],
            'technical_accuracy_score': analysis['technical_accuracy_score'],
            'communication_score': analysis['communication_score'],
            'overall_score': analysis['overall_score'],
            'strengths': json.dumps(analysis['strengths']),
            'weaknesses': json.dumps(analysis['weaknesses']),
            'missing_points': json.dumps(analysis['missing_points']),
            'suggestions': json.dumps(analysis['suggestions']),
            'ai_feedback': analysis['ai_feedback'],
            'word_count': analysis['word_count'],
            'sentiment': analysis['sentiment']
        }
        
        answer_id = insert_one('interview_answers', answer_data)
        
        # Update session progress
        self.current_session['current_question_index'] += 1
        
        update_one(
            'interview_sessions',
            {'questions_answered': idx + 1},
            {'id': self.current_session['session_id']}
        )
        
        # Return analysis with question context
        return {
            'answer_id': answer_id,
            'question_number': idx + 1,
            'question_text': question['question_text'],
            'your_answer': answer,
            'time_taken_seconds': time_taken,
            'scores': {
                'overall': analysis['overall_score'],
                'relevance': analysis['relevance_score'],
                'completeness': analysis['completeness_score'],
                'clarity': analysis['clarity_score'],
                'technical_accuracy': analysis['technical_accuracy_score'],
                'communication': analysis['communication_score']
            },
            'feedback': {
                'strengths': analysis['strengths'],
                'weaknesses': analysis['weaknesses'],
                'missing_points': analysis['missing_points'],
                'suggestions': analysis['suggestions'],
                'narrative': analysis['ai_feedback']
            },
            'sentiment': analysis['sentiment'],
            'has_more_questions': idx + 1 < len(questions)
        }
    
    def complete_session(self) -> Dict:
        """
        Complete the current interview session and generate summary
        
        Returns:
            Session summary with overall feedback
        """
        if not self.current_session:
            raise ValueError("No active session")
        
        session_id = self.current_session['session_id']
        
        # Get all answers for this session
        answers = execute_query(
            """
            SELECT 
                overall_score,
                relevance_score,
                completeness_score,
                clarity_score,
                technical_accuracy_score,
                communication_score,
                time_taken_seconds,
                sentiment
            FROM interview_answers
            WHERE session_id = %s
            ORDER BY answer_timestamp
            """,
            (session_id,)
        )
        
        if not answers:
            raise ValueError("No answers found for session")
        
        # Calculate session statistics
        num_answers = len(answers)
        avg_overall = sum(a['overall_score'] for a in answers) / num_answers
        avg_relevance = sum(a['relevance_score'] for a in answers) / num_answers
        avg_completeness = sum(a['completeness_score'] for a in answers) / num_answers
        avg_clarity = sum(a['clarity_score'] for a in answers) / num_answers
        avg_technical = sum(a['technical_accuracy_score'] for a in answers) / num_answers
        avg_communication = sum(a['communication_score'] for a in answers) / num_answers
        total_time = sum(a['time_taken_seconds'] for a in answers)
        
        # Performance rating
        if avg_overall >= 85:
            performance = 'excellent'
        elif avg_overall >= 70:
            performance = 'good'
        elif avg_overall >= 55:
            performance = 'average'
        else:
            performance = 'needs_improvement'
        
        # Generate ratings (1-5 scale)
        technical_rating = min(5, max(1, int(avg_technical / 20) + 1))
        communication_rating = min(5, max(1, int(avg_communication / 20) + 1))
        
        # Confidence based on sentiment
        confident_count = sum(1 for a in answers if a.get('sentiment') == 'confident')
        confidence_rating = min(5, max(1, int((confident_count / num_answers) * 5)))
        
        # Generate key strengths and improvements
        key_strengths = self._generate_session_strengths(answers, avg_overall)
        areas_to_improve = self._generate_session_improvements(answers, avg_overall)
        recommended_resources = self._generate_resources(areas_to_improve, performance)
        
        # Generate preparation tips
        preparation_tips = self._generate_preparation_tips(performance, areas_to_improve)
        
        # Store session feedback
        feedback_data = {
            'session_id': session_id,
            'overall_performance': performance,
            'technical_rating': technical_rating,
            'communication_rating': communication_rating,
            'confidence_rating': confidence_rating,
            'key_strengths': json.dumps(key_strengths),
            'areas_to_improve': json.dumps(areas_to_improve),
            'recommended_resources': json.dumps(recommended_resources),
            'preparation_tips': preparation_tips,
            'practice_recommendations': self._generate_practice_recommendations(performance)
        }
        
        feedback_id = insert_one('interview_feedback', feedback_data)
        
        # Update session as completed
        update_one(
            'interview_sessions',
            {
                'status': 'completed',
                'completed_at': datetime.now(),
                'average_score': avg_overall,
                'duration_seconds': total_time
            },
            {'id': session_id}
        )
        
        # Clear current session
        self.current_session = None
        
        return {
            'session_id': session_id,
            'completed': True,
            'questions_answered': num_answers,
            'total_time_seconds': total_time,
            'average_scores': {
                'overall': round(avg_overall, 1),
                'relevance': round(avg_relevance, 1),
                'completeness': round(avg_completeness, 1),
                'clarity': round(avg_clarity, 1),
                'technical_accuracy': round(avg_technical, 1),
                'communication': round(avg_communication, 1)
            },
            'performance': performance,
            'ratings': {
                'technical': technical_rating,
                'communication': communication_rating,
                'confidence': confidence_rating
            },
            'feedback': {
                'key_strengths': key_strengths,
                'areas_to_improve': areas_to_improve,
                'recommended_resources': recommended_resources,
                'preparation_tips': preparation_tips
            }
        }
    
    def get_session_history(self, limit: int = 10) -> List[Dict]:
        """
        Get user's past interview sessions
        
        Args:
            limit: Maximum number of sessions to return
        
        Returns:
            List of session summaries
        """
        if not self.user_id:
            return []
        
        sessions = execute_query(
            """
            SELECT 
                s.id,
                s.session_type,
                s.job_role,
                s.difficulty_level,
                s.total_questions,
                s.questions_answered,
                s.average_score,
                s.status,
                s.duration_seconds,
                s.started_at,
                s.completed_at,
                f.overall_performance,
                f.technical_rating,
                f.communication_rating,
                f.confidence_rating
            FROM interview_sessions s
            LEFT JOIN interview_feedback f ON s.id = f.session_id
            WHERE s.user_id = %s
            ORDER BY s.started_at DESC
            LIMIT %s
            """,
            (self.user_id, limit)
        )
        
        return sessions
    
    def _select_questions(
        self,
        session_type: str,
        job_role: str,
        difficulty_level: str,
        num_questions: int,
        resume_id: Optional[int] = None
    ) -> List[Dict]:
        """
        Select appropriate questions for the interview session
        """
        logger.info(f"Selecting {num_questions} {session_type} questions for {job_role}")
        
        # Build query based on session type
        if session_type == 'technical':
            type_filter = "question_type = 'technical'"
        elif session_type == 'behavioral':
            type_filter = "question_type IN ('behavioral', 'situational')"
        elif session_type == 'mixed':
            type_filter = "question_type IN ('technical', 'behavioral', 'situational')"
        else:  # job-specific
            type_filter = "TRUE"
        
        # Get candidate's skills if resume provided
        candidate_skills = []
        if resume_id:
            candidate_skills = self._extract_skills_from_resume(resume_id)
        
        # Query questions
        query = f"""
            SELECT 
                id, question_text, question_type, difficulty_level,
                category, job_roles, key_points, sample_answer, tags
            FROM interview_question_bank
            WHERE {type_filter}
            AND (difficulty_level = %s OR difficulty_level = 'all')
            AND %s = ANY(job_roles)
            ORDER BY RANDOM()
        """
        
        questions = execute_query(query, (difficulty_level, job_role))
        
        if not questions:
            # Fallback: get any questions matching difficulty
            logger.warning("No job-specific questions found, using generic questions")
            questions = execute_query(
                f"""
                SELECT id, question_text, question_type, difficulty_level,
                       category, job_roles, key_points, sample_answer, tags
                FROM interview_question_bank
                WHERE {type_filter}
                AND (difficulty_level = %s OR difficulty_level = 'all')
                ORDER BY RANDOM()
                LIMIT %s
                """,
                (difficulty_level, num_questions)
            )
        
        # Select balanced mix if mixed session
        if session_type == 'mixed' and len(questions) >= num_questions:
            selected = []
            technical = [q for q in questions if q['question_type'] == 'technical']
            behavioral = [q for q in questions if q['question_type'] in ('behavioral', 'situational')]
            
            # 60% technical, 40% behavioral
            num_technical = int(num_questions * 0.6)
            num_behavioral = num_questions - num_technical
            
            selected.extend(random.sample(technical, min(num_technical, len(technical))))
            selected.extend(random.sample(behavioral, min(num_behavioral, len(behavioral))))
            
            # Fill remaining if needed
            if len(selected) < num_questions:
                remaining = [q for q in questions if q not in selected]
                selected.extend(random.sample(remaining, num_questions - len(selected)))
            
            questions = selected
        else:
            questions = questions[:num_questions]
        
        return questions
    
    def _extract_skills_from_resume(self, resume_id: int) -> List[str]:
        """Extract skills from a resume"""
        try:
            resume = execute_query(
                "SELECT parsed_data FROM resumes WHERE id = %s",
                (resume_id,)
            )
            
            if resume and resume[0]['parsed_data']:
                parsed_data = resume[0]['parsed_data']
                return parsed_data.get('skills', [])
        except Exception as e:
            logger.error(f"Error extracting skills from resume: {e}")
        
        return []
    
    def _generate_session_strengths(self, answers: List[Dict], avg_overall: float) -> List[str]:
        """Generate overall session strengths"""
        strengths = []
        
        if avg_overall >= 75:
            strengths.append("Consistently strong performance across questions")
        
        # Check for high scores in specific areas
        avg_technical = sum(a['technical_accuracy_score'] for a in answers) / len(answers)
        avg_communication = sum(a['communication_score'] for a in answers) / len(answers)
        avg_clarity = sum(a['clarity_score'] for a in answers) / len(answers)
        
        if avg_technical >= 80:
            strengths.append("Excellent technical knowledge and accuracy")
        
        if avg_communication >= 80:
            strengths.append("Clear and confident communication style")
        
        if avg_clarity >= 80:
            strengths.append("Well-structured and organized responses")
        
        # Check time management
        avg_time = sum(a['time_taken_seconds'] for a in answers) / len(answers)
        if 60 <= avg_time <= 180:  # 1-3 minutes is good
            strengths.append("Good time management per question")
        
        return strengths[:5]
    
    def _generate_session_improvements(self, answers: List[Dict], avg_overall: float) -> List[str]:
        """Generate areas for improvement"""
        improvements = []
        
        # Check for low scores in specific areas
        avg_technical = sum(a['technical_accuracy_score'] for a in answers) / len(answers)
        avg_communication = sum(a['communication_score'] for a in answers) / len(answers)
        avg_completeness = sum(a['completeness_score'] for a in answers) / len(answers)
        avg_relevance = sum(a['relevance_score'] for a in answers) / len(answers)
        
        if avg_technical < 65:
            improvements.append("Deepen technical knowledge in key areas")
        
        if avg_communication < 65:
            improvements.append("Work on confident and clear communication")
        
        if avg_completeness < 65:
            improvements.append("Provide more comprehensive answers covering all key points")
        
        if avg_relevance < 65:
            improvements.append("Focus more directly on what the question asks")
        
        # Check time management
        avg_time = sum(a['time_taken_seconds'] for a in answers) / len(answers)
        if avg_time < 45:
            improvements.append("Take more time to provide thorough answers")
        elif avg_time > 240:
            improvements.append("Practice being more concise")
        
        return improvements[:5]
    
    def _generate_resources(self, areas_to_improve: List[str], performance: str) -> List[Dict]:
        """Generate recommended learning resources"""
        resources = []
        
        # Generic resources based on performance
        if performance in ('needs_improvement', 'average'):
            resources.append({
                'title': 'Cracking the Coding Interview',
                'type': 'book',
                'url': 'https://www.crackingthecodinginterview.com/',
                'reason': 'Comprehensive interview preparation guide'
            })
        
        # Specific resources based on weaknesses
        for area in areas_to_improve:
            if 'technical' in area.lower():
                resources.append({
                    'title': 'LeetCode Practice',
                    'type': 'website',
                    'url': 'https://leetcode.com/',
                    'reason': 'Practice technical interview questions'
                })
            
            if 'communication' in area.lower():
                resources.append({
                    'title': 'STAR Method Guide',
                    'type': 'article',
                    'url': 'https://www.indeed.com/career-advice/interviewing/how-to-use-the-star-interview-response-technique',
                    'reason': 'Improve behavioral interview answers'
                })
        
        return resources[:4]
    
    def _generate_preparation_tips(self, performance: str, areas_to_improve: List[str]) -> str:
        """Generate personalized preparation tips"""
        tips = []
        
        if performance == 'excellent':
            tips.append("You're doing great! Keep practicing to maintain your skill level.")
            tips.append("Focus on learning company-specific information before real interviews.")
        elif performance == 'good':
            tips.append("You're on the right track! Focus on the areas mentioned below.")
            tips.append("Practice answering questions out loud to build confidence.")
        else:
            tips.append("Practice is key! Schedule regular interview prep sessions.")
            tips.append("Record yourself answering questions and review for improvement.")
        
        # Add specific tips based on improvements needed
        if any('technical' in area.lower() for area in areas_to_improve):
            tips.append("Review fundamental concepts in your target technology stack.")
        
        if any('communication' in area.lower() for area in areas_to_improve):
            tips.append("Use the STAR method (Situation, Task, Action, Result) for structured answers.")
        
        return '\n\n'.join(tips)
    
    def _generate_practice_recommendations(self, performance: str) -> str:
        """Generate practice recommendations"""
        if performance == 'excellent':
            return "Continue practicing 2-3 times per week. Focus on advanced topics and system design."
        elif performance == 'good':
            return "Practice 3-4 times per week. Mix technical and behavioral questions."
        elif performance == 'average':
            return "Practice daily if possible. Start with fundamentals and gradually increase difficulty."
        else:
            return "Daily practice recommended. Focus on one question type at a time until comfortable."


# Convenience function
def start_interview(
    user_id: Optional[int] = None,
    session_type: str = 'mixed',
    job_role: str = 'Software Engineer',
    difficulty_level: str = 'mid',
    num_questions: int = 5
) -> Tuple[InterviewSimulator, Dict]:
    """
    Quick function to start an interview session
    
    Returns:
        Tuple of (simulator instance, session info)
    """
    simulator = InterviewSimulator(user_id=user_id)
    session_info = simulator.start_session(
        session_type=session_type,
        job_role=job_role,
        difficulty_level=difficulty_level,
        num_questions=num_questions
    )
    return simulator, session_info
