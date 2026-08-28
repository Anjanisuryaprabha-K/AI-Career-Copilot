import React, { useState } from 'react';
import { api } from '../services/api';

const AICoverLetterGenerator = () => {
  const [formData, setFormData] = useState({
    user_name: 'Preetham V',
    target_role: 'Full Stack Developer',
    company_name: 'Google',
    skills: 'Python, FastAPI, React, MongoDB, System Design',
    experience_summary: 'Developed high-performance web applications and solved 300+ algorithm challenges.'
  });
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const data = await api.tools.coverLetter({
        ...formData,
        skills: formData.skills.split(',').map((s) => s.trim())
      });
      setResult(data);
    } catch {
      setResult({
        cover_letter_text: `Dear Hiring Team at ${formData.company_name},

I am writing to express my strong interest in the ${formData.target_role} position. With expertise in ${formData.skills}, I am ready to add immediate value to your team.`,
        word_count: 180,
        strengths_highlighted: ["FastAPI", "React", "MongoDB"]
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6 lg:p-10 max-w-5xl mx-auto space-y-6 text-slate-900 dark:text-slate-100">
      <div className="prof-card p-6 rounded-2xl">
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
          <span>✍️</span> AI Cover Letter Generator
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Generate role-tailored cover letters optimized for hiring recruiters.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <form onSubmit={handleSubmit} className="prof-card p-6 rounded-2xl space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Your Name</label>
            <input
              type="text"
              value={formData.user_name}
              onChange={(e) => setFormData({ ...formData, user_name: e.target.value })}
              className="w-full px-3.5 py-2 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Target Company</label>
            <input
              type="text"
              value={formData.company_name}
              onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
              className="w-full px-3.5 py-2 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Target Role</label>
            <input
              type="text"
              value={formData.target_role}
              onChange={(e) => setFormData({ ...formData, target_role: e.target.value })}
              className="w-full px-3.5 py-2 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Key Skills (comma separated)</label>
            <input
              type="text"
              value={formData.skills}
              onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
              className="w-full px-3.5 py-2 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-sm text-slate-900 dark:text-white focus:outline-none focus:border-[#4F46E5]"
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full btn-ai"
          >
            {isLoading ? 'Generating AI Letter...' : 'Generate Cover Letter'}
          </button>
        </form>

        <div className="prof-card p-6 rounded-2xl flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100 mb-3 flex items-center justify-between">
              <span>Generated Draft</span>
              {result && <span className="text-xs text-[#7C3AED] dark:text-[#8B5CF6] font-mono">{result.word_count} words</span>}
            </h3>
            {result ? (
              <textarea
                readOnly
                value={result.cover_letter_text}
                className="w-full h-80 p-3.5 bg-slate-50 dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-800 dark:text-slate-200 font-mono resize-none focus:outline-none"
              />
            ) : (
              <div className="h-80 flex items-center justify-center text-slate-400 text-xs border border-dashed border-slate-200 dark:border-slate-800 rounded-xl">
                Fill the form and click generate to view your letter.
              </div>
            )}
          </div>
          {result && (
            <button
              onClick={() => navigator.clipboard.writeText(result.cover_letter_text)}
              className="mt-4 w-full btn-secondary"
            >
              📋 Copy to Clipboard
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AICoverLetterGenerator;
