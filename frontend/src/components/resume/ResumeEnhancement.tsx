/**
 * Resume Enhancement Component
 * Apply AI suggestions and download enhanced resume
 */

import { useState } from 'react';
import { resumeService, EnhancementSuggestion } from '../../services/resume.service';

interface ResumeEnhancementProps {
  resumeId: number;
  resumeName: string;
}

export function ResumeEnhancement({ resumeId, resumeName }: ResumeEnhancementProps) {
  const [isEnhancing, setIsEnhancing] = useState(false);
  const [suggestions, setSuggestions] = useState<EnhancementSuggestion[]>([]);
  const [selectedSuggestions, setSelectedSuggestions] = useState<string[]>([]);
  const [error, setError] = useState<string>('');

  const handleGetSuggestions = async () => {
    setIsEnhancing(true);
    setError('');
    
    try {
      const result = await resumeService.enhanceResume(resumeId, 'full');
      console.log('Enhancement result:', result);
      setSuggestions(result.suggestions || []);
    } catch (err: any) {
      console.error('Enhancement error:', err);
      setError(err.response?.data?.detail || 'Failed to get enhancement suggestions');
    } finally {
      setIsEnhancing(false);
    }
  };

  const handleToggleSuggestion = (section: string) => {
    setSelectedSuggestions(prev =>
      prev.includes(section)
        ? prev.filter(s => s !== section)
        : [...prev, section]
    );
  };

  const handleDownloadEnhanced = async () => {
    setIsEnhancing(true);
    setError('');
    
    try {
      // Download enhanced resume with selected improvements
      const blob = await resumeService.downloadEnhancedResume(
        resumeId,
        'full', // enhancement type
        selectedSuggestions
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
      alert(`Enhanced resume downloaded successfully!\n${selectedSuggestions.length} improvements applied.`);
      
      // Reset state
      setSuggestions([]);
      setSelectedSuggestions([]);
      
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
        Get AI-powered suggestions to improve your resume
      </p>

      {!suggestions.length ? (
        <button
          onClick={handleGetSuggestions}
          disabled={isEnhancing}
          className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isEnhancing ? 'Analyzing...' : 'Get Enhancement Suggestions'}
        </button>
      ) : (
        <div className="space-y-4">
          <div className="border border-gray-200 rounded-md p-4 max-h-96 overflow-y-auto">
            <h3 className="text-sm font-medium text-gray-900 mb-3">
              Select improvements to apply ({suggestions.length} suggestions found):
            </h3>
            <div className="space-y-3">
              {suggestions.map((suggestion, idx) => (
                <label 
                  key={idx} 
                  className="flex items-start space-x-3 cursor-pointer hover:bg-gray-50 p-3 rounded border border-gray-100"
                >
                  <input
                    type="checkbox"
                    checked={selectedSuggestions.includes(suggestion.section)}
                    onChange={() => handleToggleSuggestion(suggestion.section)}
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="font-medium text-sm text-gray-900">{suggestion.section}</span>
                      <span className={`text-xs px-2 py-0.5 rounded ${
                        suggestion.impact === 'high' ? 'bg-red-100 text-red-800' :
                        suggestion.impact === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {suggestion.impact} impact
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 mb-2">{suggestion.explanation}</p>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div>
                        <span className="font-medium text-gray-700">Before:</span>
                        <p className="text-gray-600 italic mt-1">{suggestion.original_text.substring(0, 100)}...</p>
                      </div>
                      <div>
                        <span className="font-medium text-gray-700">After:</span>
                        <p className="text-gray-600 mt-1">{suggestion.enhanced_text.substring(0, 100)}...</p>
                      </div>
                    </div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          <div className="flex space-x-3">
            <button
              onClick={handleDownloadEnhanced}
              disabled={selectedSuggestions.length === 0}
              className="flex-1 py-2 px-4 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Apply & Download ({selectedSuggestions.length} improvements)
            </button>
            <button
              onClick={() => {
                setSuggestions([]);
                setSelectedSuggestions([]);
              }}
              className="py-2 px-4 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

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
