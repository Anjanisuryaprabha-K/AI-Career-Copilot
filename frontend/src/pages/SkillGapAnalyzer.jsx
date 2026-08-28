import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { PageHeader, AnimatedProgressBar } from '../components/common/DesignSystemComponents';

const SkillGapAnalyzer = () => {
  const [targetRole, setTargetRole] = useState('Full Stack Developer');
  
  const skillMatrix = {
    acquired: ['React', 'JavaScript', 'Node.js', 'Express', 'MongoDB', 'HTML5', 'CSS3', 'Git', 'REST APIs'],
    missing: ['Docker', 'TypeScript', 'Redis', 'CI/CD Pipelines', 'SQL / PostgreSQL'],
    criticalNext: 'Docker & Containerization',
    readinessPercent: 68,
  };

  return (
    <div className="space-y-6">
      <PageHeader
        category="Skill Gap & Benchmarks"
        badgeText="SKILL GAP ANALYZER"
        title="Skill Gap Analyzer 🎯"
        subtitle="Compare your verified technical skills against industry placement benchmarks."
        actions={
          <div>
            <label className="block text-[11px] font-semibold text-slate-500 dark:text-slate-400 mb-1">Target Role</label>
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="px-3.5 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white text-xs font-medium focus:outline-none"
            >
              <option value="Full Stack Developer">Full Stack Developer</option>
              <option value="Backend Developer">Backend Developer</option>
              <option value="AI/ML Engineer">AI/ML Engineer</option>
            </select>
          </div>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Readiness Overview */}
        <div className="lg:col-span-4 prof-card p-6 space-y-5">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">Role Match Readiness</h3>
          <div className="text-center py-4">
            <div className="text-5xl font-extrabold text-blue-600 dark:text-blue-400 font-mono">{skillMatrix.readinessPercent}%</div>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">Target: {targetRole}</p>
            <div className="mt-3">
              <AnimatedProgressBar value={skillMatrix.readinessPercent} height="h-2.5" />
            </div>
          </div>

          <div className="p-3.5 bg-blue-500/10 border border-blue-500/20 rounded-xl text-xs space-y-1">
            <span className="font-bold text-blue-600 dark:text-blue-300">⚡ Next High Impact Skill:</span>
            <p className="text-slate-700 dark:text-slate-300">{skillMatrix.criticalNext}</p>
          </div>

          <Link
            to="/roadmap"
            className="block text-center w-full btn-primary py-2.5 text-xs font-semibold"
          >
            Generate Personalized Roadmap →
          </Link>
        </div>

        {/* Acquired vs Missing Skills */}
        <div className="lg:col-span-8 space-y-6">
          <div className="prof-card p-6 space-y-4">
            <h3 className="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">
              ✓ Acquired Skills ({skillMatrix.acquired.length})
            </h3>
            <div className="flex flex-wrap gap-2">
              {skillMatrix.acquired.map((s, i) => (
                <span key={i} className="px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-700 dark:text-emerald-300 text-xs font-medium rounded-lg">
                  {s}
                </span>
              ))}
            </div>
          </div>

          <div className="prof-card p-6 space-y-4">
            <h3 className="text-xs font-bold text-rose-600 dark:text-rose-400 uppercase tracking-wider">
              ⚠️ Missing Prerequisites ({skillMatrix.missing.length})
            </h3>
            <div className="flex flex-wrap gap-2">
              {skillMatrix.missing.map((s, i) => (
                <span key={i} className="px-3 py-1.5 bg-rose-500/10 border border-rose-500/20 text-rose-700 dark:text-rose-300 text-xs font-medium rounded-lg">
                  + {s}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SkillGapAnalyzer;
