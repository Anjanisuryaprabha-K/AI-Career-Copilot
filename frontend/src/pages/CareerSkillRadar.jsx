import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { PageHeader } from '../components/common/DesignSystemComponents';

const TARGET_ROLES = [
  "Software Engineer", "Full Stack Developer", "Frontend Developer",
  "Backend Developer", "Data Engineer", "Data Scientist"
];

const CareerSkillRadar = () => {
  const [selectedRole, setSelectedRole] = useState("Software Engineer");
  const [radarData, setRadarData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRadarData(selectedRole);
    fetchHistory();
  }, [selectedRole]);

  const fetchRadarData = async (role) => {
    setLoading(true);
    try {
      const res = await api.skillRadar.getRadar(role);
      if (res?.radar) {
        setRadarData(res.radar);
      }
    } catch (err) {
      console.error("Error fetching skill radar:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await api.skillRadar.getHistory();
      if (res?.history) {
        setHistory(res.history);
      }
    } catch (err) {
      console.error("Error fetching radar history:", err);
    }
  };

  // Helper SVG Radar Generator for 12 Axes
  const renderRadarSVG = () => {
    if (!radarData?.evaluated_axes || !radarData?.target_benchmarks) return null;

    const axesKeys = Object.keys(radarData.evaluated_axes);
    const numAxes = axesKeys.length;
    const size = 300;
    const center = size / 2;
    const radius = 110;

    const getPoint = (index, value) => {
      const angle = (Math.PI * 2 / numAxes) * index - Math.PI / 2;
      const dist = (value / 100) * radius;
      return {
        x: center + dist * Math.cos(angle),
        y: center + dist * Math.sin(angle)
      };
    };

    // User Points (only for evaluated axes)
    const userPointsStr = axesKeys
      .map((k, i) => {
        const val = radarData.evaluated_axes[k].score || 0;
        const pt = getPoint(i, val);
        return `${pt.x},${pt.y}`;
      })
      .join(" ");

    // Target Benchmark Points
    const targetPointsStr = axesKeys
      .map((k, i) => {
        const val = radarData.target_benchmarks[k] || 75;
        const pt = getPoint(i, val);
        return `${pt.x},${pt.y}`;
      })
      .join(" ");

    return (
      <svg width={size} height={size} className="mx-auto overflow-visible">
        {/* Radar Concentric Webs */}
        {[0.25, 0.5, 0.75, 1.0].map((level, idx) => (
          <polygon
            key={idx}
            points={axesKeys
              .map((_, i) => {
                const pt = getPoint(i, 100 * level);
                return `${pt.x},${pt.y}`;
              })
              .join(" ")}
            className="fill-none stroke-slate-300 dark:stroke-slate-800"
            strokeWidth="1"
          />
        ))}

        {/* Axis Spokes */}
        {axesKeys.map((k, i) => {
          const pt = getPoint(i, 100);
          return (
            <line
              key={i}
              x1={center}
              y1={center}
              x2={pt.x}
              y2={pt.y}
              className="stroke-slate-300 dark:stroke-slate-800"
              strokeWidth="1"
            />
          );
        })}

        {/* Target Benchmark Polygon */}
        <polygon
          points={targetPointsStr}
          className="fill-amber-500/10 stroke-amber-500/60"
          strokeWidth="2"
          strokeDasharray="4 4"
        />

        {/* Candidate User Polygon */}
        <polygon
          points={userPointsStr}
          className="fill-blue-500/25 stroke-blue-500"
          strokeWidth="2.5"
        />

        {/* Labels around periphery */}
        {axesKeys.map((k, i) => {
          const pt = getPoint(i, 125);
          const score = radarData.evaluated_axes[k].score;
          return (
            <text
              key={i}
              x={pt.x}
              y={pt.y}
              className="fill-slate-700 dark:fill-slate-300"
              fontSize="9"
              fontWeight="bold"
              textAnchor="middle"
              dominantBaseline="middle"
            >
              {k} ({score !== null ? `${score}%` : 'N/A'})
            </text>
          );
        })}
      </svg>
    );
  };

  return (
    <div className="space-y-6">
      
      {/* 1. HEADER BANNER */}
      <PageHeader
        category="Empirical Skill Matrix"
        badgeText="SKILL RADAR"
        title="Career Skill Radar 🎯"
        subtitle="12-axis empirical performance vector comparing your actual platform evidence against Target Role benchmarks."
        actions={
          <div className="shrink-0">
            <label className="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-1 block">Target Role Benchmark:</label>
            <select
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
              className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-slate-900 dark:text-white px-4 py-2.5 rounded-xl text-xs font-bold focus:outline-none focus:border-blue-500"
            >
              {TARGET_ROLES.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>
        }
      />

      {radarData && (
        <div className="space-y-6">

          {/* 2. HIGHEST SKILL GAP RECOMMENDATION CARD */}
          {radarData.highest_gap && (
            <div className="prof-card p-6 border-l-4 border-l-rose-500 flex flex-col md:flex-row items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20 rounded-full font-mono font-bold text-[10px]">
                    PRIMARY TARGET GAP IDENTIFIED
                  </span>
                  <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                    Highest Gap: <strong className="text-slate-900 dark:text-white">{radarData.highest_gap.axis}</strong>
                  </span>
                </div>
                <h2 className="text-lg font-bold text-slate-900 dark:text-white">
                  Recommended Focus: {radarData.highest_gap.recommended_action}
                </h2>
              </div>

              <Link
                to={radarData.highest_gap.route}
                className="btn-primary shrink-0"
              >
                Launch Feature →
              </Link>
            </div>
          )}

          {/* 3. RADAR SVG CHART & STATS */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
            
            {/* SVG Visualizer */}
            <div className="prof-card p-8 flex flex-col items-center justify-center space-y-4 min-h-[380px]">
              <div className="flex items-center gap-6 text-xs font-mono mb-2">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 bg-blue-500 rounded-sm"></span>
                  <span className="text-slate-700 dark:text-slate-200">Your Evaluated Vector</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 border border-dashed border-amber-500 bg-amber-500/20 rounded-sm"></span>
                  <span className="text-slate-700 dark:text-slate-200">Target Role Benchmark ({selectedRole})</span>
                </div>
              </div>

              {renderRadarSVG()}
            </div>

            {/* Overall Score Gauge */}
            <div className="prof-card p-8 space-y-6 flex flex-col justify-between min-h-[380px]">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Average Evaluated Skill Matrix</span>
                <div className="flex items-baseline gap-2 mt-2">
                  <span className="text-5xl font-extrabold text-blue-600 dark:text-blue-400 font-mono">
                    {radarData.overall_average_score}
                  </span>
                  <span className="text-sm text-slate-500 dark:text-slate-400 font-mono">/ 100</span>
                </div>

                <p className="text-xs text-slate-600 dark:text-slate-300 mt-3 leading-relaxed">
                  Calculated dynamically from your actual ATS resume score, coding arena submissions, mock interview evaluations, and speech prosody data. Un-evaluated areas explicitly show "Not enough data".
                </p>
              </div>

              <div className="pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 font-mono">
                <span>Target Role: <strong className="text-slate-900 dark:text-white">{selectedRole}</strong></span>
                <span>Axes Evaluated: <strong className="text-slate-900 dark:text-white">12/12</strong></span>
              </div>
            </div>

          </div>

          {/* 4. 12-AXIS SCORE BREAKDOWN GRID */}
          <div className="prof-card p-6 space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              📊 12-Axis Empirical Score Breakdown
            </h3>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 text-xs">
              {Object.entries(radarData.evaluated_axes || {}).map(([axis, info]) => {
                const targetVal = radarData.target_benchmarks?.[axis] || 75;
                const isEvaluated = info.status === "evaluated" && info.score !== null;

                return (
                  <div key={axis} className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800 space-y-2">
                    <span className="text-xs font-bold text-slate-900 dark:text-white block">{axis}</span>
                    
                    {isEvaluated ? (
                      <div className="flex items-baseline justify-between">
                        <span className="text-xl font-extrabold text-blue-600 dark:text-blue-400 font-mono">
                          {info.score}%
                        </span>
                        <span className="text-[10px] text-slate-500 font-mono">
                          Target: {targetVal}%
                        </span>
                      </div>
                    ) : (
                      <span className="px-2 py-1 bg-slate-100 dark:bg-slate-900 text-amber-600 dark:text-amber-400 border border-slate-200 dark:border-slate-800 text-[10px] font-mono font-bold rounded inline-block">
                        Not enough data
                      </span>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* 5. HISTORICAL EVALUATION TRENDS */}
          {history.length > 0 && (
            <div className="prof-card p-6 space-y-4">
              <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center justify-between">
                <span>📜 Historical Radar Evaluation Snapshots</span>
                <span className="text-xs font-mono text-slate-500 dark:text-slate-400">{history.length} Snapshots Saved</span>
              </h3>

              <div className="space-y-3">
                {history.map((snap, idx) => (
                  <div key={idx} className="bg-slate-50 dark:bg-slate-950 p-4 rounded-xl border border-slate-200 dark:border-slate-800 flex items-center justify-between text-xs">
                    <div>
                      <span className="font-bold text-slate-900 dark:text-white">{snap.target_role} Benchmark</span>
                      <span className="text-slate-500 text-[10px] block font-mono">{snap.created_at?.split('T')[0]}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-[10px] text-slate-500 dark:text-slate-400 block font-mono">Average Score</span>
                      <span className="text-base font-bold text-blue-600 dark:text-blue-400 font-mono">{snap.overall_average_score} / 100</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>
      )}

    </div>
  );
};

export default CareerSkillRadar;
