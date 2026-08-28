import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const ExternalLinkIcon = () => (
  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
  </svg>
);

const SparklesIcon = () => (
  <svg className="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
  </svg>
);

const WeaknessDetector = () => {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [reanalyzing, setReanalyzing] = useState(false);

  const fetchAnalysis = async () => {
    setLoading(true);
    try {
      const res = await api.weakness.getAnalysis();
      if (res?.analysis) {
        setAnalysis(res.analysis);
      }
    } catch (err) {
      console.error('Error fetching weakness analysis:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis();
  }, []);

  const handleReanalyze = async () => {
    setReanalyzing(true);
    try {
      const res = await api.weakness.runAnalysis();
      if (res?.analysis) {
        setAnalysis(res.analysis);
      }
    } catch (err) {
      console.error('Error triggering weakness re-analysis:', err);
    } finally {
      setReanalyzing(false);
    }
  };

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'High':
        return 'bg-red-500/20 text-red-300 border-red-500/40';
      case 'Medium':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      case 'Low':
        return 'bg-slate-800 text-slate-300 border-slate-700';
      default:
        return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-10 space-y-8">
      
      {/* 1. HEADER BANNER */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <Link to="/dashboard" className="text-xs font-semibold text-blue-400 hover:underline">
              ← Dashboard
            </Link>
            <span className="text-slate-600">•</span>
            <span className="px-2.5 py-0.5 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-semibold rounded-full font-mono flex items-center gap-1">
              <SparklesIcon /> AI DIAGNOSTICS
            </span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white mt-2 tracking-tight flex items-center gap-2">
            AI Weakness & Performance Detector 🔍
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Identifies your strongest and weakest areas based strictly on actual Coding Arena accuracy, ATS Resume Scans, Mock Interviews, and Speech Prosody metrics.
          </p>
        </div>

        <button
          onClick={handleReanalyze}
          disabled={reanalyzing || loading}
          className="px-4 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-bold rounded-xl shadow-lg transition flex items-center gap-2 self-start md:self-auto disabled:opacity-50"
        >
          <span>⚡ {reanalyzing ? 'Analyzing Performance...' : 'Re-analyze Performance'}</span>
        </button>
      </div>

      {loading ? (
        <div className="py-20 text-center text-slate-400 animate-pulse text-sm">
          Analyzing multi-module performance data...
        </div>
      ) : analysis && !analysis.has_sufficient_data ? (
        /* 2. INSUFFICIENT DATA STATE BANNER */
        <div className="bg-slate-900/90 border border-amber-500/30 p-8 rounded-2xl text-center space-y-6 max-w-3xl mx-auto shadow-2xl backdrop-blur-md">
          <div className="w-16 h-16 bg-amber-500/10 border border-amber-500/20 rounded-2xl flex items-center justify-center text-3xl mx-auto">
            📊
          </div>
          <div className="space-y-2">
            <h2 className="text-xl font-bold text-white">Not enough data yet.</h2>
            <p className="text-sm text-slate-300 max-w-xl mx-auto">
              Complete a resume scan, coding problem, or mock interview to unlock your personalized AI weakness analysis and diagnostic score cards.
            </p>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            <Link
              to="/resume-analyzer"
              className="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-xl shadow transition"
            >
              Scan Resume 📄
            </Link>
            <Link
              to="/coding-arena"
              className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow transition"
            >
              Solve Coding Problem ⚡
            </Link>
            <Link
              to="/interview-simulator"
              className="px-4 py-2.5 bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold rounded-xl shadow transition"
            >
              Launch AI Mock Interview 🎙️
            </Link>
          </div>
        </div>
      ) : analysis ? (
        <div className="space-y-8">
          
          {/* 3. HIGHEST IMPACT IMPROVEMENT BANNER */}
          {analysis.highest_impact_improvement && (
            <div className="bg-gradient-to-br from-rose-950/80 via-slate-900 to-slate-900 border border-rose-500/40 p-6 lg:p-8 rounded-2xl shadow-2xl backdrop-blur-md relative overflow-hidden space-y-4">
              <div className="flex items-center justify-between">
                <span className="px-3 py-1 bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-extrabold rounded-full uppercase tracking-wider font-mono flex items-center gap-1.5">
                  <SparklesIcon /> HIGHEST IMPACT IMPROVEMENT
                </span>
                <span className="text-xs font-mono text-slate-400">Target Goal: <strong className="text-emerald-400 font-bold">{analysis.highest_impact_improvement.target_score}%</strong></span>
              </div>

              <div>
                <h2 className="text-xl font-bold text-white">
                  {analysis.highest_impact_improvement.weakness_title}
                </h2>
                <p className="text-sm text-slate-300 mt-2 leading-relaxed font-medium">
                  {analysis.highest_impact_improvement.impact_statement}
                </p>
              </div>

              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-3 border-t border-rose-500/20">
                <div className="text-xs text-slate-400">
                  <span className="text-slate-500">Action: </span>
                  <strong className="text-white">{analysis.highest_impact_improvement.recommended_action}</strong>
                </div>

                <Link
                  to={analysis.highest_impact_improvement.target_link || '/coding-arena'}
                  className="px-5 py-2.5 bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold rounded-xl shadow-lg transition flex items-center gap-1.5 shrink-0 self-start sm:self-auto"
                >
                  <span>Start Recommendation 🚀</span>
                  <ExternalLinkIcon />
                </Link>
              </div>
            </div>
          )}

          {/* 4. AI PERFORMANCE SUMMARY CARD */}
          {analysis.ai_performance_summary && (
            <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-2 backdrop-blur-md">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1">
                <SparklesIcon /> AI Mentor Insight Summary
              </span>
              <p className="text-sm text-slate-200 leading-relaxed italic">
                "{analysis.ai_performance_summary}"
              </p>
            </div>
          )}

          {/* 5. TOP 5 WEAKNESSES & TOP 5 STRENGTHS GRID */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

            {/* TOP 5 WEAKNESSES */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <span>🚨 Top 5 Weaknesses</span>
                  <span className="text-xs font-mono px-2 py-0.5 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-full">Lowest Scores</span>
                </h2>
              </div>

              <div className="space-y-4">
                {(analysis.top_weaknesses || []).map((w, idx) => (
                  <div
                    key={w.id || idx}
                    className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl space-y-3 backdrop-blur-md hover:border-slate-700 transition"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <span className="w-6 h-6 rounded-lg bg-rose-500/20 text-rose-400 border border-rose-500/30 flex items-center justify-center font-mono font-bold text-xs">
                          #{idx + 1}
                        </span>
                        <div>
                          <h3 className="text-sm font-bold text-white">{w.title}</h3>
                          <span className="text-[11px] text-slate-400 font-mono">{w.category}</span>
                        </div>
                      </div>

                      <span className={`px-2.5 py-0.5 text-[10px] font-bold rounded border uppercase ${getSeverityBadge(w.severity)}`}>
                        {w.severity} Severity
                      </span>
                    </div>

                    {/* Score Bar */}
                    <div className="space-y-1">
                      <div className="flex justify-between text-xs font-mono">
                        <span className="text-slate-400">Current Score</span>
                        <span className="text-rose-400 font-bold">{w.current_score}%</span>
                      </div>
                      <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                        <div
                          className="h-full bg-gradient-to-r from-rose-500 to-amber-500 rounded-full"
                          style={{ width: `${Math.min(100, Math.max(5, w.current_score))}%` }}
                        />
                      </div>
                    </div>

                    {/* Evidence */}
                    <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs font-mono text-slate-300">
                      <span className="text-slate-500 block text-[10px] uppercase font-sans">Evidence Signal:</span>
                      {w.evidence}
                    </div>

                    {/* Action Link */}
                    <div className="flex items-center justify-between pt-1 text-xs">
                      <span className="text-slate-400 truncate max-w-[240px]">{w.recommended_action}</span>
                      <Link
                        to={w.target_link || '/coding-arena'}
                        className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 transition flex items-center gap-1 shrink-0"
                      >
                        Fix Weakness
                        <ExternalLinkIcon />
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* TOP 5 STRENGTHS */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                  <span>🏆 Top 5 Strengths</span>
                  <span className="text-xs font-mono px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">Highest Scores</span>
                </h2>
              </div>

              <div className="space-y-4">
                {(analysis.top_strengths || []).map((s, idx) => (
                  <div
                    key={s.id || idx}
                    className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl space-y-3 backdrop-blur-md hover:border-slate-700 transition"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex items-center gap-3">
                        <span className="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center justify-center font-mono font-bold text-xs">
                          #{idx + 1}
                        </span>
                        <div>
                          <h3 className="text-sm font-bold text-white">{s.title}</h3>
                          <span className="text-[11px] text-slate-400 font-mono">{s.category}</span>
                        </div>
                      </div>

                      <span className="px-2.5 py-0.5 text-[10px] font-bold rounded border bg-emerald-500/10 text-emerald-400 border-emerald-500/20 font-mono">
                        STRONG
                      </span>
                    </div>

                    {/* Score Bar */}
                    <div className="space-y-1">
                      <div className="flex justify-between text-xs font-mono">
                        <span className="text-slate-400">Mastery Score</span>
                        <span className="text-emerald-400 font-bold">{s.current_score}%</span>
                      </div>
                      <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                        <div
                          className="h-full bg-gradient-to-r from-blue-500 to-emerald-400 rounded-full"
                          style={{ width: `${Math.min(100, Math.max(5, s.current_score))}%` }}
                        />
                      </div>
                    </div>

                    {/* Evidence */}
                    <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs font-mono text-slate-300">
                      <span className="text-slate-500 block text-[10px] uppercase font-sans">Evidence Signal:</span>
                      {s.evidence}
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>

        </div>
      ) : null}

    </div>
  );
};

export default WeaknessDetector;
