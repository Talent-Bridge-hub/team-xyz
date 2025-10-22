import { useState, useEffect } from 'react';
import { interviewService } from '../../services/interview.service.ts';
import { resumeService } from '../../services/resume.service';
import { Resume } from '../../types/api';

interface InterviewSetupProps {
  onSessionStart: (sessionId: number) => void;
}

const InterviewSetup = ({ onSessionStart }: InterviewSetupProps) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resumes, setResumes] = useState<Resume[]>([]);
  
  // Form state
  const [sessionType, setSessionType] = useState<'technical' | 'behavioral' | 'mixed' | 'job-specific'>('mixed');
  const [jobRole, setJobRole] = useState('Software Engineer');
  const [customJobRole, setCustomJobRole] = useState('');
  const [roleInputMode, setRoleInputMode] = useState<'popular' | 'custom'>('popular');
  const [difficultyLevel, setDifficultyLevel] = useState<'junior' | 'mid' | 'senior'>('mid');
  const [numQuestions, setNumQuestions] = useState(5);
  const [resumeId, setResumeId] = useState<number | undefined>(undefined);

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      const resumeList = await resumeService.getResumes();
      setResumes(resumeList);
      if (resumeList.length > 0) {
        setResumeId(resumeList[0].id);
      }
    } catch (err) {
      console.error('Error fetching resumes:', err);
    }
  };

  const handleStartInterview = async () => {
    try {
      setLoading(true);
      setError(null);

      // Use custom role if in custom mode, otherwise use selected popular role
      const finalJobRole = roleInputMode === 'custom' ? customJobRole : jobRole;

      if (!finalJobRole || finalJobRole.trim() === '') {
        setError('Please enter a job role');
        setLoading(false);
        return;
      }

      const response = await interviewService.startSession({
        session_type: sessionType,
        job_role: finalJobRole,
        difficulty_level: difficultyLevel,
        num_questions: numQuestions,
        resume_id: resumeId
      });

      onSessionStart(response.session_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start interview. Please try again.');
      console.error('Error starting interview:', err);
    } finally {
      setLoading(false);
    }
  };

  const popularRoles = [
    'Software Engineer',
    'Frontend Developer',
    'Backend Developer',
    'Full Stack Developer',
    'Data Scientist',
    'Product Manager',
    'DevOps Engineer',
    'Mobile Developer',
    'UI/UX Designer',
    'Data Analyst'
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Configure Your Interview
          </h2>
          <p className="text-gray-600">
            Customize your practice session to match your career goals and preparation needs
          </p>
        </div>

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-red-800">{error}</p>
            </div>
          </div>
        )}

        <div className="space-y-6">
          {/* Session Type */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Interview Type
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { value: 'technical', label: 'Technical', icon: '💻', desc: 'Coding & problem solving' },
                { value: 'behavioral', label: 'Behavioral', icon: '🗣️', desc: 'Soft skills & experience' },
                { value: 'mixed', label: 'Mixed', icon: '🎯', desc: 'Combination of both' },
                { value: 'job-specific', label: 'Job-Specific', icon: '🎪', desc: 'Role-based questions' }
              ].map((type) => (
                <button
                  key={type.value}
                  onClick={() => setSessionType(type.value as any)}
                  className={`p-4 rounded-lg border-2 transition-all text-left ${
                    sessionType === type.value
                      ? 'border-blue-500 bg-blue-50 shadow-md'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="text-2xl mb-1">{type.icon}</div>
                  <div className="font-semibold text-gray-900 text-sm">{type.label}</div>
                  <div className="text-xs text-gray-500 mt-1">{type.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Job Role */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Target Job Role
            </label>
            
            {/* Mode Selection */}
            <div className="flex gap-3 mb-4">
              <button
                onClick={() => setRoleInputMode('popular')}
                className={`flex-1 px-4 py-2.5 rounded-lg border-2 transition-all font-medium text-sm ${
                  roleInputMode === 'popular'
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-300 bg-white text-gray-600 hover:border-gray-400'
                }`}
              >
                <div className="flex items-center justify-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Popular Roles
                </div>
              </button>
              <button
                onClick={() => setRoleInputMode('custom')}
                className={`flex-1 px-4 py-2.5 rounded-lg border-2 transition-all font-medium text-sm ${
                  roleInputMode === 'custom'
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-300 bg-white text-gray-600 hover:border-gray-400'
                }`}
              >
                <div className="flex items-center justify-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                  Custom Role
                </div>
              </button>
            </div>

            {/* Popular Roles Dropdown */}
            {roleInputMode === 'popular' && (
              <div className="space-y-2">
                <select
                  value={jobRole}
                  onChange={(e) => setJobRole(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white transition-all"
                >
                  {popularRoles.map((role) => (
                    <option key={role} value={role}>{role}</option>
                  ))}
                </select>
                <p className="text-xs text-gray-500 flex items-center gap-1">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Choose from our curated list of common tech roles
                </p>
              </div>
            )}

            {/* Custom Role Input */}
            {roleInputMode === 'custom' && (
              <div className="space-y-2">
                <input
                  type="text"
                  value={customJobRole}
                  onChange={(e) => setCustomJobRole(e.target.value)}
                  placeholder="e.g., Machine Learning Engineer, QA Automation Lead..."
                  className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                  autoFocus
                />
                <p className="text-xs text-gray-500 flex items-center gap-1">
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Enter any job role you're preparing for
                </p>
              </div>
            )}
          </div>

          {/* Difficulty Level */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Difficulty Level
            </label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { value: 'junior', label: 'Junior', icon: '🌱', desc: '0-2 years experience' },
                { value: 'mid', label: 'Mid-Level', icon: '🌿', desc: '2-5 years experience' },
                { value: 'senior', label: 'Senior', icon: '🌳', desc: '5+ years experience' }
              ].map((level) => (
                <button
                  key={level.value}
                  onClick={() => setDifficultyLevel(level.value as any)}
                  className={`p-4 rounded-lg border-2 transition-all text-center ${
                    difficultyLevel === level.value
                      ? 'border-blue-500 bg-blue-50 shadow-md'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="text-2xl mb-1">{level.icon}</div>
                  <div className="font-semibold text-gray-900 text-sm">{level.label}</div>
                  <div className="text-xs text-gray-500 mt-1">{level.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Number of Questions */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Number of Questions: <span className="text-blue-600 font-bold">{numQuestions}</span>
            </label>
            <input
              type="range"
              min="3"
              max="15"
              value={numQuestions}
              onChange={(e) => setNumQuestions(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>3 (Quick)</span>
              <span>5 (Standard)</span>
              <span>10 (Comprehensive)</span>
              <span>15 (Thorough)</span>
            </div>
          </div>

          {/* Resume Selection */}
          {resumes.length > 0 && (
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Use Resume (Optional)
              </label>
              <select
                value={resumeId || ''}
                onChange={(e) => setResumeId(e.target.value ? parseInt(e.target.value) : undefined)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">No resume (General questions)</option>
                {resumes.map((resume) => (
                  <option key={resume.id} value={resume.id}>
                    {resume.original_filename} - Resume #{resume.id}
                  </option>
                ))}
              </select>
              <p className="mt-1 text-xs text-gray-500">
                We'll tailor questions based on your resume if selected
              </p>
            </div>
          )}

          {/* Start Button */}
          <div className="pt-4">
            <button
              onClick={handleStartInterview}
              disabled={loading || (roleInputMode === 'custom' && !customJobRole.trim())}
              className="w-full px-6 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-semibold text-lg shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Preparing Interview...
                </>
              ) : (
                <>
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Start Interview
                  {roleInputMode === 'custom' && customJobRole.trim() && (
                    <span className="text-xs font-normal opacity-90">
                      ({customJobRole})
                    </span>
                  )}
                  {roleInputMode === 'popular' && (
                    <span className="text-xs font-normal opacity-90">
                      ({jobRole})
                    </span>
                  )}
                </>
              )}
            </button>
          </div>

          {/* Info Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex gap-3">
              <svg className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="text-sm text-blue-900">
                <p className="font-semibold mb-1">Interview Tips:</p>
                <ul className="list-disc list-inside space-y-1 text-blue-800">
                  <li>Take your time to think before answering</li>
                  <li>Speak clearly and provide specific examples</li>
                  <li>Be honest - this is practice, not a test</li>
                  <li>Review the feedback after each question</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InterviewSetup;
