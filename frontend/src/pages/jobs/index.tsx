import { useState } from 'react';
import JobList from '../../components/jobs/JobList';
import JobMatcher from '../../components/jobs/JobMatcher';
import JobCompatibilityAnalyzer from '../../components/jobs/JobCompatibilityAnalyzer';
import { JobPost, jobsService } from '../../services/jobs.service';
import JobCard from '../../components/jobs/JobCard';

type TabType = 'browse' | 'matched' | 'search' | 'compatibility';

interface SearchFilters {
  keywords?: string;
  location?: string;
  jobType?: string;
  experienceLevel?: string;
  remoteOnly?: boolean;
  minSalary?: string;
  maxSalary?: string;
  requiredSkills?: string;
}

const JobsPage = () => {
  const [activeTab, setActiveTab] = useState<TabType>('browse');
  
  // Advanced search state
  const [searchFilters, setSearchFilters] = useState<SearchFilters>({});
  const [searchResults, setSearchResults] = useState<JobPost[]>([]);
  const [searching, setSearching] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [totalResults, setTotalResults] = useState(0);

  const tabs = [
    { id: 'browse' as TabType, label: 'Browse All Jobs', icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' },
    { id: 'matched' as TabType, label: 'Matched for You', icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' },
    { id: 'search' as TabType, label: 'Advanced Search', icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' },
    { id: 'compatibility' as TabType, label: 'Compatibility Analyzer', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' },
  ];

  const handleSearchFilterChange = (key: keyof SearchFilters, value: string | boolean) => {
    setSearchFilters(prev => ({ ...prev, [key]: value || undefined }));
  };

  const handleSearch = async () => {
    try {
      setSearching(true);
      setSearchError(null);
      setHasSearched(true);
      
      // Build search request
      const searchRequest: any = {
        page: 1,
        page_size: 50
      };
      
      if (searchFilters.keywords) searchRequest.keywords = searchFilters.keywords;
      if (searchFilters.location) searchRequest.location = searchFilters.location;
      if (searchFilters.jobType) searchRequest.job_type = searchFilters.jobType;
      if (searchFilters.experienceLevel) searchRequest.experience_level = searchFilters.experienceLevel;
      if (searchFilters.remoteOnly) searchRequest.remote_only = searchFilters.remoteOnly;
      if (searchFilters.minSalary) searchRequest.min_salary = parseInt(searchFilters.minSalary);
      if (searchFilters.maxSalary) searchRequest.max_salary = parseInt(searchFilters.maxSalary);
      if (searchFilters.requiredSkills) {
        searchRequest.required_skills = searchFilters.requiredSkills
          .split(',')
          .map(s => s.trim())
          .filter(s => s.length > 0);
      }
      
      const response = await jobsService.searchJobs(searchRequest);
      setSearchResults(response.jobs);
      setTotalResults(response.total);
    } catch (err) {
      console.error('Search error:', err);
      setSearchError('Failed to search jobs. Please try again.');
    } finally {
      setSearching(false);
    }
  };

  const handleClearSearch = () => {
    setSearchFilters({});
    setSearchResults([]);
    setHasSearched(false);
    setSearchError(null);
    setTotalResults(0);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Job Opportunities</h1>
          <p className="text-gray-600">
            Discover your next career opportunity or find jobs tailored to your skills
          </p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-md mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 py-4 px-6 text-center font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-b-2 border-blue-600 text-blue-600'
                      : 'text-gray-600 hover:text-gray-900 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path 
                        strokeLinecap={"round" as const} 
                        strokeLinejoin={"round" as const} 
                        strokeWidth={2} 
                        d={tab.icon}
                      />
                    </svg>
                    <span className="hidden sm:inline">{tab.label}</span>
                  </div>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div>
          {activeTab === 'browse' && (
            <div>
              <JobList />
            </div>
          )}

          {activeTab === 'matched' && (
            <div>
              <JobMatcher />
            </div>
          )}

          {activeTab === 'search' && (
            <div className="bg-white rounded-lg shadow-md p-8">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-gray-900">Advanced Job Search</h3>
                {hasSearched && (
                  <button
                    onClick={handleClearSearch}
                    className="text-sm text-gray-600 hover:text-gray-900 flex items-center gap-1"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    Clear & New Search
                  </button>
                )}
              </div>
              
              <div className="space-y-6">
                {/* Search Form */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Keywords
                    </label>
                    <input
                      type="text"
                      value={searchFilters.keywords || ''}
                      onChange={(e) => handleSearchFilterChange('keywords', e.target.value)}
                      placeholder="e.g. Software Engineer, Python, React"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                    <p className="mt-1 text-xs text-gray-500">Search in job titles and descriptions</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Location
                    </label>
                    <input
                      type="text"
                      value={searchFilters.location || ''}
                      onChange={(e) => handleSearchFilterChange('location', e.target.value)}
                      placeholder="e.g. Tunisia, Cairo, Remote"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                    <p className="mt-1 text-xs text-gray-500">City, country, or region</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Job Type
                    </label>
                    <select 
                      value={searchFilters.jobType || ''}
                      onChange={(e) => handleSearchFilterChange('jobType', e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">All Types</option>
                      <option value="Full-time">Full-time</option>
                      <option value="Part-time">Part-time</option>
                      <option value="Contract">Contract</option>
                      <option value="Internship">Internship</option>
                      <option value="Freelance">Freelance</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Experience Level
                    </label>
                    <select 
                      value={searchFilters.experienceLevel || ''}
                      onChange={(e) => handleSearchFilterChange('experienceLevel', e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">All Levels</option>
                      <option value="Junior">Junior</option>
                      <option value="Mid-Level">Mid-Level</option>
                      <option value="Senior">Senior</option>
                      <option value="Lead">Lead</option>
                      <option value="Executive">Executive</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Minimum Salary (USD)
                    </label>
                    <input
                      type="number"
                      value={searchFilters.minSalary || ''}
                      onChange={(e) => handleSearchFilterChange('minSalary', e.target.value)}
                      placeholder="e.g. 50000"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Maximum Salary (USD)
                    </label>
                    <input
                      type="number"
                      value={searchFilters.maxSalary || ''}
                      onChange={(e) => handleSearchFilterChange('maxSalary', e.target.value)}
                      placeholder="e.g. 100000"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Required Skills (comma-separated)
                    </label>
                    <input
                      type="text"
                      value={searchFilters.requiredSkills || ''}
                      onChange={(e) => handleSearchFilterChange('requiredSkills', e.target.value)}
                      placeholder="e.g. Python, React, PostgreSQL, Docker"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                    <p className="mt-1 text-xs text-gray-500">Jobs must have all specified skills</p>
                  </div>
                </div>

                <div className="flex items-center gap-4 pt-2">
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={searchFilters.remoteOnly || false}
                      onChange={(e) => handleSearchFilterChange('remoteOnly', e.target.checked)}
                      className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700 font-medium">Remote only</span>
                  </label>
                </div>

                <button 
                  onClick={handleSearch}
                  disabled={searching}
                  className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {searching ? (
                    <>
                      <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Searching...
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path 
                          strokeLinecap={"round" as const} 
                          strokeLinejoin={"round" as const} 
                          strokeWidth={2} 
                          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                        />
                      </svg>
                      Search Jobs
                    </>
                  )}
                </button>
              </div>

              {/* Search Results */}
              <div className="mt-8 pt-8 border-t border-gray-200">
                {searchError && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                    <p className="text-red-800">{searchError}</p>
                  </div>
                )}

                {hasSearched && !searching && !searchError && (
                  <div className="mb-4">
                    <h4 className="text-lg font-semibold text-gray-900">
                      Search Results
                      <span className="ml-2 text-sm font-normal text-gray-600">
                        ({searchResults.length} {searchResults.length === 1 ? 'job' : 'jobs'} found)
                      </span>
                    </h4>
                  </div>
                )}

                {hasSearched && searchResults.length === 0 && !searching && !searchError && (
                  <div className="text-center py-12">
                    <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                            d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">No jobs found</h3>
                    <p className="text-gray-600 mb-4">
                      Try adjusting your search criteria or broadening your filters.
                    </p>
                  </div>
                )}

                {searchResults.length > 0 && (
                  <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                    {searchResults.map((job) => (
                      <JobCard 
                        key={job.id} 
                        job={job}
                        onViewDetails={(job) => window.open(job.url, '_blank')}
                      />
                    ))}
                  </div>
                )}

                {!hasSearched && (
                  <div className="text-center py-12">
                    <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} 
                            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <p className="text-gray-500">
                      Fill in the search criteria above and click "Search Jobs" to find opportunities
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Compatibility Analyzer Tab */}
          {activeTab === 'compatibility' && (
            <div className="p-6">
              <JobCompatibilityAnalyzer />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default JobsPage;
