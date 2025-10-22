import { JobPost, MatchScore } from '../../services/jobs.service';

interface JobDetailModalProps {
  isOpen: boolean;
  onClose: () => void;
  job: JobPost | null;
  matchScore?: MatchScore;
}

const JobDetailModal = ({ isOpen, onClose, job, matchScore }: JobDetailModalProps) => {
  if (!isOpen || !job) return null;

  const getSalaryDisplay = () => {
    if (!job.salary_range) return 'Not specified';
    
    const { min, max, currency, text } = job.salary_range;
    if (text) return text;
    if (min && max) return `${currency} ${min.toLocaleString()} - ${max.toLocaleString()}`;
    if (min) return `${currency} ${min.toLocaleString()}+`;
    if (max) return `Up to ${currency} ${max.toLocaleString()}`;
    return 'Not specified';
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50';
    if (score >= 60) return 'text-blue-600 bg-blue-50';
    if (score >= 40) return 'text-yellow-600 bg-yellow-50';
    return 'text-gray-600 bg-gray-50';
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-start z-10">
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900 mb-1">{job.title}</h2>
              <div className="flex items-center gap-4 text-gray-600">
                <span className="font-medium">{job.company}</span>
                <span className="flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                          d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {job.location}
                </span>
                {job.remote && (
                  <span className="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs rounded-full font-medium">
                    Remote
                  </span>
                )}
              </div>
            </div>
            <button
              onClick={onClose}
              className="ml-4 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                      d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Content */}
          <div className="px-6 py-6 space-y-6">
            {/* Match Score Section */}
            {matchScore && (
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Match Analysis</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div className={`${getScoreColor(matchScore.overall_score)} rounded-lg p-3 text-center`}>
                    <div className="text-2xl font-bold">{matchScore.overall_score}%</div>
                    <div className="text-sm font-medium">Overall</div>
                  </div>
                  <div className={`${getScoreColor(matchScore.skill_score)} rounded-lg p-3 text-center`}>
                    <div className="text-2xl font-bold">{matchScore.skill_score}%</div>
                    <div className="text-sm font-medium">Skills</div>
                  </div>
                  <div className={`${getScoreColor(matchScore.location_score)} rounded-lg p-3 text-center`}>
                    <div className="text-2xl font-bold">{matchScore.location_score}%</div>
                    <div className="text-sm font-medium">Location</div>
                  </div>
                  <div className={`${getScoreColor(matchScore.experience_score)} rounded-lg p-3 text-center`}>
                    <div className="text-2xl font-bold">{matchScore.experience_score}%</div>
                    <div className="text-sm font-medium">Experience</div>
                  </div>
                </div>

                {matchScore.breakdown && (
                  <div className="space-y-3">
                    {matchScore.breakdown.skills_matched?.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2">✓ Matched Skills:</p>
                        <div className="flex flex-wrap gap-2">
                          {matchScore.breakdown.skills_matched.map((skill, index) => (
                            <span key={index} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    {matchScore.breakdown.skills_missing?.length > 0 && (
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-2">○ Missing Skills:</p>
                        <div className="flex flex-wrap gap-2">
                          {matchScore.breakdown.skills_missing.map((skill, index) => (
                            <span key={index} className="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Job Details */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg">
              <div>
                <p className="text-sm text-gray-600 mb-1">Job Type</p>
                <p className="font-medium text-gray-900">{job.type || job.job_type || 'Not specified'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Experience Level</p>
                <p className="font-medium text-gray-900">{job.experience_level || 'Not specified'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Salary Range</p>
                <p className="font-medium text-gray-900">{getSalaryDisplay()}</p>
              </div>
              {job.region && (
                <div>
                  <p className="text-sm text-gray-600 mb-1">Region</p>
                  <p className="font-medium text-gray-900">{job.region}</p>
                </div>
              )}
              {job.posted_date && (
                <div>
                  <p className="text-sm text-gray-600 mb-1">Posted Date</p>
                  <p className="font-medium text-gray-900">
                    {new Date(job.posted_date).toLocaleDateString()}
                  </p>
                </div>
              )}
              {job.source && (
                <div>
                  <p className="text-sm text-gray-600 mb-1">Source</p>
                  <p className="font-medium text-gray-900">{job.source}</p>
                </div>
              )}
            </div>

            {/* Description */}
            {job.description && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Job Description</h3>
                <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-line">
                  {job.description}
                </div>
              </div>
            )}

            {/* Required Skills */}
            {job.required_skills && job.required_skills.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Required Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {job.required_skills.map((skill, index) => (
                    <span key={index} className="px-3 py-1.5 bg-indigo-50 text-indigo-700 text-sm rounded-lg font-medium">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Preferred Skills */}
            {job.preferred_skills && job.preferred_skills.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Preferred Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {job.preferred_skills.map((skill, index) => (
                    <span key={index} className="px-3 py-1.5 bg-gray-100 text-gray-700 text-sm rounded-lg">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="sticky bottom-0 bg-white border-t border-gray-200 px-6 py-4 flex justify-between items-center">
            <button
              onClick={onClose}
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Close
            </button>
            <button
              onClick={() => window.open(job.url, '_blank', 'noopener,noreferrer')}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center gap-2"
            >
              Apply Now
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetailModal;
