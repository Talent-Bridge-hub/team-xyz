import { JobPost, MatchScore } from '../../services/jobs.service';

interface JobCardProps {
  job: JobPost;
  matchScore?: MatchScore;
  onViewDetails: (job: JobPost) => void;
}

const JobCard = ({ job, matchScore, onViewDetails }: JobCardProps) => {
  const getSalaryDisplay = () => {
    if (!job.salary_range) return null;
    
    const { min, max, currency, text } = job.salary_range;
    if (text) return text;
    if (min && max) return `${currency} ${min.toLocaleString()} - ${max.toLocaleString()}`;
    if (min) return `${currency} ${min.toLocaleString()}+`;
    if (max) return `Up to ${currency} ${max.toLocaleString()}`;
    return null;
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'bg-green-100 text-green-800';
    if (score >= 60) return 'bg-blue-100 text-blue-800';
    if (score >= 40) return 'bg-yellow-100 text-yellow-800';
    return 'bg-gray-100 text-gray-800';
  };

  const truncateDescription = (text: string, maxLength: number = 150) => {
    if (!text) return 'No description available';
    if (text.length <= maxLength) return text;
    return text.slice(0, maxLength).trim() + '...';
  };

  const jobType = job.type || job.job_type || 'Full-time';

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6 cursor-pointer"
         onClick={() => onViewDetails(job)}>
      {/* Header: Title and Match Score */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-900 mb-1 hover:text-blue-600 transition-colors">
            {job.title}
          </h3>
          <p className="text-gray-600 font-medium">{job.company}</p>
        </div>
        {matchScore && (
          <div className={`ml-4 px-3 py-1 rounded-full text-sm font-semibold ${getScoreColor(matchScore.overall_score)}`}>
            {matchScore.overall_score}% Match
          </div>
        )}
      </div>

      {/* Location and Remote */}
      <div className="flex items-center gap-2 mb-3 text-gray-600">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <span className="text-sm">{job.location}</span>
        {job.remote && (
          <span className="ml-2 px-2 py-0.5 bg-blue-50 text-blue-700 text-xs rounded-full font-medium">
            Remote
          </span>
        )}
      </div>

      {/* Job Type and Experience Level */}
      <div className="flex gap-2 mb-3">
        <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded font-medium">
          {jobType}
        </span>
        {job.experience_level && (
          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded font-medium">
            {job.experience_level}
          </span>
        )}
      </div>

      {/* Description Preview */}
      <p className="text-gray-600 text-sm mb-4 line-clamp-2">
        {truncateDescription(job.description || '')}
      </p>

      {/* Skills */}
      {job.required_skills.length > 0 && (
        <div className="mb-4">
          <div className="flex flex-wrap gap-2">
            {job.required_skills.slice(0, 5).map((skill, index) => (
              <span key={index} className="px-2 py-1 bg-indigo-50 text-indigo-700 text-xs rounded">
                {skill}
              </span>
            ))}
            {job.required_skills.length > 5 && (
              <span className="px-2 py-1 bg-gray-50 text-gray-600 text-xs rounded">
                +{job.required_skills.length - 5} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Salary */}
      {getSalaryDisplay() && (
        <div className="flex items-center gap-2 mb-4 text-gray-700">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                  d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="text-sm font-medium">{getSalaryDisplay()}</span>
        </div>
      )}

      {/* Footer */}
      <div className="flex justify-between items-center pt-4 border-t border-gray-200">
        <div className="flex items-center gap-4 text-xs text-gray-500">
          {job.posted_date && (
            <span>Posted {new Date(job.posted_date).toLocaleDateString()}</span>
          )}
          {job.source && (
            <span className="flex items-center gap-1">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
              </svg>
              {job.source}
            </span>
          )}
        </div>
        <button
          onClick={(e: React.MouseEvent) => {
            e.stopPropagation();
            window.open(job.url, '_blank', 'noopener,noreferrer');
          }}
          className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
        >
          Apply Now
        </button>
      </div>
    </div>
  );
};

export default JobCard;
