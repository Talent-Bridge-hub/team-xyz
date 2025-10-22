-- UtopiaHire Module 4: Professional Footprint Scanner
-- Database Schema for tracking professional presence across platforms

-- User profiles: Central storage for all platform URLs
CREATE TABLE IF NOT EXISTS user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    -- Platform URLs
    linkedin_url TEXT,
    github_username VARCHAR(255),
    stackoverflow_user_id VARCHAR(50),
    
    -- Profile metadata
    full_name VARCHAR(255),
    headline TEXT,
    location VARCHAR(255),
    
    -- Status tracking
    scan_status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'scanning', 'completed', 'failed'
    last_scanned_at TIMESTAMP,
    scan_frequency VARCHAR(20) DEFAULT 'monthly',  -- 'daily', 'weekly', 'monthly'
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LinkedIn data: Store scraped LinkedIn profile information
CREATE TABLE IF NOT EXISTS linkedin_data (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER REFERENCES user_profiles(id) ON DELETE CASCADE,
    
    -- Profile basics
    headline TEXT,
    summary TEXT,
    num_connections INTEGER,
    location VARCHAR(255),
    
    -- Experience data (JSONB for flexibility)
    experience JSONB,  -- [{company, title, duration, description, skills}]
    education JSONB,   -- [{school, degree, field, years, activities}]
    skills JSONB,      -- [{skill_name, endorsement_count}]
    certifications JSONB,  -- [{name, issuer, date}]
    
    -- Activity metrics
    num_recommendations INTEGER DEFAULT 0,
    num_posts INTEGER DEFAULT 0,
    num_articles INTEGER DEFAULT 0,
    profile_views INTEGER DEFAULT 0,
    
    -- Calculated scores
    profile_completeness INTEGER CHECK (profile_completeness >= 0 AND profile_completeness <= 100),
    activity_score INTEGER CHECK (activity_score >= 0 AND activity_score <= 100),
    network_score INTEGER CHECK (network_score >= 0 AND network_score <= 100),
    
    -- Metadata
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_quality VARCHAR(20) DEFAULT 'good'  -- 'excellent', 'good', 'partial', 'poor'
);

