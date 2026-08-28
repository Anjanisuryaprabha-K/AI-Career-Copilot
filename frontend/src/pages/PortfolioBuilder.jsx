import React, { useState } from 'react';

const PortfolioBuilder = () => {
  const [profile, setProfile] = useState({
    name: 'Preetham V',
    role: 'Full Stack & AI Engineer',
    bio: 'Building scalable web applications, real-time analytics platforms, and intelligent AI tools.',
    github: 'https://github.com/preetham',
    skills: 'Python, FastAPI, React, MongoDB, System Design'
  });

  return (
    <div className="p-6 lg:p-10 max-w-5xl mx-auto space-y-6 text-slate-900 dark:text-slate-100">
      <div className="prof-card p-6 rounded-2xl">
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
          <span>🌐</span> Developer Portfolio Builder
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Generate and customize your verified recruiter-ready developer website.</p>
      </div>

      <div className="prof-card p-8 rounded-2xl space-y-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-[#4F46E5] flex items-center justify-center text-2xl font-extrabold text-white shadow-lg shadow-indigo-500/20">
            PV
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">{profile.name}</h2>
            <p className="text-sm font-semibold text-[#4F46E5] dark:text-[#6366F1]">{profile.role}</p>
          </div>
        </div>

        <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed bg-slate-50 dark:bg-[#151522] p-4 rounded-xl border border-slate-200 dark:border-slate-800">
          {profile.bio}
        </p>

        <div>
          <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">Verified Skill Highlights</h3>
          <div className="flex flex-wrap gap-2">
            {profile.skills.split(',').map((s, i) => (
              <span key={i} className="px-3 py-1 bg-[#EEF2FF] dark:bg-[#1E1B2E] border border-indigo-100 dark:border-indigo-900/40 text-[#4F46E5] dark:text-[#6366F1] rounded-lg text-xs font-semibold">
                {s.trim()}
              </span>
            ))}
          </div>
        </div>

        <div className="pt-4 border-t border-slate-200 dark:border-slate-800 flex gap-3">
          <button className="btn-primary">
            Export as HTML/React
          </button>
          <a
            href={profile.github}
            target="_blank"
            rel="noreferrer"
            className="btn-secondary"
          >
            Visit GitHub
          </a>
        </div>
      </div>
    </div>
  );
};

export default PortfolioBuilder;
