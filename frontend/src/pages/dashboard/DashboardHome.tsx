import { Link } from 'react-router-dom';
import {
  DocumentTextIcon,
  BriefcaseIcon,
  ChatBubbleBottomCenterTextIcon,
  ChartBarIcon,
  SparklesIcon,
  RocketLaunchIcon,
} from '@heroicons/react/24/outline';
import { useAuth } from '../../contexts/AuthContext';

export const DashboardHome = () => {
  const { user } = useAuth();
  
  const features = [
    {
      name: 'Resume Analyzer',
      description: 'AI-powered resume analysis and enhancement with real-time feedback',
      icon: DocumentTextIcon,
      href: '/dashboard/resume',
      color: 'blue',
    },
    {
      name: 'Job Matcher',
      description: 'Find your perfect job match with advanced AI compatibility analysis',
      icon: BriefcaseIcon,
      href: '/dashboard/jobs',
      color: 'purple',
    },
    {
      name: 'Interview Simulator',
      description: 'Practice interviews with AI-powered feedback and improvement tips',
      icon: ChatBubbleBottomCenterTextIcon,
      href: '/dashboard/interview',
      color: 'green',
    },
    {
      name: 'Digital Footprint',
      description: 'Scan and analyze your online professional presence across platforms',
      icon: ChartBarIcon,
      href: '/dashboard/footprint',
      color: 'orange',
    },
  ];

  const quickActions = [
    { name: 'Upload Resume', icon: RocketLaunchIcon, href: '/dashboard/resume' },
    { name: 'Browse Jobs', icon: SparklesIcon, href: '/dashboard/jobs' },
    { name: 'Start Interview', icon: ChatBubbleBottomCenterTextIcon, href: '/dashboard/interview' },
  ];

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  const getColorClasses = (color: string) => {
    const colors = {
      blue: {
        bg: 'bg-blue-100 dark:bg-blue-900/20',
        icon: 'bg-blue-500',
        hover: 'hover:border-blue-500',
      },
      purple: {
        bg: 'bg-purple-100 dark:bg-purple-900/20',
        icon: 'bg-purple-500',
        hover: 'hover:border-purple-500',
      },
      green: {
        bg: 'bg-green-100 dark:bg-green-900/20',
        icon: 'bg-green-500',
        hover: 'hover:border-green-500',
      },
      orange: {
        bg: 'bg-orange-100 dark:bg-orange-900/20',
        icon: 'bg-orange-500',
        hover: 'hover:border-orange-500',
      },
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-white dark:bg-slate-800 rounded-lg p-8 sm:p-12 shadow-md">
        <h1 className="text-4xl sm:text-5xl font-bold mb-4 text-slate-900 dark:text-white">
          {getGreeting()}, {user?.full_name || 'User'}!
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl">
          Welcome to your career command center. Leverage AI-powered tools to accelerate your professional journey.
        </p>
      </div>

      {/* Feature Cards Grid */}
      <div>
        <h2 className="text-2xl font-bold mb-6 text-slate-900 dark:text-white">
          Your Career Tools
        </h2>
        
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => {
            const colorClasses = getColorClasses(feature.color);
            return (
              <Link
                key={feature.name}
                to={feature.href}
                className="group"
              >
                <div className={`bg-white dark:bg-slate-800 rounded-lg p-6 shadow-md border-2 border-transparent ${colorClasses.hover} transition-all duration-300 hover:shadow-lg`}>
                  {/* Icon */}
                  <div className={`inline-flex p-3 rounded-lg ${colorClasses.icon} mb-4`}>
                    <feature.icon className="h-6 w-6 text-white" />
                  </div>
                  
                  {/* Content */}
                  <h3 className="text-lg font-bold mb-2 text-slate-900 dark:text-white">
                    {feature.name}
                  </h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    {feature.description}
                  </p>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-2xl font-bold mb-6 text-slate-900 dark:text-white">
          Quick Actions
        </h2>
        
        <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-md">
          <div className="flex flex-wrap gap-4">
            {quickActions.map((action) => (
              <Link
                key={action.name}
                to={action.href}
              >
                <button className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium shadow-md transition-all duration-300">
                  <action.icon className="h-5 w-5 text-white" />
                  {action.name}
                </button>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
