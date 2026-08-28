import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { PageHeader } from '../components/common/DesignSystemComponents';

// Helper to sanitize handle from raw username OR full profile URL
const parseHandle = (input) => {
  if (!input) return '';
  let str = input.trim();
  str = str.replace(/^https?:\/\/(www\.)?leetcode\.com\/(u\/)?/i, '');
  str = str.replace(/^https?:\/\/(www\.)?hackerrank\.com\/(profile\/)?/i, '');
  str = str.split('/')[0].split('?')[0].replace('@', '');
  return str;
};

// Inline SVG Icon Helpers
const FlameIcon = () => (
  <svg className="w-5 h-5 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
    <path fillRule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.616.953-1.04 2.14-1.304 3.49-1.28-1.077-2.023-2.6-2.128-4.043a1 1 0 00-1.636-.677c-.5.42-.962.91-1.378 1.458-1.575 2.074-2.177 4.58-1.678 7.1.332 1.677 1.258 3.167 2.57 4.256a8.04 8.04 0 005.158 1.866 8.04 8.04 0 005.158-1.866c1.312-1.089 2.238-2.579 2.57-4.256.5-2.52-.103-5.026-1.678-7.1a12.01 12.01 0 00-1.453-1.554z" clipRule="evenodd" />
  </svg>
);

const CalendarIcon = () => (
  <svg className="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);

const AwardIcon = () => (
  <svg className="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V6a2 2 0 10-2 2h2zm0 13l-4-4m4 4l4-4" />
  </svg>
);

const StarIcon = ({ filled }) => (
  <svg className={`w-4 h-4 ${filled ? 'text-amber-400 fill-amber-400' : 'text-slate-300 dark:text-slate-700 fill-slate-200 dark:fill-slate-800'}`} viewBox="0 0 20 20">
    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
  </svg>
);

const CheckCircle2Icon = () => (
  <svg className="w-4 h-4 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const ExternalLinkIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
  </svg>
);

const Link2Icon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
  </svg>
);

