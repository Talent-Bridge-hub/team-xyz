import { useState } from 'react';
import InterviewSetup from '../../components/interview/InterviewSetup.tsx';
import InterviewChat from '../../components/interview/InterviewChat.tsx';
import InterviewHistory from '../../components/interview/InterviewHistory.tsx';

type TabType = 'new' | 'active' | 'history';

const InterviewPage = () => {
  const [activeTab, setActiveTab] = useState<TabType>('new');
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);

  const tabs = [
    { 
      id: 'new' as TabType, 
      label: 'New Interview', 
      icon: 'M12 4v16m8-8H4',
      description: 'Start a new practice interview'
    },
    { 
      id: 'active' as TabType, 
      label: 'Active Session', 
      icon: 'M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
      description: 'Continue your current interview',
      badge: activeSessionId ? '1' : null
    },
    { 
      id: 'history' as TabType, 
      label: 'Interview History', 
      icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
      description: 'Review past interviews'
    },
  ];

  const handleSessionStart = (sessionId: number) => {
    setActiveSessionId(sessionId);
    setActiveTab('active');
  };

  const handleSessionComplete = () => {
    setActiveSessionId(null);
    setActiveTab('history');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🎭 AI Interview Simulator
          </h1>
          <p className="text-lg text-gray-600">
            Practice your interview skills with our AI-powered interviewer. Get instant feedback and improve!
          </p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-lg mb-6 overflow-hidden">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`group relative flex-1 py-4 px-6 text-center font-medium text-sm transition-all ${
                    activeTab === tab.id
                      ? 'border-b-2 border-blue-600 text-blue-600 bg-blue-50'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 hover:border-gray-300'
                  }`}
                >
                  <div className="flex flex-col items-center gap-2">
                    <div className="flex items-center gap-2">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path 
                          strokeLinecap="round" 
                          strokeLinejoin="round" 
                          strokeWidth={2} 
                          d={tab.icon}
                        />
                      </svg>
                      <span className="hidden sm:inline">{tab.label}</span>
                      {tab.badge && (
                        <span className="bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                          {tab.badge}
                        </span>
                      )}
                    </div>
                    <span className="text-xs text-gray-500 hidden md:block">
                      {tab.description}
                    </span>
                  </div>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="transition-all duration-300">
          {activeTab === 'new' && (
            <InterviewSetup onSessionStart={handleSessionStart} />
          )}

          {activeTab === 'active' && (
            <InterviewChat 
              sessionId={activeSessionId} 
              onSessionComplete={handleSessionComplete}
            />
          )}

          {activeTab === 'history' && (
            <InterviewHistory onViewSession={(id: number) => {
              setActiveSessionId(id);
              setActiveTab('active');
            }} />
          )}
        </div>
      </div>
    </div>
  );
};

export default InterviewPage;
