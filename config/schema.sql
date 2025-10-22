-- UtopiaHire Database Schema
-- This creates all tables needed for Resume Reviewer feature

-- Users table: Store user information
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    region VARCHAR(100),  -- e.g., "Tunisia", "Nigeria", "Egypt"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resumes table: Store uploaded resumes
CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_type VARCHAR(10) NOT NULL,  -- 'pdf' or 'docx'
    raw_text TEXT,  -- Extracted text from resume
    parsed_data JSONB,  -- Structured data (education, skills, experience)
    file_size INTEGER,  -- Size in bytes
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis results table: Store AI analysis of resumes
CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    ats_score INTEGER CHECK (ats_score >= 0 AND ats_score <= 100),
    formatting_score INTEGER CHECK (formatting_score >= 0 AND formatting_score <= 100),
    keyword_score INTEGER CHECK (keyword_score >= 0 AND keyword_score <= 100),
    overall_score INTEGER CHECK (overall_score >= 0 AND overall_score <= 100),
    suggestions JSONB,  -- Array of improvement suggestions
    strengths JSONB,    -- What's good in the resume
    weaknesses JSONB,   -- What needs improvement
    missing_sections JSONB,  -- Sections that should be added
    model_used VARCHAR(100),  -- AI model name (e.g., 'llama3.2')
    analysis_time_seconds FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Improved resumes table: Store AI-enhanced versions
CREATE TABLE IF NOT EXISTS improved_resumes (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER REFERENCES resumes(id) ON DELETE CASCADE,
    analysis_id INTEGER REFERENCES analyses(id) ON DELETE CASCADE,
    enhanced_text TEXT NOT NULL,
    enhanced_data JSONB,  -- Structured improved data
    changes_made JSONB,   -- List of specific changes
    improvement_percentage FLOAT,
    version INTEGER DEFAULT 1,  -- Allow multiple versions
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills database: Common skills to match against
CREATE TABLE IF NOT EXISTS skills_database (
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(255) UNIQUE NOT NULL,
    category VARCHAR(100),  -- e.g., 'Technical', 'Soft Skills', 'Language'
    popularity INTEGER DEFAULT 0,  -- How often it appears in job postings
    region VARCHAR(100),  -- Region-specific skills
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Job keywords: Common keywords from job descriptions
CREATE TABLE IF NOT EXISTS job_keywords (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    job_role VARCHAR(100),  -- e.g., 'Software Engineer', 'Data Scientist'
    frequency INTEGER DEFAULT 0,
    region VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_resume_id ON analyses(resume_id);
CREATE INDEX IF NOT EXISTS idx_improved_resumes_resume_id ON improved_resumes(resume_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_skills_category ON skills_database(category);
CREATE INDEX IF NOT EXISTS idx_job_keywords_role ON job_keywords(job_role);

-- Insert some sample skills for MENA/Sub-Saharan Africa region
INSERT INTO skills_database (skill_name, category, popularity, region) VALUES
    ('Python', 'Technical', 95, 'Global'),
    ('JavaScript', 'Technical', 90, 'Global'),
    ('SQL', 'Technical', 85, 'Global'),
    ('Data Analysis', 'Technical', 80, 'Global'),
    ('Communication', 'Soft Skills', 95, 'Global'),
    ('Teamwork', 'Soft Skills', 90, 'Global'),
    ('Problem Solving', 'Soft Skills', 92, 'Global'),
    ('Arabic', 'Language', 85, 'MENA'),
    ('French', 'Language', 80, 'Sub-Saharan Africa'),
    ('English', 'Language', 95, 'Global')
ON CONFLICT (skill_name) DO NOTHING;

-- Insert sample job keywords
INSERT INTO job_keywords (keyword, job_role, frequency, region) VALUES
    ('experience', 'Software Engineer', 95, 'Global'),
    ('develop', 'Software Engineer', 90, 'Global'),
    ('design', 'Software Engineer', 85, 'Global'),
    ('team', 'Software Engineer', 88, 'Global'),
    ('agile', 'Software Engineer', 75, 'Global'),
    ('bachelor', 'All', 80, 'Global'),
    ('master', 'All', 70, 'Global')
ON CONFLICT DO NOTHING;

-- Create a function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for users table
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE users IS 'Stores user account information';
COMMENT ON TABLE resumes IS 'Stores uploaded resume files and extracted data';
COMMENT ON TABLE analyses IS 'Stores AI analysis results for each resume';
COMMENT ON TABLE improved_resumes IS 'Stores AI-enhanced versions of resumes';
COMMENT ON TABLE skills_database IS 'Database of common skills for matching';
COMMENT ON TABLE job_keywords IS 'Common keywords from job descriptions';
