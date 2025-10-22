-- UtopiaHire Interview Module - Database Schema
-- AI-powered interview simulator with question bank and answer analysis

-- Interview sessions table: Track user interview practice sessions
CREATE TABLE IF NOT EXISTS interview_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    session_type VARCHAR(50) NOT NULL,  -- 'technical', 'behavioral', 'mixed', 'job-specific'
    job_role VARCHAR(255),  -- Target role (e.g., 'Software Engineer', 'Data Analyst')
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('junior', 'mid', 'senior')),
    total_questions INTEGER DEFAULT 0,
    questions_answered INTEGER DEFAULT 0,
    average_score FLOAT,  -- Overall session score (0-100)
    status VARCHAR(20) CHECK (status IN ('in_progress', 'completed', 'abandoned')),
    duration_seconds INTEGER,  -- Total time spent
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    notes TEXT  -- User notes or session summary
);

-- Question bank: Comprehensive interview questions database
CREATE TABLE IF NOT EXISTS question_bank (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,  -- 'technical', 'behavioral', 'situational', 'coding', 'system_design'
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('junior', 'mid', 'senior', 'all')),
    category VARCHAR(100),  -- 'algorithms', 'data_structures', 'web_dev', 'leadership', 'problem_solving'
    required_skills TEXT[],  -- Array of skills needed to answer (e.g., ['Python', 'OOP'])
    job_roles TEXT[],  -- Relevant roles (e.g., ['Software Engineer', 'Backend Developer'])
    region VARCHAR(100),  -- 'MENA', 'Sub-Saharan Africa', 'Global'
    sample_answer TEXT,  -- High-quality reference answer
    key_points JSONB,  -- Must-mention points in good answer
    common_mistakes JSONB,  -- What to avoid
    follow_up_questions TEXT[],  -- Potential follow-ups
    difficulty_score INTEGER CHECK (difficulty_score >= 1 AND difficulty_score <= 10),
    usage_count INTEGER DEFAULT 0,  -- Track question popularity
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interview questions asked: Track which questions were asked in each session
CREATE TABLE IF NOT EXISTS interview_questions (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES interview_sessions(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES question_bank(id) ON DELETE CASCADE,
    question_order INTEGER,  -- Order in session (1, 2, 3...)
    asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_limit_seconds INTEGER,  -- Optional time limit
    UNIQUE(session_id, question_order)
);

-- Interview answers: Store user answers and AI analysis
CREATE TABLE IF NOT EXISTS interview_answers (
    id SERIAL PRIMARY KEY,
    interview_question_id INTEGER REFERENCES interview_questions(id) ON DELETE CASCADE,
    session_id INTEGER REFERENCES interview_sessions(id) ON DELETE CASCADE,
    user_answer TEXT NOT NULL,
    answer_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_taken_seconds INTEGER,  -- How long to answer
    
    -- AI Analysis scores (0-100)
    relevance_score INTEGER CHECK (relevance_score >= 0 AND relevance_score <= 100),
    completeness_score INTEGER CHECK (completeness_score >= 0 AND completeness_score <= 100),
    clarity_score INTEGER CHECK (clarity_score >= 0 AND clarity_score <= 100),
    technical_accuracy_score INTEGER CHECK (technical_accuracy_score >= 0 AND technical_accuracy_score <= 100),
    communication_score INTEGER CHECK (communication_score >= 0 AND communication_score <= 100),
    overall_score INTEGER CHECK (overall_score >= 0 AND overall_score <= 100),
    
    -- AI Feedback
    strengths JSONB,  -- What was good about the answer
    weaknesses JSONB,  -- What could be improved
    missing_points JSONB,  -- Key points not mentioned
    suggestions JSONB,  -- Improvement suggestions
    ai_feedback TEXT,  -- Overall narrative feedback
    
    -- Metadata
    word_count INTEGER,
    sentiment VARCHAR(20),  -- 'positive', 'neutral', 'negative', 'confident', 'uncertain'
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interview feedback summary: Overall session feedback
CREATE TABLE IF NOT EXISTS interview_feedback (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES interview_sessions(id) ON DELETE CASCADE,
    overall_performance VARCHAR(50),  -- 'excellent', 'good', 'average', 'needs_improvement'
    technical_rating INTEGER CHECK (technical_rating >= 1 AND technical_rating <= 5),
    communication_rating INTEGER CHECK (communication_rating >= 1 AND communication_rating <= 5),
    confidence_rating INTEGER CHECK (confidence_rating >= 1 AND confidence_rating <= 5),
    
    -- Strengths and Areas for Improvement
    key_strengths JSONB,
    areas_to_improve JSONB,
    recommended_resources JSONB,  -- Links, courses, articles
    
    -- Preparation advice
    preparation_tips TEXT,
    practice_recommendations TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_interview_sessions_user_id ON interview_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_interview_sessions_status ON interview_sessions(status);
CREATE INDEX IF NOT EXISTS idx_interview_questions_session_id ON interview_questions(session_id);
CREATE INDEX IF NOT EXISTS idx_interview_answers_session_id ON interview_answers(session_id);
CREATE INDEX IF NOT EXISTS idx_question_bank_type ON question_bank(question_type);
CREATE INDEX IF NOT EXISTS idx_question_bank_difficulty ON question_bank(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_question_bank_category ON question_bank(category);
CREATE INDEX IF NOT EXISTS idx_interview_feedback_session_id ON interview_feedback(session_id);

-- GIN indexes for array columns (faster searching)
CREATE INDEX IF NOT EXISTS idx_question_bank_skills ON question_bank USING GIN (required_skills);
CREATE INDEX IF NOT EXISTS idx_question_bank_roles ON question_bank USING GIN (job_roles);

-- Create trigger to update question_bank.updated_at
CREATE TRIGGER update_question_bank_updated_at BEFORE UPDATE ON question_bank
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample interview questions for MENA/Africa tech roles

-- TECHNICAL QUESTIONS - Junior Level
INSERT INTO question_bank (question_text, question_type, difficulty_level, category, required_skills, job_roles, region, sample_answer, key_points, difficulty_score) VALUES
('What is the difference between a list and a tuple in Python?', 'technical', 'junior', 'programming_fundamentals', ARRAY['Python'], ARRAY['Software Engineer', 'Backend Developer', 'Data Analyst'], 'Global', 
'A list is mutable (can be changed after creation) while a tuple is immutable (cannot be changed). Lists use square brackets [], tuples use parentheses (). Lists are better for data that changes, tuples for fixed data. Tuples are faster and can be used as dictionary keys.',
'{"must_mention": ["mutability difference", "syntax difference", "use cases"], "bonus_points": ["performance", "dictionary keys", "memory efficiency"]}',
2),

('Explain what RESTful APIs are and their main principles.', 'technical', 'junior', 'web_development', ARRAY['REST APIs', 'HTTP'], ARRAY['Software Engineer', 'Full Stack Developer', 'Backend Developer'], 'Global',
'REST (Representational State Transfer) is an architectural style for web services. Main principles: 1) Stateless (each request is independent), 2) Client-Server separation, 3) Uniform interface (standard HTTP methods), 4) Resource-based (URLs identify resources), 5) Use of HTTP methods (GET, POST, PUT, DELETE). RESTful APIs return data in JSON or XML format.',
'{"must_mention": ["stateless", "HTTP methods", "resources", "client-server"], "bonus_points": ["caching", "JSON format", "status codes"]}',
3),

-- TECHNICAL QUESTIONS - Mid Level
('How would you optimize a slow database query?', 'technical', 'mid', 'databases', ARRAY['SQL', 'Database Optimization'], ARRAY['Software Engineer', 'Backend Developer', 'Data Engineer'], 'Global',
'I would: 1) Use EXPLAIN to analyze the query execution plan, 2) Add indexes on frequently queried columns, 3) Avoid SELECT *, query only needed columns, 4) Use JOIN instead of subqueries when possible, 5) Check for N+1 query problems, 6) Consider database-specific optimizations (partitioning, materialized views), 7) Monitor query performance metrics, 8) Cache frequent queries if data doesn''t change often.',
'{"must_mention": ["indexes", "EXPLAIN/query plan", "avoid unnecessary columns"], "bonus_points": ["N+1 problem", "caching", "partitioning", "monitoring"]}',
5),

('Describe the difference between synchronous and asynchronous programming.', 'technical', 'mid', 'programming_concepts', ARRAY['JavaScript', 'Python', 'Async'], ARRAY['Software Engineer', 'Full Stack Developer'], 'Global',
'Synchronous programming executes tasks sequentially - each task waits for the previous to complete. Asynchronous programming allows tasks to run independently without blocking. Use async for I/O operations (API calls, file reads) to improve performance. Examples: JavaScript promises/async-await, Python asyncio. Benefits: better resource utilization, improved user experience, handling concurrent operations.',
'{"must_mention": ["blocking vs non-blocking", "use cases", "performance benefits"], "bonus_points": ["specific examples", "callbacks/promises", "event loop"]}',
4),

-- BEHAVIORAL QUESTIONS
('Tell me about a time when you had to learn a new technology quickly for a project.', 'behavioral', 'all', 'learning_adaptability', ARRAY[]::text[], ARRAY['Software Engineer', 'Full Stack Developer', 'Data Scientist'], 'Global',
'In my previous role, we needed to migrate to a new framework within 3 weeks. I created a structured learning plan: 1) Official documentation first 2 hours daily, 2) Built small projects to practice, 3) Joined online communities for help, 4) Paired with experienced developers. Successfully completed migration on time. Key lesson: structured approach + hands-on practice + community support accelerates learning.',
'{"must_mention": ["specific situation", "learning approach", "outcome", "lesson learned"], "bonus_points": ["time management", "resources used", "measurable results"]}',
4),

('How do you handle disagreements with team members about technical decisions?', 'behavioral', 'all', 'teamwork', ARRAY['Communication']::text[], ARRAY['Software Engineer', 'Team Lead', 'Full Stack Developer'], 'Global',
'I approach disagreements professionally: 1) Listen to understand their perspective, 2) Present my view with data/examples, 3) Focus on project goals not personal opinions, 4) Suggest proof-of-concept if unclear, 5) Defer to senior/lead if needed. Example: Disagreed on database choice, we created benchmarks comparing both options, data showed PostgreSQL better for our use case. Maintained positive relationship throughout.',
'{"must_mention": ["respectful communication", "data-driven approach", "focus on goals", "specific example"], "bonus_points": ["compromise", "maintaining relationships", "learning from others"]}',
4),

-- SITUATIONAL QUESTIONS
('You discover a critical bug in production on a Friday evening. What do you do?', 'situational', 'mid', 'problem_solving', ARRAY[]::text[], ARRAY['Software Engineer', 'DevOps Engineer', 'Backend Developer'], 'Global',
'1) Assess severity - does it affect users immediately? 2) Notify team lead and stakeholders, 3) Check if quick rollback is possible, 4) If urgent: implement hotfix with minimal changes, deploy, monitor, 5) Document incident thoroughly, 6) Schedule proper fix + testing for next week, 7) Post-mortem to prevent recurrence. Communication is key - keep stakeholders informed throughout.',
'{"must_mention": ["assess impact", "communicate", "immediate action", "documentation", "follow-up"], "bonus_points": ["monitoring", "rollback strategy", "post-mortem"]}',
6),

('A client wants a feature that you know will cause performance issues. How do you handle it?', 'situational', 'senior', 'communication', ARRAY['Communication']::text[], ARRAY['Software Engineer', 'Tech Lead', 'Solutions Architect'], 'Global',
'1) Understand the business need behind the request, 2) Explain technical concerns with concrete examples/data, 3) Propose alternatives that meet business need without performance issues, 4) If they insist: provide impact analysis (load times, cost), suggest phased approach or optimization plan, 5) Document decision and risks. Balance: respect client needs while providing expert guidance.',
'{"must_mention": ["understand business need", "explain technical concerns", "propose alternatives", "document risks"], "bonus_points": ["data/examples", "compromise solutions", "long-term thinking"]}',
7),

-- MENA-SPECIFIC QUESTIONS
('How would you approach working in a multilingual team (Arabic, French, English)?', 'behavioral', 'all', 'communication', ARRAY['Communication']::text[], ARRAY['Software Engineer', 'Team Lead'], 'MENA',
'Embrace diversity as strength. Strategies: 1) Use English for technical documentation (universal standard), 2) Be patient with non-native speakers, 3) Use visual aids (diagrams, code examples), 4) Confirm understanding through summaries, 5) Leverage translation tools when needed, 6) Learn basic phrases in teammates'' languages to build rapport. Focus on clear communication over perfect language.',
'{"must_mention": ["documentation language", "clear communication", "patience", "visual aids"], "bonus_points": ["cultural awareness", "learning languages", "building rapport"]}',
3),

-- SUB-SAHARAN AFRICA-SPECIFIC QUESTIONS
('Many companies in Africa face infrastructure challenges (power, internet). How would you design a system for such environments?', 'technical', 'mid', 'system_design', ARRAY['System Design'], ARRAY['Software Engineer', 'Solutions Architect', 'Full Stack Developer'], 'Sub-Saharan Africa',
'Design for offline-first: 1) Local data storage (IndexedDB, SQLite), 2) Progressive Web Apps for mobile, 3) Sync when online, queue changes, 4) Minimize bandwidth (compress data, lazy loading), 5) Graceful degradation (core features work offline), 6) Status indicators for sync state, 7) Battery optimization. Example: M-Pesa works offline then syncs. Test on low-end devices and slow networks.',
'{"must_mention": ["offline-first design", "local storage", "sync strategy", "bandwidth optimization"], "bonus_points": ["real-world example", "mobile-first", "testing approach", "user experience"]}',
6);

-- Add more questions for different categories
INSERT INTO question_bank (question_text, question_type, difficulty_level, category, required_skills, job_roles, region, key_points, difficulty_score) VALUES
('What is your experience with version control systems like Git?', 'technical', 'junior', 'tools', ARRAY['Git'], ARRAY['Software Engineer', 'Full Stack Developer'], 'Global',
'{"must_mention": ["basic commands", "branching", "collaboration"], "bonus_points": ["merge conflicts", "git flow", "best practices"]}', 2),

('Explain the concept of object-oriented programming.', 'technical', 'junior', 'programming_fundamentals', ARRAY['OOP'], ARRAY['Software Engineer', 'Backend Developer'], 'Global',
'{"must_mention": ["classes and objects", "encapsulation", "inheritance", "polymorphism"], "bonus_points": ["abstraction", "real-world examples"]}', 3),

('How do you ensure code quality in your projects?', 'behavioral', 'mid', 'best_practices', ARRAY['Testing', 'Code Review'], ARRAY['Software Engineer', 'Team Lead'], 'Global',
'{"must_mention": ["testing", "code reviews", "coding standards"], "bonus_points": ["CI/CD", "linting", "documentation"]}', 4),

('Describe a challenging bug you fixed and how you approached it.', 'behavioral', 'all', 'problem_solving', ARRAY[]::text[], ARRAY['Software Engineer', 'Full Stack Developer'], 'Global',
'{"must_mention": ["problem description", "debugging process", "solution", "lessons learned"], "bonus_points": ["tools used", "prevented future issues"]}', 5);

COMMENT ON TABLE interview_sessions IS 'Tracks user interview practice sessions';
COMMENT ON TABLE question_bank IS 'Comprehensive database of interview questions';
COMMENT ON TABLE interview_questions IS 'Questions asked in each session';
COMMENT ON TABLE interview_answers IS 'User answers with AI analysis and scoring';
COMMENT ON TABLE interview_feedback IS 'Overall session feedback and recommendations';
