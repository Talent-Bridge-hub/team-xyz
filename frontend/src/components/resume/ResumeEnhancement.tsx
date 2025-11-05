/**
 * Resume Enhancement Component
 * Apply AI suggestions and download enhanced resume
 */

import { useState } from 'react';
import { resumeService, EnhancementSuggestion } from '../../services/resume.service';
import { useToast } from '../../contexts/ToastContext';

interface ResumeEnhancementProps {
  resumeId: number;
  resumeName: string;
}

export function ResumeEnhancement({ resumeId, resumeName }: ResumeEnhancementProps) {
  const [isEnhancing, setIsEnhancing] = useState(false);
  const [error, setError] = useState<string>('');
  const { showSuccess } = useToast();

  const handleDownloadEnhanced = async () => {
    setIsEnhancing(true);
    setError('');
    
    try {
      // Download enhanced resume with all improvements applied automatically
      const blob = await resumeService.downloadEnhancedResume(
        resumeId,
        'full' // enhancement type - applies all improvements
      );
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `enhanced_${resumeName}`;
      document.body.appendChild(a);
      a.click();
      
      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      // Show success message
      showSuccess('Enhanced resume downloaded successfully with all improvements applied!');
      
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to download enhanced resume');
    } finally {
      setIsEnhancing(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
        <svg className="h-5 w-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap={"round" as const}
            strokeLinejoin={"round" as const}
            strokeWidth={2}
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
        Enhance Resume
      </h2>

      <p className="text-sm text-gray-600 mb-4">
        Generate and download an enhanced version of your resume with AI-powered improvements. This includes stronger action verbs, quantified achievements, grammar corrections, and ATS optimization to help you stand out to employers.
      </p>

      <button
        onClick={handleDownloadEnhanced}
        disabled={isEnhancing}
        className="w-full py-2 px-4 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
      >
        {isEnhancing ? (
          <>
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Preparing Enhancement...
          </>
        ) : (
          'Download Enhancement'
        )}
      </button>

      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {/* Info Box */}
      <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
        <h4 className="text-sm font-medium text-blue-900 mb-2">📁 Your Files</h4>
        <p className="text-xs text-blue-800 mb-2">
          <strong>Original resume:</strong> <code className="bg-blue-100 px-1">{resumeName}</code>
        </p>
        <p className="text-xs text-blue-700">
          💡 <strong>Tip:</strong> Your uploaded files are stored at{' '}
          <code className="bg-blue-100 px-1">/home/firas/Utopia/data/resumes/</code>
        </p>
      </div>
    </div>
  );
}
