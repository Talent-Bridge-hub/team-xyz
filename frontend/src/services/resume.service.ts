/**
 * Resume Service
 * API client for resume upload, analysis, and enhancement
 */

import { apiClient } from './api-client';
import type { Resume, ResumeAnalysis } from '../types/api';

export interface UploadResumeResponse {
  id: number;
  filename: string;
  upload_date: string;
  file_size: number;
  file_type: string;
  message: string;
}

export interface EnhanceResumeRequest {
  resume_id: number;
  enhancement_type?: string;
  target_job?: string;
}

export interface EnhancementSuggestion {
  section: string;
  original_text: string;
  enhanced_text: string;
  improvement_type: string;
  impact: string;
  explanation: string;
}

export interface EnhanceResumeResponse {
  resume_id: number;
  enhancement_type: string;
  suggestions: EnhancementSuggestion[];
  total_suggestions: number;
  high_impact_count: number;
  medium_impact_count: number;
  low_impact_count: number;
  estimated_score_improvement: number;
  enhanced_at: string;
}

class ResumeService {
  /**
   * Upload a resume file (PDF or DOCX)
   */
  async uploadResume(file: File): Promise<UploadResumeResponse> {
    const formData = new FormData();
    formData.append('file', file);

    return await apiClient.post<UploadResumeResponse>(
      '/resumes/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
  }

  /**
   * Get list of user's resumes
   */
  async getResumes(): Promise<Resume[]> {
    interface ResumeListResponse {
      resumes: any[];
      total: number;
      page: number;
      page_size: number;
    }
    
    const response = await apiClient.get<ResumeListResponse>('/resumes/list?page=1&page_size=50');
    
    // Map backend response to frontend Resume type
    return response.resumes.map((item: any) => ({
      id: item.resume_id,
      user_id: 0, // Not provided in list
      file_path: '',
      original_filename: item.filename,
      extracted_text: '',
      skills: [],
      experience_years: undefined,
      education: undefined,
      uploaded_at: item.uploaded_at,
    }));
  }

  /**
   * Get a specific resume by ID (from list)
   */
  async getResume(id: number): Promise<Resume> {
    const resumes = await this.getResumes();
    const resume = resumes.find(r => r.id === id);
    if (!resume) {
      throw new Error('Resume not found');
    }
    return resume;
  }

  /**
   * Analyze resume (ATS score, formatting, keywords)
   */
  async getResumeAnalysis(id: number): Promise<ResumeAnalysis> {
    return await apiClient.post<ResumeAnalysis>('/resumes/analyze', {
      resume_id: id
    });
  }

  /**
   * Enhance resume with AI suggestions
   */
  async enhanceResume(
    id: number,
    enhancementType: string = 'full',
    targetJob?: string
  ): Promise<EnhanceResumeResponse> {
    return await apiClient.post<EnhanceResumeResponse>(
      '/resumes/enhance',
      { 
        resume_id: id,
        enhancement_type: enhancementType,
        target_job: targetJob
      }
    );
  }

  /**
   * Delete a resume
   */
  async deleteResume(id: number): Promise<void> {
    await apiClient.delete(`/resumes/${id}`);
  }

  /**
   * Download original resume file
   */
  async downloadOriginalResume(id: number): Promise<Blob> {
    return await apiClient.get<Blob>(`/resumes/${id}/download`, {
      responseType: 'blob',
    });
  }

  /**
   * Download enhanced resume with improvements applied
   */
  async downloadEnhancedResume(
    id: number, 
    enhancementType: string = 'full',
    selectedImprovements?: string[]
  ): Promise<Blob> {
    return await apiClient.post<Blob>(
      `/resumes/${id}/download-enhanced`,
      {
        enhancement_type: enhancementType,
        selected_improvements: selectedImprovements,
      },
      {
        responseType: 'blob',
      }
    );
  }

  /**
   * List available resume templates
   */
  async listTemplates(): Promise<{ templates: any[]; total: number; message: string }> {
    return await apiClient.get<{ templates: any[]; total: number; message: string }>('/resumes/templates');
  }

  /**
   * Download a resume template
   */
  async downloadTemplate(templateId: string): Promise<Blob> {
    return await apiClient.get<Blob>(
      `/resumes/templates/${templateId}/download`,
      {
        responseType: 'blob',
      }
    );
  }
}

export const resumeService = new ResumeService();
