"""
Groq-based AI Answer Analyzer for Interview Simulator
Analyzes interview answers using Groq's fast inference API
"""

import os
import json
import logging
from groq import Groq
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class GroqAnswerAnalyzer:
    """
    AI-powered answer analyzer using Groq API
    Evaluates interview answers across multiple dimensions
    """
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """
        Initialize the Groq Answer Analyzer
        
        Args:
            groq_api_key: Groq API key (will use env var if not provided)
        """
        self.api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required")
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        
        logger.info(f"✅ Groq Answer Analyzer initialized with model: {self.model}")
    
    def analyze_answer(
        self,
        user_answer: str,
        question_text: str,
        question_data: Dict[str, Any],
        difficulty_level: str,
        job_role: str
    ) -> Dict[str, Any]:
        """
        Analyze an interview answer using Groq AI
        
        Args:
            user_answer: The candidate's answer text
            question_text: The question that was asked
            question_data: Additional question metadata (key_points, etc.)
            difficulty_level: Question difficulty (beginner/intermediate/advanced)
            job_role: Target job role for context
        
        Returns:
            Dictionary containing:
            - overall_score: Overall score (0-100)
            - relevance_score: How relevant the answer is (0-100)
            - completeness_score: How complete the answer is (0-100)
            - clarity_score: How clear the answer is (0-100)
            - technical_accuracy_score: Technical correctness (0-100)
            - communication_score: Communication effectiveness (0-100)
            - strengths: List of answer strengths
            - weaknesses: List of answer weaknesses
            - missing_points: List of important missing points
            - suggestions: List of improvement suggestions
            - ai_feedback: Detailed narrative feedback
            - sentiment: Answer sentiment (positive/neutral/negative)
            - ai_generated: True (to indicate AI was used)
        """
        logger.info(f"🤖 Analyzing answer with Groq AI...")
        
        try:
            # Prepare key points from question data
            key_points = question_data.get('key_points', {})
            if isinstance(key_points, str):
                try:
                    key_points = json.loads(key_points)
                except:
                    key_points = {}
            
            # Build the analysis prompt
            prompt = self._build_analysis_prompt(
                user_answer=user_answer,
                question_text=question_text,
                key_points=key_points,
                difficulty_level=difficulty_level,
                job_role=job_role
            )
            
            # Call Groq API
            logger.info("📡 Calling Groq API for answer analysis...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert interview evaluator. Analyze answers objectively and provide constructive feedback. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent scoring
                max_tokens=2000
            )
            
            # Extract response
            ai_response = response.choices[0].message.content.strip()
            logger.info(f"✅ Groq API response received ({len(ai_response)} chars)")
            
            # Parse JSON response
            analysis_result = self._parse_analysis_response(ai_response)
            
            # Add metadata
            analysis_result['ai_generated'] = True
            
            logger.info(f"✅ Answer analyzed successfully. Overall score: {analysis_result['overall_score']}")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Groq answer analysis failed: {e}")
            # Return fallback scores
            return self._get_fallback_analysis(user_answer)
    
    def _build_analysis_prompt(
        self,
        user_answer: str,
        question_text: str,
        key_points: Dict[str, Any],
        difficulty_level: str,
        job_role: str
    ) -> str:
        """Build the analysis prompt for Groq"""
        
        key_points_text = ""
        if key_points and isinstance(key_points, dict):
            key_points_text = "\n".join([f"- {k}: {v}" for k, v in key_points.items()])
        
        prompt = f"""Analyze this interview answer and provide a comprehensive evaluation.

**Interview Context:**
- Job Role: {job_role}
- Difficulty Level: {difficulty_level}

**Question:**
{question_text}

{f"**Expected Key Points:**\n{key_points_text}\n" if key_points_text else ""}

**Candidate's Answer:**
{user_answer}

**Instructions:**
Evaluate the answer across these dimensions (scores 0-100):
1. **Relevance**: How well does the answer address the question?
2. **Completeness**: Are all important points covered?
3. **Clarity**: Is the answer well-structured and easy to understand?
4. **Technical Accuracy**: Is the information technically correct?
5. **Communication**: How effectively does the candidate communicate?

Provide your evaluation in this EXACT JSON format (ensure valid JSON):
{{
  "overall_score": <number 0-100>,
  "relevance_score": <number 0-100>,
  "completeness_score": <number 0-100>,
  "clarity_score": <number 0-100>,
  "technical_accuracy_score": <number 0-100>,
  "communication_score": <number 0-100>,
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>"],
  "missing_points": ["<missing point 1>", "<missing point 2>"],
  "suggestions": ["<suggestion 1>", "<suggestion 2>", "<suggestion 3>"],
  "ai_feedback": "<2-3 sentence narrative feedback summarizing the evaluation>",
  "sentiment": "<positive/neutral/negative>"
}}

IMPORTANT: 
- Respond ONLY with valid JSON, no additional text
- Be constructive and specific in feedback
- Consider the difficulty level and job role in your evaluation
- If answer is very short or off-topic, lower scores accordingly"""
        
        return prompt
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse the AI response into structured analysis"""
        
        try:
            # Try to find JSON in the response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                analysis = json.loads(json_str)
                
                # Validate required fields
                required_fields = [
                    'overall_score', 'relevance_score', 'completeness_score',
                    'clarity_score', 'technical_accuracy_score', 'communication_score',
                    'strengths', 'weaknesses', 'missing_points', 'suggestions',
                    'ai_feedback', 'sentiment'
                ]
                
                for field in required_fields:
                    if field not in analysis:
                        logger.warning(f"Missing field in AI response: {field}")
                        if field.endswith('_score'):
                            analysis[field] = 70
                        elif field in ['strengths', 'weaknesses', 'missing_points', 'suggestions']:
                            analysis[field] = []
                        elif field == 'ai_feedback':
                            analysis[field] = "Answer evaluated."
                        elif field == 'sentiment':
                            analysis[field] = 'neutral'
                
                # Ensure scores are within range
                for score_field in ['overall_score', 'relevance_score', 'completeness_score',
                                   'clarity_score', 'technical_accuracy_score', 'communication_score']:
                    if score_field in analysis:
                        analysis[score_field] = max(0, min(100, int(analysis[score_field])))
                
                logger.info("✅ Successfully parsed AI analysis response")
                return analysis
            
            else:
                raise ValueError("No JSON found in response")
        
        except Exception as e:
            logger.error(f"❌ Failed to parse AI response: {e}")
            logger.debug(f"Response was: {response[:500]}...")
            # Return fallback
            return self._get_fallback_analysis("")
    
    def _get_fallback_analysis(self, user_answer: str) -> Dict[str, Any]:
        """Generate fallback analysis when AI fails"""
        
        # Basic rule-based scoring
        answer_length = len(user_answer.split())
        
        # Simple heuristic scoring
        if answer_length == 0:
            base_score = 0
            feedback = "No answer provided."
            strengths = []
            weaknesses = ["No answer submitted"]
        elif answer_length < 20:
            base_score = 50
            feedback = "Answer is very brief. Consider providing more detail and examples."
            strengths = ["Answer submitted"]
            weaknesses = ["Answer is too brief", "Lacks detail"]
        elif answer_length < 50:
            base_score = 65
            feedback = "Good effort, but the answer could be more comprehensive."
            strengths = ["Clear communication", "Answer addresses the question"]
            weaknesses = ["Could include more examples", "Could be more detailed"]
        else:
            base_score = 75
            feedback = "Good comprehensive answer with sufficient detail."
            strengths = ["Comprehensive answer", "Good detail", "Clear communication"]
            weaknesses = []
        
        logger.info(f"⚠️ Using fallback analysis (base_score: {base_score})")
        
        return {
            'overall_score': base_score,
            'relevance_score': base_score,
            'completeness_score': base_score - 5 if base_score > 5 else base_score,
            'clarity_score': base_score,
            'technical_accuracy_score': base_score,
            'communication_score': base_score + 5 if base_score < 95 else 100,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'missing_points': ["Consider adding specific examples"],
            'suggestions': [
                "Provide more specific examples",
                "Structure your answer with clear points",
                "Consider the STAR method (Situation, Task, Action, Result)"
            ],
            'ai_feedback': feedback,
            'sentiment': 'neutral',
            'ai_generated': False
        }
    
    def batch_analyze_answers(
        self,
        qa_pairs: List[Dict[str, Any]],
        job_role: str,
        difficulty_level: str
    ) -> List[Dict[str, Any]]:
        """
        Analyze multiple answers in batch
        
        Args:
            qa_pairs: List of question-answer pairs to analyze
            job_role: Target job role
            difficulty_level: Overall difficulty level
        
        Returns:
            List of analysis results for each answer
        """
        results = []
        
        for i, qa_pair in enumerate(qa_pairs):
            logger.info(f"Analyzing answer {i+1}/{len(qa_pairs)}...")
            
            try:
                analysis = self.analyze_answer(
                    user_answer=qa_pair['answer'],
                    question_text=qa_pair['question'],
                    question_data=qa_pair.get('question_data', {}),
                    difficulty_level=difficulty_level,
                    job_role=job_role
                )
                results.append(analysis)
            
            except Exception as e:
                logger.error(f"Failed to analyze answer {i+1}: {e}")
                results.append(self._get_fallback_analysis(qa_pair.get('answer', '')))
        
        return results


# Example usage
if __name__ == "__main__":
    # Test the analyzer
    analyzer = GroqAnswerAnalyzer()
    
    test_answer = """
    Python uses dynamic typing, which means variable types are determined at runtime.
    This provides flexibility but can lead to runtime errors if not carefully managed.
    For example, you can assign x = 5 (integer) and then x = "hello" (string) without errors.
    
    Static typing, used in languages like Java or C++, requires declaring types upfront.
    This catches type errors at compile time, making code more robust but less flexible.
    
    The choice depends on the project - dynamic typing is great for rapid development and
    scripts, while static typing is better for large-scale applications requiring reliability.
    """
    
    result = analyzer.analyze_answer(
        user_answer=test_answer,
        question_text="Explain the difference between static and dynamic typing in programming languages.",
        question_data={'key_points': {'definition': 'static vs dynamic', 'examples': 'language examples'}},
        difficulty_level='intermediate',
        job_role='Software Engineer'
    )
    
    print("Analysis Result:")
    print(json.dumps(result, indent=2))
