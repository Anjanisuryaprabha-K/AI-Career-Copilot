import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { useUserProfile } from '../contexts/UserProfileContext';
import { PageHeader, ScoreBadge, AIInsightCard, AnimatedProgressBar } from '../components/common/DesignSystemComponents';

// Radial ATS Score Gauge Component
const RadialScoreGauge = ({ score }) => {
  const radius = 68;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let colorClass = 'text-[#4F46E5] dark:text-[#6366F1]';

  if (score < 50) {
    colorClass = 'text-[#DC2626]';
  } else if (score < 75) {
    colorClass = 'text-[#D97706]';
  }

  return (
    <div className="flex flex-col items-center justify-center p-6 prof-card relative shadow-inner">
      <div className="relative w-40 h-40 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
          <circle
            cx="80"
            cy="80"
            r={radius}
            className="text-slate-200 dark:text-slate-800"
            strokeWidth="12"
            stroke="currentColor"
            fill="transparent"
          />
          <circle
            cx="80"
            cy="80"
            r={radius}
            className={`${colorClass} transition-all duration-1000 ease-out`}
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            stroke="currentColor"
            fill="transparent"
          />
        </svg>

        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-4xl font-extrabold text-slate-900 dark:text-white font-mono tracking-tighter">{score}</span>
          <span className="text-[10px] text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider mt-0.5">ATS Score</span>
        </div>
      </div>

      <div className="mt-3">
        <ScoreBadge score={score} size="md" />
      </div>
    </div>
  );
};

