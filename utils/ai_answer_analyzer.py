"""
AI-Powered Answer Analyzer using Hugging Face Transformers
Provides intelligent interview answer analysis with LLM feedback

WHY THIS MODULE:
- Use free Hugging Face Inference API for AI feedback
- Generate human-like, context-aware feedback
- Intelligent scoring based on LLM understanding
- No local GPU required - uses HF's free tier
"""

import logging
import json
import re
from typing import Dict, List
from huggingface_hub import InferenceClient
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAnswerAnalyzer:
    """
    AI-powered answer analyzer using Hugging Face models
    """
    
    def __init__(self, hf_token: str = None):
        """
        Initialize the AI analyzer
        
        Args:
            hf_token: Hugging Face API token (optional, can use env var)
        """
        # Get token from environment or parameter
        self.hf_token = hf_token or os.getenv('HUGGINGFACE_TOKEN')
        
        if not self.hf_token:
            logger.warning("No HuggingFace token provided. Using public models with rate limits.")
            logger.warning("Get a free token at: https://huggingface.co/settings/tokens")
        
        # Initialize Inference Client
        self.client = InferenceClient(token=self.hf_token)
        
        # Best free model for interviews (as of 2024)
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"
        
        logger.info(f"AI Answer Analyzer initialized with model: {self.model}")
    
    def analyze_answer(
        self,
        user_answer: str,
        question_text: str,
        question_data: Dict,
        difficulty_level: str = 'mid',
        job_role: str = 'Software Engineer'
    ) -> Dict:
        """
        AI-powered comprehensive analysis of interview answer
        
        Args:
            user_answer: The candidate's answer text
            question_text: The actual question asked
            question_data: Question metadata (key_points, sample_answer, etc.)
            difficulty_level: 'junior', 'mid-level', or 'senior'
            job_role: The job role being interviewed for
        
        Returns:
            Dictionary with AI-generated scores and feedback
        """
        logger.info(f"AI analyzing answer for {job_role} ({difficulty_level} level)")
        
        try:
            # Generate AI feedback
            ai_response = self._generate_ai_feedback(
                user_answer=user_answer,
                question_text=question_text,
                question_data=question_data,
                difficulty_level=difficulty_level,
                job_role=job_role
            )
            
            # Parse AI response into structured format
            analysis = self._parse_ai_response(ai_response, user_answer)
            
            # Add metadata
            analysis['ai_model'] = self.model
            analysis['ai_generated'] = True
            
            return analysis
            
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            # Fallback to basic analysis if AI fails
            return self._fallback_analysis(user_answer, question_data)
    
    def _generate_ai_feedback(
        self,
        user_answer: str,
        question_text: str,
        question_data: Dict,
        difficulty_level: str,
        job_role: str
    ) -> str:
        """
        Generate AI feedback using Hugging Face model
        """
        # Extract key points
        key_points = question_data.get('key_points', {})
        must_mention = key_points.get('must_mention', [])
        bonus_points = key_points.get('bonus_points', [])
        question_type = question_data.get('question_type', 'general')
        
        # Craft the prompt
        prompt = self._build_prompt(
            user_answer=user_answer,
            question_text=question_text,
            question_type=question_type,
            must_mention=must_mention,
            bonus_points=bonus_points,
            difficulty_level=difficulty_level,
            job_role=job_role
        )
        
        logger.info("Sending request to Hugging Face API...")
        
        try:
            # Call Hugging Face Inference API using chat_completion
            # This is the correct method for instruction-following models like Mistral-7B-Instruct
            response = self.client.chat_completion(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                max_tokens=800,
                temperature=0.7,
                top_p=0.9
            )
            
            # Extract the generated text from the response
            if hasattr(response, 'choices') and len(response.choices) > 0:
                generated_text = response.choices[0].message.content
            elif isinstance(response, dict):
                # Fallback for dict response
                generated_text = response.get('choices', [{}])[0].get('message', {}).get('content', str(response))
            else:
                generated_text = str(response)
            
            logger.info("AI response received successfully")
            return generated_text
            
        except Exception as e:
            logger.error(f"HuggingFace API error: {str(e)}")
            raise
    
    def _build_prompt(
        self,
        user_answer: str,
        question_text: str,
        question_type: str,
        must_mention: List[str],
        bonus_points: List[str],
        difficulty_level: str,
        job_role: str
    ) -> str:
        """
        Build the prompt for the AI model (chat format, no [INST] tags)
        """
        prompt = f"""You are an expert technical interviewer evaluating a candidate's answer for a {job_role} position at {difficulty_level} level.

**Interview Question:**
{question_text}

**Question Type:** {question_type}

**Key Points Expected:**
{', '.join(must_mention) if must_mention else 'General discussion'}

**Bonus Points:**
{', '.join(bonus_points) if bonus_points else 'None specified'}

**Candidate's Answer:**
{user_answer}

---

**Task:** Analyze this interview answer and provide detailed feedback in the following JSON format:

{{
  "overall_score": <0-100>,
  "scores": {{
    "relevance": <0-100>,
    "completeness": <0-100>,
    "clarity": <0-100>,
    "technical_accuracy": <0-100>
  }},
  "strengths": [
    "strength 1",
    "strength 2",
    "strength 3"
  ],
  "weaknesses": [
    "weakness 1",
    "weakness 2"
  ],
  "missing_points": [
    "missing point 1",
    "missing point 2"
  ],
  "suggestions": [
    "suggestion 1",
    "suggestion 2",
    "suggestion 3"
  ],
  "feedback_summary": "A brief 2-3 sentence summary of the answer quality"
}}

**Scoring Guidelines:**
- **Relevance (0-100):** How directly the answer addresses the question
- **Completeness (0-100):** Coverage of key points and depth of discussion
- **Clarity (0-100):** Structure, coherence, and communication quality
- **Technical Accuracy (0-100):** Correctness of concepts and terminology

Provide honest, constructive feedback. Be specific and actionable."""
        return prompt
    
    def _parse_ai_response(self, ai_response: str, user_answer: str) -> Dict:
        """
        Parse AI response into structured format
        """
        try:
            # Extract JSON from response
            # AI might wrap JSON in markdown or text
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                parsed = json.loads(json_str)
                
                # Extract and validate scores
                overall_score = int(parsed.get('overall_score', 70))
                scores = parsed.get('scores', {})
                
                return {
                    'overall_score': min(100, max(0, overall_score)),
                    'relevance_score': min(100, max(0, int(scores.get('relevance', 70)))),
                    'completeness_score': min(100, max(0, int(scores.get('completeness', 70)))),
                    'clarity_score': min(100, max(0, int(scores.get('clarity', 70)))),
                    'technical_accuracy_score': min(100, max(0, int(scores.get('technical_accuracy', 70)))),
                    'communication_score': 75,  # Default
                    'strengths': parsed.get('strengths', [])[:5],
                    'weaknesses': parsed.get('weaknesses', [])[:5],
                    'missing_points': parsed.get('missing_points', [])[:5],
                    'suggestions': parsed.get('suggestions', [])[:6],
                    'ai_feedback': parsed.get('feedback_summary', 'Good effort on this answer.'),
                    'sentiment': self._determine_sentiment(overall_score),
                    'word_count': len(user_answer.split()),
                    'sentence_count': len(re.split(r'[.!?]+', user_answer))
                }
            else:
                logger.warning("Could not extract JSON from AI response, using fallback")
                return self._extract_text_feedback(ai_response, user_answer)
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            return self._extract_text_feedback(ai_response, user_answer)
        except Exception as e:
            logger.error(f"Response parsing error: {str(e)}")
            return self._fallback_analysis(user_answer, {})
    
    def _extract_text_feedback(self, ai_response: str, user_answer: str) -> Dict:
        """
        Extract feedback from non-JSON AI response
        """
        # Extract scores using regex
        overall_score_match = re.search(r'overall[_\s]*score[:\s]*(\d+)', ai_response, re.IGNORECASE)
        overall_score = int(overall_score_match.group(1)) if overall_score_match else 70
        
        # Extract lists
        strengths = self._extract_list_items(ai_response, ['strength', 'positive', 'good'])
        weaknesses = self._extract_list_items(ai_response, ['weakness', 'area', 'improve'])
        suggestions = self._extract_list_items(ai_response, ['suggest', 'recommend', 'try'])
        
        return {
            'overall_score': min(100, max(0, overall_score)),
            'relevance_score': overall_score,
            'completeness_score': overall_score,
            'clarity_score': overall_score,
            'technical_accuracy_score': overall_score,
            'communication_score': overall_score,
            'strengths': strengths[:5] if strengths else ['Answer shows effort'],
            'weaknesses': weaknesses[:5] if weaknesses else ['Could provide more detail'],
            'missing_points': [],
            'suggestions': suggestions[:6] if suggestions else ['Practice more with similar questions'],
            'ai_feedback': ai_response[:500],  # First 500 chars
            'sentiment': self._determine_sentiment(overall_score),
            'word_count': len(user_answer.split()),
            'sentence_count': len(re.split(r'[.!?]+', user_answer))
        }
    
    def _extract_list_items(self, text: str, keywords: List[str]) -> List[str]:
        """
        Extract list items from text based on keywords
        """
        items = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Check if line starts with bullet point or number
            if re.match(r'^[-•*\d]+[.)]?\s+', line):
                # Check if any keyword is nearby
                if any(keyword.lower() in text.lower() for keyword in keywords):
                    clean_item = re.sub(r'^[-•*\d]+[.)]?\s+', '', line)
                    if clean_item:
                        items.append(clean_item)
        
        return items
    
    def _determine_sentiment(self, overall_score: int) -> str:
        """
        Determine sentiment based on score
        """
        if overall_score >= 85:
            return 'confident'
        elif overall_score >= 70:
            return 'positive'
        elif overall_score >= 55:
            return 'neutral'
        else:
            return 'uncertain'
    
    def _fallback_analysis(self, user_answer: str, question_data: Dict) -> Dict:
        """
        Fallback analysis when AI is unavailable
        Uses simple rule-based approach
        """
        logger.warning("⚠️ Using fallback analysis (non-AI) - AI analysis failed or unavailable")
        
        word_count = len(user_answer.split())
        sentence_count = len(re.split(r'[.!?]+', user_answer))
        
        # More generous base scoring
        base_score = 70  # Changed from 65 to 70
        
        # Length bonus (more generous)
        if 50 <= word_count <= 200:
            base_score += 15  # Increased from 10
        elif word_count > 30:
            base_score += 10  # Increased from 5
        elif word_count > 20:
            base_score += 5
        
        # Structure bonus
        if sentence_count >= 5:
            base_score += 8  # More detailed answer
        elif sentence_count >= 3:
            base_score += 5
        
        # Key points check
        key_points = question_data.get('key_points', {})
        must_mention = key_points.get('must_mention', [])
        
        if must_mention and isinstance(must_mention, list):
            mentioned_count = sum(
                1 for point in must_mention 
                if isinstance(point, str) and point.lower() in user_answer.lower()
            )
            if len(must_mention) > 0:
                coverage = (mentioned_count / len(must_mention)) * 15
                base_score += int(coverage)
        
        overall_score = min(100, max(60, base_score))  # At least 60, at most 100
        
        return {
            'overall_score': overall_score,
            'relevance_score': overall_score,
            'completeness_score': max(0, overall_score - 10),
            'clarity_score': overall_score,
            'technical_accuracy_score': max(0, overall_score - 5),
            'communication_score': overall_score,
            'strengths': [
                'Answer demonstrates effort and thought',
                'Appropriate length and structure'
            ],
            'weaknesses': [
                'Could be more specific with examples',
                'Consider adding more technical detail'
            ],
            'missing_points': [point for point in must_mention if point.lower() not in user_answer.lower()][:5],
            'suggestions': [
                'Use the STAR method (Situation, Task, Action, Result)',
                'Include specific examples from your experience',
                'Practice articulating technical concepts clearly'
            ],
            'ai_feedback': 'This is a basic analysis. Enable AI for detailed feedback.',
            'sentiment': 'neutral',
            'word_count': word_count,
            'sentence_count': sentence_count,
            'ai_generated': False
        }


# Convenience function
def analyze_with_ai(
    user_answer: str,
    question_text: str,
    question_data: Dict,
    difficulty_level: str = 'mid',
    job_role: str = 'Software Engineer',
    hf_token: str = None
) -> Dict:
    """
    Quick AI analysis function
    
    Args:
        user_answer: The candidate's answer
        question_text: The question asked
        question_data: Question metadata
        difficulty_level: 'junior', 'mid-level', or 'senior'
        job_role: Job role being interviewed for
        hf_token: Hugging Face API token (optional)
    
    Returns:
        AI analysis results dictionary
    """
    analyzer = AIAnswerAnalyzer(hf_token=hf_token)
    return analyzer.analyze_answer(
        user_answer=user_answer,
        question_text=question_text,
        question_data=question_data,
        difficulty_level=difficulty_level,
        job_role=job_role
    )