-- GitHub data: Store GitHub profile and repository analysis
CREATE TABLE IF NOT EXISTS github_data (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER REFERENCES user_profiles(id) ON DELETE CASCADE,
    
    -- Profile basics
    username VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    bio TEXT,
    location VARCHAR(255),
    company VARCHAR(255),
    blog_url TEXT,
    email VARCHAR(255),
    
    -- Account metrics
    public_repos INTEGER DEFAULT 0,
    total_stars INTEGER DEFAULT 0,
    total_forks INTEGER DEFAULT 0,
    followers INTEGER DEFAULT 0,
    following INTEGER DEFAULT 0,
    
    -- Activity metrics
    total_commits_last_year INTEGER DEFAULT 0,
    total_pull_requests INTEGER DEFAULT 0,
    total_issues INTEGER DEFAULT 0,
    contribution_streak_days INTEGER DEFAULT 0,
    
    -- Repository data (JSONB for top repos)
    top_repositories JSONB,  -- [{name, stars, forks, language, description, updated_at}]
    languages_used JSONB,    -- {Python: 5000, JavaScript: 3000, ...} (bytes of code)
    
    -- Calculated scores
    code_quality_score INTEGER CHECK (code_quality_score >= 0 AND code_quality_score <= 100),
    activity_score INTEGER CHECK (activity_score >= 0 AND activity_score <= 100),
    impact_score INTEGER CHECK (impact_score >= 0 AND impact_score <= 100),
    
    -- Metadata
    account_created_at TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- StackOverflow data: Store Stack Exchange API results
CREATE TABLE IF NOT EXISTS stackoverflow_data (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER REFERENCES user_profiles(id) ON DELETE CASCADE,
    
    -- Profile basics
    user_id INTEGER NOT NULL,
    display_name VARCHAR(255),
    reputation INTEGER DEFAULT 0,
    location VARCHAR(255),
    about_me TEXT,
    website_url TEXT,
    
    -- Badge counts
    gold_badges INTEGER DEFAULT 0,
    silver_badges INTEGER DEFAULT 0,
    bronze_badges INTEGER DEFAULT 0,
    
    -- Activity metrics
    question_count INTEGER DEFAULT 0,
    answer_count INTEGER DEFAULT 0,
    accepted_answers INTEGER DEFAULT 0,
    total_views INTEGER DEFAULT 0,
    up_votes INTEGER DEFAULT 0,
    down_votes INTEGER DEFAULT 0,
    
    -- Top tags (expertise areas)
    top_tags JSONB,  -- [{tag_name, score, question_count, answer_count}]
    
    -- Activity timeline
    last_access_date TIMESTAMP,
    member_since TIMESTAMP,
    
    -- Calculated scores
    expertise_score INTEGER CHECK (expertise_score >= 0 AND expertise_score <= 100),
    helpfulness_score INTEGER CHECK (helpfulness_score >= 0 AND helpfulness_score <= 100),
    community_score INTEGER CHECK (community_score >= 0 AND community_score <= 100),
    
    -- Metadata
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Footprint scores: Overall professional footprint calculations
CREATE TABLE IF NOT EXISTS footprint_scores (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER REFERENCES user_profiles(id) ON DELETE CASCADE,
    
    -- Individual platform scores (0-100)
    linkedin_score INTEGER CHECK (linkedin_score >= 0 AND linkedin_score <= 100),
    github_score INTEGER CHECK (github_score >= 0 AND github_score <= 100),
    stackoverflow_score INTEGER CHECK (stackoverflow_score >= 0 AND stackoverflow_score <= 100),
    
    -- Overall footprint score (weighted average)
    overall_score INTEGER CHECK (overall_score >= 0 AND overall_score <= 100),
    
    -- Score breakdown
    visibility_score INTEGER CHECK (visibility_score >= 0 AND visibility_score <= 100),  -- How visible are you?
    activity_score INTEGER CHECK (activity_score >= 0 AND activity_score <= 100),       -- How active are you?
    impact_score INTEGER CHECK (impact_score >= 0 AND impact_score <= 100),             -- What's your impact?
    expertise_score INTEGER CHECK (expertise_score >= 0 AND expertise_score <= 100),    -- What's your expertise level?
    
    -- Performance category
    performance_level VARCHAR(50),  -- 'excellent', 'good', 'average', 'needs_improvement'
    
    -- Detailed feedback
    strengths JSONB,       -- What you're doing well
    weaknesses JSONB,      -- Areas to improve
    recommendations JSONB, -- Actionable suggestions
    
    -- Benchmarking (compared to peers)
    percentile INTEGER CHECK (percentile >= 0 AND percentile <= 100),  -- Top X% of users
    peer_comparison VARCHAR(50),  -- 'above_average', 'average', 'below_average'
    
    -- Timestamps
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Footprint history: Track score changes over time
CREATE TABLE IF NOT EXISTS footprint_history (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER REFERENCES user_profiles(id) ON DELETE CASCADE,
    
    -- Historical scores
    overall_score INTEGER CHECK (overall_score >= 0 AND overall_score <= 100),
    linkedin_score INTEGER,
    github_score INTEGER,
    stackoverflow_score INTEGER,
    
    -- Changes from previous scan
    score_change INTEGER,  -- Can be negative
    improvement_percentage FLOAT,
    
    -- Notable events
    events JSONB,  -- [{type: 'new_repo', description: 'Created awesome-project', date: '2025-01-15'}]
    
    -- Timestamp
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Platform credentials: Store API tokens securely (encrypted)
CREATE TABLE IF NOT EXISTS platform_credentials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    platform VARCHAR(50) NOT NULL,  -- 'github', 'linkedin', 'stackoverflow'
    api_token TEXT,  -- Encrypted token
    refresh_token TEXT,  -- For OAuth
    token_expires_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    
    UNIQUE(user_id, platform)
);

-- Scan logs: Track all scanning operations
CREATE TABLE IF NOT EXISTS scan_logs (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER REFERENCES user_profiles(id) ON DELETE CASCADE,
    
    platform VARCHAR(50) NOT NULL,  -- 'linkedin', 'github', 'stackoverflow', 'all'
    status VARCHAR(50) NOT NULL,    -- 'started', 'completed', 'failed', 'partial'
    
    -- Scan details
    data_points_collected INTEGER DEFAULT 0,
    errors_encountered JSONB,  -- [{error_type, error_message, timestamp}]
    
    -- Performance
    duration_seconds FLOAT,
    api_calls_made INTEGER DEFAULT 0,
    
    -- Timestamps
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_linkedin_data_profile_id ON linkedin_data(profile_id);
CREATE INDEX IF NOT EXISTS idx_github_data_profile_id ON github_data(profile_id);
CREATE INDEX IF NOT EXISTS idx_stackoverflow_data_profile_id ON stackoverflow_data(profile_id);
CREATE INDEX IF NOT EXISTS idx_footprint_scores_profile_id ON footprint_scores(profile_id);
CREATE INDEX IF NOT EXISTS idx_footprint_history_profile_id ON footprint_history(profile_id);
CREATE INDEX IF NOT EXISTS idx_scan_logs_profile_id ON scan_logs(profile_id);
CREATE INDEX IF NOT EXISTS idx_scan_logs_status ON scan_logs(status);

-- GIN indexes for JSONB columns (faster searches)
CREATE INDEX IF NOT EXISTS idx_linkedin_skills ON linkedin_data USING GIN (skills);
CREATE INDEX IF NOT EXISTS idx_github_languages ON github_data USING GIN (languages_used);
CREATE INDEX IF NOT EXISTS idx_stackoverflow_tags ON stackoverflow_data USING GIN (top_tags);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comments for documentation
COMMENT ON TABLE user_profiles IS 'Central storage for user professional profiles across platforms';
COMMENT ON TABLE linkedin_data IS 'Scraped LinkedIn profile data and metrics';
COMMENT ON TABLE github_data IS 'GitHub profile analysis and repository metrics';
COMMENT ON TABLE stackoverflow_data IS 'Stack Overflow/Stack Exchange reputation and activity';
COMMENT ON TABLE footprint_scores IS 'Calculated professional footprint scores and recommendations';
COMMENT ON TABLE footprint_history IS 'Historical tracking of score changes over time';
COMMENT ON TABLE platform_credentials IS 'Secure storage for platform API credentials';
COMMENT ON TABLE scan_logs IS 'Audit log of all scanning operations';

-- Sample data for testing
-- Note: Insert sample user profile for testing
-- This assumes user_id=1 exists from previous modules
INSERT INTO user_profiles (user_id, full_name, location, scan_status) VALUES
(1, 'Test User', 'Tunisia', 'pending')
ON CONFLICT DO NOTHING;
