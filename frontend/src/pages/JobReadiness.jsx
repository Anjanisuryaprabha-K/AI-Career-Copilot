import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { PageHeader, AnimatedProgressBar } from '../components/common/DesignSystemComponents';

const JobReadiness = () => {
  const navigate = useNavigate();
  const [readinessData, setReadinessData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchReadiness = async () => {
    setLoading(true);
    try {
      // Fetch central readiness data
      const res = await api.get('/api/v1/jobs/readiness');
      if (res) {
        setReadinessData(res);
      }
    } catch (err) {
      console.error('Error fetching job readiness data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReadiness();
  }, []);

  const overallScore = readinessData?.overall_readiness_score || 0;
  const tier = readinessData?.tier || "Calculating Readiness...";
  const breakdown = readinessData?.weighting_breakdown || {};
  const strengths = readinessData?.strengths || [];
  const weaknesses = readinessData?.weaknesses || [];
  const recommendedActions = readinessData?.recommended_actions || [];
  const trendHistory = readinessData?.trend_history || [];

  // Salary range estimator based on overall score
  let salaryEstimate = "₹6.0 LPA - ₹10.0 LPA";
  if (overallScore >= 85) salaryEstimate = "₹18.0 LPA - ₹35.0 LPA";
  else if (overallScore >= 70) salaryEstimate = "₹12.0 LPA - ₹18.0 LPA";
  else if (overallScore >= 50) salaryEstimate = "₹8.0 LPA - ₹12.0 LPA";

  return (
    <div className="space-y-6">
      
      {/* 1. TOP HEADER & TIER BADGE */}
      <PageHeader
        category="Readiness Index"
        badgeText="PLACEMENT INDEX"
        title="Central Job Readiness Index Engine 📊"
        subtitle="Real-time readiness score aggregating Resume Quality, Skills, Coding, Interviews, Profile, and Applications."
        actions={
          <div className="flex items-center gap-3">
            <button
              onClick={fetchReadiness}
              disabled={loading}
              className="btn-secondary"
            >
              {loading ? 'Refreshing...' : '🔄 Recalculate Readiness'}
            </button>
            <div className="px-4 py-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold rounded-xl font-mono">
              {tier}
            </div>
          </div>
        }
      />

      {loading ? (
        <div className="prof-card p-12 text-center text-slate-500 dark:text-slate-400 space-y-3">
          <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs font-mono">Aggregating candidate performance across all 6 readiness pillars...</p>
        </div>
      ) : (
        <div className="space-y-6">
          
          {/* 2. MAIN READINESS INDEX KPI + TREND CHART */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* Main Score Box */}
            <div className="lg:col-span-5 prof-card p-8 text-center space-y-4 flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Overall Job Readiness Index</span>
                <div className="text-6xl font-black text-blue-600 dark:text-blue-400 font-mono py-3">{overallScore}%</div>
                <div className="mt-2 mb-4">
                  <AnimatedProgressBar value={overallScore} height="h-3" />
                </div>
                <p className="text-xs text-emerald-600 dark:text-emerald-400 font-semibold bg-emerald-500/10 border border-emerald-500/20 py-2 rounded-xl">
                  Estimated Placement Package: {salaryEstimate}
                </p>
              </div>

              <div className="pt-4 border-t border-slate-200 dark:border-slate-800 text-left space-y-2 text-xs">
                <p className="text-slate-500 dark:text-slate-400 font-mono">Readiness Status:</p>
                <p className="text-slate-900 dark:text-white font-bold">{tier}</p>
                <p className="text-[10px] text-slate-500 font-mono">Formula: 20% Resume + 20% Skills + 20% Coding + 20% Interview + 10% Profile + 10% Applications</p>
              </div>
            </div>

            {/* Progress Trend View */}
            <div className="lg:col-span-7 prof-card p-6 space-y-6">
              <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
                <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">Readiness Score Progress Trend Over Time 📈</h3>
                <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">Live Timeline</span>
              </div>

              <div className="space-y-4 pt-2">
                {trendHistory.map((pt, idx) => (
                  <div key={idx} className="space-y-1">
                    <div className="flex justify-between text-xs font-mono">
                      <span className="text-slate-500 dark:text-slate-400">{pt.period}</span>
                      <span className="text-blue-600 dark:text-blue-400 font-bold">{pt.score}%</span>
                    </div>
                    <AnimatedProgressBar value={pt.score} height="h-2" />
                  </div>
                ))}
              </div>

              <p className="text-[11px] text-slate-500 dark:text-slate-400 italic">
                * Complete ATS resume scans, coding challenges, and mock interviews to trigger automatic readiness upgrades.
              </p>
            </div>

          </div>

          {/* 3. MULTI-PILLAR WEIGHTING BREAKDOWN GRID */}
          <div className="space-y-4">
            <h3 className="text-base font-bold text-slate-900 dark:text-white tracking-tight">6-Pillar Weighting Breakdown</h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              
              {/* 1. Resume ATS Quality */}
              <div className="prof-card p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-purple-600 dark:text-purple-400 uppercase font-mono">1. Resume Quality (20%)</span>
                  <span className="text-lg font-bold font-mono text-slate-900 dark:text-white">{breakdown.resume_score?.score || 0}%</span>
                </div>
                <AnimatedProgressBar value={breakdown.resume_score?.score || 0} height="h-1.5" />
                <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">{breakdown.resume_score?.status}</p>
              </div>

              {/* 2. Skills Mastery */}
              <div className="prof-card p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase font-mono">2. Skills Mastery (20%)</span>
                  <span className="text-lg font-bold font-mono text-slate-900 dark:text-white">{breakdown.skills_score?.score || 0}%</span>
                </div>
                <AnimatedProgressBar value={breakdown.skills_score?.score || 0} height="h-1.5" />
                <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">{breakdown.skills_score?.status}</p>
              </div>

              {/* 3. Coding Performance */}
              <div className="prof-card p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-amber-500 uppercase font-mono">3. Coding DSA (20%)</span>
                  <span className="text-lg font-bold font-mono text-slate-900 dark:text-white">{breakdown.coding_score?.score || 0}%</span>
                </div>
                <AnimatedProgressBar value={breakdown.coding_score?.score || 0} height="h-1.5" />
                <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">{breakdown.coding_score?.status}</p>
              </div>

              {/* 4. Interview Performance */}
              <div className="prof-card p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase font-mono">4. Mock Interviews (20%)</span>
                  <span className="text-lg font-bold font-mono text-slate-900 dark:text-white">{breakdown.interview_score?.score || 0}%</span>
                </div>
                <AnimatedProgressBar value={breakdown.interview_score?.score || 0} height="h-1.5" />
                <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">{breakdown.interview_score?.status}</p>
              </div>

              {/* 5. Profile Completeness */}
              <div className="prof-card p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase font-mono">5. Profile & Projects (10%)</span>
                  <span className="text-lg font-bold font-mono text-slate-900 dark:text-white">{breakdown.profile_score?.score || 0}%</span>
                </div>
                <AnimatedProgressBar value={breakdown.profile_score?.score || 0} height="h-1.5" />
                <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">{breakdown.profile_score?.status}</p>
              </div>

              {/* 6. Applications Activity */}
              <div className="prof-card p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-cyan-600 dark:text-cyan-400 uppercase font-mono">6. Applications (10%)</span>
                  <span className="text-lg font-bold font-mono text-slate-900 dark:text-white">{breakdown.application_score?.score || 0}%</span>
                </div>
                <AnimatedProgressBar value={breakdown.application_score?.score || 0} height="h-1.5" />
                <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">{breakdown.application_score?.status}</p>
              </div>

            </div>
          </div>

          {/* 4. STRENGTHS, WEAKNESSES & RECOMMENDED ACTIONS */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Candidate Strengths & Weaknesses */}
            <div className="space-y-6">
              {/* Strengths */}
              <div className="prof-card p-6 border-l-4 border-l-emerald-500 space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">✓ Identified Strengths</h4>
                <div className="space-y-2">
                  {strengths.map((s, idx) => (
                    <div key={idx} className="text-xs text-slate-700 dark:text-slate-300 flex items-start gap-2">
                      <span>•</span>
                      <span>{s}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Weaknesses */}
              {weaknesses.length > 0 && (
                <div className="prof-card p-6 border-l-4 border-l-rose-500 space-y-3">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400">⚠️ Identified Focus Areas & Gaps</h4>
                  <div className="space-y-2">
                    {weaknesses.map((w, idx) => (
                      <div key={idx} className="text-xs text-slate-700 dark:text-slate-300 flex items-start gap-2">
                        <span>•</span>
                        <span>{w}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Recommended Action Checklist */}
            <div className="prof-card p-6 space-y-4">
              <h4 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">🎯 Recommended Actions to Boost Score</h4>
              <p className="text-xs text-slate-500 dark:text-slate-400">Execute these recommended tasks to directly increase your readiness percentage:</p>

              <div className="space-y-3">
                {recommendedActions.map((rec, idx) => (
                  <div key={idx} className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl flex items-center justify-between gap-4">
                    <div>
                      <span className="text-[10px] text-blue-600 dark:text-blue-400 font-mono uppercase">{rec.module}</span>
                      <p className="text-xs font-semibold text-slate-900 dark:text-white mt-0.5">{rec.task}</p>
                    </div>
                    <button
                      onClick={() => navigate(rec.link)}
                      className="btn-primary shrink-0 text-xs py-1.5 px-3"
                    >
                      Action →
                    </button>
                  </div>
                ))}

                {recommendedActions.length === 0 && (
                  <div className="p-4 text-center text-xs text-emerald-600 dark:text-emerald-400 font-mono">
                    🎉 Excellent! All readiness pillars are in top condition. Keep practicing!
                  </div>
                )}
              </div>
            </div>

          </div>

          {/* 5. MATCHING RECRUITERS GRID */}
          <div className="prof-card p-6 space-y-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">Matching Placement Recruiters</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
              {[
                { company: 'Google', minScore: 85 },
                { company: 'Microsoft', minScore: 80 },
                { company: 'Amazon', minScore: 80 },
                { company: 'Razorpay', minScore: 75 },
                { company: 'TCS Digital', minScore: 65 },
                { company: 'Infosys Power', minScore: 70 }
              ].map((c, i) => {
                const isMatched = overallScore >= c.minScore;
                return (
                  <div key={i} className={`p-3.5 rounded-xl border flex flex-col justify-between ${
                    isMatched ? 'bg-emerald-500/10 border-emerald-500/20' : 'bg-slate-50 dark:bg-slate-950 border-slate-200 dark:border-slate-800 opacity-60'
                  }`}>
                    <span className="text-xs font-bold text-slate-900 dark:text-white">{c.company}</span>
                    <span className={`text-[10px] font-mono mt-2 ${isMatched ? 'text-emerald-600 dark:text-emerald-400 font-bold' : 'text-slate-500'}`}>
                      {isMatched ? '✓ Match Eligible' : `Needs ${c.minScore}%`}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

        </div>
      )}

    </div>
  );
};

export default JobReadiness;
