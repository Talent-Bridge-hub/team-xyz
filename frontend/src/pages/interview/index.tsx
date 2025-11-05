import { useState } from 'react';
import { motion } from 'framer-motion';
import InterviewSetup from '../../components/interview/InterviewSetup.tsx';
import InterviewChat from '../../components/interview/InterviewChat.tsx';
import InterviewHistory from '../../components/interview/InterviewHistory.tsx';
import { 
  PlusCircleIcon, 
  ChatBubbleLeftRightIcon, 
  ClockIcon 
} from '@heroicons/react/24/outline';

type TabType = 'new' | 'active' | 'history';

const InterviewPage = () => {
  const [activeTab, setActiveTab] = useState<TabType>('new');
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);

  const tabs = [
    { 
      id: 'new' as TabType, 
      label: 'New Interview', 
      Icon: PlusCircleIcon,
      description: 'Start a new practice interview',
      gradient: 'from-electric-cyan to-deep-ocean',
    },
    { 
      id: 'active' as TabType, 
      label: 'Active Session', 
      Icon: ChatBubbleLeftRightIcon,
      description: 'Continue your current interview',
      badge: activeSessionId ? '1' : null,
      gradient: 'from-stellar-purple to-royal-purple',
    },
    { 
      id: 'history' as TabType, 
      label: 'Interview History', 
      Icon: ClockIcon,
      description: 'Review past interviews',
      gradient: 'from-cosmic-gold to-amber-gold',
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
    <div className="relative min-h-screen">
      {/* Particle Background */}
      <div className="fixed inset-0 particle-bg opacity-30 pointer-events-none" />
      
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl sm:text-5xl font-bold mb-3">
            <span className="glow-text">AI Interview Simulator</span>
          </h1>
          <p className="text-lg text-slate-600 dark:text-silver-mist">
            Practice your interview skills with our AI-powered interviewer. Get instant feedback and improve!
          </p>
        </motion.div>

        {/* Tabs */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card rounded-2xl mb-8 overflow-hidden"
        >
          <nav className="flex flex-col sm:flex-row">
            {tabs.map((tab, index) => (
              <motion.button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`group relative flex-1 py-6 px-6 transition-all ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r ' + tab.gradient + ' bg-opacity-20'
                    : 'hover:bg-white/5'
                }`}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {/* Active indicator */}
                {activeTab === tab.id && (
                  <motion.div
                    layoutId="activeTab"
                    className={`absolute inset-0 bg-gradient-to-r ${tab.gradient} opacity-10`}
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
                )}
                
                <div className="relative flex flex-col items-center gap-3">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-xl ${
                      activeTab === tab.id 
                        ? `bg-gradient-to-r ${tab.gradient}` 
                        : 'bg-white/5'
                    } transition-all group-hover:scale-110`}>
                      <tab.Icon className={`w-6 h-6 ${
                        activeTab === tab.id ? 'text-white' : 'text-slate-400 dark:text-silver-mist'
                      }`} />
                    </div>
                    <span className={`font-medium ${
                      activeTab === tab.id 
                        ? 'text-midnight dark:text-white' 
                        : 'text-slate-600 dark:text-silver-mist'
                    }`}>
                      {tab.label}
                    </span>
                    {tab.badge && (
                      <motion.span 
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="bg-gradient-to-r from-red-500 to-pink-500 text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center shadow-glow-purple"
                      >
                        {tab.badge}
                      </motion.span>
                    )}
                  </div>
                  <span className={`text-xs hidden md:block ${
                    activeTab === tab.id 
                      ? 'text-slate-600 dark:text-silver-mist' 
                      : 'text-slate-500 dark:text-slate-400'
                  }`}>
                    {tab.description}
                  </span>
                </div>

                {/* Border indicator */}
                {activeTab === tab.id && (
                  <motion.div
                    layoutId="tabBorder"
                    className={`absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r ${tab.gradient}`}
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
                )}
              </motion.button>
            ))}
          </nav>
        </motion.div>

        {/* Tab Content */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.3 }}
        >
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
        </motion.div>
      </div>
    </div>
  );
};

export default InterviewPage;
