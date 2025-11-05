import { useState, useEffect } from 'react';
import { jobsService, JobCompatibilityResponse } from '../../services/jobs.service';
import { resumeService } from '../../services/resume.service';
import type { Resume } from '../../types/api';
import { useToast } from '../../contexts/ToastContext';
import { Spinner } from '../common/LoadingComponents';

const JobCompatibilityAnalyzer = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState<number | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [company, setCompany] = useState('');
  const [requiredSkills, setRequiredSkills] = useState('');
  
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<JobCompatibilityResponse | null>(null);
  
  const { showSuccess, showError, showWarning } = useToast();

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      const response = await resumeService.getResumes();
      setResumes(response);
      if (response.length > 0) {
        setSelectedResumeId(response[0].id);
      }
    } catch (err) {
      showError('Failed to load resumes. Please try again.');
      console.error('Failed to load resumes:', err);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedResumeId) {
      showWarning('Please select a resume to analyze.');
      return;
    }

    if (!jobDescription.trim()) {
      showWarning('Please enter a job description.');
      return;
    }

    if (jobDescription.trim().length < 50) {
      showWarning('Job description must be at least 50 characters long. Please provide more details.');
      return;
    }

    try {
      setAnalyzing(true);
      setResult(null);

      const request = {
        resume_id: selectedResumeId,
        job_description: jobDescription.trim(),
        job_title: jobTitle.trim() || undefined,
        company: company.trim() || undefined,
        required_skills: requiredSkills
          ? requiredSkills.split(',').map(s => s.trim()).filter(s => s)
          : undefined,
      };

      const response = await jobsService.analyzeJobCompatibility(request);
      setResult(response);
      showSuccess('Compatibility analysis completed successfully!');
    } catch (err: any) {
      console.error('Compatibility analysis failed:', err);
      
      // Enhanced error handling
      let errorMessage = 'Failed to analyze compatibility. Please try again.';
      
      if (err.response?.status === 400) {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') {
          errorMessage = detail;
        } else if (Array.isArray(detail)) {
          // Pydantic validation errors
          errorMessage = detail.map((e: any) => 
            `${e.loc.join('.')}: ${e.msg}`
          ).join(', ');
        }
      } else if (err.response?.status === 404) {
        errorMessage = 'Resume not found. Please select a valid resume.';
      } else if (err.response?.status === 401 || err.response?.status === 403) {
        errorMessage = 'Authentication error. Please log in again.';
      } else if (err.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.message) {
        errorMessage = err.message;
      }
      
      showError(errorMessage);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleClear = () => {
    setJobDescription('');
    setJobTitle('');
    setCompany('');
    setRequiredSkills('');
    setResult(null);
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-blue-100';
    if (score >= 40) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Job Compatibility Analyzer
        </h2>
        <p className="text-gray-600 mb-6">
          Analyze how well your resume matches a specific job posting using AI-powered analysis
        </p>

        <div className="space-y-4">
          {/* Resume Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Your Resume *
            </label>
            <select
              value={selectedResumeId || ''}
              onChange={(e) => setSelectedResumeId(Number(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              disabled={analyzing}
            >
              <option value="">-- Select a resume --</option>
              {resumes.map((resume) => (
                <option key={resume.id} value={resume.id}>
                  {resume.original_filename} (Uploaded: {new Date(resume.uploaded_at).toLocaleDateString()})
                </option>
              ))}
            </select>
            {resumes.length === 0 && (
              <p className="mt-2 text-sm text-amber-600">
                No resumes found. Please upload a resume first.
              </p>
            )}
          </div>

          {/* Job Title (Optional) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Title (Optional)
            </label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              placeholder="e.g., Senior Software Engineer"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              disabled={analyzing}
            />
          </div>

          {/* Company (Optional) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Company (Optional)
            </label>
            <input
              type="text"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              placeholder="e.g., TechCorp Inc."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              disabled={analyzing}
            />
          </div>

          {/* Job Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Description * (minimum 50 characters)
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full job description here..."
              rows={10}
              className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent ${
                jobDescription.length > 0 && jobDescription.length < 50
                  ? 'border-amber-300 bg-amber-50'
                  : 'border-gray-300'
              }`}
              disabled={analyzing}
            />
            <p className={`mt-1 text-sm ${
              jobDescription.length < 50 && jobDescription.length > 0
                ? 'text-amber-600 font-medium'
                : 'text-gray-500'
            }`}>
              {jobDescription.length} / 50 characters minimum
              {jobDescription.length > 0 && jobDescription.length < 50 && (
                <span className="ml-2">({50 - jobDescription.length} more needed)</span>
              )}
            </p>
          </div>

          {/* Required Skills (Optional) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Required Skills (Optional)
            </label>
            <input
              type="text"
              value={requiredSkills}
              onChange={(e) => setRequiredSkills(e.target.value)}
              placeholder="e.g., Python, React, AWS (comma-separated)"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              disabled={analyzing}
            />
            <p className="mt-1 text-sm text-gray-500">
              Separate multiple skills with commas
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleAnalyze}
              disabled={analyzing || !selectedResumeId || !jobDescription.trim()}
              className="flex-1 bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium flex items-center justify-center gap-2 min-h-[44px]"
            >
              {analyzing && <Spinner size="sm" className="border-white border-t-transparent" />}
              {analyzing ? (
                <span>Analyzing...</span>) : (
                <span>Analyze Compatibility</span>
              )}
            </button>
            <button
              onClick={handleClear}
              disabled={analyzing}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium min-h-[44px]"
            >
              Clear
            </button>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {analyzing && (
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <div className="flex flex-col items-center justify-center space-y-4">
            <Spinner size="lg" />
            <div className="text-center">
              <p className="text-lg font-semibold text-gray-900">Analyzing Compatibility...</p>
              <p className="text-sm text-gray-600 mt-2">This may take a few moments</p>
            </div>
          </div>
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
          {/* Header */}
          <div className="border-b pb-4">
            <h3 className="text-2xl font-bold text-gray-900">
              Compatibility Analysis Results
            </h3>
            {result.job_title && (
              <p className="text-lg text-gray-600 mt-1">
                {result.job_title}
                {result.company && ` at ${result.company}`}
              </p>
            )}
          </div>

          {/* Overall Score */}
          <div className={`${getScoreBgColor(result.overall_match_score)} rounded-lg p-6`}>
            <div className="text-center">
              <p className="text-sm font-medium text-gray-600 mb-2">Overall Match Score</p>
              <p className={`text-6xl font-bold ${getScoreColor(result.overall_match_score)}`}>
                {result.overall_match_score}%
              </p>
            </div>
          </div>

          {/* Detailed Scores */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm font-medium text-gray-600 mb-2">Skills Match</p>
              <p className={`text-3xl font-bold ${getScoreColor(result.skill_match_score)}`}>
                {result.skill_match_score}%
              </p>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm font-medium text-gray-600 mb-2">Experience Match</p>
              <p className={`text-3xl font-bold ${getScoreColor(result.experience_match_score)}`}>
                {result.experience_match_score}%
              </p>
            </div>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm font-medium text-gray-600 mb-2">Education Match</p>
              <p className={`text-3xl font-bold ${getScoreColor(result.education_match_score)}`}>
                {result.education_match_score}%
              </p>
            </div>
          </div>

          {/* AI Summary */}
          {result.ai_summary && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-semibold text-blue-900 mb-2 flex items-center">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 2a8 8 0 100 16 8 8 0 000-16zm1 11H9v-2h2v2zm0-4H9V5h2v4z"/>
                </svg>
                AI Summary
              </h4>
              <p className="text-blue-800 text-sm">{result.ai_summary}</p>
            </div>
          )}

          {/* Matched Skills */}
          {result.matched_skills.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                <svg className="w-5 h-5 mr-2 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                </svg>
                Matched Skills ({result.matched_skills.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {result.matched_skills.map((skill, index) => (
                  <span
                    key={index}
                    className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium"
                  >
                    ✓ {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Missing Skills */}
          {result.missing_skills.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                <svg className="w-5 h-5 mr-2 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                </svg>
                Skills to Develop ({result.missing_skills.length})
              </h4>
              <div className="flex flex-wrap gap-2">
                {result.missing_skills.map((skill, index) => (
                  <span
                    key={index}
                    className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Strengths */}
          {result.strengths.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Your Strengths</h4>
              <ul className="space-y-2">
                {result.strengths.map((strength, index) => (
                  <li key={index} className="flex items-start">
                    <svg className="w-5 h-5 text-green-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                    </svg>
                    <span className="text-gray-700">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Gaps */}
          {result.gaps.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Areas for Improvement</h4>
              <ul className="space-y-2">
                {result.gaps.map((gap, index) => (
                  <li key={index} className="flex items-start">
                    <svg className="w-5 h-5 text-amber-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
                    </svg>
                    <span className="text-gray-700">{gap}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          {result.recommendations.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Recommendations</h4>
              <ul className="space-y-2">
                {result.recommendations.map((rec, index) => (
                  <li key={index} className="flex items-start">
                    <svg className="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
                    </svg>
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Detailed AI Analysis */}
          {result.ai_detailed_analysis && (
            <div className="border-t pt-6">
              <h4 className="font-semibold text-gray-900 mb-3">Detailed Analysis</h4>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-700 whitespace-pre-line">{result.ai_detailed_analysis}</p>
              </div>
            </div>
          )}

          {/* Timestamp */}
          <p className="text-sm text-gray-500 text-center">
            Analyzed at {new Date(result.analyzed_at).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
};

export default JobCompatibilityAnalyzer;
