import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const AIJobSalaryPredictor = () => {
  const [role, setRole] = useState('Full Stack Developer');
  const [experience, setExperience] = useState('Fresher (0-2 years)');
  const [location, setLocation] = useState('India');
  const [company, setCompany] = useState('Tier-1 Product Tech');
  const [skills, setSkills] = useState('Python, React, FastAPI, MongoDB, System Design');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handlePredict = async (e) => {
    e?.preventDefault();
    setLoading(true);
    try {
      const skillsArr = skills.split(',').map(s => s.trim()).filter(Boolean);
      const res = await api.jobs.predictSalary({
        target_role: role,
        skills: skillsArr,
        experience,
        location,
        company_name: company
      });
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handlePredict({ preventDefault: () => {} });
  }, []);

  return (
    <div className="min-h-screen bg-[#F8F9FC] dark:bg-[#0B0B14] text-slate-900 dark:text-slate-100 p-6 lg:p-10 space-y-6">
      <div className="flex items-center justify-between prof-card p-6 rounded-2xl">
        <div>
          <Link to="/dashboard" className="text-slate-500 hover:text-[#4F46E5] text-sm font-semibold">
            ← Back to Dashboard
          </Link>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white mt-2 flex items-center gap-2">
            AI Placement Salary & Compensation Predictor 💰
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Data-driven compensation estimation backed by live market search benchmarks & stored in MongoDB.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Form */}
        <form onSubmit={handlePredict} className="lg:col-span-6 prof-card rounded-2xl p-6 space-y-4 text-xs">
          <div>
            <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1">Target Engineering Role</label>
            <input
              type="text"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full px-3.5 py-2.5 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
            />
          </div>

          <div>
            <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1">Technical Skills</label>
            <input
              type="text"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              className="w-full px-3.5 py-2.5 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1">Experience</label>
              <select
                value={experience}
                onChange={(e) => setExperience(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
              >
                <option value="Fresher (0-2 years)">Fresher / 0-2 yrs</option>
                <option value="2-4 years">Mid-level / 2-4 yrs</option>
                <option value="Senior 5+ yrs">Senior 5+ yrs</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1">Target Company</label>
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full btn-ai"
          >
            {loading ? 'Analyzing Market Trends...' : '⚡ Predict Placement Salary Range'}
          </button>
        </form>

        {/* Prediction Results */}
        <div className="lg:col-span-6 space-y-4">
          {result && (
            <div className="prof-card rounded-2xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Estimated CTC Range</span>
                <span className="px-2.5 py-0.5 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 text-[10px] font-bold rounded-full">
                  Saved in MongoDB
                </span>
              </div>

              <div className="flex items-baseline gap-2">
                <span className="text-4xl font-extrabold text-slate-900 dark:text-white">{result.estimated_range}</span>
                <span className="text-xs text-slate-500 dark:text-slate-400 ml-2">Median: <strong className="text-[#7C3AED] dark:text-[#8B5CF6]">{result.median_salary}</strong></span>
              </div>

              <div className="p-3.5 bg-slate-50 dark:bg-[#151522] rounded-xl border border-slate-200 dark:border-slate-800 space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Market Demand Index:</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-bold">{result.market_demand}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500 dark:text-slate-400">Model Confidence:</span>
                  <span className="text-[#4F46E5] dark:text-[#6366F1] font-bold">{result.confidence_score}%</span>
                </div>
              </div>

              {result.data_sources?.length > 0 && (
                <div className="space-y-1.5 pt-2 border-t border-slate-200 dark:border-slate-800 text-xs">
                  <p className="text-[11px] font-bold text-slate-500 dark:text-slate-400">🌐 Live Market Sources:</p>
                  {result.data_sources.map((s, idx) => (
                    <a key={idx} href={s.url} target="_blank" rel="noreferrer" className="block text-[10px] text-[#4F46E5] dark:text-[#6366F1] hover:underline truncate">
                      • {s.title} ({s.source})
                    </a>
                  ))}
                </div>
              )}

              <p className="text-[10px] text-slate-400 italic pt-1">{result.disclaimer}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIJobSalaryPredictor;
