import { useState, useEffect } from 'react';
import { jobsService, JobMatch, MatchScore } from '../../services/jobs.service';
import { resumeService } from '../../services/resume.service';
import { Resume } from '../../types/api';
import JobList from './JobList';
import JobDetailModal from './JobDetailModal';

const JobMatcher = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState<number | null>(null);
  const [locationPreference, setLocationPreference] = useState<string[]>([]);
  const [jobTypes, setJobTypes] = useState<string[]>([]);
  const [experienceLevels, setExperienceLevels] = useState<string[]>([]);
  const [minScore, setMinScore] = useState(60);
  const [limit, setLimit] = useState(50);
  
  const [loading, setLoading] = useState(false);
  const [loadingResumes, setLoadingResumes] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [matches, setMatches] = useState<JobMatch[]>([]);
  const [matchResults, setMatchResults] = useState<{
    total_jobs_searched: number;
    matches_found: number;
    avg_match_score: number;
    processing_time_ms: number;
  } | null>(null);

  const [selectedJob, setSelectedJob] = useState<JobMatch | null>(null);

  // Fetch resumes on mount
  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      setLoadingResumes(true);
      const resumeList = await resumeService.getResumes();
      setResumes(resumeList);
      if (resumeList.length > 0) {
        setSelectedResumeId(resumeList[0].id);
      }
    } catch (err) {
      console.error('Error fetching resumes:', err);
      setError('Failed to load resumes. Please upload a resume first.');
    } finally {
      setLoadingResumes(false);
    }
  };

  const handleMatch = async () => {
    if (!selectedResumeId) {
      setError('Please select a resume');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      setMatches([]);
      setMatchResults(null);

      const response = await jobsService.matchJobs({
        resume_id: selectedResumeId,
        location_preference: locationPreference.length > 0 ? locationPreference : undefined,
        job_types: jobTypes.length > 0 ? jobTypes : undefined,
        experience_level: experienceLevels.length > 0 ? experienceLevels : undefined,
        min_score: minScore,
        limit: limit,
      });

      setMatches(response.matches);
      setMatchResults({
        total_jobs_searched: response.total_jobs_searched,
        matches_found: response.matches_found,
        avg_match_score: response.avg_match_score,
        processing_time_ms: response.processing_time_ms,
      });
    } catch (err) {
      setError('Failed to match jobs. Please try again.');
      console.error('Error matching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleArrayValue = (array: string[], value: string, setter: (arr: string[]) => void) => {
    if (array.includes(value)) {
      setter(array.filter(v => v !== value));
    } else {
      setter([...array, value]);
    }
  };

  // Convert matches to JobPost array for JobList
  const jobsFromMatches = matches.map(match => match.job);
  
  // Create match scores map for JobList
  const matchScoresMap = new Map<string, MatchScore>();
  matches.forEach(match => {
    matchScoresMap.set(match.job.id, match.match_score);
  });

  if (loadingResumes) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (resumes.length === 0) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-8 text-center">
        <svg className="w-16 h-16 text-yellow-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No Resumes Found</h3>
        <p className="text-gray-600 mb-4">
          You need to upload a resume before you can match jobs.
        </p>
        <a
          href="/resume"
          className="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          Upload Resume
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Matching Configuration */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Configure Job Matching</h3>
        
        <div className="space-y-4">
          {/* Resume Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Resume
            </label>
            <select
              value={selectedResumeId || ''}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setSelectedResumeId(Number(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              {resumes.map(resume => (
                <option key={resume.id} value={resume.id}>
                  {resume.original_filename} (Uploaded {new Date(resume.uploaded_at).toLocaleDateString()})
                </option>
              ))}
            </select>
          </div>

          {/* Location Preference */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Location Preference (Optional)
            </label>
            <div className="flex flex-wrap gap-2">
              {['MENA', 'Tunisia', 'Egypt', 'Morocco', 'Algeria', 'UAE', 'Saudi Arabia', 'Jordan', 'Lebanon', 'Qatar', 'Kuwait', 'Bahrain', 'Oman', 'Sub-Saharan Africa', 'Nigeria', 'Kenya', 'South Africa', 'Ghana', 'Ethiopia', 'Tanzania', 'Uganda', 'Rwanda', 'Remote'].map(location => (
                <button
                  key={location}
                  onClick={() => toggleArrayValue(locationPreference, location, setLocationPreference)}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                    locationPreference.includes(location)
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {location.replace(/_/g, ' ')}
                </button>
              ))}
            </div>
          </div>

          {/* Job Types */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Types (Optional)
            </label>
            <div className="flex flex-wrap gap-2">
              {['Full-time', 'Part-time', 'Contract', 'Internship', 'Freelance'].map(type => (
                <button
                  key={type}
                  onClick={() => toggleArrayValue(jobTypes, type, setJobTypes)}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                    jobTypes.includes(type)
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>

          {/* Experience Levels */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Experience Levels (Optional)
            </label>
            <div className="flex flex-wrap gap-2">
              {['Junior', 'Mid-Level', 'Senior', 'Lead', 'Executive'].map(level => (
                <button
                  key={level}
                  onClick={() => toggleArrayValue(experienceLevels, level, setExperienceLevels)}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                    experienceLevels.includes(level)
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>

          {/* Min Score Slider */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Minimum Match Score: {minScore}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              step="5"
              value={minScore}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setMinScore(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>0%</span>
              <span>50%</span>
              <span>100%</span>
            </div>
          </div>

          {/* Max Results */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Maximum Results
            </label>
            <select
              value={limit}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setLimit(Number(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value={25}>25 jobs</option>
              <option value={50}>50 jobs</option>
              <option value={100}>100 jobs</option>
              <option value={200}>200 jobs</option>
            </select>
          </div>

          {/* Match Button */}
          <button
            onClick={handleMatch}
            disabled={loading || !selectedResumeId}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Matching Jobs...
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                        d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Find Matching Jobs
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <svg className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Match Results Summary */}
      {matchResults && (
        <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Match Results</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">{matchResults.total_jobs_searched}</div>
              <div className="text-sm text-gray-600">Jobs Searched</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">{matchResults.matches_found}</div>
              <div className="text-sm text-gray-600">Matches Found</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-indigo-600">{Math.round(matchResults.avg_match_score)}%</div>
              <div className="text-sm text-gray-600">Avg. Match Score</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">{(matchResults.processing_time_ms / 1000).toFixed(2)}s</div>
              <div className="text-sm text-gray-600">Processing Time</div>
            </div>
          </div>
        </div>
      )}

      {/* Matched Jobs List */}
      {matches.length > 0 && (
        <div>
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Your Matched Jobs ({matches.length})
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            {matches.map(match => (
              <div key={match.job.id} onClick={() => setSelectedJob(match)} className="cursor-pointer">
                <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6">
                  {/* Match Score Badge */}
                  <div className="flex justify-between items-start mb-3">
                    <h4 className="text-lg font-semibold text-gray-900">{match.job.title}</h4>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      match.match_score.overall_score >= 80 ? 'bg-green-100 text-green-800' :
                      match.match_score.overall_score >= 60 ? 'bg-blue-100 text-blue-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {match.match_score.overall_score}%
                    </span>
                  </div>
                  
                  <p className="text-gray-600 font-medium mb-2">{match.job.company}</p>
                  <p className="text-gray-500 text-sm mb-4">{match.job.location}</p>
                  
                  {/* Score Breakdown */}
                  <div className="grid grid-cols-3 gap-2 mb-4 text-xs">
                    <div className="text-center p-2 bg-gray-50 rounded">
                      <div className="font-bold text-gray-900">{match.match_score.skill_score}%</div>
                      <div className="text-gray-600">Skills</div>
                    </div>
                    <div className="text-center p-2 bg-gray-50 rounded">
                      <div className="font-bold text-gray-900">{match.match_score.location_score}%</div>
                      <div className="text-gray-600">Location</div>
                    </div>
                    <div className="text-center p-2 bg-gray-50 rounded">
                      <div className="font-bold text-gray-900">{match.match_score.experience_score}%</div>
                      <div className="text-gray-600">Experience</div>
                    </div>
                  </div>

                  <button
                    onClick={(e: React.MouseEvent) => {
                      e.stopPropagation();
                      window.open(match.job.url, '_blank', 'noopener,noreferrer');
                    }}
                    className="w-full px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Apply Now
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Job Detail Modal */}
      {selectedJob && (
        <JobDetailModal
          isOpen={!!selectedJob}
          onClose={() => setSelectedJob(null)}
          job={selectedJob.job}
          matchScore={selectedJob.match_score}
        />
      )}
    </div>
  );
};

export default JobMatcher;
