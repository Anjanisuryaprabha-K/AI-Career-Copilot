import { api } from '../services/api';
import React, { useState, useEffect } from 'react';

const ProjectRecommendations = () => {
  const [data, setData] = useState({ courses: [], projects: [] });

  useEffect(() => {
    api.skills.getRecommendations()
      .then((d) => setData(d))
      .catch(() => {});
  }, []);

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8 text-slate-100">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>🚀</span> Recommended Courses & Capstone Projects
        </h1>
        <p className="text-sm text-slate-400 mt-1">Curated high-impact courses and resume-ready projects to elevate your profile.</p>
      </div>

      <div className="space-y-4">
        <h2 className="text-lg font-bold text-cyan-400">⭐ Placement-Ready Capstone Projects</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.projects?.map((p, i) => (
            <div key={i} className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-3">
              <div className="flex justify-between items-start">
                <h3 className="font-bold text-white text-sm">{p.title}</h3>
                <span className="px-2 py-0.5 rounded bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs">
                  {p.difficulty}
                </span>
              </div>
              <p className="text-xs text-slate-400">{p.highlights}</p>
              <div className="flex flex-wrap gap-1">
                {p.tech_stack?.map((t, idx) => (
                  <span key={idx} className="px-2 py-0.5 rounded bg-slate-800 text-[11px] text-slate-300">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-lg font-bold text-indigo-400">📚 Recommended Courses & Roadmaps</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.courses?.map((c, i) => (
            <div key={i} className="p-5 bg-slate-900 border border-slate-800 rounded-2xl space-y-2">
              <div className="flex justify-between items-start">
                <h3 className="font-bold text-white text-sm">{c.title}</h3>
                <span className="text-xs text-slate-400">{c.duration}</span>
              </div>
              <p className="text-xs text-slate-400">{c.platform}</p>
              <a
                href={c.url}
                target="_blank"
                rel="noreferrer"
                className="inline-block mt-2 text-xs font-semibold text-cyan-400 hover:underline"
              >
                Access Course →
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProjectRecommendations;
