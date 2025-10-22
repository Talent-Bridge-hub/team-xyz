// API Response Types

export interface User {
  id: number;
  email: string;
  full_name: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name: string;
}

// Resume Types
export interface Resume {
  id: number;
  user_id: number;
  file_path: string;
  original_filename: string;
  extracted_text: string;
  skills: string[];
  experience_years?: number;
  education?: string[];
  uploaded_at: string;
}

export interface ResumeAnalysis {
  resume_id: number;
  strengths: string[];
  weaknesses: string[];
  improvement_suggestions: string[];
  overall_score: number;
  skill_match_score: number;
  experience_score: number;
  education_score: number;
  analyzed_at: string;
}

// Job Types
export interface Job {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  requirements: string[];
  salary_range?: string;
  job_type: string;
  experience_level: string;
  skills: string[];
  posted_date: string;
  source: string;
  url?: string;
}

export interface JobMatch {
  job_id: number;
  resume_id: number;
  match_score: number;
  skill_match: number;
  experience_match: number;
  matched_skills: string[];
  missing_skills: string[];
  recommendations: string[];
  matched_at: string;
}

// Interview Types
export interface InterviewSession {
  id: number;
  user_id: number;
  job_title?: string;
  difficulty_level: string;
  status: string;
  total_questions: number;
  completed_questions: number;
  overall_score?: number;
  started_at: string;
  completed_at?: string;
}

export interface InterviewQuestion {
  id: number;
  session_id: number;
  question_text: string;
  question_type: string;
  difficulty: string;
  expected_topics: string[];
  asked_at: string;
}

export interface InterviewAnswer {
  id: number;
  session_id: number;
  question_id: number;
  answer_text: string;
  scores: {
    relevance_score: number;
    technical_accuracy: number;
    communication_score: number;
    completeness_score: number;
    confidence_score: number;
    overall_score: number;
  };
  feedback: string;
  answered_at: string;
}

// Footprint Types
export interface GitHubProfile {
  username: string;
  name?: string;
  bio?: string;
  location?: string;
  company?: string;
  blog_url?: string;
  email?: string;
  public_repos: number;
  followers: number;
  following: number;
  account_created_at: string;
}

export interface GitHubRepository {
  name: string;
  description?: string;
  language?: string;
  stars: number;
  forks: number;
  url: string;
  updated_at: string;
  has_readme: boolean;
  has_license: boolean;
}

export interface GitHubAnalysis {
  profile: GitHubProfile;
  top_repositories: GitHubRepository[];
  total_stars: number;
  total_forks: number;
  languages: Record<string, number>;
  activity: {
    total_events: number;
    commits: number;
    pull_requests: number;
    issues: number;
    reviews: number;
    activity_streak: number;
    active_days: number;
  };
  scores: {
    code_quality_score: number;
    activity_score: number;
    impact_score: number;
    overall_github_score: number;
  };
  visibility_level: string;
  analyzed_at: string;
}

export interface StackOverflowProfile {
  user_id: number;
  display_name: string;
  reputation: number;
  location?: string;
  website_url?: string;
  profile_link: string;
  badges: {
    gold: number;
    silver: number;
    bronze: number;
    total: number;
  };
  creation_date: string;
  last_access_date: string;
}

export interface StackOverflowAnalysis {
  profile: StackOverflowProfile;
  top_tags: Array<{
    name: string;
    count: number;
    score: number;
  }>;
  activity: {
    total_answers: number;
    accepted_answers: number;
    total_questions: number;
    answer_score: number;
    question_score: number;
    total_views: number;
  };
  scores: {
    expertise_score: number;
    helpfulness_score: number;
    community_score: number;
    overall_stackoverflow_score: number;
  };
  visibility_level: string;
  analyzed_at: string;
}

export interface FootprintScan {
  scan_id: number;
  user_id: number;
  github_analysis?: GitHubAnalysis;
  stackoverflow_analysis?: StackOverflowAnalysis;
  privacy_report?: {
    overall_risk_level: string;
    issues_found: any[];
    exposed_information: string[];
    visibility_score: number;
    recommendations: string[];
  };
  overall_visibility_score: number;
  professional_score: number;
  scanned_at: string;
  message?: string;
}

export interface FootprintRecommendations {
  scan_id: number;
  profile_recommendations: any[];
  career_insights: Array<{
    insight_type: string;
    title: string;
    description: string;
    evidence: string[];
  }>;
  skill_gaps: any[];
  competitive_analysis: {
    github_percentile: string;
    stackoverflow_percentile: string;
    overall_ranking: string;
  };
  generated_at: string;
}
