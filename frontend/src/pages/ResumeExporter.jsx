import React, { useState } from 'react';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { PageHeader } from '../components/common/DesignSystemComponents';

const ResumeExporter = () => {
  const { user } = useAuth();
  const [latexData, setLatexData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = async () => {
    setIsLoading(true);
    try {
      const data = await api.resume.generateLatex({
        user_name: user?.name || "Preetham V",
        email: user?.email || "preetham@placement.edu",
        skills: user?.skills || ["Python", "FastAPI", "React", "MongoDB", "Docker"]
      });
      setLatexData(data.data);
    } catch {}
    finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <PageHeader
        category="Resume Tools"
        badgeText="LATEX ATS SOURCE"
        title="1-Click ATS LaTeX Resume Exporter 📄"
        subtitle="Export clean, single-column Overleaf-compatible LaTeX source code formatted for 100% ATS readability."
      />

      <div className="prof-card p-8 space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h3 className="text-base font-bold text-slate-900 dark:text-white">Generate Clean ATS Resume Source</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Single-column, zero-table layout verified for automated applicant tracking systems.</p>
          </div>
          <button
            onClick={handleGenerate}
            disabled={isLoading}
            className="btn-ai shrink-0"
          >
            {isLoading ? 'Generating LaTeX...' : 'Generate LaTeX Code ✨'}
          </button>
        </div>

        {latexData && (
          <div className="space-y-3 pt-6 border-t border-slate-200 dark:border-slate-800">
            <div className="flex justify-between items-center">
              <span className="text-xs font-mono text-cyan-600 dark:text-cyan-400 font-bold">{latexData.filename}</span>
              <button
                onClick={() => navigator.clipboard.writeText(latexData.latex_source)}
                className="btn-secondary"
              >
                📋 Copy LaTeX Code
              </button>
            </div>
            <textarea
              readOnly
              value={latexData.latex_source}
              className="w-full h-80 p-4 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl font-mono text-xs text-slate-800 dark:text-slate-200 resize-none focus:outline-none"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeExporter;
