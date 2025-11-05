import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  CodeBracketIcon, 
  ChatBubbleLeftRightIcon, 
  SparklesIcon,
  BriefcaseIcon,
  RocketLaunchIcon 
} from '@heroicons/react/24/outline';
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
  const [hoveredType, setHoveredType] = useState<string | null>(null);

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

  const interviewTypes = [
    { 
      value: 'technical', 
      label: 'Technical', 
      Icon: CodeBracketIcon, 
      desc: 'Coding & problem solving',
      gradient: 'from-electric-cyan to-deep-ocean'
    },
    { 
      value: 'behavioral', 
      label: 'Behavioral', 
      Icon: ChatBubbleLeftRightIcon, 
      desc: 'Soft skills & experience',
      gradient: 'from-stellar-purple to-royal-purple'
    },
    { 
      value: 'mixed', 
      label: 'Mixed', 
      Icon: SparklesIcon, 
      desc: 'Combination of both',
      gradient: 'from-cosmic-gold to-amber-gold'
    },
    { 
      value: 'job-specific', 
      label: 'Job-Specific', 
      Icon: BriefcaseIcon, 
      desc: 'Role-based questions',
      gradient: 'from-electric-cyan to-stellar-purple'
    }
  ];

  const difficultyLevels = [
    { value: 'junior', label: 'Junior', desc: '0-2 years', color: 'electric-cyan' },
    { value: 'mid', label: 'Mid-Level', desc: '2-5 years', color: 'stellar-purple' },
    { value: 'senior', label: 'Senior', desc: '5+ years', color: 'cosmic-gold' }
  ];

  // Calculate progress percentage for circular ring
  const questionProgress = ((numQuestions - 3) / (15 - 3)) * 100;
  const circumference = 2 * Math.PI * 45; // radius = 45
  const strokeDashoffset = circumference - (questionProgress / 100) * circumference;

  return (
    <div className="max-w-5xl mx-auto">
      <div className="bg-white dark:bg-slate-800 rounded-lg p-8 shadow-lg">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2 text-slate-900 dark:text-white">
            Configure Your Interview
          </h2>
          <p className="text-slate-600 dark:text-slate-400">
            Customize your practice session to match your career goals and preparation needs
          </p>
        </div>

          {error && (
            <div className="mb-6 bg-red-50 dark:bg-red-900/20 border-2 border-red-500 rounded-lg p-4">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-red-100 dark:bg-red-900/50 rounded-lg">
                  <svg className="w-5 h-5 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                          d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <p className="text-red-700 dark:text-red-300 font-medium">{error}</p>
              </div>
            </div>
          )}

          <div className="space-y-8">
            {/* Interview Type */}
            <div>
              <label className="block text-sm font-semibold text-slate-900 dark:text-white mb-4">
                Interview Type
              </label>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                {interviewTypes.map((type) => (
                  <button
                    key={type.value}
                    onClick={() => setSessionType(type.value as any)}
                    className={`p-6 rounded-lg border-2 transition-all ${
                      sessionType === type.value
                        ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
                        : 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 hover:border-blue-400'
                    }`}
                  >
                    <type.Icon className={`w-10 h-10 mb-3 mx-auto ${
                      sessionType === type.value ? 'text-blue-600 dark:text-blue-400' : 'text-slate-600 dark:text-slate-400'
                    }`} />
                    <div className={`font-bold text-base mb-1 ${
                      sessionType === type.value ? 'text-blue-700 dark:text-blue-300' : 'text-slate-900 dark:text-white'
                    }`}>
                      {type.label}
                    </div>
                    <div className="text-xs text-slate-600 dark:text-slate-400 mt-2">
                      {type.desc}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Difficulty Level */}
            <div>
              <label className="block text-sm font-semibold text-slate-900 dark:text-white mb-4">
                Difficulty Level
              </label>
              <div className="bg-slate-50 dark:bg-slate-700 rounded-lg p-6">
                <div className="flex justify-between items-center gap-4">
                  {difficultyLevels.map((level) => (
                    <button
                      key={level.value}
                      onClick={() => setDifficultyLevel(level.value as any)}
                      className={`flex-1 flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-all ${
                        difficultyLevel === level.value
                          ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/30'
                          : 'border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 hover:border-blue-400'
                      }`}
                    >
                      <div className={`w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg ${
                        difficultyLevel === level.value
                          ? 'bg-blue-500 text-white'
                          : 'bg-slate-200 dark:bg-slate-600 text-slate-700 dark:text-slate-300'
                      }`}>
                        {level.label[0]}
                      </div>
                      <div className={`text-sm font-bold ${
                        difficultyLevel === level.value ? 'text-blue-700 dark:text-blue-300' : 'text-slate-900 dark:text-white'
                      }`}>
                        {level.label}
                      </div>
                      <div className="text-xs text-slate-600 dark:text-slate-400">
                        {level.desc}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Question Count */}
            <div>
              <label className="block text-sm font-semibold text-slate-900 dark:text-white mb-4">
                Number of Questions
              </label>
              <div className="bg-slate-50 dark:bg-slate-700 rounded-lg p-6">
                <div className="flex flex-col md:flex-row items-center gap-8">
                  {/* Number Display */}
                  <div className="flex-shrink-0 text-center">
                    <div className="text-6xl font-black text-blue-600 dark:text-blue-400">
                      {numQuestions}
                    </div>
                    <div className="text-sm font-semibold text-slate-700 dark:text-slate-300 mt-2">
                      questions
                    </div>
                  </div>

                  {/* Slider */}
                  <div className="flex-1 w-full">
                    <input
                      type="range"
                      min="3"
                      max="15"
                      value={numQuestions}
                      onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                      className="w-full h-2 bg-slate-300 dark:bg-slate-600 rounded-lg appearance-none cursor-pointer
                        [&::-webkit-slider-thumb]:appearance-none
                        [&::-webkit-slider-thumb]:w-5
                        [&::-webkit-slider-thumb]:h-5
                        [&::-webkit-slider-thumb]:rounded-full
                        [&::-webkit-slider-thumb]:bg-blue-500
                        [&::-webkit-slider-thumb]:cursor-pointer
                        [&::-webkit-slider-thumb]:hover:bg-blue-600"
                    />
                    <div className="flex justify-between text-xs font-medium mt-3 text-slate-600 dark:text-slate-400">
                      <span>Quick (3)</span>
                      <span>Standard (5)</span>
                      <span>Deep (10)</span>
                      <span>Thorough (15)</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Job Role */}
            <div>
              <label className="block text-sm font-semibold text-slate-900 dark:text-white mb-4">
                Target Job Role
              </label>
              <div className="bg-slate-50 dark:bg-slate-700 rounded-lg p-6 space-y-4">
                {/* Mode Selection */}
                <div className="flex gap-3">
                  <button
                    onClick={() => setRoleInputMode('popular')}
                    className={`flex-1 px-4 py-2 rounded-lg font-medium transition-all ${
                      roleInputMode === 'popular'
                        ? 'bg-blue-500 text-white'
                        : 'bg-white dark:bg-slate-600 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-500'
                    }`}
                  >
                    Popular Roles
                  </button>
                  <button
                    onClick={() => setRoleInputMode('custom')}
                    className={`flex-1 px-4 py-2 rounded-lg font-medium transition-all ${
                      roleInputMode === 'custom'
                        ? 'bg-blue-500 text-white'
                        : 'bg-white dark:bg-slate-600 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-500'
                    }`}
                  >
                    Custom Role
                  </button>
                </div>

                {/* Input */}
                {roleInputMode === 'popular' ? (
                  <select
                    value={jobRole}
                    onChange={(e) => setJobRole(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white dark:bg-slate-800 border-2 border-slate-300 dark:border-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 transition-all text-slate-900 dark:text-white"
                  >
                    <option value="Software Engineer">Software Engineer</option>
                    <option value="Frontend Developer">Frontend Developer</option>
                    <option value="Backend Developer">Backend Developer</option>
                    <option value="Full Stack Developer">Full Stack Developer</option>
                    <option value="Data Scientist">Data Scientist</option>
                    <option value="Product Manager">Product Manager</option>
                    <option value="DevOps Engineer">DevOps Engineer</option>
                    <option value="Mobile Developer">Mobile Developer</option>
                    <option value="UI/UX Designer">UI/UX Designer</option>
                    <option value="Data Analyst">Data Analyst</option>
                  </select>
                ) : (
                  <input
                    type="text"
                    value={customJobRole}
                    onChange={(e) => setCustomJobRole(e.target.value)}
                    placeholder="e.g., Machine Learning Engineer..."
                    className="w-full px-4 py-3 rounded-lg bg-white dark:bg-slate-800 border-2 border-slate-300 dark:border-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 transition-all text-slate-900 dark:text-white placeholder-slate-500 dark:placeholder-slate-400"
                    autoFocus
                  />
                )}
              </div>
            </div>

            {/* Resume Selection */}
            {resumes.length > 0 && (
              <div>
                <label className="block text-sm font-semibold text-slate-900 dark:text-white mb-4">
                  Use Resume (Optional)
                </label>
                <select
                  value={resumeId || ''}
                  onChange={(e) => setResumeId(e.target.value ? parseInt(e.target.value) : undefined)}
                  className="w-full px-4 py-3 rounded-lg bg-white dark:bg-slate-800 border-2 border-slate-300 dark:border-slate-600 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 transition-all text-slate-900 dark:text-white"
                >
                  <option value="">No resume (General questions)</option>
                  {resumes.map((resume) => (
                    <option key={resume.id} value={resume.id}>
                      {resume.original_filename}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Start Button */}
            <button
              onClick={handleStartInterview}
              disabled={loading || (roleInputMode === 'custom' && !customJobRole.trim())}
              className="w-full px-8 py-4 rounded-lg bg-blue-600 hover:bg-blue-700 disabled:bg-slate-400 disabled:cursor-not-allowed text-white font-bold text-lg transition-colors flex items-center justify-center gap-3"
            >
              {loading ? (
                <>
                  <svg className="animate-spin w-6 h-6" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Preparing Interview...
                </>
              ) : (
                <>
                  <RocketLaunchIcon className="w-6 h-6" />
                  Start Interview
                </>
              )}
            </button>
          </div>
      </div>
    </div>
  );
};

export default InterviewSetup;
