"""
Answer Analyzer Module for UtopiaHire
Analyzes interview answers using NLP and provides scoring + feedback

WHY THIS MODULE:
- Evaluate answer quality (relevance, completeness, clarity)
- Provide constructive feedback for improvement
- Score across multiple dimensions
- Help job seekers practice and improve interview skills
"""

import logging
import re
from typing import Dict, List, Tuple
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)


class AnswerAnalyzer:
    """
    Analyze interview answers and provide scoring + feedback
    """
    
    # Quality indicators
    POSITIVE_INDICATORS = [
        # Technical depth
        'implemented', 'developed', 'designed', 'optimized', 'debugged',
        'analyzed', 'researched', 'tested', 'deployed', 'maintained',
        
        # Results
        'improved', 'increased', 'reduced', 'achieved', 'delivered',
        'successfully', 'efficiently', 'effectively',
        
        # Collaboration
        'team', 'collaborated', 'communicated', 'coordinated', 'mentored',
        'presented', 'documented',
        
        # Problem-solving
        'challenge', 'solution', 'approach', 'strategy', 'methodology',
        'resolved', 'addressed', 'identified'
    ]
    
    NEGATIVE_INDICATORS = [
        'maybe', 'possibly', 'perhaps', 'kind of', 'sort of',
        'i think', 'i guess', 'not sure', 'don\'t know',
        'um', 'uh', 'like'  # filler words
    ]
    
    # Minimum word counts for quality
    MIN_WORDS_JUNIOR = 30
    MIN_WORDS_MID = 50
    MIN_WORDS_SENIOR = 70
    
    def __init__(self):
        """Initialize the answer analyzer"""
        self.stop_words = set(stopwords.words('english'))
        logger.info("Answer analyzer initialized")
    
    def analyze_answer(
        self,
        user_answer: str,
        question_data: Dict,
        difficulty_level: str = 'mid'
    ) -> Dict:
        """
        Comprehensive analysis of interview answer
        
        Args:
            user_answer: The candidate's answer text
            question_data: Question metadata (key_points, sample_answer, etc.)
            difficulty_level: 'junior', 'mid', or 'senior'
        
        Returns:
            Dictionary with scores and feedback
        """
        logger.info(f"Analyzing answer for {difficulty_level} level question")
        
        # Basic metrics
        word_count = len(word_tokenize(user_answer))
        sentence_count = len(sent_tokenize(user_answer))
        
        # Individual scoring dimensions
        relevance_score = self._score_relevance(user_answer, question_data)
        completeness_score = self._score_completeness(user_answer, question_data)
        clarity_score = self._score_clarity(user_answer, word_count, sentence_count)
        technical_accuracy_score = self._score_technical_accuracy(user_answer, question_data)
        communication_score = self._score_communication(user_answer)
        
        # Overall score (weighted average)
        overall_score = int(
            relevance_score * 0.25 +
            completeness_score * 0.25 +
            clarity_score * 0.20 +
            technical_accuracy_score * 0.20 +
            communication_score * 0.10
        )
        
        # Generate feedback
        strengths = self._identify_strengths(
            user_answer, relevance_score, completeness_score,
            clarity_score, technical_accuracy_score, communication_score
        )
        
        weaknesses = self._identify_weaknesses(
            user_answer, relevance_score, completeness_score,
            clarity_score, technical_accuracy_score, communication_score,
            word_count, difficulty_level
        )
        
        missing_points = self._identify_missing_points(user_answer, question_data)
        suggestions = self._generate_suggestions(weaknesses, missing_points, overall_score)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(user_answer)
        
        # AI narrative feedback
        ai_feedback = self._generate_narrative_feedback(
            overall_score, strengths, weaknesses, missing_points
        )
        
        return {
            'relevance_score': relevance_score,
            'completeness_score': completeness_score,
            'clarity_score': clarity_score,
            'technical_accuracy_score': technical_accuracy_score,
            'communication_score': communication_score,
            'overall_score': overall_score,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'sentiment': sentiment,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'missing_points': missing_points,
            'suggestions': suggestions,
            'ai_feedback': ai_feedback
        }
    
    def _score_relevance(self, answer: str, question_data: Dict) -> int:
        """
        Score how relevant the answer is to the question (0-100)
        """
        answer_lower = answer.lower()
        score = 50  # Base score
        
        # Check for key points mention
        key_points = question_data.get('key_points', {})
        must_mention = key_points.get('must_mention', [])
        
        if must_mention:
            mentioned_count = sum(
                1 for point in must_mention 
                if point.lower() in answer_lower
            )
            coverage = (mentioned_count / len(must_mention)) * 50
            score += int(coverage)
        
        # Check question category keywords
        category = question_data.get('category', '')
        category_keywords = category.replace('_', ' ').split()
        
        keyword_mentions = sum(
            1 for keyword in category_keywords
            if keyword.lower() in answer_lower
        )
        if category_keywords:
            score += min(15, keyword_mentions * 5)
        
        return min(100, max(0, score))
    
    def _score_completeness(self, answer: str, question_data: Dict) -> int:
        """
        Score how complete/thorough the answer is (0-100)
        """
        score = 40  # Base score
        
        # Check coverage of key points
        key_points = question_data.get('key_points', {})
        must_mention = key_points.get('must_mention', [])
        bonus_points = key_points.get('bonus_points', [])
        
        answer_lower = answer.lower()
        
        # Must mention points (60% of score)
        if must_mention:
            mentioned = sum(1 for point in must_mention if point.lower() in answer_lower)
            score += int((mentioned / len(must_mention)) * 40)
        
        # Bonus points (20% of score)
        if bonus_points:
            bonus_mentioned = sum(1 for point in bonus_points if point.lower() in answer_lower)
            score += int((bonus_mentioned / len(bonus_points)) * 20)
        
        return min(100, max(0, score))
    
    def _score_clarity(self, answer: str, word_count: int, sentence_count: int) -> int:
        """
        Score how clear and well-structured the answer is (0-100)
        """
        score = 50  # Base score
        
        # Average sentence length (ideal: 15-25 words)
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
            if 15 <= avg_sentence_length <= 25:
                score += 20
            elif 10 <= avg_sentence_length < 15 or 25 < avg_sentence_length <= 30:
                score += 10
        
        # Check for structure indicators
        structure_indicators = [
            'first', 'second', 'third', 'finally', 'in conclusion',
            'for example', 'such as', 'specifically',
            '1)', '2)', '3)', 'step 1', 'step 2'
        ]
        
        answer_lower = answer.lower()
        structure_count = sum(1 for indicator in structure_indicators if indicator in answer_lower)
        score += min(15, structure_count * 5)
        
        # Penalize excessive filler words
        filler_count = sum(1 for filler in self.NEGATIVE_INDICATORS if filler in answer_lower)
        score -= min(20, filler_count * 5)
        
        # Check for paragraphs/organization
        paragraphs = answer.split('\n\n')
        if len(paragraphs) > 1:
            score += 15
        
        return min(100, max(0, score))
    
    def _score_technical_accuracy(self, answer: str, question_data: Dict) -> int:
        """
        Score technical accuracy (0-100)
        Based on presence of correct terminology and concepts
        """
        score = 50  # Base score
        
        answer_lower = answer.lower()
        question_type = question_data.get('question_type', '')
        
        # For technical questions, check for technical terms
        if question_type == 'technical':
            required_skills = question_data.get('required_skills', [])
            
            if required_skills:
                skills_mentioned = sum(
                    1 for skill in required_skills
                    if skill.lower() in answer_lower
                )
                score += int((skills_mentioned / len(required_skills)) * 30)
            
            # Check for code examples or technical details
            has_code = bool(re.search(r'```|`[^`]+`|\w+\(\)', answer))
            if has_code:
                score += 10
            
            # Check for technical depth indicators
            technical_terms = ['algorithm', 'complexity', 'performance', 'optimization',
                              'architecture', 'design pattern', 'database', 'query',
                              'function', 'class', 'method', 'variable']
            
            technical_depth = sum(1 for term in technical_terms if term in answer_lower)
            score += min(10, technical_depth * 2)
        
        # For behavioral questions, check for STAR method
        elif question_type == 'behavioral':
            star_elements = ['situation', 'task', 'action', 'result']
            star_count = sum(1 for element in star_elements if element in answer_lower)
            
            # Or check for story structure
            has_context = any(word in answer_lower for word in ['when', 'project', 'role', 'time'])
            has_action = any(word in answer_lower for word in ['did', 'implemented', 'decided', 'approached'])
            has_result = any(word in answer_lower for word in ['result', 'outcome', 'achieved', 'learned'])
            
            if has_context:
                score += 15
            if has_action:
                score += 15
            if has_result:
                score += 20
        
        return min(100, max(0, score))
    
    def _score_communication(self, answer: str) -> int:
        """
        Score communication effectiveness (0-100)
        """
        score = 50  # Base score
        
        answer_lower = answer.lower()
        words = word_tokenize(answer_lower)
        
        # Check for positive action verbs
        positive_count = sum(1 for word in words if word in self.POSITIVE_INDICATORS)
        score += min(25, positive_count * 3)
        
        # Penalize uncertainty markers
        negative_count = sum(1 for phrase in self.NEGATIVE_INDICATORS if phrase in answer_lower)
        score -= min(20, negative_count * 5)
        
        # Check for confidence indicators
        confidence_words = ['confident', 'successfully', 'effectively', 'proficient', 'experienced']
        confidence_count = sum(1 for word in confidence_words if word in answer_lower)
        score += min(15, confidence_count * 5)
        
        # Check for specific examples
        has_example = any(phrase in answer_lower for phrase in 
                         ['for example', 'for instance', 'specifically', 'such as'])
        if has_example:
            score += 10
        
        return min(100, max(0, score))
    
    def _identify_strengths(
        self,
        answer: str,
        relevance: int,
        completeness: int,
        clarity: int,
        technical: int,
        communication: int
    ) -> List[str]:
        """
        Identify what was good about the answer
        """
        strengths = []
        
        if relevance >= 75:
            strengths.append("Directly addressed the question with relevant information")
        
        if completeness >= 75:
            strengths.append("Provided comprehensive coverage of key points")
        
        if clarity >= 75:
            strengths.append("Well-structured and easy to follow answer")
        
        if technical >= 75:
            strengths.append("Demonstrated strong technical knowledge")
        
        if communication >= 75:
            strengths.append("Communicated clearly and confidently")
        
        # Check for specific patterns
        answer_lower = answer.lower()
        
        if any(word in answer_lower for word in ['example', 'instance', 'project']):
            strengths.append("Used concrete examples to illustrate points")
        
        if any(word in answer_lower for word in ['result', 'outcome', 'achieved', 'improved']):
            strengths.append("Focused on measurable results and outcomes")
        
        if len(re.findall(r'\d+', answer)) >= 2:
            strengths.append("Quantified achievements with specific numbers")
        
        return strengths[:5]  # Top 5 strengths
    
    def _identify_weaknesses(
        self,
        answer: str,
        relevance: int,
        completeness: int,
        clarity: int,
        technical: int,
        communication: int,
        word_count: int,
        difficulty_level: str
    ) -> List[str]:
        """
        Identify areas for improvement
        """
        weaknesses = []
        
        # Score-based weaknesses
        if relevance < 60:
            weaknesses.append("Answer could be more focused on the specific question asked")
        
        if completeness < 60:
            weaknesses.append("Missing some key points - provide more comprehensive coverage")
        
        if clarity < 60:
            weaknesses.append("Structure could be improved for better clarity")
        
        if technical < 60:
            weaknesses.append("Could demonstrate deeper technical understanding")
        
        if communication < 60:
            weaknesses.append("Consider using more confident and active language")
        
        # Length-based feedback
        min_words = {
            'junior': self.MIN_WORDS_JUNIOR,
            'mid': self.MIN_WORDS_MID,
            'senior': self.MIN_WORDS_SENIOR
        }.get(difficulty_level, self.MIN_WORDS_MID)
        
        if word_count < min_words:
            weaknesses.append(f"Answer is too brief - aim for at least {min_words} words for {difficulty_level} level")
        elif word_count > min_words * 3:
            weaknesses.append("Answer is quite lengthy - practice being more concise")
        
        # Pattern-based weaknesses
        answer_lower = answer.lower()
        
        filler_count = sum(1 for filler in self.NEGATIVE_INDICATORS if filler in answer_lower)
        if filler_count >= 3:
            weaknesses.append("Reduce filler words (um, maybe, sort of) for more confidence")
        
        if not any(word in answer_lower for word in ['example', 'instance', 'project', 'experience']):
            weaknesses.append("Include specific examples from your experience")
        
        return weaknesses[:5]  # Top 5 weaknesses
    
    def _identify_missing_points(self, answer: str, question_data: Dict) -> List[str]:
        """
        Identify key points not mentioned in the answer
        """
        key_points = question_data.get('key_points', {})
        must_mention = key_points.get('must_mention', [])
        bonus_points = key_points.get('bonus_points', [])
        
        answer_lower = answer.lower()
        
        missing = []
        
        # Check must-mention points
        for point in must_mention:
            if point.lower() not in answer_lower:
                missing.append(f"Key point: {point}")
        
        # Check bonus points
        for point in bonus_points:
            if point.lower() not in answer_lower:
                missing.append(f"Bonus: {point}")
        
        return missing[:5]  # Top 5 missing points
    
    def _generate_suggestions(
        self,
        weaknesses: List[str],
        missing_points: List[str],
        overall_score: int
    ) -> List[str]:
        """
        Generate actionable improvement suggestions
        """
        suggestions = []
        
        if overall_score < 60:
            suggestions.append("Focus on addressing the question more directly with specific examples")
            suggestions.append("Use the STAR method (Situation, Task, Action, Result) for behavioral questions")
        
        if overall_score < 75:
            suggestions.append("Practice structuring your answers with clear beginning, middle, and end")
            suggestions.append("Include more specific technical details and terminology")
        
        # Add specific suggestions based on missing points
        if missing_points:
            suggestions.append(f"Don't forget to mention: {', '.join(missing_points[:3])}")
        
        # General tips
        suggestions.append("Practice answering similar questions out loud to build confidence")
        suggestions.append("Quantify your achievements with numbers and percentages when possible")
        suggestions.append("Prepare 2-3 strong examples you can adapt to different questions")
        
        return suggestions[:6]  # Top 6 suggestions
    
    def _analyze_sentiment(self, answer: str) -> str:
        """
        Analyze the sentiment/confidence of the answer
        """
        answer_lower = answer.lower()
        
        # Confidence indicators
        confident_words = ['confident', 'successfully', 'achieved', 'accomplished', 
                          'effectively', 'proficient', 'expert', 'strong']
        
        uncertain_words = ['maybe', 'perhaps', 'not sure', 'i think', 'i guess',
                          'probably', 'might', 'could be']
        
        confident_count = sum(1 for word in confident_words if word in answer_lower)
        uncertain_count = sum(1 for word in uncertain_words if word in answer_lower)
        
        if confident_count > uncertain_count + 2:
            return 'confident'
        elif uncertain_count > confident_count + 2:
            return 'uncertain'
        elif confident_count > 0:
            return 'positive'
        else:
            return 'neutral'
    
    def _generate_narrative_feedback(
        self,
        overall_score: int,
        strengths: List[str],
        weaknesses: List[str],
        missing_points: List[str]
    ) -> str:
        """
        Generate human-readable narrative feedback
        """
        feedback_parts = []
        
        # Opening based on score
        if overall_score >= 85:
            feedback_parts.append("Excellent answer! You demonstrated strong understanding and communication.")
        elif overall_score >= 70:
            feedback_parts.append("Good answer overall. You covered the main points well.")
        elif overall_score >= 55:
            feedback_parts.append("Decent answer, but there's room for improvement.")
        else:
            feedback_parts.append("This answer needs significant improvement to meet expectations.")
        
        # Strengths
        if strengths:
            feedback_parts.append("\n\n**What you did well:**")
            for strength in strengths[:3]:
                feedback_parts.append(f"• {strength}")
        
        # Areas for improvement
        if weaknesses or missing_points:
            feedback_parts.append("\n\n**Areas to improve:**")
            for weakness in weaknesses[:3]:
                feedback_parts.append(f"• {weakness}")
            
            if missing_points:
                feedback_parts.append(f"\n**Key points to add:** {', '.join(missing_points[:3])}")
        
        # Closing encouragement
        if overall_score < 70:
            feedback_parts.append("\n\nPractice with similar questions and focus on providing specific examples from your experience.")
        else:
            feedback_parts.append("\n\nKeep practicing to maintain and improve your interview skills!")
        
        return '\n'.join(feedback_parts)


# Convenience function for quick analysis
def analyze_interview_answer(
    user_answer: str,
    question_data: Dict,
    difficulty_level: str = 'mid'
) -> Dict:
    """
    Quick analysis function
    
    Args:
        user_answer: The candidate's answer
        question_data: Question metadata
        difficulty_level: 'junior', 'mid', or 'senior'
    
    Returns:
        Analysis results dictionary
    """
    analyzer = AnswerAnalyzer()
    return analyzer.analyze_answer(user_answer, question_data, difficulty_level)
