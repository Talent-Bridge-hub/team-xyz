"""
Database Migration: Create interview-related tables
Creates tables for interview sessions, questions, answers, and feedback
"""

import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(backend_dir)
sys.path.insert(0, project_root)

from config import database as db_module


def create_interview_tables():
    """
    Create all interview-related tables
    """
    
    # Drop existing tables if they exist (for clean migration)
    drop_queries = [
        "DROP TABLE IF EXISTS interview_feedback CASCADE;",
        "DROP TABLE IF EXISTS interview_answers CASCADE;",
        "DROP TABLE IF EXISTS interview_questions CASCADE;",
        "DROP TABLE IF EXISTS interview_sessions CASCADE;",
        "DROP TABLE IF EXISTS question_bank CASCADE;"
    ]
    
    # 1. Question Bank table (stores all available questions)
    create_question_bank = """
    CREATE TABLE IF NOT EXISTS question_bank (
        id SERIAL PRIMARY KEY,
        question_text TEXT NOT NULL,
        question_type VARCHAR(50) NOT NULL,
        category VARCHAR(100),
        difficulty_level VARCHAR(20) NOT NULL,
        job_roles TEXT[] DEFAULT '{}',
        required_skills TEXT[] DEFAULT '{}',
        region VARCHAR(50) DEFAULT 'all',
        sample_answer TEXT,
        key_points TEXT[] DEFAULT '{}',
        common_mistakes TEXT[] DEFAULT '{}',
        follow_up_questions TEXT[] DEFAULT '{}',
        difficulty_score INTEGER DEFAULT 50,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # 2. Interview Sessions table
    create_sessions = """
    CREATE TABLE IF NOT EXISTS interview_sessions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        resume_id INTEGER,
        session_type VARCHAR(50) NOT NULL,
        job_role VARCHAR(200) NOT NULL,
        difficulty_level VARCHAR(20) NOT NULL,
        total_questions INTEGER NOT NULL,
        questions_answered INTEGER DEFAULT 0,
        status VARCHAR(20) DEFAULT 'in_progress',
        average_score FLOAT,
        duration_seconds INTEGER,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE SET NULL
    );
    """
    
    # 3. Interview Questions table (links questions to sessions)
    create_interview_questions = """
    CREATE TABLE IF NOT EXISTS interview_questions (
        id SERIAL PRIMARY KEY,
        session_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        question_order INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES interview_sessions(id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES question_bank(id) ON DELETE CASCADE
    );
    """
    
    # 4. Interview Answers table
    create_answers = """
    CREATE TABLE IF NOT EXISTS interview_answers (
        id SERIAL PRIMARY KEY,
        interview_question_id INTEGER NOT NULL,
        session_id INTEGER NOT NULL,
        user_answer TEXT NOT NULL,
        time_taken_seconds INTEGER NOT NULL,
        relevance_score FLOAT NOT NULL,
        completeness_score FLOAT NOT NULL,
        clarity_score FLOAT NOT NULL,
        technical_accuracy_score FLOAT NOT NULL,
        communication_score FLOAT NOT NULL,
        overall_score FLOAT NOT NULL,
        strengths TEXT,
        weaknesses TEXT,
        missing_points TEXT,
        suggestions TEXT,
        ai_feedback TEXT,
        word_count INTEGER,
        sentiment VARCHAR(50),
        answer_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (interview_question_id) REFERENCES interview_questions(id) ON DELETE CASCADE,
        FOREIGN KEY (session_id) REFERENCES interview_sessions(id) ON DELETE CASCADE
    );
    """
    
    # 5. Interview Feedback table (overall session feedback)
    create_feedback = """
    CREATE TABLE IF NOT EXISTS interview_feedback (
        id SERIAL PRIMARY KEY,
        session_id INTEGER NOT NULL UNIQUE,
        overall_performance VARCHAR(50) NOT NULL,
        technical_rating INTEGER CHECK (technical_rating >= 1 AND technical_rating <= 5),
        communication_rating INTEGER CHECK (communication_rating >= 1 AND communication_rating <= 5),
        confidence_rating INTEGER CHECK (confidence_rating >= 1 AND confidence_rating <= 5),
        key_strengths TEXT,
        areas_to_improve TEXT,
        recommended_resources TEXT,
        preparation_tips TEXT,
        practice_recommendations TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (session_id) REFERENCES interview_sessions(id) ON DELETE CASCADE
    );
    """
    
    # Indexes for better query performance
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON interview_sessions(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_sessions_status ON interview_sessions(status);",
        "CREATE INDEX IF NOT EXISTS idx_sessions_started_at ON interview_sessions(started_at DESC);",
        "CREATE INDEX IF NOT EXISTS idx_questions_session_id ON interview_questions(session_id);",
        "CREATE INDEX IF NOT EXISTS idx_answers_session_id ON interview_answers(session_id);",
        "CREATE INDEX IF NOT EXISTS idx_question_bank_type ON question_bank(question_type);",
        "CREATE INDEX IF NOT EXISTS idx_question_bank_difficulty ON question_bank(difficulty_level);",
        "CREATE INDEX IF NOT EXISTS idx_question_bank_job_roles ON question_bank USING GIN(job_roles);",
    ]
    
    try:
        print("Creating interview tables...")
        
        # Initialize connection pool
        db_module.initialize_connection_pool()
        
        # Drop existing tables
        print("  - Dropping existing tables if they exist...")
        for query in drop_queries:
            db_module.execute_query(query, fetch=False)
        
        # Create tables
        print("  - Creating question_bank table...")
        db_module.execute_query(create_question_bank, fetch=False)
        
        print("  - Creating interview_sessions table...")
        db_module.execute_query(create_sessions, fetch=False)
        
        print("  - Creating interview_questions table...")
        db_module.execute_query(create_interview_questions, fetch=False)
        
        print("  - Creating interview_answers table...")
        db_module.execute_query(create_answers, fetch=False)
        
        print("  - Creating interview_feedback table...")
        db_module.execute_query(create_feedback, fetch=False)
        
        # Create indexes
        print("  - Creating indexes...")
        for index_query in indexes:
            db_module.execute_query(index_query, fetch=False)
        
        # Seed question bank with sample questions
        print("  - Seeding question bank with sample questions...")
        seed_sample_questions()
        
        print("✓ Interview tables created successfully!")
        print("\nTables created:")
        print("  - question_bank: Stores all interview questions")
        print("  - interview_sessions: Tracks interview sessions")
        print("  - interview_questions: Links questions to sessions")
        print("  - interview_answers: Stores user answers and scores")
        print("  - interview_feedback: Overall session feedback")
        print("\n✓ Created 8 indexes for optimized queries")
        print("✓ Seeded question bank with sample questions")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating interview tables: {e}")
        import traceback
        traceback.print_exc()
        return False


def seed_sample_questions():
    """Seed the question bank with sample interview questions"""
    
    sample_questions = [
        # Technical Questions
        {
            'question_text': 'Explain the difference between REST and GraphQL APIs. When would you choose one over the other?',
            'question_type': 'technical',
            'category': 'APIs',
            'difficulty_level': 'mid',
            'job_roles': ['Software Engineer', 'Backend Developer', 'Full Stack Developer'],
            'required_skills': ['REST', 'GraphQL', 'APIs'],
            'region': 'all',
            'key_points': ['REST uses multiple endpoints', 'GraphQL uses single endpoint', 'REST over-fetching/under-fetching', 'GraphQL precise data fetching'],
            'common_mistakes': ['Not mentioning trade-offs', 'Only theoretical knowledge'],
            'follow_up_questions': ['Have you implemented GraphQL in production?', 'How do you handle caching?'],
            'difficulty_score': 60
        },
        {
            'question_text': 'What is your experience with database optimization? Describe a time when you improved query performance.',
            'question_type': 'technical',
            'category': 'Database',
            'difficulty_level': 'senior',
            'job_roles': ['Software Engineer', 'Backend Developer', 'Database Administrator'],
            'required_skills': ['SQL', 'Database', 'Performance'],
            'region': 'all',
            'key_points': ['Identified slow queries', 'Used indexing', 'Query optimization techniques', 'Measurable results'],
            'common_mistakes': ['Vague answers', 'No specific metrics'],
            'follow_up_questions': ['What tools did you use?', 'How much improvement did you achieve?'],
            'difficulty_score': 75
        },
        {
            'question_text': 'Explain how you would design a scalable system for handling 1 million concurrent users.',
            'question_type': 'technical',
            'category': 'System Design',
            'difficulty_level': 'senior',
            'job_roles': ['Software Engineer', 'System Architect', 'Backend Developer'],
            'required_skills': ['System Design', 'Scalability', 'Architecture'],
            'region': 'all',
            'key_points': ['Load balancing', 'Caching', 'Database sharding', 'Microservices', 'CDN'],
            'common_mistakes': ['Not considering bottlenecks', 'Ignoring trade-offs'],
            'follow_up_questions': ['How would you handle database writes?', 'What about data consistency?'],
            'difficulty_score': 85
        },
        
        # Behavioral Questions
        {
            'question_text': 'Tell me about a time when you had to work under pressure to meet a tight deadline. How did you handle it?',
            'question_type': 'behavioral',
            'category': 'Stress Management',
            'difficulty_level': 'junior',
            'job_roles': ['Software Engineer', 'Developer', 'Any'],
            'required_skills': [],
            'region': 'all',
            'key_points': ['Situation description', 'Actions taken', 'Prioritization', 'Result achieved'],
            'common_mistakes': ['Blaming others', 'Not showing problem-solving'],
            'follow_up_questions': ['What would you do differently?', 'What did you learn?'],
            'difficulty_score': 40
        },
        {
            'question_text': 'Describe a situation where you had a conflict with a team member. How did you resolve it?',
            'question_type': 'behavioral',
            'category': 'Teamwork',
            'difficulty_level': 'mid',
            'job_roles': ['Software Engineer', 'Developer', 'Any'],
            'required_skills': [],
            'region': 'all',
            'key_points': ['Clear conflict description', 'Communication approach', 'Resolution steps', 'Positive outcome'],
            'common_mistakes': ['Avoiding the question', 'Being confrontational'],
            'follow_up_questions': ['What did you learn?', 'How is your relationship now?'],
            'difficulty_score': 55
        },
        
        # Situational Questions
        {
            'question_text': 'If you discovered a critical bug in production right before a major release, what would you do?',
            'question_type': 'situational',
            'category': 'Problem Solving',
            'difficulty_level': 'mid',
            'job_roles': ['Software Engineer', 'Developer', 'Any'],
            'required_skills': [],
            'region': 'all',
            'key_points': ['Assess severity', 'Inform stakeholders', 'Quick fix vs rollback', 'Risk analysis'],
            'common_mistakes': ['Panic response', 'Not considering options'],
            'follow_up_questions': ['How would you prevent this?', 'Who would you notify first?'],
            'difficulty_score': 65
        },
    ]
    
    for question in sample_questions:
        try:
            db_module.insert_one('question_bank', question)
        except Exception as e:
            print(f"  ⚠  Error inserting question: {e}")
    
    print(f"  ✓ Seeded {len(sample_questions)} sample questions")


if __name__ == '__main__':
    print("=" * 70)
    print("Database Migration: Create Interview Tables")
    print("=" * 70)
    print()
    
    success = create_interview_tables()
    
    if success:
        print("\n" + "=" * 70)
        print("Migration completed successfully!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("Migration failed!")
        print("=" * 70)
        sys.exit(1)
