import { useState, useEffect } from 'react';
import { JobPost, MatchScore, jobsService } from '../../services/jobs.service';
import JobCard from './JobCard';
import JobChromaGrid from './JobChromaGrid';

interface JobListProps {
  matchScores?: Map<string, MatchScore>;
  initialFilters?: JobFilters;
}

interface JobFilters {
  location?: string;
  jobType?: string;
  experienceLevel?: string;
  remoteOnly?: boolean;
}

type ViewMode = 'grid' | 'list' | 'chroma';

const JobList = ({ matchScores, initialFilters }: JobListProps) => {
  const [jobs, setJobs] = useState<JobPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [selectedJob, setSelectedJob] = useState<JobPost | null>(null);
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalJobs, setTotalJobs] = useState(0);
  const pageSize = 20;

  // Filters
  const [filters, setFilters] = useState<JobFilters>(initialFilters || {});

  // Fetch jobs
  useEffect(() => {
    fetchJobs();
  }, [currentPage, filters]);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await jobsService.listJobs(
        currentPage,
        pageSize,
        filters.location,
        filters.jobType,
        filters.remoteOnly || false
      );

      setJobs(response.jobs);
      setTotalPages(response.total_pages);
      setTotalJobs(response.total);
    } catch (err) {
      setError('Failed to load jobs. Please try again.');
      console.error('Error fetching jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: keyof JobFilters, value: string | boolean | undefined) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setCurrentPage(1); // Reset to first page when filters change
  };

  const handleViewDetails = (job: JobPost) => {
    setSelectedJob(job);
  };

  // Loading state
  if (loading && jobs.length === 0) {
    return (
      <div className="space-y-4">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow-md p-6 animate-pulse">
            <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-full mb-4"></div>
            <div className="flex gap-2">
              <div className="h-6 bg-gray-200 rounded w-16"></div>
              <div className="h-6 bg-gray-200 rounded w-16"></div>
              <div className="h-6 bg-gray-200 rounded w-16"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <svg className="w-12 h-12 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p className="text-red-800 font-medium mb-2">{error}</p>
        <button
          onClick={fetchJobs}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  // Empty state
  if (jobs.length === 0 && !loading) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-12 text-center">
        <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No jobs found</h3>
        <p className="text-gray-600 mb-4">
          Try adjusting your filters or check back later for new opportunities.
        </p>
        <button
          onClick={() => {
            setFilters({});
            setCurrentPage(1);
          }}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Clear Filters
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with filters and view toggle */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          {/* Filters */}
          <div className="flex flex-wrap gap-3 flex-1">
            {/* Location Filter */}
            <select
              value={filters.location || ''}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => handleFilterChange('location', e.target.value || undefined)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Locations</option>
              <optgroup label="🌍 MENA Region">
                <option value="MENA">All MENA</option>
                <option value="Tunisia">🇹🇳 Tunisia</option>
                <option value="Egypt">🇪🇬 Egypt</option>
                <option value="Morocco">🇲🇦 Morocco</option>
                <option value="Algeria">🇩🇿 Algeria</option>
                <option value="UAE">🇦🇪 UAE</option>
                <option value="Saudi Arabia">🇸🇦 Saudi Arabia</option>
                <option value="Jordan">🇯🇴 Jordan</option>
                <option value="Lebanon">🇱🇧 Lebanon</option>
                <option value="Qatar">🇶🇦 Qatar</option>
                <option value="Kuwait">🇰🇼 Kuwait</option>
                <option value="Bahrain">🇧🇭 Bahrain</option>
                <option value="Oman">🇴🇲 Oman</option>
                <option value="Libya">🇱🇾 Libya</option>
                <option value="Iraq">🇮🇶 Iraq</option>
                <option value="Syria">🇸🇾 Syria</option>
                <option value="Yemen">🇾🇪 Yemen</option>
              </optgroup>
              <optgroup label="🌍 Sub-Saharan Africa">
                <option value="SUB_SAHARAN_AFRICA">All Sub-Saharan Africa</option>
                <option value="Nigeria">🇳🇬 Nigeria</option>
                <option value="Kenya">🇰🇪 Kenya</option>
                <option value="South Africa">🇿🇦 South Africa</option>
                <option value="Ghana">🇬🇭 Ghana</option>
                <option value="Ethiopia">🇪🇹 Ethiopia</option>
                <option value="Tanzania">🇹🇿 Tanzania</option>
                <option value="Uganda">🇺🇬 Uganda</option>
                <option value="Rwanda">🇷🇼 Rwanda</option>
                <option value="Senegal">🇸🇳 Senegal</option>
              </optgroup>
              <optgroup label="🌐 Other Regions">
                <option value="NORTH_AMERICA">North America</option>
                <option value="EUROPE">Europe</option>
                <option value="ASIA">Asia</option>
              </optgroup>
            </select>

            {/* Job Type Filter */}
            <select
              value={filters.jobType || ''}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => handleFilterChange('jobType', e.target.value || undefined)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Types</option>
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Internship">Internship</option>
              <option value="Freelance">Freelance</option>
            </select>

            {/* Experience Level Filter */}
            <select
              value={filters.experienceLevel || ''}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) => handleFilterChange('experienceLevel', e.target.value || undefined)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Levels</option>
              <option value="Junior">Junior</option>
              <option value="Mid-Level">Mid-Level</option>
              <option value="Senior">Senior</option>
              <option value="Lead">Lead</option>
              <option value="Executive">Executive</option>
            </select>

            {/* Remote Only Toggle */}
            <label className="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-lg text-sm cursor-pointer hover:bg-gray-50">
              <input
                type="checkbox"
                checked={filters.remoteOnly || false}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleFilterChange('remoteOnly', e.target.checked)}
                className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
              />
              <span className="text-gray-700">Remote Only</span>
            </label>
          </div>

          {/* View Mode Toggle */}
          <div className="flex gap-2 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                viewMode === 'grid'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="Grid View"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                      d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                viewMode === 'list'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="List View"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                      d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode('chroma')}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                viewMode === 'chroma'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="Chroma Effect View"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                      d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
            </button>
          </div>
        </div>

        {/* Results count */}
        <div className="mt-4 text-sm text-gray-600">
          Showing {jobs.length} of {totalJobs} jobs
          {loading && <span className="ml-2 text-blue-600">• Refreshing...</span>}
        </div>
      </div>

      {/* Job Cards */}
      {viewMode === 'chroma' ? (
        <div style={{ minHeight: '600px', position: 'relative' }}>
          <JobChromaGrid 
            jobs={jobs}
            radius={300}
            damping={0.45}
            fadeOut={0.6}
            ease="power3.out"
            columns={3}
            onJobClick={handleViewDetails}
          />
        </div>
      ) : (
        <div className={viewMode === 'grid' 
          ? 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6'
          : 'space-y-4'
        }>
          {jobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              matchScore={matchScores?.get(job.id)}
              onViewDetails={handleViewDetails}
            />
          ))}
        </div>
      )}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-2 pt-6">
          <button
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          
          <div className="flex gap-2">
            {[...Array(Math.min(5, totalPages))].map((_, i) => {
              let pageNum;
              if (totalPages <= 5) {
                pageNum = i + 1;
              } else if (currentPage <= 3) {
                pageNum = i + 1;
              } else if (currentPage >= totalPages - 2) {
                pageNum = totalPages - 4 + i;
              } else {
                pageNum = currentPage - 2 + i;
              }

              return (
                <button
                  key={pageNum}
                  onClick={() => setCurrentPage(pageNum)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    currentPage === pageNum
                      ? 'bg-blue-600 text-white'
                      : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  {pageNum}
                </button>
              );
            })}
          </div>

          <button
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default JobList;
