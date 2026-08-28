import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { useUserProfile } from '../contexts/UserProfileContext';
import { PageHeader, AnimatedProgressBar } from '../components/common/DesignSystemComponents';

// SVG Icons
const PlayIcon = () => (
  <svg className="w-4 h-4 text-rose-500 fill-rose-500" viewBox="0 0 24 24">
    <path d="M8 5v14l11-7z" />
  </svg>
);

const ExternalLinkIcon = () => (
  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
  </svg>
);

const BookmarkIcon = ({ filled }) => (
  <svg className={`w-4 h-4 ${filled ? 'text-amber-500 fill-amber-500' : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-200'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
  </svg>
);

const SearchIcon = () => (
  <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
);

const PlacementRoadmapTracker = () => {
  const { detectedRole } = useUserProfile();

  // Active Tab: 'topics' (Technical Learning) vs 'adaptive' (Adaptive Career Roadmap) vs 'bookmarks' (Saved Resources)
  const [activeMainTab, setActiveMainTab] = useState('topics');

  // ==========================================
  // TECHNICAL LEARNING TOPICS STATE
  // ==========================================
  const [topicsData, setTopicsData] = useState(null);
  const [loadingTopics, setLoadingTopics] = useState(true);
  const [selectedTopicId, setSelectedTopicId] = useState(null);
  const [selectedTopicDetail, setSelectedTopicDetail] = useState(null);
  const [loadingTopicDetail, setLoadingTopicDetail] = useState(false);

  // Search & Filter state
  const [topicSearchInput, setTopicSearchInput] = useState('');
  const [activeSearchQuery, setActiveSearchQuery] = useState('');
  const [topicCatFilter, setTopicCatFilter] = useState('all');
  const [topicStatusFilter, setTopicStatusFilter] = useState('all'); // Default: All Statuses
  const [bookmarksList, setBookmarksList] = useState([]);

  // Ref for scrolling to continue learning target
  const subtopicRefs = useRef({});

  // ==========================================
  // ADAPTIVE CAREER ROADMAP STATE
  // ==========================================
  const [adaptiveData, setAdaptiveData] = useState(null);
  const [rolesOptions, setRolesOptions] = useState({
    supported_roles: [
      "Software Engineer", "Full Stack Developer", "Frontend Developer", "Backend Developer",
      "Java Developer", "Python Developer", "Data Engineer", "Data Scientist",
      "Machine Learning Engineer", "DevOps Engineer", "Cloud Engineer"
    ],
    experience_levels: ["Entry Level / Fresh Grad", "Mid Level (2-4 Yrs)", "Senior Level (5+ Yrs)"],
    company_types: ["MAANG / Tier-1 Product", "Mid-Size Product", "Startup / Service-Based"],
    prep_timeframes: [2, 4, 8, 12],
    skill_levels: ["Beginner", "Intermediate", "Advanced"]
  });

  const [configForm, setConfigForm] = useState({
    target_role: detectedRole || "Software Engineer",
    experience_level: "Entry Level / Fresh Grad",
    company_type: "MAANG / Tier-1 Product",
    prep_time_weeks: 4,
    skill_level: "Intermediate"
  });

  const [loadingAdaptive, setLoadingAdaptive] = useState(true);
  const [recalculating, setRecalculating] = useState(false);
  const [savingConfig, setSavingConfig] = useState(false);

  // Fetch Topics Catalog
  const loadTopicsCatalog = async () => {
    setLoadingTopics(true);
    try {
      const res = await api.skills.getTechnicalTopics();
      if (res?.topics) {
        setTopicsData(res);
      }
    } catch (err) {
      console.error('Error loading technical topics catalog:', err);
    } finally {
      setLoadingTopics(false);
    }
  };

  // Fetch Saved Bookmarks
  const loadBookmarks = async () => {
    try {
      const res = await api.roadmap.getBookmarks();
      if (res?.bookmarks) {
        setBookmarksList(res.bookmarks);
      }
    } catch (err) {
      console.error('Error loading bookmarks:', err);
    }
  };

  // Fetch Single Topic Detail View
  const loadTopicDetail = async (tId) => {
    setSelectedTopicId(tId);
    setLoadingTopicDetail(true);
    try {
      const res = await api.skills.getTechnicalTopicDetail(tId);
      if (res?.topic) {
        setSelectedTopicDetail(res.topic);
      }
    } catch (err) {
      console.error(`Error loading topic detail for '${tId}':`, err);
    } finally {
      setLoadingTopicDetail(false);
    }
  };

  // Fetch Adaptive Roadmap initial
  useEffect(() => {
    const fetchAdaptiveInitial = async () => {
      setLoadingAdaptive(true);
      try {
        const rolesRes = await api.roadmap.getAdaptiveRoles();
        if (rolesRes?.supported_roles) {
          setRolesOptions(rolesRes);
        }
        const res = await api.roadmap.getAdaptive();
        if (res?.roadmap) {
          setAdaptiveData(res.roadmap);
          if (res.roadmap.config) {
            setConfigForm(res.roadmap.config);
          }
        }
      } catch (err) {
        console.error('Error fetching adaptive roadmap:', err);
      } finally {
        setLoadingAdaptive(false);
      }
    };
    fetchAdaptiveInitial();
    loadTopicsCatalog();
    loadBookmarks();
  }, []);

  // Handle Search Submission
  const handleSearchSubmit = (e) => {
    if (e) e.preventDefault();
    setActiveSearchQuery(topicSearchInput.trim());
  };

  const handleClearFilters = () => {
    setTopicSearchInput('');
    setActiveSearchQuery('');
    setTopicCatFilter('all');
    setTopicStatusFilter('all');
  };

  // Handle Explicit Status Change for Subtopic Resource
  const handleSetResourceStatus = async (resourceId, newStatus, topicName) => {
    if (selectedTopicDetail) {
      const updatedResources = selectedTopicDetail.resources.map(r => {
        if (r.id === resourceId) {
          return { ...r, completion_status: newStatus };
        }
        return r;
      });

      const totalRes = updatedResources.length;
      const completedRes = updatedResources.filter(r => r.completion_status === 'completed').length;
      const inProgressRes = updatedResources.filter(r => r.completion_status === 'in_progress').length;
      const newPct = Math.round((completedRes / Math.max(1, totalRes)) * 100);
      const firstIncomplete = updatedResources.find(r => r.completion_status !== 'completed');

      setSelectedTopicDetail({
        ...selectedTopicDetail,
        resources: updatedResources,
        completed_videos_count: completedRes,
        in_progress_videos_count: inProgressRes,
        remaining_videos_count: Math.max(0, totalRes - completedRes),
        progress_percentage: newPct,
        is_completed: completedRes === totalRes && totalRes > 0,
        continue_learning_resource: firstIncomplete || updatedResources[0]
      });
    }

    try {
      await api.skills.setTopicResourceProgress(resourceId, newStatus, topicName || "General");
      // Background sync catalog progress metrics
      loadTopicsCatalog();
    } catch (err) {
      console.error('Failed to update resource status:', err);
    }
  };

  // Handle Bookmark Toggle
  const handleToggleBookmark = async (resource) => {
    const isBookmarked = resource.is_bookmarked;
    if (selectedTopicDetail) {
      const updatedResources = selectedTopicDetail.resources.map(r => {
        if (r.id === resource.id) {
          return { ...r, is_bookmarked: !isBookmarked };
        }
        return r;
      });
      setSelectedTopicDetail({ ...selectedTopicDetail, resources: updatedResources });
    }

    try {
      if (isBookmarked) {
        await api.roadmap.unbookmarkResource(resource.id);
      } else {
        await api.roadmap.bookmarkResource(resource.id, resource);
      }
      loadBookmarks();
    } catch (err) {
      console.error('Error toggling bookmark:', err);
    }
  };

  // Handle Continue Learning Scroll & Focus
  const handleContinueLearningClick = (targetResId) => {
    if (subtopicRefs.current[targetResId]) {
      subtopicRefs.current[targetResId].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  // Filtered Topics List logic
  const filteredTopics = (topicsData?.topics || []).filter(topic => {
    // 1. Category Filter
    if (topicCatFilter !== 'all') {
      const catLower = topicCatFilter.toLowerCase();
      const topicCatLower = (topic.category || '').toLowerCase();
      if (!topicCatLower.includes(catLower) && catLower !== 'all') return false;
    }

    // 2. Status Filter
    if (topicStatusFilter === 'completed' && !topic.is_completed) return false;
    if (topicStatusFilter === 'in_progress' && (topic.completed_videos_count === 0 || topic.is_completed)) return false;
    if (topicStatusFilter === 'not_started' && topic.completed_videos_count > 0) return false;

    // 3. Search Query Filter
    if (activeSearchQuery) {
      const q = activeSearchQuery.toLowerCase();
      const titleMatch = (topic.title || '').toLowerCase().includes(q);
      const fullTitleMatch = (topic.full_title || '').toLowerCase().includes(q);
      const descMatch = (topic.description || '').toLowerCase().includes(q);
      const tagMatch = (topic.tags || []).some(t => t.toLowerCase().includes(q));
      const seqMatch = (topic.sequence || []).some(s => s.toLowerCase().includes(q));
      if (!titleMatch && !fullTitleMatch && !descMatch && !tagMatch && !seqMatch) return false;
    }

    return true;
  });

  // Category Icon / Pill List
  const categoryPills = [
    { id: "all", name: "All Categories", icon: "📚" },
    { id: "dsa", name: "DSA & Algorithms", icon: "🧠" },
    { id: "languages", name: "Programming Languages", icon: "💻" },
    { id: "web", name: "Web Development", icon: "🌐" },
    { id: "databases", name: "Databases", icon: "🗄" },
    { id: "cs", name: "Computer Science", icon: "🖥" },
    { id: "tools", name: "Developer Tools", icon: "🛠" },
    { id: "cloud", name: "Cloud & DevOps", icon: "☁️" },
    { id: "system_design", name: "System Design", icon: "🏗" }
  ];

  return (
    <div className="space-y-6">

      {/* 1. PAGE HEADER & NAVIGATION SWITCHER */}
      <PageHeader
        category="Roadmap & Guidance"
        badgeText="TECHNICAL LEARNING HUB"
        title="Placement Readiness & Technical Learning Roadmap 🎯"
        subtitle="Master individual technical topics (DSA, SQL, HTML, CSS, JavaScript, React, Java, Python, Docker, OS, System Design) with structured subtopics, verified YouTube learning resources, and completion tracking."
        actions={
          <div className="flex items-center bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-1 shrink-0 text-xs font-bold flex-wrap gap-1">
            <button
              onClick={() => { setActiveMainTab('topics'); setSelectedTopicId(null); }}
              className={`px-4 py-2 rounded-lg transition flex items-center gap-2 ${
                activeMainTab === 'topics'
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <span>📚 Learning Topics</span>
            </button>

            <button
              onClick={() => setActiveMainTab('adaptive')}
              className={`px-4 py-2 rounded-lg transition flex items-center gap-2 ${
                activeMainTab === 'adaptive'
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <span>🧠 Adaptive Career Roadmap</span>
            </button>

            <button
              onClick={() => setActiveMainTab('bookmarks')}
              className={`px-4 py-2 rounded-lg transition flex items-center gap-2 ${
                activeMainTab === 'bookmarks'
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <span>🔖 Saved ({bookmarksList.length})</span>
            </button>
          </div>
        }
      />

      {/* TAB 1: TECHNICAL LEARNING TOPICS VIEW */}
      {activeMainTab === 'topics' && (
        <div className="space-y-6">

          {/* SINGLE TOPIC DETAIL VIEW */}
          {selectedTopicId && selectedTopicDetail ? (
            <div className="space-y-6 animate-fadeIn">

              {/* Header Bar & Back Button */}
              <div className="prof-card p-6 border-l-4 border-l-indigo-600 space-y-4">
                <button
                  onClick={() => setSelectedTopicId(null)}
                  className="text-xs font-bold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
                >
                  ← Back to All Learning Topics
                </button>

                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <span className="text-4xl p-2.5 bg-indigo-50 dark:bg-indigo-950/50 rounded-2xl border border-indigo-100 dark:border-indigo-900/50">{selectedTopicDetail.icon || '📚'}</span>
                    <div>
                      <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                        {selectedTopicDetail.category}
                      </span>
                      <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                        {selectedTopicDetail.full_title || selectedTopicDetail.title}
                      </h2>
                      <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                        {selectedTopicDetail.description}
                      </p>
                    </div>
                  </div>

                  <div className="flex flex-col items-start md:items-end gap-2 shrink-0">
                    <div className="text-left md:text-right">
                      <span className="text-xs text-slate-500 font-mono">Topic Completion Rate</span>
                      <div className="text-lg font-bold text-slate-900 dark:text-white font-mono">
                        {selectedTopicDetail.completed_videos_count} / {selectedTopicDetail.total_videos} Subtopics ({selectedTopicDetail.progress_percentage}%)
                      </div>
                    </div>
                    <div className="w-56">
                      <AnimatedProgressBar value={selectedTopicDetail.progress_percentage} height="h-2.5" />
                    </div>
                  </div>
                </div>
              </div>

              {/* CONTINUE LEARNING HIGHLIGHT CARD */}
              {selectedTopicDetail.continue_learning_resource && (
                <div className="prof-card p-5 bg-gradient-to-r from-indigo-50/70 to-purple-50/70 dark:from-indigo-950/40 dark:to-purple-950/40 border border-indigo-200 dark:border-indigo-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <span className="px-2.5 py-0.5 bg-indigo-600 text-white text-[10px] font-bold rounded-full uppercase tracking-wider">
                      🎯 CONTINUE LEARNING NEXT
                    </span>
                    <h3 className="text-base font-bold text-slate-900 dark:text-white mt-1">
                      {selectedTopicDetail.continue_learning_resource.title}
                    </h3>
                    <p className="text-xs text-slate-600 dark:text-slate-300">
                      {selectedTopicDetail.continue_learning_resource.description}
                    </p>
                    {selectedTopicDetail.next_recommended && (
                      <p className="text-[11px] text-indigo-600 dark:text-indigo-400 font-semibold italic mt-1">
                        Sequence Recommendation: {selectedTopicDetail.next_recommended}
                      </p>
                    )}
                  </div>

                  <div className="flex items-center gap-2 shrink-0 flex-wrap">
                    <a
                      href={selectedTopicDetail.continue_learning_resource.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold rounded-xl transition flex items-center gap-1.5 shadow-sm"
                    >
                      <PlayIcon />
                      <span>Watch YouTube Tutorial ↗</span>
                    </a>
                    <button
                      onClick={() => handleContinueLearningClick(selectedTopicDetail.continue_learning_resource.id)}
                      className="btn-primary flex items-center gap-1.5"
                    >
                      <span>Jump to Subtopic ↓</span>
                    </button>
                  </div>
                </div>
              )}

              {/* SUBTOPICS LIST HEADER */}
              <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <span>📚 Structured Learning Sequence</span>
                  <span className="text-xs font-mono text-slate-500">({selectedTopicDetail.resources?.length} Subtopics)</span>
                </h3>
                <span className="text-xs text-slate-500 font-mono">
                  Explicit status selection persists to MongoDB
                </span>
              </div>

              {/* SUBTOPICS RESOURCE LIST */}
              <div className="space-y-4">
                {selectedTopicDetail.resources?.map((res, index) => {
                  const isDone = res.completion_status === 'completed';
                  const isInProg = res.completion_status === 'in_progress';

                  return (
                    <div
                      key={res.id}
                      ref={(el) => (subtopicRefs.current[res.id] = el)}
                      className={`prof-card p-5 transition flex flex-col md:flex-row md:items-center justify-between gap-4 border ${
                        isDone
                          ? 'border-emerald-500/40 bg-emerald-50/20 dark:bg-emerald-950/10'
                          : isInProg
                          ? 'border-indigo-500/60 shadow-md bg-indigo-50/10 dark:bg-indigo-950/10'
                          : 'border-slate-200 dark:border-slate-800'
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        {/* Status Number Badge */}
                        <div className="mt-0.5 shrink-0">
                          {isDone ? (
                            <span className="w-7 h-7 rounded-full bg-emerald-600 text-white flex items-center justify-center text-xs font-bold shadow-sm">✓</span>
                          ) : isInProg ? (
                            <span className="w-7 h-7 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs font-bold shadow-sm animate-pulse">▶</span>
                          ) : (
                            <span className="w-7 h-7 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-400 flex items-center justify-center text-xs font-bold">{index + 1}</span>
                          )}
                        </div>

                        <div className="space-y-1">
                          <div className="flex items-center gap-2 flex-wrap">
                            <h4 className={`text-sm font-bold ${isDone ? 'line-through text-slate-400 dark:text-slate-500' : 'text-slate-900 dark:text-white'}`}>
                              {res.title}
                            </h4>

                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${
                              res.difficulty === 'Beginner' ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20' :
                              res.difficulty === 'Intermediate' ? 'bg-amber-500/10 text-amber-600 border-amber-500/20' :
                              'bg-rose-500/10 text-rose-600 border-rose-500/20'
                            }`}>
                              {res.difficulty || 'Intermediate'}
                            </span>

                            <span className="px-2 py-0.5 bg-rose-500/10 text-rose-600 text-[10px] font-bold rounded border border-rose-500/20 font-mono">
                              YouTube
                            </span>
                          </div>

                          <p className="text-xs text-slate-600 dark:text-slate-300">
                            {res.description}
                          </p>

                          <div className="flex items-center gap-3 text-[11px] font-mono mt-1">
                            <span className={isDone ? 'text-emerald-600 dark:text-emerald-400 font-bold' : isInProg ? 'text-indigo-600 dark:text-indigo-400 font-bold' : 'text-slate-400'}>
                              Status: {isDone ? '✓ Completed' : isInProg ? '▶ In Progress' : '○ Not Started'}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Controls & Explicit Status Buttons */}
                      <div className="flex items-center gap-2 flex-wrap shrink-0 self-end md:self-auto">
                        <button
                          onClick={() => handleToggleBookmark(res)}
                          title={res.is_bookmarked ? 'Remove Bookmark' : 'Save Resource'}
                          className="p-2 bg-slate-100 dark:bg-slate-800 rounded-xl hover:bg-slate-200 dark:hover:bg-slate-700 transition"
                        >
                          <BookmarkIcon filled={res.is_bookmarked} />
                        </button>

                        <a
                          href={res.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-3.5 py-1.5 bg-rose-500 hover:bg-rose-600 text-white text-xs font-semibold rounded-xl transition flex items-center gap-1.5 shadow-sm"
                        >
                          <PlayIcon />
                          <span>Watch Video ↗</span>
                        </a>

                        {/* Explicit Status Button Group */}
                        <div className="flex items-center bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-0.5 text-[11px] font-semibold">
                          <button
                            onClick={() => handleSetResourceStatus(res.id, 'not_started', selectedTopicDetail.title)}
                            className={`px-2.5 py-1 rounded-lg transition ${
                              !isDone && !isInProg ? 'bg-slate-400 text-white shadow' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'
                            }`}
                          >
                            ○ Not Started
                          </button>
                          <button
                            onClick={() => handleSetResourceStatus(res.id, 'in_progress', selectedTopicDetail.title)}
                            className={`px-2.5 py-1 rounded-lg transition ${
                              isInProg ? 'bg-indigo-600 text-white shadow' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'
                            }`}
                          >
                            ▶ In Progress
                          </button>
                          <button
                            onClick={() => handleSetResourceStatus(res.id, 'completed', selectedTopicDetail.title)}
                            className={`px-2.5 py-1 rounded-lg transition ${
                              isDone ? 'bg-emerald-600 text-white shadow' : 'text-slate-500 hover:text-slate-900 dark:hover:text-white'
                            }`}
                          >
                            ✓ Completed
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

            </div>
          ) : (
            <>
              {/* MY LEARNING DASHBOARD OVERVIEW HEADER */}
              {topicsData?.overall_learning && (
                <div className="prof-card p-6 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white space-y-4">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                    <div>
                      <span className="text-xs font-bold uppercase tracking-wider text-indigo-400 font-mono">MY LEARNING DASHBOARD</span>
                      <h2 className="text-xl font-bold mt-1">Overall Technical Mastery</h2>
                      <p className="text-xs text-slate-400 mt-0.5">
                        Track progress across individual technical topics and algorithms.
                      </p>
                    </div>

                    <div className="flex items-center gap-6">
                      <div className="text-center">
                        <span className="text-slate-400 block text-xs font-mono">Topics</span>
                        <strong className="text-lg font-bold font-mono">{topicsData.overall_learning.total_topics}</strong>
                      </div>
                      <div className="text-center">
                        <span className="text-slate-400 block text-xs font-mono">Subtopics Completed</span>
                        <strong className="text-lg font-bold text-emerald-400 font-mono">{topicsData.overall_learning.completed_resources}</strong>
                      </div>
                      <div className="text-center">
                        <span className="text-slate-400 block text-xs font-mono">Overall Rate</span>
                        <strong className="text-xl font-bold text-indigo-400 font-mono">{topicsData.overall_learning.overall_progress_percentage}%</strong>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between text-xs font-mono text-slate-300">
                      <span>Subtopic Resource Completion</span>
                      <span>{topicsData.overall_learning.completed_resources} / {topicsData.overall_learning.total_resources} Subtopics</span>
                    </div>
                    <AnimatedProgressBar value={topicsData.overall_learning.overall_progress_percentage} height="h-3" />
                  </div>
                </div>
              )}

              {/* SEARCH & FILTER TOOLBAR */}
              <div className="prof-card p-5 space-y-4">
                <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row items-stretch md:items-center gap-3">
                  
                  {/* Search Input */}
                  <div className="relative flex-1">
                    <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                      <SearchIcon />
                    </div>
                    <input
                      type="text"
                      placeholder="🔍 Search technical topics (e.g., DSA, SQL, React, Python, Docker, HTML)..."
                      value={topicSearchInput}
                      onChange={(e) => setTopicSearchInput(e.target.value)}
                      onKeyDown={(e) => { if (e.key === 'Enter') handleSearchSubmit(e); }}
                      className="w-full pl-10 pr-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white focus:outline-none focus:border-indigo-500"
                    />
                  </div>

                  {/* Search Button */}
                  <button
                    type="submit"
                    className="btn-primary shrink-0 flex items-center justify-center gap-1.5 text-xs py-2.5 px-5"
                  >
                    <span>Search</span>
                  </button>

                  {/* Status Filter Dropdown */}
                  <select
                    value={topicStatusFilter}
                    onChange={(e) => setTopicStatusFilter(e.target.value)}
                    className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 px-3 py-2.5 rounded-xl text-xs focus:outline-none shrink-0 font-medium"
                  >
                    <option value="all">All Statuses</option>
                    <option value="not_started">Not Started</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">✓ Completed</option>
                  </select>

                  {(activeSearchQuery || topicCatFilter !== 'all' || topicStatusFilter !== 'all') && (
                    <button
                      type="button"
                      onClick={handleClearFilters}
                      className="text-xs text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 underline shrink-0 px-2"
                    >
                      Clear Filters
                    </button>
                  )}
                </form>

                {/* Category Pills */}
                <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-thin text-xs font-semibold">
                  {categoryPills.map(cat => (
                    <button
                      key={cat.id}
                      onClick={() => setTopicCatFilter(cat.id === 'all' ? 'all' : cat.name)}
                      className={`px-3 py-1.5 rounded-lg shrink-0 transition flex items-center gap-1.5 ${
                        (cat.id === 'all' && topicCatFilter === 'all') || (topicCatFilter === cat.name)
                          ? 'bg-indigo-600 text-white shadow'
                          : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                      }`}
                    >
                      <span>{cat.icon}</span>
                      <span>{cat.name}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* TECHNICAL TOPIC CARDS GRID */}
              {loadingTopics ? (
                <div className="py-16 text-center text-slate-500 animate-pulse text-sm prof-card">
                  Loading Technical Topics & MongoDB Catalog...
                </div>
              ) : filteredTopics.length === 0 ? (
                <div className="py-12 px-6 text-center space-y-3 prof-card">
                  <div className="text-3xl">🔍</div>
                  <h3 className="text-sm font-bold text-slate-800 dark:text-white">
                    No technical topics matched your current filter criteria
                  </h3>
                  <p className="text-xs text-slate-500 max-w-md mx-auto">
                    {activeSearchQuery
                      ? `No topics found matching '${activeSearchQuery}' with status '${topicStatusFilter}'.`
                      : `No topics found in category '${topicCatFilter}' with status '${topicStatusFilter}'.`}
                  </p>
                  <button
                    onClick={handleClearFilters}
                    className="btn-secondary text-xs px-4 py-2"
                  >
                    Reset Search & Filters
                  </button>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                  {filteredTopics.map((topic) => {
                    const isDone = topic.is_completed;
                    const inProg = topic.completed_videos_count > 0 && !isDone;

                    return (
                      <div
                        key={topic.id}
                        className={`prof-card p-5 flex flex-col justify-between space-y-4 hover:shadow-lg transition border ${
                          isDone
                            ? 'border-emerald-500/40 bg-emerald-50/10 dark:bg-emerald-950/10'
                            : inProg
                            ? 'border-indigo-500/50'
                            : 'border-slate-200 dark:border-slate-800'
                        }`}
                      >
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-3xl">{topic.icon || '📚'}</span>
                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold font-mono uppercase border ${
                              isDone ? 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20' :
                              inProg ? 'bg-indigo-500/10 text-indigo-600 border-indigo-500/20' :
                              'bg-slate-100 dark:bg-slate-800 text-slate-500 border-slate-200 dark:border-slate-700'
                            }`}>
                              {isDone ? '✓ Completed' : inProg ? '▶ In Progress' : '○ Not Started'}
                            </span>
                          </div>

                          <h3 className="text-base font-bold text-slate-900 dark:text-white">
                            {topic.title}
                          </h3>

                          <p className="text-xs text-slate-500 dark:text-slate-400 line-clamp-2 leading-relaxed">
                            {topic.description}
                          </p>
                        </div>

                        <div className="space-y-3 pt-3 border-t border-slate-200 dark:border-slate-800">
                          <div className="space-y-1">
                            <div className="flex justify-between text-[11px] font-mono">
                              <span className="text-slate-500">Subtopic Completion</span>
                              <span className="font-bold text-slate-900 dark:text-white">
                                {topic.completed_videos_count} / {topic.total_videos} ({topic.progress_percentage}%)
                              </span>
                            </div>
                            <AnimatedProgressBar value={topic.progress_percentage} height="h-2" />
                          </div>

                          <div className="flex items-center gap-2 pt-1">
                            <a
                              href={topic.youtube_url || (topic.continue_learning_resource ? topic.continue_learning_resource.url : `https://www.youtube.com/results?search_query=${encodeURIComponent(topic.title + ' tutorial')}`)}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex-1 py-2 px-2.5 bg-rose-600 hover:bg-rose-700 text-white text-xs font-semibold rounded-xl transition flex items-center justify-center gap-1 shadow-sm shrink-0"
                            >
                              <PlayIcon />
                              <span>Watch YouTube ↗</span>
                            </a>

                            <button
                              onClick={() => loadTopicDetail(topic.id)}
                              className={`flex-1 py-2 px-2.5 rounded-xl text-xs font-semibold transition flex items-center justify-center gap-1 ${
                                isDone
                                  ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20'
                                  : 'btn-primary'
                              }`}
                            >
                              <span>Subtopics ({topic.total_videos}) →</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </>
          )}

        </div>
      )}

      {/* TAB 2: ADAPTIVE CAREER ROADMAP VIEW */}
      {activeMainTab === 'adaptive' && (
        <div className="space-y-6">
          <div className="prof-card p-6 space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
              <div>
                <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <span>🎯 Career Preparation Target Parameters</span>
                </h2>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Customize target role, experience level, and company tier for career milestone preparation.
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={async () => {
                    setRecalculating(true);
                    try {
                      const res = await api.roadmap.recalculateAdaptive();
                      if (res?.roadmap) setAdaptiveData(res.roadmap);
                    } catch (e) {
                      console.error(e);
                    } finally {
                      setRecalculating(false);
                    }
                  }}
                  disabled={recalculating}
                  className="btn-secondary flex items-center gap-1.5"
                >
                  <span>⚡ Recalculate AI Roadmap</span>
                </button>

                <button
                  type="button"
                  onClick={async () => {
                    setSavingConfig(true);
                    try {
                      const res = await api.roadmap.configureAdaptive(configForm);
                      if (res?.roadmap) setAdaptiveData(res.roadmap);
                    } catch (e) {
                      console.error(e);
                    } finally {
                      setSavingConfig(false);
                    }
                  }}
                  disabled={savingConfig}
                  className="btn-primary"
                >
                  {savingConfig ? 'Updating...' : 'Save Parameters'}
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-600 dark:text-slate-400">Target Role</label>
                <select
                  value={configForm.target_role}
                  onChange={(e) => setConfigForm({ ...configForm, target_role: e.target.value })}
                  className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-3 py-2 text-xs font-medium text-slate-900 dark:text-white focus:outline-none focus:border-indigo-500"
                >
                  {rolesOptions.supported_roles.map(r => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-600 dark:text-slate-400">Experience Tier</label>
                <select
                  value={configForm.experience_level}
                  onChange={(e) => setConfigForm({ ...configForm, experience_level: e.target.value })}
                  className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-3 py-2 text-xs font-medium text-slate-900 dark:text-white focus:outline-none focus:border-indigo-500"
                >
                  {rolesOptions.experience_levels.map(lvl => (
                    <option key={lvl} value={lvl}>{lvl}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-600 dark:text-slate-400">Company Target</label>
                <select
                  value={configForm.company_type}
                  onChange={(e) => setConfigForm({ ...configForm, company_type: e.target.value })}
                  className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-3 py-2 text-xs font-medium text-slate-900 dark:text-white focus:outline-none focus:border-indigo-500"
                >
                  {rolesOptions.company_types.map(c => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-600 dark:text-slate-400">Timeframe (Weeks)</label>
                <select
                  value={configForm.prep_time_weeks}
                  onChange={(e) => setConfigForm({ ...configForm, prep_time_weeks: parseInt(e.target.value) })}
                  className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-3 py-2 text-xs font-medium text-slate-900 dark:text-white focus:outline-none focus:border-indigo-500"
                >
                  {rolesOptions.prep_timeframes.map(w => (
                    <option key={w} value={w}>{w} Weeks Intensive</option>
                  ))}
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-600 dark:text-slate-400">Skill Level</label>
                <select
                  value={configForm.skill_level}
                  onChange={(e) => setConfigForm({ ...configForm, skill_level: e.target.value })}
                  className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-3 py-2 text-xs font-medium text-slate-900 dark:text-white focus:outline-none focus:border-indigo-500"
                >
                  {rolesOptions.skill_levels.map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {loadingAdaptive ? (
            <div className="py-16 text-center text-slate-500 animate-pulse text-sm prof-card">
              Loading adaptive preparation roadmap...
            </div>
          ) : adaptiveData ? (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="prof-card p-6 space-y-4">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Readiness Progress</span>
                  <AnimatedProgressBar value={adaptiveData.overall_progress} height="h-3" />
                  <div className="grid grid-cols-2 gap-3 pt-2 text-xs border-t border-slate-200 dark:border-slate-800 font-mono">
                    <div>
                      <span className="text-slate-500 block">Completed</span>
                      <strong className="text-slate-900 dark:text-white text-base">{adaptiveData.completed_tasks_count} / {adaptiveData.total_tasks}</strong>
                    </div>
                    <div>
                      <span className="text-slate-500 block">Remaining</span>
                      <strong className="text-amber-500 text-base">{adaptiveData.remaining_tasks_count}</strong>
                    </div>
                  </div>
                </div>

                <div className="prof-card p-6 space-y-2 lg:col-span-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-500">Current Focus</span>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                    {adaptiveData.current_focus || "General Preparation"}
                  </h3>
                  <p className="text-xs text-slate-500">
                    Role Target: <strong className="text-indigo-600 dark:text-indigo-400">{adaptiveData.config?.target_role}</strong> ({adaptiveData.config?.company_type})
                  </p>
                </div>
              </div>

              {/* TIMELINE LIST */}
              <div className="space-y-4">
                {(adaptiveData.items || []).map((item, idx) => (
                  <div key={item.id} className="prof-card p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border border-slate-200 dark:border-slate-800">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono font-bold text-indigo-600">#{idx + 1}</span>
                        <h4 className="text-sm font-bold text-slate-900 dark:text-white">{item.title}</h4>
                      </div>
                      <p className="text-xs text-slate-500">{item.description}</p>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <button
                        onClick={() => {
                          setSelectedTopicId(item.category === 'SQL Preparation' ? 'sql' : 'dsa');
                          setActiveMainTab('topics');
                        }}
                        className="btn-secondary text-xs px-3 py-1.5"
                      >
                        Learn Topic →
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : null}
        </div>
      )}

      {/* TAB 3: BOOKMARKS VIEW */}
      {activeMainTab === 'bookmarks' && (
        <div className="space-y-6">
          <div className="prof-card p-6">
            <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <span>🔖 My Saved YouTube Resources</span>
              <span className="text-xs font-mono text-slate-500">({bookmarksList.length} Bookmarks)</span>
            </h2>
            <p className="text-xs text-slate-500 mt-1">
              Access your saved technical tutorials and video learning guides.
            </p>

            {bookmarksList.length === 0 ? (
              <div className="py-16 text-center text-slate-500 text-xs italic">
                No saved resources yet. Click the bookmark icon on any YouTube resource card to save it.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                {bookmarksList.map(bm => {
                  const res = bm.resource || bm;
                  return (
                    <div key={bm.resource_id || bm.id} className="prof-card p-4 flex flex-col justify-between space-y-3 border border-slate-200 dark:border-slate-800">
                      <div className="space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="px-2 py-0.5 bg-indigo-500/10 text-indigo-600 text-[10px] font-bold rounded">
                            {bm.topic || 'General'}
                          </span>
                          <button
                            onClick={() => handleToggleBookmark({ id: bm.resource_id, is_bookmarked: true })}
                            className="text-xs text-rose-500 hover:underline"
                          >
                            Remove
                          </button>
                        </div>
                        <h4 className="text-sm font-bold text-slate-900 dark:text-white">{res.title || bm.title}</h4>
                      </div>

                      <a
                        href={res.url || bm.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn-primary self-start flex items-center gap-1.5 text-xs"
                      >
                        <PlayIcon />
                        <span>Watch Video ↗</span>
                      </a>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  );
};

export default PlacementRoadmapTracker;
