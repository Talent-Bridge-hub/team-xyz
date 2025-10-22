/**
 * Resume List Component
 * Grid display of uploaded resumes with actions
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { resumeService } from '../../services/resume.service';
import { ResumeTemplatesModal } from './ResumeTemplatesModal';
import type { Resume } from '../../types/api';

interface ResumeListProps {
  onResumeSelect: (resumeId: number) => void;
  refreshTrigger?: number;
}

export function ResumeList({ onResumeSelect, refreshTrigger }: ResumeListProps) {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [showTemplatesModal, setShowTemplatesModal] = useState(false);

  useEffect(() => {
    loadResumes();
  }, [refreshTrigger]);

  const loadResumes = async () => {
    setIsLoading(true);
    setError('');
    try {
      const data = await resumeService.getResumes();
      setResumes(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load resumes');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this resume?')) return;

    try {
      await resumeService.deleteResume(id);
      setResumes(resumes.filter((r) => r.id !== id));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to delete resume');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getATSScoreColor = (score?: number) => {
    if (!score) return 'text-gray-500';
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="flex justify-center items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Loading resumes...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center text-red-600">
          <p>{error}</p>
          <button
            onClick={loadResumes}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (resumes.length === 0) {
    return (
      <>
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="text-center">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap={"round" as const}
                strokeLinejoin={"round" as const}
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 className="mt-4 text-lg font-medium text-gray-900">No resumes yet</h3>
            <p className="mt-2 text-sm text-gray-500 mb-4">
              Upload your first resume to get started with AI-powered analysis
            </p>
            
            {/* Template Button */}
            <button
              onClick={() => setShowTemplatesModal(true)}
              className="mt-2 inline-flex items-center px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-md hover:from-purple-700 hover:to-blue-700 transition shadow-md"
            >
              <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Use a Template
            </button>
            <p className="mt-2 text-xs text-gray-500">
              Start with a professional, ATS-friendly template
            </p>
          </div>
        </div>
        
        {/* Templates Modal */}
        <ResumeTemplatesModal 
          isOpen={showTemplatesModal}
          onClose={() => setShowTemplatesModal(false)}
        />
      </>
    );
  }

  return (
    <>
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">Your Resumes</h2>
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setShowTemplatesModal(true)}
              className="inline-flex items-center px-3 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white text-sm rounded-md hover:from-purple-700 hover:to-blue-700 transition shadow-md"
            >
              <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Use Template
            </button>
            <span className="text-sm text-gray-500">{resumes.length} resume(s)</span>
          </div>
        </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {resumes.map((resume) => (
          <div
            key={resume.id}
            onClick={() => onResumeSelect(resume.id)}
            className="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow border border-gray-200 hover:border-blue-500"
          >
            {/* Resume Icon */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="bg-blue-100 rounded-lg p-3">
                  <svg
                    className="h-6 w-6 text-blue-600"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap={"round" as const}
                      strokeLinejoin={"round" as const}
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 truncate max-w-[150px]">
                    {resume.original_filename}
                  </h3>
                  <p className="text-xs text-gray-500">{formatDate(resume.uploaded_at)}</p>
                </div>
              </div>

              {/* Delete Button */}
              <button
                onClick={(e: React.MouseEvent) => handleDelete(resume.id, e)}
                className="text-gray-400 hover:text-red-600 transition-colors"
                title="Delete resume"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap={"round" as const}
                    strokeLinejoin={"round" as const}
                    strokeWidth={2}
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
              </button>
            </div>

            {/* Skills */}
            {resume.skills && resume.skills.length > 0 ? (
              <div className="mb-3">
                <span className="text-xs font-medium text-gray-600 block mb-1">Skills</span>
                <div className="flex flex-wrap gap-1">
                  {resume.skills.slice(0, 3).map((skill, idx) => (
                    <span
                      key={idx}
                      className="inline-block px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded"
                    >
                      {skill}
                    </span>
                  ))}
                  {resume.skills.length > 3 && (
                    <span className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">
                      +{resume.skills.length - 3} more
                    </span>
                  )}
                </div>
              </div>
            ) : (
              <div className="mb-3">
                <span className="text-xs text-gray-500 italic">Processing...</span>
              </div>
            )}

            {/* Experience */}
            {resume.experience_years !== undefined && resume.experience_years !== null && (
              <div className="mb-3 text-xs text-gray-600">
                <span className="font-medium">{resume.experience_years}</span> years of experience
              </div>
            )}

            {/* View Analysis Button */}
            <button
              onClick={() => onResumeSelect(resume.id)}
              className="mt-4 w-full py-2 px-4 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
            >
              View Analysis
            </button>
          </div>
        ))}
      </div>
      </div>
      
      {/* Templates Modal */}
      <ResumeTemplatesModal 
        isOpen={showTemplatesModal}
        onClose={() => setShowTemplatesModal(false)}
      />
    </>
  );
}
