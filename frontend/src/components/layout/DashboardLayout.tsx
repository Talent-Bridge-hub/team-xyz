import { useState } from 'react';
import type { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { ThemeToggle } from '../common/ThemeToggle';
import { Logo } from '../common/Logo';

interface DashboardLayoutProps {
  children: ReactNode;
}

export const DashboardLayout = ({ children }: DashboardLayoutProps) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
    { name: 'Resume', href: '/dashboard/resume', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
    { name: 'Jobs', href: '/dashboard/jobs', icon: 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
    { name: 'Interview', href: '/dashboard/interview', icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z' },
    { name: 'Footprint', href: '/dashboard/footprint', icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' },
  ];

  return (
    <div className="h-screen flex overflow-hidden bg-pearl-white dark:bg-space-navy transition-colors">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 bg-gray-600 bg-opacity-75 z-20 md:hidden"
            onClick={() => setSidebarOpen(false)}
          />
          
          {/* Mobile sidebar */}
          <div className="fixed inset-y-0 left-0 flex flex-col w-64 glass-card border-r border-electric-cyan/20 z-30 md:hidden">
            <div className="flex items-center justify-between flex-shrink-0 px-4 pt-5 pb-4 border-b border-gray-200 dark:border-gray-700">
              <Logo variant="compact" />
              <button
                type="button"
                className="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
                onClick={() => setSidebarOpen(false)}
              >
                <span className="sr-only">Close sidebar</span>
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="mt-5 flex-grow flex flex-col overflow-y-auto">
              <nav className="flex-1 px-2 space-y-1">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      onClick={() => setSidebarOpen(false)}
                      className={`${
                        isActive
                          ? 'bg-gradient-to-r from-electric-cyan/20 to-stellar-purple/20 text-electric-cyan border-l-2 border-electric-cyan'
                          : 'text-slate-600 dark:text-silver-mist hover:bg-electric-cyan/10 hover:text-electric-cyan'
                      } group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-all`}
                    >
                      <svg
                        className={`${
                          isActive ? 'text-electric-cyan' : 'text-slate-400 dark:text-silver-mist group-hover:text-electric-cyan'
                        } mr-3 flex-shrink-0 h-6 w-6 transition-colors`}
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={item.icon} />
                      </svg>
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </div>
          </div>
        </>
      )}

      {/* Desktop Sidebar */}
      <div className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64">
          <div className="flex flex-col flex-grow pt-5 pb-4 overflow-y-auto glass-card border-r border-electric-cyan/20">
            <div className="flex items-center flex-shrink-0 px-4 pb-4 border-b border-gray-200 dark:border-gray-700">
              <Logo variant="compact" />
            </div>
                        <div className="mt-5 flex-grow flex flex-col">
              <nav className="flex-1 px-2 space-y-1">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`${
                        isActive
                          ? 'bg-gradient-to-r from-electric-cyan/20 to-stellar-purple/20 text-electric-cyan border-l-2 border-electric-cyan'
                          : 'text-slate-600 dark:text-silver-mist hover:bg-electric-cyan/10 hover:text-electric-cyan'
                      } group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-all`}
                    >
                      <svg
                        className={`${
                          isActive ? 'text-electric-cyan' : 'text-slate-400 dark:text-silver-mist group-hover:text-electric-cyan'
                        } mr-3 flex-shrink-0 h-6 w-6 transition-colors`}
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} d={item.icon} />
                      </svg>
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex flex-col w-0 flex-1 overflow-hidden">
        {/* Top bar */}
        <div className="relative z-10 flex-shrink-0 flex h-16 glass-card shadow-lg">
          <button
            type={"button" as const}
            className="px-4 border-r border-electric-cyan/20 text-slate-500 dark:text-silver-mist hover:text-electric-cyan focus:outline-none focus:ring-2 focus:ring-inset focus:ring-electric-cyan md:hidden transition-colors"
            onClick={() => setSidebarOpen(true)}
          >
            <span className="sr-only">Open sidebar</span>
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap={"round" as const} strokeLinejoin={"round" as const} strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div className="flex-1 px-4 flex justify-between">
            <div className="flex-1 flex">
              {/* Search can go here */}
            </div>
            <div className="ml-4 flex items-center md:ml-6 gap-4">
              <ThemeToggle />
              <div className="ml-3 relative">
                <div className="flex items-center space-x-3">
                  <span className="text-sm font-medium text-gray-700 dark:text-silver-mist">{user?.full_name}</span>
                  <button
                    onClick={logout}
                    className="text-sm text-gray-500 hover:text-gray-700 dark:text-silver-mist dark:hover:text-white transition-colors"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="flex-1 relative overflow-y-auto focus:outline-none">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};
