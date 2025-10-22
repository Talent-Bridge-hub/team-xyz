/**
 * Resume Page
 * Main page for resume management - upload, list, and analyze resumes
 */

import { useState } from 'react';
import { ResumeUploadForm } from '../../components/resume/ResumeUploadForm';
import { ResumeList } from '../../components/resume/ResumeList';
import { ResumeAnalysisView } from '../../components/resume/ResumeAnalysisView';

type View = 'list' | 'analysis';

export function ResumePage() {
  const [currentView, setCurrentView] = useState<View>('list');
  const [selectedResumeId, setSelectedResumeId] = useState<number | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadSuccess = (resumeId: number) => {
    // Refresh the resume list
    setRefreshTrigger((prev) => prev + 1);
    
    // Show success message
    alert('Resume uploaded successfully! Analysis in progress...');
    
    // Optionally, navigate to analysis view
    // setSelectedResumeId(resumeId);
    // setCurrentView('analysis');
  };

  const handleResumeSelect = (resumeId: number) => {
    setSelectedResumeId(resumeId);
    setCurrentView('analysis');
  };

  const handleBackToList = () => {
    setSelectedResumeId(null);
    setCurrentView('list');
    // Refresh list in case analysis completed
    setRefreshTrigger((prev) => prev + 1);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {currentView === 'list' ? (
        <div className="space-y-8">
          {/* Page Header */}
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Resume Analyzer</h1>
            <p className="mt-2 text-gray-600">
              Upload your resume for AI-powered analysis and get instant feedback on how to improve it
            </p>
          </div>

          {/* Upload Form */}
          <ResumeUploadForm 
            onUploadSuccess={handleUploadSuccess}
            onUploadError={(error: string) => alert(`Upload failed: ${error}`)}
          />

          {/* Resume List */}
          <ResumeList 
            onResumeSelect={handleResumeSelect}
            refreshTrigger={refreshTrigger}
          />
        </div>
      ) : (
        /* Analysis View */
        selectedResumeId && (
          <ResumeAnalysisView
            resumeId={selectedResumeId}
            onBack={handleBackToList}
          />
        )
      )}
    </div>
  );
}
