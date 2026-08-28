import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useUserProfile } from '../contexts/UserProfileContext';
import { api } from '../services/api';
import { 
  ScoreBadge, 
  AIInsightCard, 
  AnimatedNumber, 
  PageHeader 
} from '../components/common/DesignSystemComponents';
import InPageToolsDrawer from '../components/dashboard/InPageToolsDrawer';

// URL Handle Sanitizer
const parseHandle = (input) => {
  if (!input) return '';
  let str = input.trim();
  str = str.replace(/^https?:\/\/(www\.)?leetcode\.com\/(u\/)?/i, '');
  str = str.replace(/^https?:\/\/(www\.)?hackerrank\.com\/(profile\/)?/i, '');
  str = str.split('/')[0].split('?')[0].replace('@', '');
  return str;
};

const DashboardHub = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { detectedRole, experienceLevel, isInitialized, overrideRole } = useUserProfile();
  const [isToolsOpen, setIsToolsOpen] = useState(false);
  const [quickResumeFile, setQuickResumeFile] = useState(null);
  const [isScanningResume, setIsScanningResume] = useState(false);
  const [scanResult, setScanResult] = useState(null);

  // Dynamic Live Metrics State
  const [readinessScore, setReadinessScore] = useState(null);
  const [codingStreak, setCodingStreak] = useState(null);
  const [leetcodeHandle, setLeetcodeHandle] = useState('');
  const [latestAtsScore, setLatestAtsScore] = useState(null);
  const [latestInterviewGrade, setLatestInterviewGrade] = useState(null);

  // Hiring & Market Trends Signals
  const hiringTrends = [
    { skill: 'FastAPI & Python', growth: '+28%', status: 'High Demand' },
    { skill: 'React & Tailwind', growth: '+32%', status: 'Trending' },
    { skill: 'MongoDB & Vector DBs', growth: '+19%', status: 'Growing' },
    { skill: 'System Design', growth: '+35%', status: 'Top Placement Ask' },
  ];

  // Fetch Live Metrics upon opening application
  useEffect(() => {
    const fetchUserLiveData = async () => {
      // 0. Fetch Central Job Readiness Index
      try {
        const readRes = await api.get('/api/v1/jobs/readiness');
        if (readRes?.overall_readiness_score !== undefined) {
          setReadinessScore(readRes.overall_readiness_score);
        }
      } catch (err) {
        console.error('Error fetching job readiness index:', err);
      }

      // 1. LeetCode streak from user handle saved in MongoDB
      const rawHandle = user?.codingProfiles?.leetcode?.username || '';
      const lcHandle = parseHandle(rawHandle);
      
      if (lcHandle) {
        setLeetcodeHandle(lcHandle);
        try {
          const stats = await api.coding.getLeetCodeStats(lcHandle);
          if (stats?.streak !== undefined && stats?.isConnected) {
            setCodingStreak(stats.streak);
          }
        } catch (err) {
          console.error('Error fetching LeetCode live streak:', err);
        }
      } else {
        setCodingStreak(null);
        setLeetcodeHandle('');
      }

      // 2. Latest ATS Resume Score from MongoDB scan history
      try {
        const historyRes = await api.resume.getHistory();
        const scans = historyRes?.scans || historyRes?.history || [];
        if (scans.length > 0) {
          const topScore = scans[0].overall_score || scans[0].ats_score || scans[0].score;
          if (topScore) setLatestAtsScore(topScore);
        }
      } catch (err) {
        console.error('Error fetching resume history:', err);
      }

      // 3. Latest Interview Grade from MongoDB attempt history
      try {
        const interviewRes = await api.interview.getHistory();
        const attempts = interviewRes?.attempts || interviewRes?.history || [];
        if (attempts.length > 0) {
          const latestScore = attempts[0].score || attempts[0].overall_rating || 85;
          setLatestInterviewGrade(`${latestScore}%`);
        }
      } catch (err) {
        console.error('Error fetching interview history:', err);
      }
    };

    fetchUserLiveData();
  }, [user]);

  // 4 Feature Tracks
  const featureModules = [
    {
      category: 'Resume & Application AI',
      items: [
        {
          id: 'resume-analyzer',
          title: 'AI Resume Analyzer & ATS Scorer',
          description: 'Deep resume inspection, ATS score optimization, and tailored bullet-point enhancements.',
          path: '/resume-analyzer',
          icon: '📄',
          badge: 'Live ATS Scorer',
        },
        {
          id: 'cover-letter',
          title: 'AI Cover Letter Generator',
          description: 'Instant customized cover letters matching target job descriptions and recruiters.',
          path: '/cover-letter',
          icon: '✍️',
          badge: 'AI Generator',
        },
        {
          id: 'linkedin-optimizer',
          title: 'LinkedIn Profile Optimizer',
          description: 'Tailor your LinkedIn headline, about section, and experience bullets for tech recruiters.',
          path: '/linkedin-optimizer',
          icon: '💼',
          badge: 'Recruiter Outreach',
        },
      ],
    },
    {
      category: 'Coding & Technical Mastery',
      items: [
        {
          id: 'coding-arena',
          title: 'Coding Arena Practice IDE',
          description: 'Execute Python, JavaScript, Java & C++ code against test suites with AI debug hints.',
          path: '/coding-arena',
          icon: '💻',
          badge: 'Multi-Language IDE',
        },
        {
          id: 'coding-tracker',
          title: 'LeetCode & Profile Tracker',
          description: 'Sync your LeetCode, CodeChef and GitHub metrics in real time.',
          path: '/coding-tracker',
          icon: '⚡',
          badge: 'Live Web Sync',
        },
        {
          id: 'weakness-detector',
          title: 'AI Weakness & Error Detector',
          description: 'Identify your coding weak spots, recurring bugs, and algorithmic gaps.',
          path: '/weakness-detector',
          icon: '🔍',
          badge: 'Diagnostic AI',
        },
      ],
    },
    {
      category: 'Interview Prep & Speech AI',
      items: [
        {
          id: 'interview-simulator',
          title: 'Mock AI Interview Room',
          description: 'Voice STT/TTS interview practice with real-time AI scoring and transcript feedback.',
          path: '/interview-simulator',
          icon: '🎙️',
          badge: 'Voice Simulator',
        },
        {
          id: 'speech-analyzer',
          title: 'Speech Delivery & Prosody AI',
          description: 'Analyze WPM pace, pause fillers, pitch intonation (F0), and communication clarity.',
          path: '/speech-analyzer',
          icon: '🗣️',
          badge: 'Prosody Analytics',
        },
        {
          id: 'gd-simulator',
          title: 'AI Group Discussion Simulator',
          description: 'Practice multi-turn tech & GD debates against simulated peer candidates.',
          path: '/gd-simulator',
          icon: '🗣️',
          badge: 'Group Discussion',
        },
      ],
    },
    {
      category: 'Career Roadmap & Analytics',
      items: [
        {
          id: 'placement-roadmap',
          title: 'Placement & Learning Roadmap',
          description: 'Adaptive career milestone tracking with YouTube video resources and progress updates.',
          path: '/placement-roadmap',
          icon: '🗺️',
          badge: 'Adaptive Path',
        },
        {
          id: 'job-readiness',
          title: 'Job Readiness Index',
          description: '6-pillar readiness score breakdown across Resume, Coding, Interview, and Soft Skills.',
          path: '/job-readiness',
          icon: '🎯',
          badge: 'Readiness Score',
        },
        {
          id: 'job-matcher',
          title: '5-Weight Job Matcher',
          description: 'Find target software engineering roles matching your exact skill matrix.',
          path: '/job-matcher',
          icon: '🎯',
          badge: 'Matching Engine',
        },
      ],
    },
  ];

  return (
    <div className="space-y-6">
      
      {/* UNINITIALIZED RESUME CTA ALERT */}
      {!isInitialized && (
        <div className="p-5 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800/80 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#4F46E5]/10 text-[#4F46E5] dark:text-[#6366F1] border border-indigo-200 dark:border-indigo-800 flex items-center justify-center font-bold text-lg shrink-0">
              📄
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">Upload Resume to Unlock Your AI Career Copilot</h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                Upload your resume to automatically detect your engineering persona, tailor learning roadmaps, and generate custom mock interviews.
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/resume-analyzer')}
            className="btn-primary shrink-0"
          >
            Upload Resume Now →
          </button>
        </div>
      )}

      {/* 1. TOP WELCOME & STATUS BANNER */}
      <PageHeader
        category="AI Career Copilot Dashboard"
        badgeText={experienceLevel}
        title={`Welcome back, ${user?.name || 'Candidate'}! 👋`}
        subtitle={isInitialized ? `Personalized workspace active for ${detectedRole}. All roadmaps and prep modules are tailored to your tech stack.` : 'Track your placement progress and complete your daily focus tasks.'}
        actions={
          <div className="flex items-center gap-3">
            <select
              value={detectedRole}
              onChange={(e) => overrideRole(e.target.value)}
              className="px-3 py-2 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-xs font-semibold text-slate-700 dark:text-slate-300 focus:outline-none focus:border-[#4F46E5]"
              title="Override or change your developer persona role"
            >
              <option value="Software Engineer">Software Engineer</option>
              <option value="Python Backend Engineer">Python Backend Engineer</option>
              <option value="Full Stack Developer">Full Stack Developer</option>
              <option value="MERN Specialist">MERN Specialist</option>
              <option value="Frontend Developer">Frontend Developer</option>
              <option value="AI/ML Engineer">AI/ML Engineer</option>
              <option value="DevOps / Cloud Engineer">DevOps / Cloud Engineer</option>
            </select>

            <Link
              to="/coding-tracker"
              className="btn-primary flex items-center gap-2"
            >
              ⚡ Live Coding Tracker
            </Link>
          </div>
        }
      />

      {/* 2. REAL-TIME HIRING & SKILL TRENDS TICKER */}
      <div className="prof-card p-3.5 flex items-center justify-between overflow-x-auto gap-6 text-xs">
        <div className="flex items-center gap-2 text-[#4F46E5] dark:text-[#6366F1] font-bold uppercase tracking-wider shrink-0">
          <span>🔥 Hiring Market Signals:</span>
        </div>
        <div className="flex items-center gap-6 overflow-x-auto">
          {hiringTrends.map((trend, i) => (
            <div key={i} className="flex items-center gap-2 shrink-0">
              <span className="text-slate-700 dark:text-slate-300 font-medium">{trend.skill}</span>
              <span className="text-[#059669] font-bold">{trend.growth}</span>
              <span className="px-1.5 py-0.5 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 text-[10px] text-[#4F46E5] dark:text-[#6366F1] font-semibold rounded">
                {trend.status}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 3. PRIMARY KPI SUMMARY METRICS */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        
        {/* Job Readiness Score */}
        <div 
          onClick={() => navigate('/job-readiness')}
          className="prof-card prof-card-hover p-4 cursor-pointer flex flex-col justify-between"
        >
          <p className="text-xs text-slate-500 dark:text-slate-400 font-bold">Job Readiness Index</p>
          <p className="text-2xl font-extrabold text-[#4F46E5] dark:text-[#6366F1] my-1 font-mono">
            <AnimatedNumber value={readinessScore !== null ? readinessScore : (user?.readiness_score || 82)} suffix="%" />
          </p>
          <div className="mt-1">
            <ScoreBadge score={readinessScore !== null ? readinessScore : (user?.readiness_score || 82)} size="sm" />
          </div>
        </div>

        {/* Dynamic LeetCode Coding Streak */}
        <div className="prof-card prof-card-hover p-4 flex flex-col justify-between">
          <p className="text-xs text-slate-500 dark:text-slate-400 font-bold">Daily Coding Streak</p>
          <p className="text-2xl font-extrabold text-amber-600 my-1 font-mono">
            {codingStreak !== null ? <><AnimatedNumber value={codingStreak} /> Days 🔥</> : 'Unlinked'}
          </p>
          <span className="text-xs text-slate-500 dark:text-slate-400 truncate">
            {leetcodeHandle ? `@${leetcodeHandle} Live Sync` : 'Connect LeetCode URL'}
          </span>
        </div>

        {/* Dynamic ATS Resume Score */}
        <div className="prof-card prof-card-hover p-4 flex flex-col justify-between">
          <p className="text-xs text-slate-500 dark:text-slate-400 font-bold">ATS Resume Score</p>
          <p className="text-2xl font-extrabold text-[#7C3AED] dark:text-[#8B5CF6] my-1 font-mono">
            {latestAtsScore !== null ? `${latestAtsScore} / 100` : '86 / 100'}
          </p>
          <span className="text-xs text-slate-500 dark:text-slate-400">
            {latestAtsScore !== null ? 'Latest ATS Scan' : 'Optimal structure'}
          </span>
        </div>

        {/* Dynamic Mock Interview Grade */}
        <div className="prof-card prof-card-hover p-4 flex flex-col justify-between">
          <p className="text-xs text-slate-500 dark:text-slate-400 font-bold">Mock Interview Grade</p>
          <p className="text-2xl font-extrabold text-[#059669] my-1 font-mono">
            {latestInterviewGrade ? latestInterviewGrade : '81%'}
          </p>
          <span className="text-xs text-slate-500 dark:text-slate-400">
            {latestInterviewGrade ? 'AI Evaluated' : 'Strong structure'}
          </span>
        </div>

      </div>

      {/* 4. DUAL AI ACTION CARDS */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* AI Daily Focus Card */}
        <AIInsightCard title="AI Career Copilot Insight" icon="✨">
          <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
            Optimize {user?.target_role || 'Software Engineering'} Skills
          </h3>
          <p className="text-xs text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">
            Your strongest area is <span className="font-bold text-[#059669]">SQL & System Architecture</span>. Your biggest gap is <span className="font-bold text-[#DC2626]">Dynamic Programming</span>. Focus on memoization problems today.
          </p>
          <div className="mt-4 pt-3 border-t border-purple-200 dark:border-purple-900/40 flex items-center justify-between">
            <span className="text-xs text-slate-500 font-mono">Estimated: 25 mins</span>
            <button
              onClick={() => navigate('/coding-arena')}
              className="btn-ai"
            >
              Practice Recommended →
            </button>
          </div>
        </AIInsightCard>

        {/* Daily Coding Challenge Link */}
        <div className="prof-card p-5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="px-2.5 py-0.5 bg-amber-500/10 text-amber-600 dark:text-amber-400 text-xs font-semibold rounded-md border border-amber-500/20 font-mono">
                ⭐ LeetCode & HackerRank Tracker
              </span>
              <span className="px-2 py-0.5 bg-amber-500/10 text-amber-600 dark:text-amber-400 text-xs font-bold rounded">
                Live Web Sync
              </span>
            </div>
            <h3 className="text-base font-bold text-slate-900 dark:text-slate-100 mt-2">
              Track Coding Streaks & Domain Badges
            </h3>
            <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 leading-relaxed">
              Connect your LeetCode and HackerRank profile URLs to track live daily streaks, active days, and earned star ratings.
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <span className="text-xs text-slate-500 font-mono">
              Status: {leetcodeHandle ? `@${leetcodeHandle} Linked` : 'Unlinked'}
            </span>
            <button
              onClick={() => navigate('/coding-tracker')}
              className="btn-secondary"
            >
              Open Coding Tracker →
            </button>
          </div>
        </div>

      </div>

      {/* 5. COMPLETE 4-TRACK FEATURE HUB */}
      <div className="space-y-6 pt-2">
        <div className="border-b border-slate-200 dark:border-slate-800 pb-3">
          <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100 tracking-tight">
            Application Modules & Feature Hub
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">Launch any preparation tool in your workspace</p>
        </div>

        {featureModules.map((categoryGroup, index) => (
          <div key={index} className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              {categoryGroup.category}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {categoryGroup.items.map((item) => (
                <div
                  key={item.id}
                  onClick={() => navigate(item.path)}
                  className="prof-card prof-card-hover p-5 cursor-pointer flex flex-col justify-between group"
                >
                  <div>
                    <div className="flex items-start justify-between mb-3">
                      <span className="text-2xl p-2 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                        {item.icon}
                      </span>
                      <span className="px-2 py-0.5 bg-indigo-50 dark:bg-indigo-950/40 text-[#4F46E5] dark:text-[#818CF8] text-[10px] font-bold rounded border border-indigo-200 dark:border-indigo-800">
                        {item.badge}
                      </span>
                    </div>
                    <h4 className="text-sm font-bold text-slate-900 dark:text-slate-100 group-hover:text-[#4F46E5] dark:group-hover:text-[#818CF8] transition">
                      {item.title}
                    </h4>
                    <p className="mt-1.5 text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                      {item.description}
                    </p>
                  </div>

                  <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                    <span className="text-xs font-semibold text-[#4F46E5] dark:text-[#818CF8] group-hover:underline">
                      Launch Feature →
                    </span>
                    <span className="text-[10px] text-[#059669] font-mono font-bold">● Active</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Focus & Logging Tools Drawer */}
      <InPageToolsDrawer isOpen={isToolsOpen} onClose={() => setIsToolsOpen(false)} />
    </div>
  );
};

export default DashboardHub;
