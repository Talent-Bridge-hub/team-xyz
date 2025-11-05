/**
 * Jobs Service
 * API client for job scraping, matching, and search operations
 */

import { apiClient } from './api-client';

// Types
export interface SalaryRange {
  min?: number;
  max?: number;
  currency: string;
  text?: string;
}

export interface JobPost {
  id: string;
  title: string;
  company: string;
  location: string;
  region?: string;
  type: string;
  experience_level?: string;
  description: string;
  required_skills: string[];
  preferred_skills: string[];
  salary_range?: SalaryRange;
  posted_date?: string;
  remote: boolean;
  url: string;
  source?: string;
  fetched_at?: string;
}

export interface MatchScore {
  overall_score: number;
  skill_score: number;
  location_score: number;
  experience_score: number;
  breakdown: {
    skills_matched: string[];
    skills_missing: string[];
    location_match: boolean;
    experience_match: string;
  };
}

export interface JobMatch {
  job: JobPost;
  match_score: MatchScore;
}

export interface JobScrapingRequest {
  queries: string[];
  locations: string[];
  num_results_per_query: number;
}

export interface JobScrapingResponse {
  jobs_scraped: number;
  jobs_stored: number;
  queries_processed: number;
  locations_processed: number;
  api_used?: string;
  scraping_duration_ms: number;
  message: string;
}

export interface JobMatchingRequest {
  resume_id: number;
  location_preference?: string[];
  job_types?: string[];
  experience_level?: string[];
  min_score?: number;
  limit?: number;
}

export interface JobMatchingResponse {
  matches: JobMatch[];
  total_jobs_searched: number;
  matches_found: number;
  avg_match_score: number;
  processing_time_ms: number;
  message: string;
}

export interface JobSearchRequest {
  query?: string;
  location?: string;
  job_type?: string;
  experience_level?: string;
  min_score?: number;
  page?: number;
  page_size?: number;
}

export interface JobListResponse {
  jobs: JobPost[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface MarketInsights {
  total_jobs: number;
  by_region: Record<string, number>;
  by_job_type: Record<string, number>;
  by_experience_level: Record<string, number>;
  top_skills: Array<{ skill: string; count: number }>;
  avg_salary: SalaryRange;
  remote_percentage: number;
  top_companies: Array<{ company: string; count: number }>;
}

// Job Compatibility Analysis
export interface JobCompatibilityRequest {
  resume_id: number;
  job_description: string;
  job_title?: string;
  company?: string;
  required_skills?: string[];
}

export interface JobCompatibilityResponse {
  resume_id: number;
  job_title?: string;
  company?: string;
  overall_match_score: number;
  skill_match_score: number;
  experience_match_score: number;
  education_match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  strengths: string[];
  gaps: string[];
  recommendations: string[];
  ai_summary?: string;
  ai_detailed_analysis?: string;
  analyzed_at: string;
}

class JobsService {
  /**
   * Scrape jobs from external APIs
   */
  async scrapeJobs(request: JobScrapingRequest): Promise<JobScrapingResponse> {
    return await apiClient.post<JobScrapingResponse>('/jobs/scrape', request);
  }

  /**
   * Match jobs with a resume
   */
  async matchJobs(request: JobMatchingRequest): Promise<JobMatchingResponse> {
    return await apiClient.post<JobMatchingResponse>('/jobs/match', request);
  }

  /**
   * List all jobs with optional filters
   */
  async listJobs(
    page: number = 1,
    pageSize: number = 20,
    location?: string,
    jobType?: string,
    remoteOnly: boolean = false,
    experienceLevel?: string
  ): Promise<JobListResponse> {
    const params: Record<string, any> = {
      page,
      page_size: pageSize,
    };
    
    if (location) params.location = location;
    if (jobType) params.job_type = jobType;
    if (remoteOnly) params.remote_only = true;
    if (experienceLevel) params.experience_level = experienceLevel;

    return await apiClient.get<JobListResponse>('/jobs/list', { params });
  }

  /**
   * Search jobs with advanced filters
   */
  async searchJobs(request: JobSearchRequest): Promise<JobListResponse> {
    return await apiClient.post<JobListResponse>('/jobs/search', request);
  }

  /**
   * Get job details by ID
   */
  async getJobDetails(jobId: string): Promise<JobPost> {
    return await apiClient.get<JobPost>(`/jobs/${jobId}`);
  }

  /**
   * Get market insights and statistics
   */
  async getMarketInsights(): Promise<MarketInsights> {
    return await apiClient.get<MarketInsights>('/jobs/market-insights');
  }

  /**
   * Analyze compatibility between a resume and job description
   */
  async analyzeJobCompatibility(request: JobCompatibilityRequest): Promise<JobCompatibilityResponse> {
    return await apiClient.post<JobCompatibilityResponse>('/jobs/compatibility', request);
  }
}

export const jobsService = new JobsService();
