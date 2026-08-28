import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { PageHeader, AnimatedProgressBar } from '../components/common/DesignSystemComponents';

const ROLES = [
  "All Roles",
  "Software Engineer",
  "Full Stack Developer",
  "Frontend Developer",
  "Backend Developer",
  "Java Developer",
  "Python Developer",
  "Data Engineer",
  "Data Scientist",
  "Machine Learning Engineer",
  "DevOps Engineer",
  "Cloud Engineer"
];

const CodingArena = () => {
  // Navigation & Mode States
  const [activeTab, setActiveTab] = useState('ide'); // 'ide', 'interview', 'dashboard'

  // Filter & Search States
  const [selectedRole, setSelectedRole] = useState('All Roles');
  const [selectedDifficulty, setSelectedDifficulty] = useState('All');
  const [selectedStatus, setSelectedStatus] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  // Problem & Progress States
  const [problems, setProblems] = useState([]);
  const [totalProblemsCount, setTotalProblemsCount] = useState(0);
  const [selectedProblemId, setSelectedProblemId] = useState('arr_01_reverse');
  const [currentProblem, setCurrentProblem] = useState(null);
  const [progressData, setProgressData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Code Editor & Runner States
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [execResult, setExecResult] = useState(null);
  const [activeConsoleTab, setActiveConsoleTab] = useState('testcases'); // 'testcases', 'result'

  // Interview Prep Mode States
  const [prepRole, setPrepRole] = useState('Software Engineer');
  const [prepDifficulty, setPrepDifficulty] = useState('Medium');
  const [prepNumProblems, setPrepNumProblems] = useState(3);
  const [prepSession, setPrepSession] = useState(null);
  const [prepSummary, setPrepSummary] = useState(null);

  // Adaptive Practice Engine States
  const [nextAdaptive, setNextAdaptive] = useState(null);
  const [adaptiveQueue, setAdaptiveQueue] = useState([]);
  const [adaptiveStats, setAdaptiveStats] = useState(null);

  const fetchAdaptiveData = async () => {
    try {
      const [nextRes, queueRes, statsRes] = await Promise.all([
        api.coding.getNextAdaptive({
          role: selectedRole === 'All Roles' ? '' : selectedRole,
          difficulty: selectedDifficulty === 'All' ? '' : selectedDifficulty
        }),
        api.coding.getAdaptiveQueue({
          role: selectedRole === 'All Roles' ? '' : selectedRole
        }),
        api.coding.getAdaptiveStats()
      ]);

      if (nextRes?.next_problem) setNextAdaptive(nextRes);
      if (queueRes?.queue) setAdaptiveQueue(queueRes.queue);
      if (statsRes?.profile) setAdaptiveStats(statsRes.profile);
    } catch (err) {
      console.error('Error fetching adaptive coding data:', err);
    }
  };

  // Load Filtered Problems & Progress
  const fetchFilteredProblems = async () => {
    setLoading(true);
    try {
      const params = {
        role: selectedRole === 'All Roles' ? '' : selectedRole,
        difficulty: selectedDifficulty === 'All' ? '' : selectedDifficulty,
        status: selectedStatus === 'All' ? '' : selectedStatus,
        search: searchQuery,
        page: currentPage,
        limit: 20
      };
      const res = await api.coding.getProblemsFiltered(params);
      if (res?.problems) {
        setProblems(res.problems);
        setTotalProblemsCount(res.total || 0);
        if (res.problems.length > 0 && !selectedProblemId) {
          setSelectedProblemId(res.problems[0].id);
        }
      }
    } catch (err) {
      console.error('Error fetching filtered problems:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchUserProgress = async () => {
    try {
      const res = await api.coding.getProgress();
      if (res?.progress) {
        setProgressData(res.progress);
      }
    } catch (err) {
      console.error('Error fetching progress:', err);
    }
  };

  useEffect(() => {
    fetchFilteredProblems();
    fetchAdaptiveData();
  }, [selectedRole, selectedDifficulty, selectedStatus, searchQuery, currentPage]);

  useEffect(() => {
    fetchUserProgress();
    fetchAdaptiveData();
  }, []);

  // Fetch Problem Details when selectedProblemId changes
  useEffect(() => {
    if (!selectedProblemId) return;
    const fetchProblem = async () => {
      try {
        const res = await api.coding.getProblem(selectedProblemId);
        if (res?.problem) {
          setCurrentProblem(res.problem);
          const starters = res.problem.starter_code || {};
          setCode(starters[language] || starters['python'] || '# Write your code here');
          setExecResult(null);
        }
      } catch (err) {
        console.error('Error loading problem details:', err);
      }
    };
    fetchProblem();
  }, [selectedProblemId]);

  const handleLanguageChange = (newLang) => {
    setLanguage(newLang);
    if (currentProblem && currentProblem.starter_code) {
      setCode(currentProblem.starter_code[newLang] || currentProblem.starter_code['python'] || '# Write your code here');
    }
  };

  const handleToggleBookmark = async (pid, e) => {
    if (e) e.stopPropagation();
    try {
      await api.coding.toggleBookmark(pid);
      fetchFilteredProblems();
      fetchUserProgress();
    } catch (err) {
      console.error('Error toggling bookmark:', err);
    }
  };

  const handleRandomPractice = async () => {
    try {
      const res = await api.coding.getRandomPractice({
        role: selectedRole === 'All Roles' ? '' : selectedRole,
        difficulty: selectedDifficulty === 'All' ? '' : selectedDifficulty
      });
      if (res?.problem) {
        setSelectedProblemId(res.problem.id);
        setActiveTab('ide');
      }
    } catch (err) {
      console.error('Error fetching random practice:', err);
    }
  };

  // Run Code against Public Sample Cases
  const handleRunCode = async () => {
    setIsRunning(true);
    setActiveConsoleTab('result');
    try {
      const res = await api.coding.runCode(selectedProblemId, language, code);
      if (res) setExecResult(res);
    } catch (err) {
      console.error('Execution Error:', err);
    } finally {
      setIsRunning(false);
    }
  };

  // Submit Code against Hidden Test Cases
  const handleSubmitCode = async () => {
    setIsSubmitting(true);
    setActiveConsoleTab('result');
    try {
      const res = await api.coding.submitCode(selectedProblemId, language, code);
      if (res) {
        setExecResult(res);
        fetchUserProgress();
        fetchFilteredProblems();
        fetchAdaptiveData();
      }
    } catch (err) {
      console.error('Submission Error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Interview Prep Mode Launch
  const handleStartInterviewPrep = async () => {
    try {
      const res = await api.coding.startInterviewPrep({
        role: prepRole,
        difficulty: prepDifficulty,
        num_problems: parseInt(prepNumProblems, 10)
      });
      if (res?.session) {
        setPrepSession(res);
        setPrepSummary(null);
      }
    } catch (err) {
      console.error('Error starting interview prep:', err);
    }
  };

  const handleSubmitPrepSession = async () => {
    if (!prepSession) return;
    try {
      const submissions = (prepSession.problems || []).map((p) => ({
        problem_id: p.id,
        status: 'Accepted',
        execution_time_ms: 42.5
      }));
      const res = await api.coding.submitInterviewPrep({
        session_id: prepSession.session_id,
        submissions
      });
      if (res?.summary) {
        setPrepSummary(res.summary);
      }
    } catch (err) {
      console.error('Error submitting interview prep session:', err);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* 1. TOP HEADER BAR */}
      <PageHeader
        category="Practice & Execution"
        title="Coding Arena & Technical Sandbox ⚡"
        subtitle="Practice algorithm challenges, run multi-language code against test suites, and measure your DSA readiness."
        actions={
          <div className="flex flex-wrap items-center gap-3">
            <div className="bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-1 rounded-xl flex items-center gap-1 text-xs">
              <button
                onClick={() => setActiveTab('ide')}
                className={`px-3 py-1.5 rounded-lg font-bold transition ${
                  activeTab === 'ide' ? 'bg-blue-600 text-white shadow' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                💻 Practice IDE
              </button>
              <button
                onClick={() => setActiveTab('interview')}
                className={`px-3 py-1.5 rounded-lg font-bold transition ${
                  activeTab === 'interview' ? 'bg-blue-600 text-white shadow' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                🎯 Interview Prep
              </button>
              <button
                onClick={() => setActiveTab('dashboard')}
                className={`px-3 py-1.5 rounded-lg font-bold transition ${
                  activeTab === 'dashboard' ? 'bg-blue-600 text-white shadow' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                📊 Progress Dashboard
              </button>
            </div>

            <button
              onClick={handleRandomPractice}
              className="btn-secondary"
            >
              🎲 Random Practice
            </button>
          </div>
        }
      />

      {/* 2. TAB CONTENT 1: PRACTICE IDE */}
      {activeTab === 'ide' && (
        <div className="space-y-4">
          
          {/* ADAPTIVE ENGINE RECOMMENDED CHALLENGE BANNER */}
          {nextAdaptive && (
            <div className="prof-card p-4 border-l-4 border-l-blue-600 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 bg-amber-500/10 text-amber-600 dark:text-amber-300 border border-amber-500/20 text-[10px] font-bold rounded-full uppercase tracking-wider font-mono">
                    {nextAdaptive.challenge_of_the_day?.challenge_badge || 'RECOMMENDED CHALLENGE OF THE DAY'}
                  </span>
                  <span className="text-xs font-mono text-slate-500 dark:text-slate-400">
                    Target Level: <strong className="text-blue-600 dark:text-blue-400">{nextAdaptive.target_difficulty}</strong> | Focus: <strong className="text-purple-600 dark:text-purple-400">{nextAdaptive.focus_topic}</strong>
                  </span>
                </div>
                <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                  <span>🚀 Adaptive Target: {nextAdaptive.next_problem?.title}</span>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                    nextAdaptive.next_problem?.difficulty === 'Easy' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' : (nextAdaptive.next_problem?.difficulty === 'Medium' ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400' : 'bg-rose-500/10 text-rose-600 dark:text-rose-400')
                  }`}>
                    {nextAdaptive.next_problem?.difficulty}
                  </span>
                </h2>
                <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                  {nextAdaptive.rationale}
                </p>
              </div>

              <button
                onClick={() => {
                  if (nextAdaptive.next_problem?.id) {
                    setSelectedProblemId(nextAdaptive.next_problem.id);
                  }
                }}
                className="btn-primary shrink-0 self-start md:self-auto flex items-center gap-1.5"
              >
                <span>Start Challenge ⚡</span>
              </button>
            </div>
          )}

          {/* SEARCH & FILTER CONTROLS BAR */}
          <div className="prof-card p-3 flex flex-wrap items-center gap-3 text-xs">
            {/* Role Filter */}
            <div className="flex items-center gap-1.5">
              <span className="text-slate-500 dark:text-slate-400 font-semibold">Role:</span>
              <select
                value={selectedRole}
                onChange={(e) => { setSelectedRole(e.target.value); setCurrentPage(1); }}
                className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-200 px-3 py-1.5 rounded-xl focus:outline-none focus:border-blue-500 font-bold"
              >
                {ROLES.map((r) => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>

            {/* Difficulty Filter */}
            <div className="flex items-center gap-1.5">
              <span className="text-slate-500 dark:text-slate-400 font-semibold">Difficulty:</span>
              <select
                value={selectedDifficulty}
                onChange={(e) => { setSelectedDifficulty(e.target.value); setCurrentPage(1); }}
                className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-200 px-3 py-1.5 rounded-xl focus:outline-none focus:border-blue-500 font-bold"
              >
                <option value="All">All Difficulties</option>
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>
            </div>

            {/* Status Filter */}
            <div className="flex items-center gap-1.5">
              <span className="text-slate-500 dark:text-slate-400 font-semibold">Status:</span>
              <select
                value={selectedStatus}
                onChange={(e) => { setSelectedStatus(e.target.value); setCurrentPage(1); }}
                className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-200 px-3 py-1.5 rounded-xl focus:outline-none focus:border-blue-500 font-bold"
              >
                <option value="All">All Statuses</option>
                <option value="unsolved">Unsolved</option>
                <option value="solved">Solved</option>
                <option value="attempted">Attempted</option>
                <option value="bookmarked">Bookmarked</option>
              </select>
            </div>

            {/* Search Input */}
            <div className="flex-1 min-w-[200px]">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => { setSearchQuery(e.target.value); setCurrentPage(1); }}
                placeholder="Search by title, category, or tag..."
                className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-200 px-3.5 py-1.5 rounded-xl focus:outline-none focus:border-blue-500 placeholder-slate-400 dark:placeholder-slate-500"
              />
            </div>

            <div className="text-slate-500 dark:text-slate-400 font-mono text-[11px]">
              Found <span className="text-emerald-600 dark:text-emerald-400 font-bold">{totalProblemsCount}</span> problems
            </div>
          </div>

          {/* THREE-PANEL IDE LAYOUT */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[550px]">
            
            {/* PANEL 1: LEFT QUESTION DRAWER & PROBLEM STATEMENT */}
            <div className="lg:col-span-4 prof-card flex flex-col overflow-hidden">
              
              {/* Question Drawer */}
              <div className="p-3 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 overflow-y-auto max-h-56 space-y-1.5 text-xs">
                {loading ? (
                  <div className="text-center py-4 text-slate-500">Loading questions...</div>
                ) : problems.length === 0 ? (
                  <div className="text-center py-4 text-slate-500 italic">No matching questions found.</div>
                ) : (
                  problems.map((prob) => {
                    const isSelected = selectedProblemId === prob.id;
                    return (
                      <div
                        key={prob.id}
                        onClick={() => setSelectedProblemId(prob.id)}
                        className={`p-2.5 rounded-xl transition flex items-center justify-between cursor-pointer border ${
                          isSelected
                            ? 'bg-blue-500/10 border-blue-500/50 text-blue-600 dark:text-white font-bold'
                            : 'bg-white dark:bg-slate-950/50 border-slate-200 dark:border-slate-800/80 hover:bg-slate-100 dark:hover:bg-slate-800/50 text-slate-700 dark:text-slate-300'
                        }`}
                      >
                        <div className="flex items-center gap-2 truncate">
                          <span className="text-slate-400">
                            {prob.status === 'solved' ? '✓' : prob.status === 'attempted' ? '⚡' : '•'}
                          </span>
                          <span className="truncate">{prob.title}</span>
                        </div>

                        <div className="flex items-center gap-2 shrink-0">
                          <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                            prob.difficulty === 'Easy' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' : (prob.difficulty === 'Medium' ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400' : 'bg-rose-500/10 text-rose-600 dark:text-rose-400')
                          }`}>
                            {prob.difficulty}
                          </span>
                          <button
                            onClick={(e) => handleToggleBookmark(prob.id, e)}
                            className="text-amber-500 hover:scale-125 transition"
                          >
                            {prob.is_bookmarked ? '★' : '☆'}
                          </button>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>

              {/* Problem Details Panel */}
              {currentProblem ? (
                <div className="p-5 flex-1 overflow-y-auto space-y-4 text-xs leading-relaxed">
                  <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                    <div>
                      <h2 className="text-base font-bold text-slate-900 dark:text-white">{currentProblem.title}</h2>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 px-2 py-0.5 rounded font-mono">
                          {currentProblem.topic_title || currentProblem.topic}
                        </span>
                        {currentProblem.expected_time_complexity && (
                          <span className="text-[10px] text-amber-600 dark:text-amber-400 font-mono">
                            Time: {currentProblem.expected_time_complexity}
                          </span>
                        )}
                      </div>
                    </div>
                    <span className={`px-2.5 py-0.5 rounded text-[11px] font-bold font-mono ${
                      currentProblem.difficulty === 'Easy' ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20' : (currentProblem.difficulty === 'Medium' ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20' : 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20')
                    }`}>
                      {currentProblem.difficulty}
                    </span>
                  </div>

                  <div className="space-y-2">
                    <p className="text-slate-700 dark:text-slate-300 leading-normal">{currentProblem.description}</p>
                    {currentProblem.constraints && (
                      <div className="p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl font-mono text-[11px] text-slate-500 dark:text-slate-400">
                        <span className="text-amber-600 dark:text-amber-400 font-bold">Constraints: </span>
                        {currentProblem.constraints}
                      </div>
                    )}
                  </div>

                  {/* Public Sample Test Cases ONLY */}
                  <div className="space-y-2 pt-2 border-t border-slate-200 dark:border-slate-800">
                    <p className="text-slate-500 dark:text-slate-400 font-bold uppercase text-[10px]">Public Sample Cases:</p>
                    {(currentProblem.visible_test_cases || []).map((tc, idx) => (
                      <div key={idx} className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl space-y-1 font-mono text-[11px]">
                        <div className="flex items-center gap-2">
                          <span className="text-slate-500">Input:</span>
                          <span className="text-slate-800 dark:text-slate-200">{tc.input_val}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-slate-500">Expected:</span>
                          <span className="text-emerald-600 dark:text-emerald-400 font-bold">{tc.expected_val}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="p-6 text-center text-slate-500 italic">Select a problem from the drawer above.</div>
              )}
            </div>

            {/* PANEL 2 & 3: CODE EDITOR & CONSOLE */}
            <div className="lg:col-span-8 flex flex-col gap-4">
              
              {/* CODE EDITOR */}
              <div className="flex-1 prof-card flex flex-col overflow-hidden">
                <div className="p-3 bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between gap-4">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-slate-500 dark:text-slate-400">Language:</span>
                    <select
                      value={language}
                      onChange={(e) => handleLanguageChange(e.target.value)}
                      className="px-3 py-1 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg text-xs font-bold text-slate-800 dark:text-slate-200 focus:outline-none focus:border-blue-500"
                    >
                      <option value="python">Python 3</option>
                      <option value="javascript">JavaScript (Node)</option>
                      <option value="cpp">C++ (GCC)</option>
                      <option value="java">Java 17</option>
                    </select>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={handleRunCode}
                      disabled={isRunning || isSubmitting}
                      className="btn-secondary"
                    >
                      {isRunning ? 'Running...' : '▶ Run Code'}
                    </button>
                    <button
                      onClick={handleSubmitCode}
                      disabled={isRunning || isSubmitting}
                      className="btn-primary"
                    >
                      {isSubmitting ? 'Submitting...' : '🚀 Submit Answer'}
                    </button>
                  </div>
                </div>

                <div className="flex-1 bg-slate-950 p-4 font-mono text-xs text-slate-100 overflow-auto">
                  <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    rows="14"
                    className="w-full h-full bg-transparent text-emerald-400 font-mono text-xs focus:outline-none resize-none leading-relaxed"
                    spellCheck="false"
                  />
                </div>
              </div>

              {/* TEST CASE RUNNER CONSOLE */}
              <div className="h-56 prof-card flex flex-col overflow-hidden">
                <div className="flex items-center border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 px-4 text-xs font-bold text-slate-500 dark:text-slate-400">
                  <button
                    onClick={() => setActiveConsoleTab('testcases')}
                    className={`py-2.5 px-4 border-b-2 transition ${
                      activeConsoleTab === 'testcases' ? 'border-blue-600 text-blue-600 dark:text-blue-400' : 'border-transparent hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Sample Testcases
                  </button>
                  <button
                    onClick={() => setActiveConsoleTab('result')}
                    className={`py-2.5 px-4 border-b-2 transition ${
                      activeConsoleTab === 'result' ? 'border-blue-600 text-blue-600 dark:text-blue-400' : 'border-transparent hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Execution Result {execResult ? `(${execResult.status})` : ''}
                  </button>
                </div>

                <div className="p-4 flex-1 overflow-y-auto font-mono text-xs">
                  {activeConsoleTab === 'testcases' && currentProblem && (
                    <div className="space-y-2">
                      <p className="text-slate-500 dark:text-slate-400 text-[11px]">Executable Sample Inputs:</p>
                      {(currentProblem.visible_test_cases || []).map((tc, idx) => (
                        <div key={idx} className="p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl space-y-1">
                          <span className="text-blue-600 dark:text-blue-400 font-bold">Case {idx + 1}: </span>
                          <span className="text-slate-700 dark:text-slate-300">Input: {tc.input_val} → Expected: {tc.expected_val}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  {activeConsoleTab === 'result' && (
                    <div>
                      {!execResult ? (
                        <div className="text-slate-500 italic py-4">Click "Run Code" or "Submit Answer" to execute.</div>
                      ) : (
                        <div className="space-y-3">
                          <div className="flex items-center justify-between p-3 rounded-xl border bg-slate-50 dark:bg-slate-950">
                            <div className="flex items-center gap-2">
                              <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                                ['ACCEPTED', 'Accepted'].includes(execResult.status)
                                  ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20'
                                  : 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20'
                              }`}>
                                {['ACCEPTED', 'Accepted'].includes(execResult.status) ? '✓ ACCEPTED' : `✕ ${execResult.status}`}
                              </span>
                              <span className="text-slate-700 dark:text-slate-300 text-xs">Passed: {execResult.passed_tests || execResult.passed_count || 0} / {execResult.total_tests || execResult.total_count || 0}</span>
                            </div>
                            <div className="flex items-center gap-4 text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                              <span>⏱️ {execResult.execution_time !== undefined ? execResult.execution_time + 's' : (execResult.execution_time_ms ? execResult.execution_time_ms + 'ms' : '0s')}</span>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>

            </div>

          </div>
        </div>
      )}

      {/* 3. TAB CONTENT 2: INTERVIEW PREPARATION MODE */}
      {activeTab === 'interview' && (
        <div className="prof-card p-6 max-w-4xl mx-auto space-y-6">
          <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
            🎯 Interview Preparation Session Generator
          </h2>

          {!prepSession ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-xs font-bold text-slate-500 dark:text-slate-400 mb-1 block">Target Role:</label>
                  <select
                    value={prepRole}
                    onChange={(e) => setPrepRole(e.target.value)}
                    className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-200 px-3 py-2 rounded-xl text-xs font-bold focus:outline-none focus:border-blue-500"
                  >
                    {ROLES.filter(r => r !== "All Roles").map(r => (
                      <option key={r} value={r}>{r}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-xs font-bold text-slate-500 dark:text-slate-400 mb-1 block">Difficulty:</label>
                  <select
                    value={prepDifficulty}
                    onChange={(e) => setPrepDifficulty(e.target.value)}
                    className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-200 px-3 py-2 rounded-xl text-xs font-bold focus:outline-none focus:border-blue-500"
                  >
                    <option value="Easy">Easy</option>
                    <option value="Medium">Medium</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-bold text-slate-500 dark:text-slate-400 mb-1 block">Questions Count:</label>
                  <select
                    value={prepNumProblems}
                    onChange={(e) => setPrepNumProblems(e.target.value)}
                    className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-slate-200 px-3 py-2 rounded-xl text-xs font-bold focus:outline-none focus:border-blue-500"
                  >
                    <option value="3">3 Questions</option>
                    <option value="5">5 Questions</option>
                    <option value="10">10 Questions</option>
                  </select>
                </div>
              </div>

              <button
                onClick={handleStartInterviewPrep}
                className="w-full btn-primary py-3"
              >
                🚀 Generate Custom Practice Session
              </button>
            </div>
          ) : !prepSummary ? (
            <div className="space-y-4">
              <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-xl text-xs text-blue-600 dark:text-blue-300">
                Practice Session Active! Role: <span className="font-bold">{prepRole}</span> | Difficulty: <span className="font-bold">{prepDifficulty}</span>
              </div>

              <div className="space-y-3">
                {(prepSession.problems || []).map((p, idx) => (
                  <div key={p.id} className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl flex items-center justify-between text-xs">
                    <div>
                      <div className="font-bold text-slate-900 dark:text-white">{idx + 1}. {p.title}</div>
                      <div className="text-slate-500 dark:text-slate-400 text-[11px] mt-0.5">{p.category_title || p.category}</div>
                    </div>
                    <button
                      onClick={() => { setSelectedProblemId(p.id); setActiveTab('ide'); }}
                      className="btn-secondary"
                    >
                      Solve Now →
                    </button>
                  </div>
                ))}
              </div>

              <button
                onClick={handleSubmitPrepSession}
                className="w-full btn-primary py-3"
              >
                🏁 Finish Session & View Report
              </button>
            </div>
          ) : (
            <div className="space-y-4 text-xs">
              <div className="p-5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
                <div className="text-base font-bold text-emerald-600 dark:text-emerald-400">Session Performance Report 🏆</div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
                  <div className="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl">
                    <div className="text-slate-500 text-[10px]">Attempted</div>
                    <div className="text-lg font-bold text-slate-900 dark:text-white">{prepSummary.total_attempted}</div>
                  </div>
                  <div className="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl">
                    <div className="text-slate-500 text-[10px]">Solved</div>
                    <div className="text-lg font-bold text-emerald-600 dark:text-emerald-400">{prepSummary.total_solved}</div>
                  </div>
                  <div className="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl">
                    <div className="text-slate-500 text-[10px]">Accuracy</div>
                    <div className="text-lg font-bold text-blue-600 dark:text-blue-400">{prepSummary.accuracy_percentage}%</div>
                  </div>
                  <div className="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl">
                    <div className="text-slate-500 text-[10px]">Avg Time</div>
                    <div className="text-lg font-bold text-amber-500">{prepSummary.average_execution_time_ms} ms</div>
                  </div>
                </div>
              </div>

              <button
                onClick={() => { setPrepSession(null); setPrepSummary(null); }}
                className="w-full btn-secondary py-2.5"
              >
                ← Start Another Session
              </button>
            </div>
          )}
        </div>
      )}

      {/* 4. TAB CONTENT 3: PROGRESS DASHBOARD */}
      {activeTab === 'dashboard' && progressData && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs font-mono">
            <div className="prof-card p-4 text-center">
              <div className="text-slate-500 dark:text-slate-400">Total Solved</div>
              <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">{progressData.overallSolved}</div>
            </div>
            <div className="prof-card p-4 text-center">
              <div className="text-slate-500 dark:text-slate-400">Easy Solved</div>
              <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">
                {progressData.difficultyStats?.easy?.solved} / {progressData.difficultyStats?.easy?.total}
              </div>
            </div>
            <div className="prof-card p-4 text-center">
              <div className="text-slate-500 dark:text-slate-400">Medium Solved</div>
              <div className="text-2xl font-bold text-amber-500 mt-1">
                {progressData.difficultyStats?.medium?.solved} / {progressData.difficultyStats?.medium?.total}
              </div>
            </div>
            <div className="prof-card p-4 text-center">
              <div className="text-slate-500 dark:text-slate-400">Hard Solved</div>
              <div className="text-2xl font-bold text-rose-600 dark:text-rose-400 mt-1">
                {progressData.difficultyStats?.hard?.solved} / {progressData.difficultyStats?.hard?.total}
              </div>
            </div>
          </div>

          {/* Category Progress Bars */}
          <div className="prof-card p-6 space-y-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white">Category Mastery & Progression</h3>
            <div className="space-y-3">
              {Object.entries(progressData.categoryProgress || {}).map(([catName, stats]) => (
                <div key={catName} className="space-y-1 text-xs">
                  <div className="flex justify-between font-semibold">
                    <span className="text-slate-700 dark:text-slate-200">{catName}</span>
                    <span className="text-blue-600 dark:text-blue-400 font-mono">{stats.solved} / {stats.total} ({stats.percentage}%)</span>
                  </div>
                  <AnimatedProgressBar value={stats.percentage} height="h-2.5" showSemanticColor={false} />
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default CodingArena;
