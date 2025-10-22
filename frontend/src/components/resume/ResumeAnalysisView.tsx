/**
 * Resume Analysis View Component
 * Displays detailed analysis with scores and recommendations
 */

import { useState, useEffect } from 'react';
import { resumeService } from '../../services/resume.service';
import type { Resume, ResumeAnalysis } from '../../types/api';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';
import { ResumeEnhancement } from './ResumeEnhancement';

interface ResumeAnalysisViewProps {
  resumeId: number;
  onBack: () => void;
}

export function ResumeAnalysisView({ resumeId, onBack }: ResumeAnalysisViewProps) {
  const [resume, setResume] = useState<Resume | null>(null);
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadResumeData();
  }, [resumeId]);

  const loadResumeData = async () => {
    setIsLoading(true);
    setError('');
    try {
      const [resumeData, analysisData] = await Promise.all([
        resumeService.getResume(resumeId),
        resumeService.getResumeAnalysis(resumeId),
      ]);
      setResume(resumeData);
      setAnalysis(analysisData);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load resume analysis');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="flex justify-center items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span className="ml-3 text-gray-600">Analyzing resume...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="text-center">
          <p className="text-red-600">{error}</p>
          <div className="mt-4 space-x-3">
            <button
              onClick={loadResumeData}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Try Again
            </button>
            <button
              onClick={onBack}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
            >
              Go Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!resume || !analysis) {
    return null;
  }

  // Prepare chart data
  const chartData = [
    { metric: 'Overall', score: analysis.overall_score },
    { metric: 'Skills', score: analysis.skill_match_score },
    { metric: 'Experience', score: analysis.experience_score },
    { metric: 'Education', score: analysis.education_score },
  ];

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  const handleDownloadOriginal = async () => {
    try {
      const blob = await resumeService.downloadOriginalResume(resumeId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = resume?.original_filename || 'resume.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err: any) {
      alert('Failed to download resume: ' + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-4">
          <button
            onClick={onBack}
            className="flex items-center text-blue-600 hover:text-blue-700"
          >
            <svg className="h-5 w-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap={"round" as const}
                strokeLinejoin={"round" as const}
                strokeWidth={2}
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            Back to Resumes
          </button>
          <button
            onClick={handleDownloadOriginal}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap={"round" as const}
                strokeLinejoin={"round" as const}
                strokeWidth={2}
                d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            Download Original
          </button>
        </div>

        <div className="flex items-center justify-between mt-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{resume.original_filename}</h1>
            <p className="text-sm text-gray-500 mt-1">
              Uploaded {new Date(resume.uploaded_at).toLocaleDateString()}
            </p>
          </div>
          <div className={`text-center px-6 py-4 rounded-lg ${getScoreBgColor(analysis.overall_score)}`}>
            <div className={`text-3xl font-bold ${getScoreColor(analysis.overall_score)}`}>
              {analysis.overall_score}%
            </div>
            <div className="text-sm text-gray-600 mt-1">Overall Score</div>
          </div>
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Scores Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Score Breakdown</h2>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={chartData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="metric" />
              <PolarRadiusAxis domain={[0, 100]} />
              <Radar name="Score" dataKey="score" stroke="#2563eb" fill="#3b82f6" fillOpacity={0.6} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Individual Scores */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Detailed Scores</h2>
          <div className="space-y-4">
            {chartData.map((item) => (
              <div key={item.metric}>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-medium text-gray-700">{item.metric}</span>
                  <span className={`text-sm font-bold ${getScoreColor(item.score)}`}>
                    {item.score}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      item.score >= 80 ? 'bg-green-600' : item.score >= 60 ? 'bg-yellow-600' : 'bg-red-600'
                    }`}
                    style={{ width: `${item.score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Strengths */}
      {analysis.strengths && analysis.strengths.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="h-5 w-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap={"round" as const}
                strokeLinejoin={"round" as const}
                strokeWidth={2}
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            Strengths
          </h2>
          <ul className="space-y-2">
            {analysis.strengths.map((strength, idx) => (
              <li key={idx} className="flex items-start">
                <span className="text-green-600 mr-2">•</span>
                <span className="text-gray-700">{strength}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Weaknesses */}
      {analysis.weaknesses && analysis.weaknesses.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="h-5 w-5 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap={"round" as const}
                strokeLinejoin={"round" as const}
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            Areas for Improvement
          </h2>
          <ul className="space-y-2">
            {analysis.weaknesses.map((weakness, idx) => (
              <li key={idx} className="flex items-start">
                <span className="text-red-600 mr-2">•</span>
                <span className="text-gray-700">{weakness}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Improvement Suggestions */}
      {analysis.improvement_suggestions && analysis.improvement_suggestions.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <svg className="h-5 w-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap={"round" as const}
                strokeLinejoin={"round" as const}
                strokeWidth={2}
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
            AI Suggestions
          </h2>
          <ul className="space-y-2">
            {analysis.improvement_suggestions.map((suggestion, idx) => (
              <li key={idx} className="flex items-start">
                <span className="text-blue-600 mr-2">💡</span>
                <span className="text-gray-700">{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Skills */}
      {resume.skills && resume.skills.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Extracted Skills</h2>
          <div className="flex flex-wrap gap-2">
            {resume.skills.map((skill, idx) => (
              <span
                key={idx}
                className="inline-block px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-full"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Education */}
      {resume.education && resume.education.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Education</h2>
          <ul className="space-y-2">
            {resume.education.map((edu, idx) => (
              <li key={idx} className="flex items-start">
                <svg className="h-5 w-5 text-blue-600 mr-2 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap={"round" as const}
                    strokeLinejoin={"round" as const}
                    strokeWidth={2}
                    d="M12 14l9-5-9-5-9 5 9 5z M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"
                  />
                </svg>
                <span className="text-gray-700">{edu}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Resume Enhancement */}
      <ResumeEnhancement 
        resumeId={resumeId} 
        resumeName={resume.original_filename}
      />
    </div>
  );
}
