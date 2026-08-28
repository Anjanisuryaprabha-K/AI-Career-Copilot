import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

const navGroups = [
  {
    title: 'Core Analytics',
    items: [
      { path: '/dashboard', label: 'Dashboard Hub', icon: '📊' },
      { path: '/job-readiness', label: 'Job Readiness Index', icon: '🎯' },
      { path: '/skill-radar', label: 'Career Skill Radar', icon: '🎯' },
      { path: '/weakness-detector', label: 'AI Weakness Detector', icon: '🔍' },
      { path: '/analytics', label: 'Deep Analytics', icon: '📈' },
    ]
  },
  {
    title: 'Career & Prep',
    items: [
      { path: '/resume-analyzer', label: 'ATS Resume Scorer', icon: '📄' },
      { path: '/placement-roadmap', label: 'Placement Roadmap', icon: '🗺️' },
      { path: '/study-planner', label: 'AI Study Planner', icon: '📅' },
      { path: '/company-prep', label: 'Company Specific Prep', icon: '🏢' },
      { path: '/skill-gap', label: 'Skill Gap Analyzer', icon: '⚡' },
      { path: '/job-matcher', label: 'Job Role Matcher', icon: '🎯' },
      { path: '/applications', label: 'Application Kanban', icon: '📋' },
      { path: '/company-insights', label: 'Company Archives', icon: '🏛️' },
    ]
  },
  {
    title: 'Practice & AI Mock',
    items: [
      { path: '/interview-simulator', label: 'Mock Interview AI', icon: '🎙️' },
      { path: '/coding-arena', label: 'Coding Arena', icon: '💻' },
      { path: '/gd-simulator', label: 'GD Simulator AI', icon: '🗣️' },
      { path: '/speech-analyzer', label: 'Speech Prosody AI', icon: '🗣️' },
      { path: '/oa-simulator', label: 'Mock OA Exam', icon: '⏱️' },
      { path: '/star-builder', label: 'STAR Method AI', icon: '⭐' },
      { path: '/chat-assistant', label: 'AI Mentor Chat', icon: '🤖' },
    ]
  },
  {
    title: 'Portfolio & Admin',
    items: [
      { path: '/coding-tracker', label: 'Coding Tracker', icon: '⚡' },
      { path: '/github-analyzer', label: 'GitHub Scorer', icon: '🐙' },
      { path: '/cover-letter', label: 'Cover Letter AI', icon: '✍️' },
      { path: '/linkedin-optimizer', label: 'LinkedIn Optimizer', icon: '💼' },
      { path: '/portfolio-builder', label: 'Portfolio Builder', icon: '🌐' },
      { path: '/resume-export', label: 'LaTeX Exporter', icon: '📑' },
      { path: '/admin-portal', label: 'Placement Admin', icon: '🏛️' },
    ]
  }
];

const Sidebar = ({ isMobileOpen, onCloseMobile }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const sidebarContent = (
    <div className="flex flex-col h-full justify-between">
      <div className="space-y-4 overflow-y-auto max-h-[calc(100vh-10rem)] pr-1">
        {/* Toggle Collapse Button (Desktop Only) */}
        <div className="hidden md:flex justify-end mb-1">
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-indigo-50 dark:hover:bg-slate-800 transition"
            title={isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
          >
            <span className="text-xs">{isCollapsed ? '⏩' : '⏪'}</span>
          </button>
        </div>

        {navGroups.map((group, idx) => (
          <div key={idx}>
            {!isCollapsed && (
              <p className="text-[10px] font-extrabold uppercase tracking-wider text-slate-400 dark:text-slate-500 px-3 mb-1.5">
                {group.title}
              </p>
            )}
            <div className="space-y-1">
              {group.items.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => onCloseMobile && onCloseMobile()}
                  title={isCollapsed ? item.label : undefined}
                  className={({ isActive }) =>
                    `sidebar-link-smooth group flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-semibold ${
                      isActive
                        ? 'bg-[#EEF2FF] dark:bg-[#1E1B2E] text-[#4F46E5] dark:text-[#6366F1] border-l-4 border-l-[#4F46E5] dark:border-l-[#6366F1] font-bold shadow-xs'
                        : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-[#EEF2FF]/60 dark:hover:bg-[#1E1B2E]/60'
                    } ${isCollapsed ? 'justify-center px-2' : ''}`
                  }
                >
                  <span className="sidebar-icon text-base shrink-0">{item.icon}</span>
                  {!isCollapsed && <span className="truncate">{item.label}</span>}
                </NavLink>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Footer Banner */}
      {!isCollapsed && (
        <div className="mt-4 p-3 rounded-xl bg-[#EEF2FF]/80 dark:bg-[#1E1B2E] border border-indigo-100 dark:border-indigo-900/30 text-center">
          <p className="text-xs font-bold text-slate-900 dark:text-slate-100">Placement Mode</p>
          <p className="text-[10px] text-[#4F46E5] dark:text-[#6366F1] font-bold mt-0.5">Tier 1 Target (₹18-28 LPA)</p>
        </div>
      )}
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside
        className={`border-r border-slate-200 dark:border-slate-800/80 bg-white dark:bg-[#151522] p-3 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-4rem)] sticky top-16 transition-all duration-300 ${
          isCollapsed ? 'w-16' : 'w-64'
        }`}
      >
        {sidebarContent}
      </aside>

      {/* Mobile Drawer Backdrop & Drawer */}
      {isMobileOpen && (
        <div className="fixed inset-0 z-40 md:hidden flex">
          <div
            className="fixed inset-0 bg-slate-950/60 backdrop-blur-sm"
            onClick={onCloseMobile}
          />
          <aside className="relative w-64 max-w-xs bg-white dark:bg-[#151522] border-r border-slate-200 dark:border-slate-800 p-4 flex flex-col justify-between z-50 h-full">
            <div className="flex items-center justify-between mb-4">
              <span className="font-bold text-slate-900 dark:text-slate-100 text-sm">Navigation</span>
              <button
                onClick={onCloseMobile}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                ✕
              </button>
            </div>
            {sidebarContent}
          </aside>
        </div>
      )}
    </>
  );
};

export default Sidebar;