const ResumeAnalyzer = () => {
  const { user } = useAuth();
  const { rehydrateProfile } = useUserProfile();

  // Input Controls
  const [activeInputMode, setActiveInputMode] = useState('file'); // 'file' or 'text'
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [resumeText, setResumeText] = useState('');
  const [targetRole, setTargetRole] = useState('Software Engineer');
  const [customJd, setCustomJd] = useState('');
  const [companyName, setCompanyName] = useState('');

  // Status & Progress States
  const [analyzing, setAnalyzing] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [errorMsg, setErrorMsg] = useState('');

  // Analysis Result & Display State
  const [analysisResult, setAnalysisResult] = useState(null);
  const [activeTab, setActiveTab] = useState('overview'); // 'overview', 'roadmap', 'structured', 'jdmatch', 'breakdown', 'typos', 'history'
  const [actionChecklist, setActionChecklist] = useState([]);
  const [completedRoadmapTasks, setCompletedRoadmapTasks] = useState({});

  const toggleRoadmapTask = (taskId) => {
    setCompletedRoadmapTasks(prev => ({ ...prev, [taskId]: !prev[taskId] }));
  };
  
  // History State
  const [historyList, setHistoryList] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  // Fetch scan history on component mount
  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    setLoadingHistory(true);
    try {
      const res = await api.resume.getHistory();
      if (res?.scans) {
        setHistoryList(res.scans);
      }
    } catch (err) {
      console.warn('Failed to load scan history:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  // Drag & Drop Handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file) => {
    setErrorMsg('');
    const ext = file.name.split('.').pop().toLowerCase();
    if (ext !== 'pdf' && ext !== 'docx') {
      setErrorMsg('Invalid file format. Only .pdf and .docx documents are supported.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setErrorMsg('File size exceeds the 5MB limit. Please upload a smaller document.');
      return;
    }
    setSelectedFile(file);
  };

  // Run ATS Analysis
  const handleAnalyze = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setAnalyzing(true);
    setUploadProgress(15);

    try {
      let res;
      if (activeInputMode === 'file') {
        if (!selectedFile) {
          setErrorMsg('Please select or drop a valid .pdf / .docx file first.');
          setAnalyzing(false);
          return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('target_role', targetRole);
        formData.append('custom_jd', customJd);
        formData.append('company_name', companyName);

        setUploadProgress(45);
        res = await api.resume.analyzeFile(formData);
        setUploadProgress(85);
      } else {
        if (!resumeText.trim()) {
          setErrorMsg('Please enter or paste your resume text to analyze.');
          setAnalyzing(false);
          return;
        }

        setUploadProgress(50);
        res = await api.resume.analyzeText(resumeText, targetRole, customJd, companyName);
        setUploadProgress(85);
      }

      setUploadProgress(100);
      setTimeout(() => {
        if (res?.data) {
          setAnalysisResult(res.data);
          setActionChecklist(res.data.action_item_checklist || []);
          setActiveTab('overview');
          if (rehydrateProfile) rehydrateProfile();
          fetchHistory(); // Refresh history
        }
        setAnalyzing(false);
      }, 400);

    } catch (err) {
      setErrorMsg(err.message || 'An error occurred during resume analysis. Please try again.');
      setAnalyzing(false);
    }
  };

  const toggleChecklistItem = (id) => {
    setActionChecklist(prev =>
      prev.map(item => item.id === id ? { ...item, resolved: !item.resolved } : item)
    );
  };

  const loadPastScan = (scan) => {
    const data = scan.scan_data || scan;
    setAnalysisResult(data);
    setActionChecklist(data.action_item_checklist || []);
    setActiveTab('overview');
  };

  return (
    <div className="space-y-6">
      
      {/* 1. PAGE HEADER */}
      <PageHeader
        category="Resume Intelligence"
        badgeText="REAL-TIME NLP ENGINE"
        title="AI Resume Analyzer & ATS Scorer 📄"
        subtitle="Extract structured contact info, education, experience, and skills while computing real-time section-level ATS scores and job description match fits."
        actions={
          <div className="flex items-center gap-3">
            <button
              onClick={() => setActiveTab(activeTab === 'history' ? 'overview' : 'history')}
              className="btn-secondary"
            >
              📜 Scan History ({historyList.length})
            </button>

            {analysisResult && (
              <button
                onClick={() => {
                  setAnalysisResult(null);
                  setSelectedFile(null);
                  setResumeText('');
                  setErrorMsg('');
                }}
                className="btn-primary"
              >
                + New Resume Scan
              </button>
            )}
          </div>
        }
      />

      {/* 2. MAIN WORKSPACE CONTENT */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* LEFT FORM PANEL */}
        <div className="lg:col-span-5 prof-card p-6 space-y-5 self-start">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
            <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100">Resume Input Source</h3>
            <div className="flex items-center bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg p-0.5 text-xs">
              <button
                type="button"
                onClick={() => setActiveInputMode('file')}
                className={`px-3 py-1.5 rounded-md font-semibold transition ${
                  activeInputMode === 'file' ? 'bg-blue-600 text-white shadow' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                Upload File (.pdf/.docx)
              </button>
              <button
                type="button"
                onClick={() => setActiveInputMode('text')}
                className={`px-3 py-1.5 rounded-md font-semibold transition ${
                  activeInputMode === 'text' ? 'bg-blue-600 text-white shadow' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                Paste Text
              </button>
            </div>
          </div>

          {errorMsg && (
            <div className="p-3.5 bg-rose-500/10 border border-rose-500/20 rounded-xl text-xs text-rose-600 dark:text-rose-400 font-medium flex items-center justify-between">
              <span>⚠️ {errorMsg}</span>
              <button onClick={() => setErrorMsg('')} className="text-rose-600 dark:text-rose-400 hover:opacity-80 font-bold ml-2">✕</button>
            </div>
          )}

          <form onSubmit={handleAnalyze} className="space-y-4 text-xs">
            
            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-semibold mb-1">Target Engineering Role</label>
              <select
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 focus:outline-none focus:border-blue-500"
              >
                <option value="Software Engineer">Software Engineer</option>
                <option value="Python Backend Engineer">Python Backend Engineer</option>
                <option value="Full Stack Developer">Full Stack Developer</option>
                <option value="MERN Specialist">MERN Specialist</option>
                <option value="Frontend Developer">Frontend Developer</option>
                <option value="Backend Developer">Backend Developer</option>
                <option value="AI/ML Engineer">AI/ML Engineer</option>
                <option value="DevOps / Cloud Engineer">DevOps / Cloud Engineer</option>
                <option value="Data Engineer">Data Engineer</option>
              </select>
            </div>

            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-semibold mb-1">Target Company Name (Optional)</label>
              <input
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="e.g. Google, Amazon, Microsoft..."
                className="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-semibold mb-1">
                Target Job Description (Optional for Tailored Match Analysis)
              </label>
              <textarea
                value={customJd}
                onChange={(e) => setCustomJd(e.target.value)}
                placeholder="Paste job description requirements, responsibilities or skills here to compare against..."
                rows="3"
                className="w-full px-3.5 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-blue-500 resize-none"
              />
            </div>

            {/* Drag & Drop or Text Area */}
            {activeInputMode === 'file' ? (
              <div
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-2xl p-6 text-center transition cursor-pointer relative ${
                  dragActive ? 'border-blue-500 bg-blue-500/10' : 'border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 hover:border-slate-300 dark:hover:border-slate-700'
                }`}
              >
                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                
                <div className="space-y-2">
                  <div className="w-12 h-12 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-600 dark:text-blue-400 flex items-center justify-center mx-auto text-xl">
                    📁
                  </div>
                  {selectedFile ? (
                    <div>
                      <p className="text-sm font-bold text-emerald-600 dark:text-emerald-400">{selectedFile.name}</p>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 font-mono">{(selectedFile.size / 1024).toFixed(1)} KB</p>
                    </div>
                  ) : (
                    <div>
                      <p className="text-sm font-bold text-slate-900 dark:text-slate-100">Drag & drop your resume file here</p>
                      <p className="text-xs text-slate-500 dark:text-slate-400">Supports .PDF or .DOCX (Max 5MB)</p>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div>
                <label className="block text-slate-700 dark:text-slate-300 font-semibold mb-1">Resume Text Content</label>
                <textarea
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  placeholder="Paste your full raw resume content here..."
                  rows="7"
                  className="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:border-blue-500 font-mono"
                />
              </div>
            )}

            {analyzing && (
              <div className="space-y-1.5 pt-2">
                <div className="flex justify-between text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                  <span>Parsing sections, extracting details & computing ATS sub-scores...</span>
                  <span>{uploadProgress}%</span>
                </div>
                <AnimatedProgressBar value={uploadProgress} height="h-2" showSemanticColor={false} />
              </div>
            )}

            <button
              type="submit"
              disabled={analyzing}
              className="w-full btn-primary py-3 disabled:opacity-50"
            >
              {analyzing ? 'Analyzing Resume Structure...' : 'Run Real-Time ATS Score & Analysis 🚀'}
            </button>
          </form>
        </div>

        {/* RIGHT ANALYSIS RESULTS & TABS */}
        <div className="lg:col-span-7 space-y-6">

          {/* MAIN RESULTS DISPLAY */}
          {!analysisResult && activeTab !== 'history' ? (
            <div className="prof-card p-12 text-center space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center mx-auto text-3xl text-slate-400">
                📊
              </div>
              <h3 className="text-lg font-bold text-slate-900 dark:text-slate-100">No Active Resume Report</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto">
                Upload your PDF/DOCX resume or paste your text on the left to compute section-level ATS scores, extract structured experience/education, and perform job description comparison.
              </p>
              {historyList.length > 0 && (
                <button
                  onClick={() => setActiveTab('history')}
                  className="btn-outline"
                >
                  View Previous Analysis History ({historyList.length})
                </button>
              )}
            </div>
          ) : (
            <div className="space-y-6">

              {/* RADIAL SCORE & CANDIDATE SUMMARY */}
              {analysisResult && (
                <div className="prof-card p-6 flex flex-col sm:flex-row items-center justify-between gap-6">
                  <RadialScoreGauge score={analysisResult.overall_score} />

                  <div className="flex-1 space-y-3 text-xs w-full">
                    <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center justify-between">
                      <span>ATS Candidate Summary</span>
                      {analysisResult.jd_match_analysis?.jd_provided && (
                        <span className="px-2.5 py-0.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-600 dark:text-indigo-400 text-[10px] rounded-full font-mono">
                          JD Match: {analysisResult.jd_match_analysis.match_percentage}%
                        </span>
                      )}
                    </h3>

                    <div className="grid grid-cols-2 gap-2.5 font-mono">
                      <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-2.5 rounded-xl">
                        <p className="text-[10px] text-slate-500 uppercase">Target Role</p>
                        <p className="text-slate-800 dark:text-slate-200 font-bold mt-0.5 truncate">{analysisResult.target_role}</p>
                      </div>
                      <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-2.5 rounded-xl">
                        <p className="text-[10px] text-slate-500 uppercase">Words Parsed</p>
                        <p className="text-blue-600 dark:text-blue-400 font-bold mt-0.5">{analysisResult.word_count || 0} Words</p>
                      </div>
                      <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-2.5 rounded-xl">
                        <p className="text-[10px] text-slate-500 uppercase">Matched Skills</p>
                        <p className="text-emerald-600 dark:text-emerald-400 font-bold mt-0.5">{analysisResult.matched_keywords?.length || 0} Skills</p>
                      </div>
                      <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-2.5 rounded-xl">
                        <p className="text-[10px] text-slate-500 uppercase">Typos Flagged</p>
                        <p className="text-rose-600 dark:text-rose-400 font-bold mt-0.5">{analysisResult.spelling_errors?.length || 0} Typos</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* TABS CONTAINER */}
              <div className="prof-card overflow-hidden">
                <div className="flex items-center border-b border-slate-200 dark:border-slate-800 overflow-x-auto text-xs font-semibold">
                  <button
                    onClick={() => setActiveTab('overview')}
                    className={`px-4 py-3 border-b-2 transition shrink-0 ${
                      activeTab === 'overview' ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-500/5' : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Overview & Section Scores
                  </button>
                  <button
                    onClick={() => setActiveTab('roadmap')}
                    className={`px-4 py-3 border-b-2 transition shrink-0 ${
                      activeTab === 'roadmap' ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-500/5' : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Learning Roadmap 🛣️
                  </button>
                  <button
                    onClick={() => setActiveTab('structured')}
                    className={`px-4 py-3 border-b-2 transition shrink-0 ${
                      activeTab === 'structured' ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-500/5' : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Structured Extractions
                  </button>
                  <button
                    onClick={() => setActiveTab('jdmatch')}
                    className={`px-4 py-3 border-b-2 transition shrink-0 ${
                      activeTab === 'jdmatch' ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-500/5' : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    JD Match & Keywords
                  </button>
                  <button
                    onClick={() => setActiveTab('breakdown')}
                    className={`px-4 py-3 border-b-2 transition shrink-0 ${
                      activeTab === 'breakdown' ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-500/5' : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    ATS Checklist
                  </button>
                  <button
                    onClick={() => setActiveTab('typos')}
                    className={`px-4 py-3 border-b-2 transition shrink-0 ${
                      activeTab === 'typos' ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-500/5' : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Typos ({analysisResult?.spelling_errors?.length || 0})
                  </button>
                  <button
                    onClick={() => setActiveTab('history')}
                    className={`px-4 py-3 border-b-2 transition shrink-0 ${
                      activeTab === 'history' ? 'border-blue-600 text-blue-600 dark:text-blue-400 bg-blue-500/5' : 'border-transparent text-slate-500 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    Scan History ({historyList.length})
                  </button>
                </div>

                <div className="p-6 text-xs">
                  
                  {/* TAB 1: OVERVIEW & SECTION-LEVEL SCORES */}
                  {activeTab === 'overview' && analysisResult && (
                    <div className="space-y-6">
                      
                      {/* SECTION SCORES GRID */}
                      <div>
                        <h4 className="text-sm font-bold text-slate-900 dark:text-white mb-3">Section-Level Quality Scores</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {Object.entries(analysisResult.section_scores || {}).map(([secKey, secData]) => {
                            return (
                              <div key={secKey} className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl space-y-2">
                                <div className="flex items-center justify-between font-semibold">
                                  <span className="text-slate-800 dark:text-slate-200 capitalize">{secKey.replace('_', ' ')}</span>
                                  <ScoreBadge score={secData.score} size="sm" />
                                </div>
                                <AnimatedProgressBar value={secData.score} height="h-1.5" />
                                <p className="text-[11px] text-slate-500 dark:text-slate-400">{secData.recommendation}</p>
                              </div>
                            );
                          })}
                        </div>
                      </div>

                      {/* POST ATS SCORE LEARNING ROADMAP PREVIEW */}
                      <AIInsightCard title="Post-ATS Scan Learning Roadmap" icon="🛣️">
                        <div className="flex items-center justify-between mb-3">
                          <div>
                            <p className="text-[11px] text-slate-600 dark:text-slate-400">Tailored action plan for <strong className="text-blue-600 dark:text-blue-400">{analysisResult.target_role}</strong> based on your ATS score ({analysisResult.overall_score}/100).</p>
                          </div>
                          <button
                            onClick={() => setActiveTab('roadmap')}
                            className="btn-primary shrink-0"
                          >
                            Full Roadmap ➔
                          </button>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">
                          {(analysisResult.learning_roadmap?.phases || []).map((ph, idx) => (
                            <div key={idx} className="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-3 rounded-xl space-y-1">
                              <span className="px-2 py-0.5 bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20 text-[10px] font-mono font-bold rounded-md">
                                {ph.duration}
                              </span>
                              <p className="font-bold text-slate-900 dark:text-slate-200 text-xs mt-1 truncate">{ph.title}</p>
                              <p className="text-[10px] text-slate-500 dark:text-slate-400 line-clamp-2">{ph.focus}</p>
                            </div>
                          ))}
                        </div>
                      </AIInsightCard>

                      {/* WEAK RESUME SECTIONS WARNING */}
                      {analysisResult.weak_sections?.length > 0 && (
                        <div className="bg-rose-500/10 border border-rose-500/20 p-4 rounded-xl space-y-2">
                          <h4 className="text-xs font-bold text-rose-600 dark:text-rose-400 flex items-center gap-1.5">
                            ⚠️ Weak Resume Sections Requiring Upgrade:
                          </h4>
                          <div className="space-y-1.5">
                            {analysisResult.weak_sections.map((ws, i) => (
                              <div key={i} className="text-xs text-rose-600 dark:text-rose-300">
                                • <strong className="font-semibold text-slate-900 dark:text-white">{ws.section}:</strong> {ws.recommendation}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* CANDIDATE STRENGTHS */}
                      {analysisResult.strengths?.length > 0 && (
                        <div className="bg-emerald-500/10 border border-emerald-500/20 p-4 rounded-xl space-y-2">
                          <h4 className="text-xs font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
                            🌟 Resume Strengths & Highlights:
                          </h4>
                          <div className="space-y-1.5">
                            {analysisResult.strengths.map((str, i) => (
                              <div key={i} className="text-xs text-emerald-600 dark:text-emerald-300">
                                ✓ {str}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                    </div>
                  )}

                  {/* TAB 2: PERSONALIZED LEARNING ROADMAP */}
                  {activeTab === 'roadmap' && analysisResult && (
                    <div className="space-y-6">
                      
                      {/* ROADMAP OVERVIEW HEADER */}
                      <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl space-y-4">
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="px-2.5 py-0.5 bg-blue-500/10 border border-blue-500/30 text-blue-600 dark:text-blue-400 text-[10px] font-mono font-bold rounded-full">
                                POST-ATS ACTION PLAN
                              </span>
                              <span className="text-slate-500 dark:text-slate-400 text-xs">• Est. Timeframe: {analysisResult.learning_roadmap?.estimated_timeframe || '4 - 6 Weeks'}</span>
                            </div>
                            <h3 className="text-base font-bold text-slate-900 dark:text-white mt-1">
                              Learning Roadmap for {analysisResult.target_role} 🛣️
                            </h3>
                            <p className="text-slate-500 dark:text-slate-400 text-xs">
                              Dynamic learning plan generated from your ATS score ({analysisResult.overall_score}/100) and missing skill competencies.
                            </p>
                          </div>

                          <div className="flex items-center gap-2 flex-wrap shrink-0">
                            <Link
                              to="/coding-arena"
                              className="btn-primary flex items-center gap-1.5"
                            >
                              <span>💻</span> Practice Coding Arena
                            </Link>
                            <Link
                              to="/speech-analyzer"
                              className="btn-secondary flex items-center gap-1.5"
                            >
                              <span>🎙️</span> AI Voice Analyzer
                            </Link>
                          </div>
                        </div>

                        {/* ROADMAP PROGRESS METRIC */}
                        {(() => {
                          const allItems = (analysisResult.learning_roadmap?.phases || []).flatMap(p => p.items || []);
                          const totalCnt = allItems.length || 1;
                          const doneCnt = allItems.filter(item => completedRoadmapTasks[item.id]).length;
                          const pct = Math.round((doneCnt / totalCnt) * 100);

                          return (
                            <div className="pt-2 border-t border-slate-200 dark:border-slate-900 space-y-1.5">
                              <div className="flex justify-between text-xs font-semibold">
                                <span className="text-slate-700 dark:text-slate-300">Overall Roadmap Progress:</span>
                                <span className="text-blue-600 dark:text-blue-400 font-mono">{doneCnt} / {totalCnt} Milestones Completed ({pct}%)</span>
                              </div>
                              <AnimatedProgressBar value={pct} height="h-2" showSemanticColor={false} />
                            </div>
                          );
                        })()}
                      </div>

                      {/* PHASES LIST */}
                      <div className="space-y-4">
                        {(analysisResult.learning_roadmap?.phases || []).map((ph) => (
                          <div key={ph.phase} className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl space-y-3.5">
                            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-900 pb-3">
                              <div className="space-y-0.5">
                                <span className="px-2.5 py-0.5 bg-indigo-500/10 border border-indigo-500/30 text-indigo-600 dark:text-indigo-300 text-[10px] font-mono font-bold rounded-full">
                                  {ph.duration}
                                </span>
                                <h4 className="text-sm font-bold text-slate-900 dark:text-white mt-1">{ph.title}</h4>
                                <p className="text-slate-500 dark:text-slate-400 text-xs">{ph.focus}</p>
                              </div>
                            </div>

                            {/* PHASE ITEMS */}
                            <div className="space-y-2">
                              {(ph.items || []).map((item) => {
                                const isDone = Boolean(completedRoadmapTasks[item.id]);

                                return (
                                  <div
                                    key={item.id}
                                    onClick={() => toggleRoadmapTask(item.id)}
                                    className={`p-3 rounded-xl border transition cursor-pointer flex items-center justify-between gap-3 ${
                                      isDone ? 'bg-slate-100 dark:bg-slate-950/40 border-slate-200 dark:border-slate-900 text-slate-400 line-through' : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200'
                                    }`}
                                  >
                                    <div className="flex items-center gap-3">
                                      <input
                                        type="checkbox"
                                        checked={isDone}
                                        onChange={() => {}}
                                        className="w-4 h-4 text-blue-600 rounded bg-slate-100 dark:bg-slate-950 border-slate-300 dark:border-slate-700 focus:ring-0 cursor-pointer"
                                      />
                                      <div>
                                        <p className="font-medium text-xs text-slate-900 dark:text-slate-100">{item.task}</p>
                                        <p className="text-[10px] text-slate-500 dark:text-slate-400 font-mono mt-0.5">Resource: {item.resource}</p>
                                      </div>
                                    </div>

                                    <span className="px-2.5 py-0.5 bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-[10px] font-mono text-slate-600 dark:text-slate-300 rounded-md shrink-0">
                                      {item.category}
                                    </span>
                                  </div>
                                );
                              })}
                            </div>
                          </div>
                        ))}
                      </div>

                    </div>
                  )}

                  {/* TAB 3: STRUCTURED EXTRACTION */}
                  {activeTab === 'structured' && analysisResult?.structured_extraction && (
                    <div className="space-y-6">
                      
                      {/* CONTACT INFO */}
                      <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl space-y-2">
                        <h4 className="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider">Contact Information</h4>
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 font-mono text-xs">
                          <div><span className="text-slate-500">Name:</span> <span className="text-slate-900 dark:text-slate-200 font-bold">{analysisResult.structured_extraction.contact_info?.name || "Candidate"}</span></div>
                          <div><span className="text-slate-500">Email:</span> <span className="text-emerald-600 dark:text-emerald-400">{analysisResult.structured_extraction.contact_info?.email || "Missing"}</span></div>
                          <div><span className="text-slate-500">Phone:</span> <span className="text-slate-800 dark:text-slate-200">{analysisResult.structured_extraction.contact_info?.phone || "Missing"}</span></div>
                          <div><span className="text-slate-500">LinkedIn:</span> <span className="text-blue-600 dark:text-blue-400">{analysisResult.structured_extraction.contact_info?.linkedin || "Not specified"}</span></div>
                          <div><span className="text-slate-500">GitHub:</span> <span className="text-purple-600 dark:text-purple-400">{analysisResult.structured_extraction.contact_info?.github || "Not specified"}</span></div>
                          <div><span className="text-slate-500">Location:</span> <span className="text-slate-700 dark:text-slate-300">{analysisResult.structured_extraction.contact_info?.location || "Not specified"}</span></div>
                        </div>
                      </div>

                      {/* SKILLS */}
                      <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl space-y-3">
                        <h4 className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider">Extracted Skill Inventory</h4>
                        
                        <div>
                          <p className="text-[11px] text-slate-500 dark:text-slate-400 mb-1.5">Technical Skills ({analysisResult.structured_extraction.skills?.technical?.length || 0}):</p>
                          <div className="flex items-center gap-1.5 flex-wrap">
                            {(analysisResult.structured_extraction.skills?.technical || []).map((sk, i) => (
                              <span key={i} className="px-2.5 py-1 bg-indigo-500/10 border border-indigo-500/30 text-indigo-600 dark:text-indigo-300 rounded-lg font-mono">
                                {sk}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div>
                          <p className="text-[11px] text-slate-500 dark:text-slate-400 mb-1.5">Tools & Developer Ecosystem:</p>
                          <div className="flex items-center gap-1.5 flex-wrap">
                            {(analysisResult.structured_extraction.skills?.tools || []).map((sk, i) => (
                              <span key={i} className="px-2.5 py-1 bg-purple-500/10 border border-purple-500/30 text-purple-600 dark:text-purple-300 rounded-lg font-mono">
                                {sk}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* EDUCATION */}
                      {analysisResult.structured_extraction.education?.length > 0 && (
                        <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl space-y-2">
                          <h4 className="text-xs font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider">Education</h4>
                          <div className="space-y-2">
                            {analysisResult.structured_extraction.education.map((edu, i) => (
                              <div key={i} className="border-l-2 border-amber-500/50 pl-3 py-1">
                                <p className="font-bold text-slate-900 dark:text-slate-100">{edu.degree}</p>
                                <p className="text-slate-500 dark:text-slate-400 text-[11px]">{edu.institution} • {edu.year}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* EXPERIENCE */}
                      {analysisResult.structured_extraction.experience?.length > 0 && (
                        <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl space-y-3">
                          <h4 className="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">Work Experience</h4>
                          <div className="space-y-3">
                            {analysisResult.structured_extraction.experience.map((exp, i) => (
                              <div key={i} className="border-l-2 border-emerald-500/50 pl-3 py-1 space-y-1">
                                <p className="font-bold text-slate-900 dark:text-slate-100">{exp.title}</p>
                                <p className="text-slate-500 dark:text-slate-400 text-[11px]">{exp.company} ({exp.dates})</p>
                                {exp.bullets?.length > 0 && (
                                  <ul className="list-disc list-inside text-slate-600 dark:text-slate-300 space-y-0.5 text-[11px]">
                                    {exp.bullets.map((b, bi) => (
                                      <li key={bi}>{b}</li>
                                    ))}
                                  </ul>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                    </div>
                  )}

                  {/* TAB 4: JD COMPARISON & KEYWORDS */}
                  {activeTab === 'jdmatch' && analysisResult && (
                    <div className="space-y-5">
                      <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl flex items-center justify-between">
                        <div>
                          <h4 className="text-xs font-bold text-slate-900 dark:text-white">Target Job Description Fit</h4>
                          <p className="text-[11px] text-slate-500 dark:text-slate-400">
                            {analysisResult.jd_match_analysis?.jd_provided ? "Compared directly against user-provided JD requirements." : "Compared against industry standard requirements for target role."}
                          </p>
                        </div>
                        <div className="text-right">
                          <span className="text-2xl font-bold font-mono text-indigo-600 dark:text-indigo-400">
                            {analysisResult.jd_match_analysis?.match_percentage || analysisResult.overall_score}%
                          </span>
                          <p className="text-[10px] text-slate-500 uppercase">Match Fit</p>
                        </div>
                      </div>

                      <div>
                        <p className="text-slate-700 dark:text-slate-300 font-semibold mb-2">Matched Competencies ({analysisResult.matched_keywords?.length || 0}):</p>
                        <div className="flex items-center gap-2 flex-wrap">
                          {(analysisResult.matched_keywords || []).map((kw, i) => (
                            <span key={i} className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-300 font-medium rounded-lg font-mono">
                              ✓ {kw}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="pt-3 border-t border-slate-200 dark:border-slate-800">
                        <p className="text-slate-700 dark:text-slate-300 font-semibold mb-2">Missing High-Value Keywords ({analysisResult.missing_keywords?.length || 0}):</p>
                        <div className="flex items-center gap-2 flex-wrap">
                          {(analysisResult.missing_keywords || []).map((kw, i) => (
                            <span key={i} className="px-3 py-1 bg-rose-500/10 border border-rose-500/30 text-rose-600 dark:text-rose-300 font-medium rounded-lg font-mono">
                              + {kw}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* TAB 5: ATS BREAKDOWN & CHECKLIST */}
                  {activeTab === 'breakdown' && analysisResult && (
                    <div className="space-y-5">
                      <div className="space-y-3">
                        <h4 className="text-xs font-bold text-slate-900 dark:text-white">5 Weighted Sub-Score Weights</h4>
                        <div>
                          <div className="flex justify-between font-semibold mb-1">
                            <span className="text-slate-700 dark:text-slate-300">1. Section Completeness (20%)</span>
                            <span className="text-blue-600 dark:text-blue-400 font-mono">{analysisResult.breakdown.section_completeness} / 20 pts</span>
                          </div>
                          <AnimatedProgressBar value={(analysisResult.breakdown.section_completeness / 20) * 100} height="h-2" showSemanticColor={false} />
                        </div>

                        <div>
                          <div className="flex justify-between font-semibold mb-1">
                            <span className="text-slate-700 dark:text-slate-300">2. Quantifiable Impact & Power Verbs (25%)</span>
                            <span className="text-amber-600 dark:text-amber-400 font-mono">{analysisResult.breakdown.quantifiable_impact} / 25 pts</span>
                          </div>
                          <AnimatedProgressBar value={(analysisResult.breakdown.quantifiable_impact / 25) * 100} height="h-2" showSemanticColor={false} />
                        </div>

                        <div>
                          <div className="flex justify-between font-semibold mb-1">
                            <span className="text-slate-700 dark:text-slate-300">3. Skill Density & Technical Keywords (25%)</span>
                            <span className="text-indigo-600 dark:text-indigo-400 font-mono">{analysisResult.breakdown.skill_density} / 25 pts</span>
                          </div>
                          <AnimatedProgressBar value={(analysisResult.breakdown.skill_density / 25) * 100} height="h-2" showSemanticColor={false} />
                        </div>
                      </div>

                      <div className="pt-4 border-t border-slate-200 dark:border-slate-800 space-y-3">
                        <h4 className="text-xs font-bold text-slate-900 dark:text-white">Actionable ATS Upgrade Checklist</h4>
                        <div className="space-y-2">
                          {actionChecklist.map((item) => (
                            <div
                              key={item.id}
                              onClick={() => toggleChecklistItem(item.id)}
                              className={`p-3 rounded-xl border transition cursor-pointer flex items-center gap-3 ${
                                item.resolved ? 'bg-slate-100 dark:bg-slate-950/40 border-slate-200 dark:border-slate-900 text-slate-400 line-through' : 'bg-slate-50 dark:bg-slate-950 border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200'
                              }`}
                            >
                              <input
                                type="checkbox"
                                checked={item.resolved}
                                onChange={() => {}}
                                className="w-4 h-4 text-blue-600 rounded bg-slate-100 dark:bg-slate-900 border-slate-300 dark:border-slate-700 focus:ring-0"
                              />
                              <div className="flex-1 flex items-center justify-between">
                                <span className="font-medium">{item.task}</span>
                                <span className="px-2 py-0.5 text-[10px] rounded font-mono border bg-slate-100 dark:bg-slate-900 border-slate-200 dark:border-slate-700">
                                  {item.badge || 'Action Item'}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* TAB 6: SCAN HISTORY */}
                  {activeTab === 'history' && (
                    <div className="space-y-4">
                      <div className="flex items-center justify-between">
                        <h4 className="text-xs font-bold text-slate-900 dark:text-white">Your Historical Resume Analyses</h4>
                        <button onClick={fetchHistory} className="text-xs text-blue-600 dark:text-blue-400 hover:underline">
                          Refresh List 🔄
                        </button>
                      </div>

                      {loadingHistory ? (
                        <div className="py-8 text-center text-slate-500 dark:text-slate-400 text-xs">Loading previous resume scans...</div>
                      ) : historyList.length === 0 ? (
                        <div className="py-8 text-center text-slate-500 dark:text-slate-400 text-xs">
                          No previous scans stored yet. Run your first analysis on the left!
                        </div>
                      ) : (
                        <div className="space-y-2.5">
                          {historyList.map((scan, idx) => {
                            const score = scan.overall_score || scan.scan_data?.overall_score || 0;

                            return (
                              <div key={scan._id || idx} className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl flex items-center justify-between gap-4">
                                <div className="space-y-0.5">
                                  <div className="flex items-center gap-2">
                                    <span className="font-bold text-slate-900 dark:text-white">{scan.target_role || "Software Engineer"}</span>
                                    <ScoreBadge score={score} size="sm" />
                                  </div>
                                  <p className="text-[11px] text-slate-500 dark:text-slate-400 font-mono">
                                    Date: {scan.created_at ? new Date(scan.created_at).toLocaleDateString() : "Recent"}
                                  </p>
                                </div>

                                <button
                                  onClick={() => loadPastScan(scan)}
                                  className="btn-secondary"
                                >
                                  View Analysis Report ➔
                                </button>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  )}

                </div>
              </div>

            </div>
          )}

        </div>

      </div>

    </div>
  );
};

export default ResumeAnalyzer;
