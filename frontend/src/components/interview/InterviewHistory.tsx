import { useState, useEffect } from 'react';
import { interviewService } from '../../services/interview.service.ts';
import { useToast } from '../../contexts/ToastContext';
import { SkeletonCard } from '../common/Skeleton';

interface SessionListItem {
  id: number;  // Changed from session_id to id
  job_role: string;
  session_type: string;
  difficulty_level: string;
  total_questions: number;
  questions_answered: number;
  average_score: number | null;  // Can be null if not completed
  status: string;
  started_at: string;  // Changed from created_at to started_at
  completed_at: string | null;
}

interface InterviewHistoryProps {
  onViewSession: (sessionId: number) => void;
}

const InterviewHistory = ({ onViewSession }: InterviewHistoryProps) => {
  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSession, setSelectedSession] = useState<any>(null);
  const [showDetails, setShowDetails] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState<number | null>(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const { showSuccess, showError } = useToast();

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await interviewService.listSessions();
      setSessions(data.sessions || []);
    } catch (err: any) {
      console.error('Error loading sessions:', err);
      setError(err.response?.data?.detail || 'Failed to load interview history');
    } finally {
      setLoading(false);
    }
  };

  const loadSessionDetails = async (sessionId: number) => {
    try {
      console.log(`[HISTORY] Loading session details for session ${sessionId}`);
      setError(null);
      setDetailsLoading(true);
      const details = await interviewService.getSessionDetails(sessionId);
      console.log('[HISTORY] Session details loaded:', details);
      setSelectedSession(details);
      setShowDetails(true);
      console.log('[HISTORY] Modal should now be visible');
    } catch (err: any) {
      console.error('[HISTORY] Error loading session details:', err);
      console.error('[HISTORY] Error response:', err.response);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to load session details';
      setError(errorMessage);
      showError(`Error loading report: ${errorMessage}`);
    } finally {
      setDetailsLoading(false);
    }
  };

  const handleDeleteSession = async (sessionId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    
    if (!window.confirm('Are you sure you want to delete this interview session? This action cannot be undone.')) {
      return;
    }

    try {
      setDeleteLoading(sessionId);
      setError(null);
      const result = await interviewService.deleteSession(sessionId);
      console.log('Delete result:', result);
      
      // Remove from local state
      setSessions(sessions.filter(s => s.id !== sessionId));
      
      // Close details modal if it's open for this session
      if (selectedSession && (selectedSession.session_id === sessionId || selectedSession.id === sessionId)) {
        setShowDetails(false);
        setSelectedSession(null);
      }
      
      // Show success message
      showSuccess('Interview session deleted successfully!');
    } catch (err: any) {
      console.error('Error deleting session:', err);
      console.error('Error response:', err.response);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to delete session';
      setError(errorMessage);
      showError(`Error: ${errorMessage}`);
    } finally {
      setDeleteLoading(null);
    }
  };

  const getStatusBadge = (status: string) => {
    const styles = {
      in_progress: 'bg-green-100 text-green-800',
      completed: 'bg-blue-100 text-blue-800',
      cancelled: 'bg-gray-100 text-gray-800',
    };
    
    const labels = {
      in_progress: 'In Progress',
      completed: 'Completed',
      cancelled: 'Cancelled',
    };
    
    return (
      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${styles[status as keyof typeof styles]}`}>
        {labels[status as keyof typeof labels] || status}
      </span>
    );
  };

  const getScoreColor = (score: number): string => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreEmoji = (score: number): string => {
    if (score >= 90) return '🌟';
    if (score >= 80) return '✨';
    if (score >= 70) return '👍';
    if (score >= 60) return '👌';
    return '📝';
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const getDuration = (start: string, end: string | null): string => {
    if (!end) return 'In progress';
    const startDate = new Date(start);
    const endDate = new Date(end);
    const durationMs = endDate.getTime() - startDate.getTime();
    const minutes = Math.floor(durationMs / 60000);
    const seconds = Math.floor((durationMs % 60000) / 1000);
    return `${minutes}m ${seconds}s`;
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        {/* Stats Overview Skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
              <div className="animate-pulse flex items-center gap-3">
                <div className="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded-lg" />
                <div className="flex-1 space-y-2">
                  <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-20" />
                  <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-12" />
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Sessions List Skeleton */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-gray-700">
            <div className="animate-pulse space-y-2">
              <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-48" />
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-64" />
            </div>
          </div>
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="p-6">
                <div className="animate-pulse space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1 space-y-3">
                      <div className="flex items-center gap-3">
                        <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-48" />
                        <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-20" />
                      </div>
                      <div className="flex gap-4">
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24" />
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24" />
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-32" />
                      </div>
                      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-64" />
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="h-16 w-16 bg-gray-200 dark:bg-gray-700 rounded" />
                      <div className="h-10 w-32 bg-gray-200 dark:bg-gray-700 rounded-lg" />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error && !sessions.length) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-6">
        <div className="flex items-center gap-3">
          <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 className="font-semibold text-red-900">Error Loading History</h3>
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (sessions.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-12 text-center">
        <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No Interview History</h3>
        <p className="text-gray-600 mb-6">
          You haven't completed any interviews yet. Start your first interview to build your history.
        </p>
        <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold">
          Start First Interview
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Sessions</p>
              <p className="text-2xl font-bold text-gray-900">{sessions.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-gray-900">
                {sessions.filter(s => s.status === 'completed').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-600">Avg Score</p>
              <p className="text-2xl font-bold text-gray-900">
                {sessions.filter(s => s.status === 'completed' && s.average_score !== null).length > 0
                  ? Math.round(
                      sessions
                        .filter(s => s.status === 'completed' && s.average_score !== null)
                        .reduce((sum, s) => sum + (s.average_score || 0), 0) /
                        sessions.filter(s => s.status === 'completed' && s.average_score !== null).length
                    )
                  : 0}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p className="text-sm text-gray-600">In Progress</p>
              <p className="text-2xl font-bold text-gray-900">
                {sessions.filter(s => s.status === 'in_progress').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Sessions List */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Interview History</h2>
          <p className="text-sm text-gray-600 mt-1">View and analyze your past interview sessions</p>
        </div>

        <div className="divide-y divide-gray-200">
          {sessions.map((session) => (
            <div
              key={session.id}
              className="p-6 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{session.job_role}</h3>
                    {getStatusBadge(session.status)}
                  </div>

                  <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-3">
                    <span className="flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                              d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                      </svg>
                      {session.session_type}
                    </span>
                    <span className="flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      {session.difficulty_level}
                    </span>
                    <span className="flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                              d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {session.questions_answered}/{session.total_questions} questions
                    </span>
                    <span className="flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {getDuration(session.started_at, session.completed_at)}
                    </span>
                  </div>

                  <p className="text-sm text-gray-500">
                    Started: {formatDate(session.started_at)}
                    {session.completed_at && ` • Completed: ${formatDate(session.completed_at)}`}
                  </p>
                </div>

                <div className="flex items-center gap-3 ml-6">
                  {session.status === 'completed' && session.average_score !== null && (
                    <div className="text-right">
                      <div className={`text-3xl font-bold ${getScoreColor(session.average_score)}`}>
                        {getScoreEmoji(session.average_score)} {session.average_score}
                      </div>
                      <p className="text-sm text-gray-600">Average Score</p>
                    </div>
                  )}

                  {session.status === 'completed' && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        loadSessionDetails(session.id);
                      }}
                      disabled={detailsLoading}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold text-sm flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                      title="View detailed report"
                    >
                      {detailsLoading ? (
                        <>
                          <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Loading...
                        </>
                      ) : (
                        <>
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          View Report
                        </>
                      )}
                    </button>
                  )}

                  {session.status === 'in_progress' && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onViewSession(session.id);
                      }}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-semibold text-sm flex items-center gap-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Continue Interview
                    </button>
                  )}

                  <button
                    onClick={(e) => handleDeleteSession(session.id, e)}
                    disabled={deleteLoading === session.id}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
                    title="Delete session"
                  >
                    {deleteLoading === session.id ? (
                      <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Session Details Modal */}
      {showDetails && selectedSession && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">{selectedSession.job_role}</h2>
              <button
                onClick={() => setShowDetails(false)}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="p-6">
              {/* Session Info */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Type</p>
                  <p className="font-semibold text-gray-900">{selectedSession.session_type}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Difficulty</p>
                  <p className="font-semibold text-gray-900">{selectedSession.difficulty_level}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Questions</p>
                  <p className="font-semibold text-gray-900">
                    {selectedSession.questions_answered}/{selectedSession.total_questions}
                  </p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-1">Avg Score</p>
                  <p className={`font-semibold text-xl ${selectedSession.average_scores ? getScoreColor(selectedSession.average_scores.overall) : 'text-gray-400'}`}>
                    {selectedSession.average_scores ? Math.round(selectedSession.average_scores.overall) : 'N/A'}
                  </p>
                </div>
              </div>

              {/* Questions & Answers */}
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Questions & Answers</h3>
              
              {!selectedSession.questions_and_answers || selectedSession.questions_and_answers.length === 0 ? (
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
                  <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-gray-600">No questions answered yet</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {selectedSession.questions_and_answers.map((qa: any, index: number) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-5">
                      <div className="flex items-start justify-between mb-3">
                        <h4 className="font-semibold text-gray-900">Question {qa.question_number}</h4>
                        {qa.scores && (
                          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getScoreColor(qa.scores.overall)}`}>
                            {getScoreEmoji(qa.scores.overall)} {Math.round(qa.scores.overall)}/100
                          </span>
                        )}
                      </div>
                      
                      <div className="mb-4">
                        <p className="text-gray-700 whitespace-pre-wrap">{qa.question_text}</p>
                      </div>
                      
                      {qa.user_answer ? (
                        <>
                          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-4">
                            <p className="text-sm font-medium text-gray-700 mb-1">Your Answer:</p>
                            <p className="text-gray-800 whitespace-pre-wrap">{qa.user_answer}</p>
                          </div>

                          {qa.feedback && (
                            <div className="space-y-3">
                              {qa.feedback.strengths?.length > 0 && (
                                <div>
                                  <p className="text-sm font-semibold text-green-700 mb-1">✅ Strengths:</p>
                                  <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                                    {qa.feedback.strengths.map((s: string, i: number) => (
                                      <li key={i}>{s}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}

                              {qa.feedback.weaknesses?.length > 0 && (
                                <div>
                                  <p className="text-sm font-semibold text-yellow-700 mb-1">⚠️ Areas to Improve:</p>
                                  <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                                    {qa.feedback.weaknesses.map((w: string, i: number) => (
                                      <li key={i}>{w}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}

                              {qa.feedback.suggestions?.length > 0 && (
                                <div>
                                  <p className="text-sm font-semibold text-blue-700 mb-1">💡 Suggestions:</p>
                                  <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
                                    {qa.feedback.suggestions.map((s: string, i: number) => (
                                      <li key={i}>{s}</li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </div>
                          )}
                        </>
                      ) : (
                        <div className="bg-gray-50 border border-gray-300 rounded p-4">
                          <p className="text-sm text-gray-600 italic">Not answered yet</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {/* Overall Session Feedback / BILAN */}
              {selectedSession.status === 'completed' && selectedSession.feedback && (
                <div className="mt-8 border-t border-gray-200 pt-6">
                  <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Overall Assessment (BILAN)
                  </h3>

                  {/* Performance Summary */}
                  {selectedSession.average_scores && (
                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 mb-6">
                      <h4 className="text-lg font-semibold text-gray-900 mb-4">Performance Breakdown</h4>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        <div className="bg-white rounded-lg p-3 text-center">
                          <p className="text-sm text-gray-600 mb-1">Overall</p>
                          <p className={`text-2xl font-bold ${getScoreColor(selectedSession.average_scores.overall)}`}>
                            {Math.round(selectedSession.average_scores.overall)}%
                          </p>
                        </div>
                        <div className="bg-white rounded-lg p-3 text-center">
                          <p className="text-sm text-gray-600 mb-1">Relevance</p>
                          <p className={`text-2xl font-bold ${getScoreColor(selectedSession.average_scores.relevance)}`}>
                            {Math.round(selectedSession.average_scores.relevance)}%
                          </p>
                        </div>
                        <div className="bg-white rounded-lg p-3 text-center">
                          <p className="text-sm text-gray-600 mb-1">Completeness</p>
                          <p className={`text-2xl font-bold ${getScoreColor(selectedSession.average_scores.completeness)}`}>
                            {Math.round(selectedSession.average_scores.completeness)}%
                          </p>
                        </div>
                        <div className="bg-white rounded-lg p-3 text-center">
                          <p className="text-sm text-gray-600 mb-1">Clarity</p>
                          <p className={`text-2xl font-bold ${getScoreColor(selectedSession.average_scores.clarity)}`}>
                            {Math.round(selectedSession.average_scores.clarity)}%
                          </p>
                        </div>
                        <div className="bg-white rounded-lg p-3 text-center">
                          <p className="text-sm text-gray-600 mb-1">Technical</p>
                          <p className={`text-2xl font-bold ${getScoreColor(selectedSession.average_scores.technical_accuracy)}`}>
                            {Math.round(selectedSession.average_scores.technical_accuracy)}%
                          </p>
                        </div>
                        <div className="bg-white rounded-lg p-3 text-center">
                          <p className="text-sm text-gray-600 mb-1">Communication</p>
                          <p className={`text-2xl font-bold ${getScoreColor(selectedSession.average_scores.communication)}`}>
                            {Math.round(selectedSession.average_scores.communication)}%
                          </p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Strengths */}
                  {selectedSession.feedback.strengths && selectedSession.feedback.strengths.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-green-700 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Key Strengths
                      </h4>
                      <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded-r-lg">
                        <ul className="space-y-2">
                          {selectedSession.feedback.strengths.map((strength: string, i: number) => (
                            <li key={i} className="flex items-start gap-2">
                              <span className="text-green-600 mt-1">✓</span>
                              <span className="text-gray-700">{strength}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {/* Areas to Improve */}
                  {selectedSession.feedback.areas_to_improve && selectedSession.feedback.areas_to_improve.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-yellow-700 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        Areas for Improvement
                      </h4>
                      <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded-r-lg">
                        <ul className="space-y-2">
                          {selectedSession.feedback.areas_to_improve.map((area: string, i: number) => (
                            <li key={i} className="flex items-start gap-2">
                              <span className="text-yellow-600 mt-1">→</span>
                              <span className="text-gray-700">{area}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {/* Recommended Resources */}
                  {selectedSession.feedback.recommended_resources && selectedSession.feedback.recommended_resources.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-purple-700 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                        Recommended Resources
                      </h4>
                      <div className="bg-purple-50 border-l-4 border-purple-500 p-4 rounded-r-lg">
                        <ul className="space-y-2">
                          {selectedSession.feedback.recommended_resources.map((resource: string, i: number) => (
                            <li key={i} className="flex items-start gap-2">
                              <span className="text-purple-600 mt-1">📚</span>
                              <span className="text-gray-700">{resource}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {/* Preparation Tips */}
                  {selectedSession.feedback.preparation_tips && (
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-blue-700 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        Preparation Tips
                      </h4>
                      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg">
                        <p className="text-gray-700 whitespace-pre-wrap">{selectedSession.feedback.preparation_tips}</p>
                      </div>
                    </div>
                  )}

                  {/* Practice Recommendations */}
                  {selectedSession.feedback.practice_recommendations && (
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-indigo-700 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        Practice Recommendations
                      </h4>
                      <div className="bg-indigo-50 border-l-4 border-indigo-500 p-4 rounded-r-lg">
                        <p className="text-gray-700 whitespace-pre-wrap">{selectedSession.feedback.practice_recommendations}</p>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InterviewHistory;
