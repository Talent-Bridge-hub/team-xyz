#!/usr/bin/env python3
"""
Test AI Interview Integration
Quick test to verify AI analyzer is working
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai_answer_analyzer import AIAnswerAnalyzer

def test_ai_analyzer():
    """Test the AI answer analyzer"""
    
    print("=" * 60)
    print("🧪 Testing AI Interview Analyzer")
    print("=" * 60)
    
    # Sample data
    question_text = "Tell me about your experience with React and state management."
    
    question_data = {
        'question_type': 'technical',
        'key_points': {
            'must_mention': ['react', 'state', 'hooks', 'components'],
            'bonus_points': ['redux', 'context api', 'performance']
        },
        'required_skills': ['React', 'JavaScript', 'TypeScript']
    }
    
    user_answer = """
    I have 3 years of experience working with React. I've built several 
    production applications using React hooks like useState and useEffect 
    for state management. I'm also familiar with Redux for global state 
    management and Context API for simpler use cases. I've optimized 
    component performance using React.memo and useMemo hooks.
    """
    
    print("\n📝 Question:", question_text)
    print("\n👤 Answer:", user_answer.strip())
    print("\n" + "-" * 60)
    print("🤖 Analyzing with AI...")
    print("-" * 60)
    
    try:
        # Initialize analyzer
        analyzer = AIAnswerAnalyzer()
        
        # Analyze
        result = analyzer.analyze_answer(
            user_answer=user_answer,
            question_text=question_text,
            question_data=question_data,
            difficulty_level='mid-level',
            job_role='Software Engineer'
        )
        
        # Display results
        print("\n✅ AI Analysis Complete!\n")
        
        print("📊 SCORES:")
        print(f"  Overall:            {result['overall_score']}/100")
        print(f"  Relevance:          {result['relevance_score']}/100")
        print(f"  Completeness:       {result['completeness_score']}/100")
        print(f"  Clarity:            {result['clarity_score']}/100")
        print(f"  Technical Accuracy: {result['technical_accuracy_score']}/100")
        
        print(f"\n✨ STRENGTHS ({len(result['strengths'])}):")
        for i, strength in enumerate(result['strengths'], 1):
            print(f"  {i}. {strength}")
        
        print(f"\n⚠️  WEAKNESSES ({len(result['weaknesses'])}):")
        for i, weakness in enumerate(result['weaknesses'], 1):
            print(f"  {i}. {weakness}")
        
        print(f"\n📝 MISSING POINTS ({len(result['missing_points'])}):")
        if result['missing_points']:
            for i, point in enumerate(result['missing_points'], 1):
                print(f"  {i}. {point}")
        else:
            print("  None - all key points covered!")
        
        print(f"\n💡 SUGGESTIONS ({len(result['suggestions'])}):")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")
        
        print(f"\n🎯 AI FEEDBACK:")
        print(f"  {result['ai_feedback']}")
        
        print(f"\n📈 METADATA:")
        print(f"  Words: {result['word_count']}")
        print(f"  Sentences: {result['sentence_count']}")
        print(f"  Sentiment: {result['sentiment']}")
        print(f"  AI Generated: {result.get('ai_generated', False)}")
        print(f"  Model: {result.get('ai_model', 'N/A')}")
        
        print("\n" + "=" * 60)
        print("✅ TEST PASSED - AI Integration Working!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\n" + "=" * 60)
        print("⚠️  TEST FAILED - Check error above")
        print("=" * 60)
        print("\n💡 TROUBLESHOOTING:")
        print("  1. Make sure HUGGINGFACE_TOKEN is set in .env")
        print("  2. Check internet connection")
        print("  3. Verify HF token is valid")
        print("  4. System will fallback to basic mode if AI fails")
        return False

if __name__ == '__main__':
    test_ai_analyzer()
