-- Interview Question Bank Schema and Sample Data
-- This creates the question bank and populates it with interview questions

-- Create question bank table
CREATE TABLE IF NOT EXISTS interview_question_bank (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL, -- 'technical', 'behavioral', 'situational'
    category VARCHAR(100), -- 'programming', 'system_design', 'leadership', etc.
    difficulty_level VARCHAR(20) NOT NULL, -- 'junior', 'mid', 'senior'
    job_roles TEXT[], -- Array of applicable job roles
    key_points JSONB, -- Expected key points in answer
    sample_answer TEXT,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_question_type ON interview_question_bank(question_type);
CREATE INDEX IF NOT EXISTS idx_difficulty_level ON interview_question_bank(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_job_roles ON interview_question_bank USING GIN(job_roles);

-- Insert Technical Questions for Software Engineers

-- Junior Level Technical
INSERT INTO interview_question_bank (question_text, question_type, category, difficulty_level, job_roles, key_points, tags) VALUES
('Explain the difference between var, let, and const in JavaScript.', 'technical', 'programming', 'junior', 
 ARRAY['Software Engineer', 'Frontend Developer', 'Full Stack Developer'],
 '{"must_mention": ["var is function-scoped", "let is block-scoped", "const is immutable"], "bonus_points": ["hoisting", "temporal dead zone"]}',
 ARRAY['javascript', 'variables', 'fundamentals']),

('What is the difference between == and === in JavaScript?', 'technical', 'programming', 'junior',
 ARRAY['Software Engineer', 'Frontend Developer', 'Full Stack Developer'],
 '{"must_mention": ["== type coercion", "=== strict equality", "checks type and value"], "bonus_points": ["performance", "best practices"]}',
 ARRAY['javascript', 'operators', 'comparison']),

('What is a REST API and how does it work?', 'technical', 'web_development', 'junior',
 ARRAY['Software Engineer', 'Backend Developer', 'Full Stack Developer'],
 '{"must_mention": ["HTTP methods", "stateless", "resources", "endpoints"], "bonus_points": ["CRUD operations", "status codes"]}',
 ARRAY['api', 'rest', 'http']),

('Explain what Git is and why version control is important.', 'technical', 'tools', 'junior',
 ARRAY['Software Engineer', 'DevOps Engineer', 'Full Stack Developer'],
 '{"must_mention": ["version control", "collaboration", "history tracking", "branching"], "bonus_points": ["git commands", "workflow"]}',
 ARRAY['git', 'version-control', 'collaboration']),

('What is the difference between SQL and NoSQL databases?', 'technical', 'database', 'junior',
 ARRAY['Software Engineer', 'Backend Developer', 'Database Administrator'],
 '{"must_mention": ["relational vs non-relational", "schema", "use cases"], "bonus_points": ["examples", "scalability"]}',
 ARRAY['database', 'sql', 'nosql']);

-- Mid Level Technical
INSERT INTO interview_question_bank (question_text, question_type, category, difficulty_level, job_roles, key_points, tags) VALUES
('Explain how React hooks work and give examples of useState and useEffect.', 'technical', 'frontend', 'mid',
 ARRAY['Software Engineer', 'Frontend Developer', 'Full Stack Developer'],
 '{"must_mention": ["state management", "side effects", "lifecycle", "examples"], "bonus_points": ["custom hooks", "dependency array", "performance"]}',
 ARRAY['react', 'hooks', 'frontend']),

('What are microservices and what are their advantages and disadvantages?', 'technical', 'architecture', 'mid',
 ARRAY['Software Engineer', 'Backend Developer', 'Solutions Architect'],
 '{"must_mention": ["independent services", "scalability", "complexity"], "bonus_points": ["vs monolith", "communication patterns", "deployment"]}',
 ARRAY['architecture', 'microservices', 'design']),

('Explain the CAP theorem and its implications for distributed systems.', 'technical', 'distributed_systems', 'mid',
 ARRAY['Software Engineer', 'Backend Developer', 'Solutions Architect'],
 '{"must_mention": ["Consistency", "Availability", "Partition tolerance", "tradeoffs"], "bonus_points": ["real-world examples", "eventual consistency"]}',
 ARRAY['distributed-systems', 'theory', 'architecture']),

('How would you optimize a slow database query?', 'technical', 'performance', 'mid',
 ARRAY['Software Engineer', 'Backend Developer', 'Database Administrator'],
 '{"must_mention": ["indexes", "query analysis", "execution plan"], "bonus_points": ["caching", "denormalization", "query rewriting"]}',
 ARRAY['database', 'optimization', 'performance']),

('Explain dependency injection and why it is useful.', 'technical', 'design_patterns', 'mid',
 ARRAY['Software Engineer', 'Backend Developer'],
 '{"must_mention": ["decoupling", "testability", "flexibility"], "bonus_points": ["inversion of control", "examples", "frameworks"]}',
 ARRAY['design-patterns', 'dependency-injection', 'architecture']);

-- Senior Level Technical
INSERT INTO interview_question_bank (question_text, question_type, category, difficulty_level, job_roles, key_points, tags) VALUES
('Design a system like Twitter that can handle millions of users. Discuss scalability, data storage, and real-time updates.', 'technical', 'system_design', 'senior',
 ARRAY['Software Engineer', 'Solutions Architect', 'Tech Lead'],
 '{"must_mention": ["load balancing", "caching", "database sharding", "message queue", "CDN"], "bonus_points": ["fan-out strategy", "timeline generation", "search"]}',
 ARRAY['system-design', 'scalability', 'architecture']),

('How would you design a rate limiter for an API? Discuss algorithms and implementation.', 'technical', 'system_design', 'senior',
 ARRAY['Software Engineer', 'Backend Developer', 'Solutions Architect'],
 '{"must_mention": ["token bucket", "sliding window", "distributed systems"], "bonus_points": ["redis", "performance", "edge cases"]}',
 ARRAY['system-design', 'rate-limiting', 'algorithms']),

('Explain event-driven architecture and when you would use it.', 'technical', 'architecture', 'senior',
 ARRAY['Software Engineer', 'Solutions Architect', 'Backend Developer'],
 '{"must_mention": ["events", "publishers", "subscribers", "asynchronous"], "bonus_points": ["event sourcing", "CQRS", "message brokers"]}',
 ARRAY['architecture', 'event-driven', 'design-patterns']);

-- Behavioral Questions

-- Junior Level Behavioral
INSERT INTO interview_question_bank (question_text, question_type, category, difficulty_level, job_roles, key_points, tags) VALUES
('Tell me about a time you had to learn a new technology quickly.', 'behavioral', 'learning', 'junior',
 ARRAY['Software Engineer', 'Frontend Developer', 'Backend Developer'],
 '{"must_mention": ["situation", "learning approach", "outcome"], "bonus_points": ["resources used", "challenges", "application"]}',
 ARRAY['learning', 'adaptability', 'growth']),

('Describe a challenging bug you fixed. How did you approach it?', 'behavioral', 'problem_solving', 'junior',
 ARRAY['Software Engineer', 'Full Stack Developer'],
 '{"must_mention": ["problem", "debugging process", "solution", "result"], "bonus_points": ["tools used", "learnings", "prevention"]}',
 ARRAY['debugging', 'problem-solving', 'technical']),

('Tell me about a time you worked on a team project.', 'behavioral', 'teamwork', 'junior',
 ARRAY['Software Engineer', 'Frontend Developer', 'Backend Developer'],
 '{"must_mention": ["role", "collaboration", "outcome"], "bonus_points": ["challenges", "communication", "contribution"]}',
 ARRAY['teamwork', 'collaboration', 'communication']);

-- Mid Level Behavioral
INSERT INTO interview_question_bank (question_text, question_type, category, difficulty_level, job_roles, key_points, tags) VALUES
('Describe a time when you had to make a technical decision with incomplete information.', 'behavioral', 'decision_making', 'mid',
 ARRAY['Software Engineer', 'Tech Lead', 'Solutions Architect'],
 '{"must_mention": ["situation", "analysis", "decision", "outcome"], "bonus_points": ["tradeoffs", "stakeholders", "lessons learned"]}',
 ARRAY['decision-making', 'critical-thinking', 'leadership']),

('Tell me about a time you disagreed with a team member about a technical approach. How did you handle it?', 'behavioral', 'conflict_resolution', 'mid',
 ARRAY['Software Engineer', 'Tech Lead', 'Senior Developer'],
 '{"must_mention": ["disagreement", "communication", "resolution", "outcome"], "bonus_points": ["respect", "data-driven", "compromise"]}',
 ARRAY['conflict-resolution', 'communication', 'teamwork']),

('Describe a project where you had to balance technical debt with new features.', 'behavioral', 'prioritization', 'mid',
 ARRAY['Software Engineer', 'Tech Lead', 'Engineering Manager'],
 '{"must_mention": ["situation", "prioritization", "approach", "result"], "bonus_points": ["stakeholder management", "metrics", "tradeoffs"]}',
 ARRAY['prioritization', 'technical-debt', 'management']);

-- Senior Level Behavioral
INSERT INTO interview_question_bank (question_text, question_type, category, difficulty_level, job_roles, key_points, tags) VALUES
('Tell me about a time you led a technical initiative that had significant business impact.', 'behavioral', 'leadership', 'senior',
 ARRAY['Tech Lead', 'Engineering Manager', 'Solutions Architect'],
 '{"must_mention": ["initiative", "leadership", "business impact", "outcome"], "bonus_points": ["metrics", "team management", "challenges"]}',
 ARRAY['leadership', 'impact', 'business']),

('Describe how you mentored junior developers and helped them grow.', 'behavioral', 'mentorship', 'senior',
 ARRAY['Senior Developer', 'Tech Lead', 'Engineering Manager'],
 '{"must_mention": ["approach", "specific examples", "growth", "impact"], "bonus_points": ["feedback", "teaching methods", "long-term results"]}',
 ARRAY['mentorship', 'leadership', 'team-development']),

('Tell me about a time you had to make a critical architecture decision under pressure.', 'behavioral', 'leadership', 'senior',
 ARRAY['Solutions Architect', 'Tech Lead', 'Engineering Manager'],
 '{"must_mention": ["situation", "analysis", "decision", "execution", "outcome"], "bonus_points": ["stakeholder communication", "risk management", "lessons"]}',
 ARRAY['architecture', 'decision-making', 'leadership']);

-- Data Science / ML Questions
INSERT INTO interview_question_bank (question_text, question_type, category, difficulty_level, job_roles, key_points, tags) VALUES
('Explain the bias-variance tradeoff in machine learning.', 'technical', 'machine_learning', 'mid',
 ARRAY['Data Scientist', 'ML Engineer', 'AI Engineer'],
 '{"must_mention": ["bias", "variance", "overfitting", "underfitting"], "bonus_points": ["model complexity", "examples", "solutions"]}',
 ARRAY['machine-learning', 'theory', 'modeling']),

('How would you approach building a recommendation system?', 'technical', 'machine_learning', 'senior',
 ARRAY['Data Scientist', 'ML Engineer', 'Senior Software Engineer'],
 '{"must_mention": ["collaborative filtering", "content-based", "data collection", "evaluation"], "bonus_points": ["cold start", "scalability", "real-time"]}',
 ARRAY['recommendation-systems', 'machine-learning', 'system-design']);

-- DevOps Questions
INSERT INTO interview_question_bank (question_text, question_type, category, difficulty_level, job_roles, key_points, tags) VALUES
('Explain what CI/CD is and why it is important.', 'technical', 'devops', 'mid',
 ARRAY['DevOps Engineer', 'Software Engineer', 'Site Reliability Engineer'],
 '{"must_mention": ["continuous integration", "continuous deployment", "automation", "testing"], "bonus_points": ["tools", "pipeline", "benefits"]}',
 ARRAY['cicd', 'devops', 'automation']),

('How would you design a monitoring and alerting system for a production application?', 'technical', 'infrastructure', 'senior',
 ARRAY['DevOps Engineer', 'Site Reliability Engineer', 'Solutions Architect'],
 '{"must_mention": ["metrics", "logs", "traces", "alerting", "dashboards"], "bonus_points": ["tools", "incident response", "SLOs"]}',
 ARRAY['monitoring', 'observability', 'infrastructure']);

-- Product Manager Questions
INSERT INTO interview_question_bank (question_text, question_type, category, difficulty_level, job_roles, key_points, tags) VALUES
('How would you prioritize features for a product roadmap?', 'behavioral', 'product_management', 'mid',
 ARRAY['Product Manager', 'Technical Product Manager'],
 '{"must_mention": ["criteria", "stakeholders", "data", "framework"], "bonus_points": ["RICE", "trade-offs", "communication"]}',
 ARRAY['product-management', 'prioritization', 'strategy']),

('Tell me about a time you launched a feature that failed. What did you learn?', 'behavioral', 'learning', 'mid',
 ARRAY['Product Manager', 'Technical Product Manager', 'Engineering Manager'],
 '{"must_mention": ["feature", "failure", "analysis", "learnings"], "bonus_points": ["metrics", "recovery", "prevention"]}',
 ARRAY['product-management', 'failure', 'learning']);

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_interview_question_bank_updated_at BEFORE UPDATE
    ON interview_question_bank FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Verify insertion
SELECT 
    difficulty_level,
    question_type,
    COUNT(*) as count
FROM interview_question_bank
GROUP BY difficulty_level, question_type
ORDER BY difficulty_level, question_type;
