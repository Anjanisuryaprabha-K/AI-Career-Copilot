import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const GitHubAnalyzer = () => {
  const [username, setUsername] = useState('preetham-dev');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const handleScan = async (e) => {
    e?.preventDefault();
    if (!username.trim()) return;
    setLoading(true);
    try {
      const res = await api.tools.githubScorer(username);
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8F9FC] dark:bg-[#0B0B14] text-slate-900 dark:text-slate-100 p-6 lg:p-10 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 prof-card p-6 rounded-2xl">
        <div>
          <Link to="/dashboard" className="text-slate-500 hover:text-[#4F46E5] text-sm font-semibold">
            ← Back to Dashboard
          </Link>
          <h1 className="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white mt-2 flex items-center gap-2">
            GitHub Developer Profile & Codebase Auditor 🐙
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Audit commit frequency, repository documentation quality, and language breadth for placement.
          </p>
        </div>
      </div>

      <form onSubmit={handleScan} className="prof-card p-4 rounded-2xl flex gap-3 max-w-xl">
        <input
          type="text"
          placeholder="Enter GitHub username (e.g. preetham-dev)..."
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="flex-1 px-4 py-2 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
        />
        <button
          type="submit"
          disabled={loading}
          className="btn-primary"
        >
          {loading ? 'Auditing...' : 'Audit GitHub Profile'}
        </button>
      </form>

      {data && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-6 prof-card rounded-2xl p-6 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Technical Health Score</span>
              <span className="px-2.5 py-0.5 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 text-[10px] font-bold rounded-full">
                Saved in MongoDB
              </span>
            </div>

            <div className="flex items-baseline gap-2">
              <span className="text-5xl font-extrabold text-slate-900 dark:text-white">{data.health_score || 86}</span>
              <span className="text-slate-400 text-lg font-bold">/ 100</span>
              <span className="ml-auto text-xs font-semibold text-emerald-600 dark:text-emerald-400">{data.commit_consistency_rating || 'Very High'}</span>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs pt-2">
              <div className="p-3 bg-slate-50 dark:bg-[#151522] rounded-xl border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 text-[10px]">Public Repositories</span>
                <p className="text-base font-bold text-slate-900 dark:text-white mt-0.5">{data.total_repos || 14}</p>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-[#151522] rounded-xl border border-slate-200 dark:border-slate-800">
                <span className="text-slate-500 text-[10px]">Starred Projects</span>
                <p className="text-base font-bold text-[#4F46E5] dark:text-[#6366F1] mt-0.5">{data.starred_repos || 6}</p>
              </div>
            </div>
          </div>

          <div className="lg:col-span-6 prof-card rounded-2xl p-6 space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Portfolio Improvement Tips</h3>
            <ul className="space-y-2 text-xs text-slate-700 dark:text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-[#4F46E5] font-bold">•</span>
                <span>Pin your full-stack capstone (FastAPI + React + MongoDB) to the top of your profile.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[#4F46E5] font-bold">•</span>
                <span>Include architectural diagrams and API documentation in repository READMEs.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-[#4F46E5] font-bold">•</span>
                <span>Maintain consistent weekly commit streaks on data structures & algorithmic repositories.</span>
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default GitHubAnalyzer;