const CodingProfilesTracker = () => {
  const { user, updateProfile } = useAuth();
  
  // Input fields for Handles or URLs
  const [leetcodeInput, setLeetcodeInput] = useState('');
  const [hackerrankInput, setHackerrankInput] = useState('');
  
  const [leetcodeUsername, setLeetcodeUsername] = useState('');
  const [hackerrankUsername, setHackerrankUsername] = useState('');
  
  // Live API Response Data States
  const [dailyChallenge, setDailyChallenge] = useState(null);
  const [leetcodeData, setLeetcodeData] = useState(null);
  const [hackerrankData, setHackerrankData] = useState(null);
  
  // Loading & Modal States
  const [loadingDaily, setLoadingDaily] = useState(true);
  const [loadingProfiles, setLoadingProfiles] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [connectLoading, setConnectLoading] = useState(false);
  const [modalSuccess, setModalSuccess] = useState('');
  const [modalError, setModalError] = useState('');

  // Extract handles from MongoDB user document on mount
  useEffect(() => {
    const lc = parseHandle(user?.codingProfiles?.leetcode?.username || '');
    const hr = parseHandle(user?.codingProfiles?.hackerrank?.username || '');
    setLeetcodeUsername(lc);
    setLeetcodeInput(lc);
    setHackerrankUsername(hr);
    setHackerrankInput(hr);
  }, [user]);

  // Fetch LeetCode Daily Challenge
  useEffect(() => {
    const fetchDaily = async () => {
      setLoadingDaily(true);
      try {
        const res = await api.coding.getDailyChallenge();
        setDailyChallenge(res);
      } catch (err) {
        console.error('Daily challenge error:', err);
      } finally {
        setLoadingDaily(false);
      }
    };
    fetchDaily();
  }, []);

  // Live Auto-Sync: Fetch LeetCode & HackerRank Profile Data from Net on Open
  const loadProfileStats = async () => {
    const lc = parseHandle(leetcodeUsername || user?.codingProfiles?.leetcode?.username);
    const hr = parseHandle(hackerrankUsername || user?.codingProfiles?.hackerrank?.username);
    
    if (!lc && !hr) {
      setLeetcodeData(null);
      setHackerrankData(null);
      return;
    }
    setLoadingProfiles(true);
    try {
      const [lcRes, hrRes] = await Promise.all([
        lc ? api.coding.getLeetCodeStats(lc) : Promise.resolve(null),
        hr ? api.coding.getHackerRankStats(hr) : Promise.resolve(null)
      ]);
      if (lcRes) setLeetcodeData(lcRes);
      if (hrRes) setHackerrankData(hrRes);
    } catch (err) {
      console.error('Error fetching coding profiles:', err);
    } finally {
      setLoadingProfiles(false);
    }
  };

  useEffect(() => {
    loadProfileStats();
  }, [leetcodeUsername, hackerrankUsername]);

  // Connect & Save Handles Modal Submit
  const handleConnectSubmit = async (e) => {
    e.preventDefault();
    setModalError('');
    setModalSuccess('');
    setConnectLoading(true);
    
    const parsedLc = parseHandle(leetcodeInput);
    const parsedHr = parseHandle(hackerrankInput);

    try {
      const res = await api.coding.connectProfiles({
        leetcode_username: parsedLc,
        hackerrank_username: parsedHr
      });
      
      setLeetcodeUsername(parsedLc);
      setHackerrankUsername(parsedHr);

      setModalSuccess('Handles verified & saved in MongoDB! Syncing live data...');
      if (res?.codingProfiles && updateProfile) {
        await updateProfile({ codingProfiles: res.codingProfiles });
      }
      
      setTimeout(() => {
        setIsModalOpen(false);
        setModalSuccess('');
        loadProfileStats();
      }, 1200);
    } catch (err) {
      setModalError(err.message || 'Failed to save handles. Please check input URL or username.');
    } finally {
      setConnectLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* 1. TOP HEADER BANNER & CONNECT HANDLES CTA */}
      <PageHeader
        category="Competitive Programming"
        badgeText="LIVE WEB SYNC"
        title="Competitive Programming Tracker ⚡"
        subtitle="Paste your LeetCode & HackerRank Profile URLs or Usernames to track real-time streaks, problem metrics, and badges."
        actions={
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsModalOpen(true)}
              className="btn-primary flex items-center gap-2"
            >
              <Link2Icon />
              {leetcodeUsername || hackerrankUsername ? 'Manage Handles / URLs' : 'Connect Profiles'}
            </button>
            <Link
              to="/coding-arena"
              className="btn-secondary"
            >
              Coding Arena Sandbox →
            </Link>
          </div>
        }
      />

      {/* 2. LEETCODE DAILY CODING CHALLENGE BANNER */}
      <div className="prof-card p-6 border-l-4 border-l-amber-500 space-y-4">
        <div className="flex items-center justify-between">
          <span className="px-3 py-1 bg-amber-500/10 text-amber-600 dark:text-amber-300 text-xs font-semibold rounded-md border border-amber-500/20 flex items-center gap-1.5 font-mono">
            ⭐ LEETCODE DAILY CHALLENGE #{dailyChallenge?.frontend_id || '3'}
          </span>
          <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
            Date: {dailyChallenge?.date || 'Today'}
          </span>
        </div>

        {loadingDaily ? (
          <div className="py-6 text-center text-slate-500 dark:text-slate-400 animate-pulse text-xs">
            Fetching today's challenge live from LeetCode GraphQL...
          </div>
        ) : (
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                  {dailyChallenge?.title || "Longest Substring Without Repeating Characters"}
                </h2>
                <span className={`px-2.5 py-0.5 text-xs font-bold rounded-md ${
                  dailyChallenge?.difficulty === 'Easy' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20' :
                  dailyChallenge?.difficulty === 'Hard' ? 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20' :
                  'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20'
                }`}>
                  {dailyChallenge?.difficulty || 'Medium'}
                </span>
              </div>

              <div className="flex items-center gap-2 mt-3 flex-wrap">
                {(dailyChallenge?.tags || ['Hash Table', 'Sliding Window', 'String']).map((tag, idx) => (
                  <span key={idx} className="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[11px] rounded-lg border border-slate-200 dark:border-slate-700 font-mono">
                    #{tag}
                  </span>
                ))}
              </div>
            </div>

            <a
              href={dailyChallenge?.link || "https://leetcode.com/problems/longest-substring-without-repeating-characters/"}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary self-start md:self-auto flex items-center gap-2 shrink-0"
            >
              Solve Today's Challenge
              <ExternalLinkIcon />
            </a>
          </div>
        )}
      </div>

      {/* 3. DUAL PLATFORM SECTIONS (LEETCODE & HACKERRANK) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* LEETCODE TRACKER CARD */}
        <div className="prof-card p-6 flex flex-col justify-between space-y-6">
          <div>
            <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center font-bold text-amber-600 dark:text-amber-400 text-lg">
                  LC
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    LeetCode Live Profile
                    {leetcodeData?.isConnected && <CheckCircle2Icon />}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                    {leetcodeUsername ? `@${leetcodeUsername}` : 'Not Connected'}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setIsModalOpen(true)}
                className="text-xs text-blue-600 dark:text-blue-400 hover:underline font-semibold"
              >
                {leetcodeUsername ? 'Edit Handle / URL' : 'Connect Profile'}
              </button>
            </div>

            {!leetcodeUsername || !leetcodeData?.isConnected ? (
              /* Unlinked Empty State */
              <div className="py-12 text-center space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center mx-auto text-xl text-slate-400">
                  🔗
                </div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white">No LeetCode Handle Linked</h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 max-w-xs mx-auto">
                  Paste your LeetCode profile URL (e.g. https://leetcode.com/u/your_name) to track live streak and solved problem counts.
                </p>
                <button
                  onClick={() => setIsModalOpen(true)}
                  className="btn-primary"
                >
                  + Link LeetCode Profile
                </button>
              </div>
            ) : (
              /* Connected Live Data State */
              <div className="space-y-5 mt-5">
                {/* LeetCode Key Metrics (Streak & Active Days) */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl flex items-center gap-3">
                    <FlameIcon />
                    <div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 uppercase font-semibold">Active Streak</p>
                      <p className="text-xl font-extrabold text-amber-500 font-mono mt-0.5">
                        {leetcodeData.streak ?? 0} Days 🔥
                      </p>
                    </div>
                  </div>
                  <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl flex items-center gap-3">
                    <CalendarIcon />
                    <div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 uppercase font-semibold">Total Active Days</p>
                      <p className="text-xl font-extrabold text-blue-600 dark:text-blue-400 font-mono mt-0.5">
                        {leetcodeData.totalActiveDays ?? 0} Days
                      </p>
                    </div>
                  </div>
                </div>

                {/* Solved Breakdown Matrix */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-500 dark:text-slate-400 font-semibold">Problems Solved Breakdown</span>
                    <span className="text-slate-900 dark:text-white font-mono font-bold">
                      {leetcodeData.totalSolved ?? 0} Total Solved
                    </span>
                  </div>
                  <div className="grid grid-cols-3 gap-3 text-center">
                    <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-3 rounded-xl">
                      <p className="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold uppercase">Easy</p>
                      <p className="text-lg font-bold text-slate-900 dark:text-white font-mono mt-0.5">{leetcodeData.easySolved ?? 0}</p>
                    </div>
                    <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-3 rounded-xl">
                      <p className="text-[10px] text-amber-600 dark:text-amber-400 font-bold uppercase">Medium</p>
                      <p className="text-lg font-bold text-slate-900 dark:text-white font-mono mt-0.5">{leetcodeData.mediumSolved ?? 0}</p>
                    </div>
                    <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-3 rounded-xl">
                      <p className="text-[10px] text-rose-600 dark:text-rose-400 font-bold uppercase">Hard</p>
                      <p className="text-lg font-bold text-slate-900 dark:text-white font-mono mt-0.5">{leetcodeData.hardSolved ?? 0}</p>
                    </div>
                  </div>
                </div>

                {/* Profile Badges */}
                {leetcodeData.badges && leetcodeData.badges.length > 0 && (
                  <div className="pt-4 border-t border-slate-200 dark:border-slate-800">
                    <p className="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2.5 flex items-center gap-1.5">
                      <AwardIcon /> Earned Profile Badges:
                    </p>
                    <div className="flex items-center gap-2 flex-wrap">
                      {leetcodeData.badges.map((badge, i) => (
                        <span key={i} className="px-3 py-1 bg-purple-500/10 border border-purple-500/20 text-purple-600 dark:text-purple-300 text-xs font-semibold rounded-lg">
                          🏅 {badge}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* HACKERRANK TRACKER CARD */}
        <div className="prof-card p-6 flex flex-col justify-between space-y-6">
          <div>
            <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center font-bold text-emerald-600 dark:text-emerald-400 text-lg">
                  HR
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    HackerRank Live Profile
                    {hackerrankData?.isConnected && <CheckCircle2Icon />}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                    {hackerrankUsername ? `@${hackerrankUsername}` : 'Not Connected'}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setIsModalOpen(true)}
                className="text-xs text-blue-600 dark:text-blue-400 hover:underline font-semibold"
              >
                {hackerrankUsername ? 'Edit Handle / URL' : 'Connect Profile'}
              </button>
            </div>

            {!hackerrankUsername || !hackerrankData?.isConnected ? (
              /* Unlinked Empty State */
              <div className="py-12 text-center space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center mx-auto text-xl text-slate-400">
                  ⭐
                </div>
                <h4 className="text-sm font-bold text-slate-900 dark:text-white">No HackerRank Handle Linked</h4>
                <p className="text-xs text-slate-500 dark:text-slate-400 max-w-xs mx-auto">
                  Paste your HackerRank profile URL (e.g. https://www.hackerrank.com/profile/your_name) to showcase your domain badges.
                </p>
                <button
                  onClick={() => setIsModalOpen(true)}
                  className="btn-primary"
                >
                  + Link HackerRank Profile
                </button>
              </div>
            ) : (
              /* Connected Live Data State */
              <div className="mt-5 space-y-4">
                <p className="text-xs font-semibold text-slate-500 dark:text-slate-400">
                  Verified Skill Badges & Star Ratings
                </p>

                {hackerrankData.badges && hackerrankData.badges.length > 0 ? (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {hackerrankData.badges.map((badge, idx) => (
                      <div key={idx} className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-slate-800 dark:text-slate-200">{badge.name}</span>
                          <span className="text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400">{badge.stars} ⭐ Stars</span>
                        </div>
                        <div className="flex items-center gap-1">
                          {[1, 2, 3, 4, 5, 6].map((starIdx) => (
                            <StarIcon key={starIdx} filled={starIdx <= badge.stars} />
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 dark:text-slate-400 py-4 text-center">No badges earned yet for @{hackerrankUsername}.</p>
                )}
              </div>
            )}
          </div>

          <div className="pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
            <span>Live auto-synced from HackerRank Web API</span>
            <span className="text-emerald-600 dark:text-emerald-400 font-mono font-bold">● Live Sync</span>
          </div>
        </div>

      </div>

      {/* 4. CONNECT PLATFORM HANDLES / URLS MODAL DIALOG */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm">
          <div className="w-full max-w-md prof-card p-6 shadow-2xl space-y-5">
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Link2Icon /> Connect LeetCode & HackerRank
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-900 dark:hover:text-white text-lg font-bold"
              >
                ✕
              </button>
            </div>

            {modalSuccess && (
              <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-xs text-emerald-600 dark:text-emerald-300 font-medium text-center">
                ✓ {modalSuccess}
              </div>
            )}

            {modalError && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl text-xs text-rose-600 dark:text-rose-300 font-medium text-center">
                {modalError}
              </div>
            )}

            <form onSubmit={handleConnectSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block text-slate-700 dark:text-slate-300 font-semibold mb-1">
                  LeetCode Username or Profile URL
                </label>
                <input
                  type="text"
                  value={leetcodeInput}
                  onChange={(e) => setLeetcodeInput(e.target.value)}
                  placeholder="e.g. https://leetcode.com/u/your_username or your_username"
                  className="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
                />
                <p className="text-[10px] text-slate-500 mt-1">You can paste your full LeetCode profile URL!</p>
              </div>

              <div>
                <label className="block text-slate-700 dark:text-slate-300 font-semibold mb-1">
                  HackerRank Username or Profile URL
                </label>
                <input
                  type="text"
                  value={hackerrankInput}
                  onChange={(e) => setHackerrankInput(e.target.value)}
                  placeholder="e.g. https://www.hackerrank.com/profile/your_username or your_username"
                  className="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-blue-500"
                />
                <p className="text-[10px] text-slate-500 mt-1">You can paste your full HackerRank profile URL!</p>
              </div>

              <div className="flex items-center gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={connectLoading}
                  className="btn-primary flex-1"
                >
                  {connectLoading ? 'Syncing...' : 'Save & Sync Handles'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default CodingProfilesTracker;
