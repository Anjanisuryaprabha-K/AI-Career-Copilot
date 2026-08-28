import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

const AILinkedInOptimizer = () => {
  const [role, setRole] = useState('Full Stack Developer');
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchOptimization = async () => {
    setIsLoading(true);
    try {
      const json = await api.tools.linkedinOptimizer({ target_role: role, skills: ['Python', 'FastAPI', 'React', 'MongoDB'] });
      setData(json);
    } catch {
      setData({
        profile_strength_score: 85,
        headline_suggestions: [
          `${role} | Ex-Intern | Python, FastAPI, React | 300+ LeetCode Solved`,
          `Aspiring ${role} | Passionate about Scalable Systems & AI Platforms`
        ],
        about_summary: "Dedicated software engineer with passion for building scalable web systems and algorithmic problem solving.",
        top_keywords_to_add: ["FastAPI", "React", "MongoDB", "System Design", "Microservices", "REST APIs"]
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchOptimization();
  }, []);

  return (
    <div className="p-6 lg:p-10 max-w-5xl mx-auto space-y-6 text-slate-900 dark:text-slate-100">
      <div className="prof-card p-6 rounded-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
            <span>💼</span> AI LinkedIn Profile Optimizer
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Optimize your profile headline, summary, and keywords for tech recruiters.</p>
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="px-3 py-1.5 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
          />
          <button
            onClick={fetchOptimization}
            disabled={isLoading}
            className="btn-ai"
          >
            {isLoading ? 'Optimizing...' : 'Optimize Profile'}
          </button>
        </div>
      </div>

      {data && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-6">
            <div className="ai-insight-card p-6 space-y-3">
              <h3 className="text-sm font-bold text-[#7C3AED] dark:text-[#8B5CF6] flex items-center gap-1.5">
                <span>✨</span> Recommended Headlines
              </h3>
              {data.headline_suggestions.map((h, i) => (
                <div key={i} className="p-3 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-xs font-mono text-slate-800 dark:text-slate-200 flex justify-between items-center">
                  <span>{h}</span>
                  <button onClick={() => navigator.clipboard.writeText(h)} className="text-slate-400 hover:text-[#4F46E5] text-xs font-semibold">Copy</button>
                </div>
              ))}
            </div>

            <div className="prof-card p-6 space-y-3">
              <h3 className="text-sm font-bold text-[#4F46E5] dark:text-[#6366F1]">📝 Optimized About Summary</h3>
              <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed bg-slate-50 dark:bg-[#151522] p-4 rounded-xl border border-slate-200 dark:border-slate-800">
                {data.about_summary}
              </p>
            </div>
          </div>

          <div className="space-y-6">
            <div className="prof-card p-6 text-center">
              <p className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Profile Strength</p>
              <p className="text-4xl font-extrabold text-[#059669] my-2">{data.profile_strength_score}%</p>
              <p className="text-xs text-slate-500 dark:text-slate-400">Optimized for Placement Search</p>
            </div>

            <div className="prof-card p-6 space-y-2">
              <p className="text-xs font-bold text-slate-700 dark:text-slate-300">High-Visibility Keywords</p>
              <div className="flex flex-wrap gap-1.5">
                {data.top_keywords_to_add.map((kw, i) => (
                  <span key={i} className="px-2 py-1 rounded-md bg-[#F5F3FF] dark:bg-[#241D38] border border-[#DDD6FE] dark:border-[#3B2D54] text-[#7C3AED] dark:text-[#8B5CF6] text-[11px] font-semibold">
                    +{kw}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AILinkedInOptimizer;
