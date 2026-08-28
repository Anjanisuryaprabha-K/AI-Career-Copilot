import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const ExternalLinkIcon = () => (
  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
  </svg>
);

const SparklesIcon = () => (
  <svg className="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
  </svg>
);

const CompanyPrep = () => {
  const [catalog, setCatalog] = useState([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState('ibm');
  const [selectedRole, setSelectedRole] = useState('Software Engineer');
  const [prepPlan, setPrepPlan] = useState(null);
  const [loadingCatalog, setLoadingCatalog] = useState(true);
  const [loadingPlan, setLoadingPlan] = useState(false);

  // Fetch company catalog on mount
  useEffect(() => {
    const fetchCatalog = async () => {
      setLoadingCatalog(true);
      try {
        const res = await api.companyPrep.getCatalog();
        if (res?.companies) {
          setCatalog(res.companies);
          if (res.companies.length > 0) {
            const first = res.companies[0];
            setSelectedCompanyId(first.id);
            setSelectedRole(first.default_role || first.supported_roles[0]);
          }
        }
      } catch (err) {
        console.error('Error fetching company catalog:', err);
      } finally {
        setLoadingCatalog(false);
      }
    };
    fetchCatalog();
  }, []);

  // Fetch preparation plan whenever selectedCompanyId or selectedRole changes
  const loadPrepPlan = async (cid, role) => {
    setLoadingPlan(true);
    try {
      const res = await api.companyPrep.getPlan(cid, role);
      if (res?.plan) {
        setPrepPlan(res.plan);
      }
    } catch (err) {
      console.error('Error loading company prep plan:', err);
    } finally {
      setLoadingPlan(false);
    }
  };

  useEffect(() => {
    if (selectedCompanyId) {
      loadPrepPlan(selectedCompanyId, selectedRole);
    }
  }, [selectedCompanyId, selectedRole]);

  // Handle Company Selection
  const handleCompanySelect = (cid) => {
    setSelectedCompanyId(cid);
    const comp = catalog.find(c => c.id === cid);
    if (comp && comp.supported_roles?.length > 0) {
      setSelectedRole(comp.default_role || comp.supported_roles[0]);
    }
  };

  const selectedCompanyMeta = catalog.find(c => c.id === selectedCompanyId);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-10 space-y-8">
      
      {/* 1. HEADER BANNER */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <Link to="/dashboard" className="text-xs font-semibold text-blue-400 hover:underline">
              ← Dashboard
            </Link>
            <span className="text-slate-600">•</span>
            <span className="px-2.5 py-0.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold rounded-full font-mono flex items-center gap-1">
              <SparklesIcon /> TARGETED RECRUITMENT PREPARATION
            </span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white mt-2 tracking-tight flex items-center gap-2">
            Company-Specific Placement Preparation 🏢
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Tailor your preparation to target tech companies with role-specific skill gap analysis, coding topics, round breakdowns, and AI recommendations.
          </p>
        </div>

        {/* Action Link to Company Insights */}
        <Link
          to="/company-insights"
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition flex items-center gap-1.5 shrink-0 self-start md:self-auto"
        >
          <span>View Company Archives 🏢</span>
        </Link>
      </div>

      {/* 2. COMPANY SELECTOR & ROLE TOOLBAR */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
        <div className="flex items-center justify-between">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Select Target Company:
          </label>
          {selectedCompanyMeta && (
            <span className="text-xs font-mono text-indigo-400 font-semibold">
              Tier: {selectedCompanyMeta.tier} | Avg CTC: {selectedCompanyMeta.avg_ctc}
            </span>
          )}
        </div>

        {/* Company Cards List */}
        <div className="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-thin">
          {catalog.map((comp) => {
            const isSelected = selectedCompanyId === comp.id;
            return (
              <button
                key={comp.id}
                onClick={() => handleCompanySelect(comp.id)}
                className={`px-4 py-3 rounded-2xl text-xs font-bold transition flex items-center gap-2.5 shrink-0 border ${
                  isSelected
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white border-blue-400 shadow-lg shadow-blue-600/30'
                    : 'bg-slate-950 text-slate-300 border-slate-800 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <span className="text-base">{comp.logo || '🏢'}</span>
                <div className="text-left">
                  <div className="font-bold">{comp.name}</div>
                  <div className={`text-[10px] ${isSelected ? 'text-blue-200' : 'text-slate-500'} font-mono`}>{comp.difficulty}</div>
                </div>
              </button>
            );
          })}
        </div>

        {/* Target Role Selector */}
        {selectedCompanyMeta && (
          <div className="flex flex-col sm:flex-row sm:items-center gap-4 pt-3 border-t border-slate-800">
            <label className="text-xs font-semibold text-slate-400 shrink-0">Select Target Role:</label>
            <div className="flex items-center gap-2 overflow-x-auto">
              {(selectedCompanyMeta.supported_roles || []).map((r) => {
                const isRoleSelected = selectedRole === r;
                return (
                  <button
                    key={r}
                    onClick={() => setSelectedRole(r)}
                    className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition ${
                      isRoleSelected
                        ? 'bg-blue-500/20 text-blue-300 border border-blue-500/40 shadow-sm'
                        : 'bg-slate-950 text-slate-400 border border-slate-800 hover:text-slate-200'
                    }`}
                  >
                    {r}
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* 3. TRANSPARENCY & DISCLAIMER BANNER */}
      <div className="bg-slate-900/60 border border-slate-800/80 p-4 rounded-xl flex items-start gap-3 text-xs text-slate-400">
        <span className="text-amber-400 text-base shrink-0">ℹ️</span>
        <div>
          <strong className="text-slate-200 font-semibold block">Company Insights & Preparation Framework:</strong>
          Preparation recommendations combine known public company tech stacks, standard industry assessment benchmarks, and AI-driven skill gap evaluations. Recommendations do not represent exact leaked exam questions or guaranteed hiring criteria.
        </div>
      </div>

      {loadingPlan ? (
        <div className="py-20 text-center text-slate-400 animate-pulse text-sm">
          Calculating company-specific readiness and generating targeted plan...
        </div>
      ) : prepPlan ? (
        <div className="space-y-8">

          {/* 4. OVERALL READINESS DASHBOARD */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">

            {/* Overall Score Card */}
            <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl flex flex-col justify-between space-y-4 backdrop-blur-md shadow-xl lg:col-span-1">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Company Match Score</span>
                <div className="flex items-baseline gap-2 mt-2">
                  <span className="text-3xl font-extrabold text-emerald-400 font-mono">
                    {prepPlan.readiness_summary.overall_readiness}%
                  </span>
                  <span className="text-xs text-slate-400 font-mono">Match</span>
                </div>

                <div className="h-3 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800 mt-3">
                  <div
                    className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-emerald-400 transition-all duration-500 rounded-full"
                    style={{ width: `${prepPlan.readiness_summary.overall_readiness}%` }}
                  />
                </div>
              </div>

              <div className="text-xs text-slate-400 pt-2 border-t border-slate-800 font-mono">
                Target: <strong className="text-white">{prepPlan.company.name}</strong> ({prepPlan.target_role})
              </div>
            </div>

            {/* Pillar Breakdown Cards */}
            <div className="lg:col-span-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

              {/* Coding Readiness */}
              <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl flex flex-col justify-between space-y-2 backdrop-blur-md">
                <span className="text-xs font-semibold text-slate-400">Coding Readiness</span>
                <span className="text-2xl font-extrabold text-blue-400 font-mono">{prepPlan.readiness_summary.coding_readiness}%</span>
                <Link to="/coding-arena" className="text-[11px] text-blue-400 hover:underline font-semibold flex items-center gap-1">
                  Practice Coding ⚡
                </Link>
              </div>

              {/* Interview Readiness */}
              <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl flex flex-col justify-between space-y-2 backdrop-blur-md">
                <span className="text-xs font-semibold text-slate-400">Interview Readiness</span>
                <span className="text-2xl font-extrabold text-purple-400 font-mono">{prepPlan.readiness_summary.interview_readiness}%</span>
                <Link to="/interview-simulator" className="text-[11px] text-purple-400 hover:underline font-semibold flex items-center gap-1">
                  Mock Interview 🎙️
                </Link>
              </div>

              {/* Resume ATS Match */}
              <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl flex flex-col justify-between space-y-2 backdrop-blur-md">
                <span className="text-xs font-semibold text-slate-400">Resume ATS Match</span>
                <span className="text-2xl font-extrabold text-amber-400 font-mono">{prepPlan.readiness_summary.resume_match_score}%</span>
                <Link to="/resume-analyzer" className="text-[11px] text-amber-400 hover:underline font-semibold flex items-center gap-1">
                  Scan Resume 📄
                </Link>
              </div>

              {/* Skill Overlap */}
              <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl flex flex-col justify-between space-y-2 backdrop-blur-md">
                <span className="text-xs font-semibold text-slate-400">Required Skills Fit</span>
                <span className="text-2xl font-extrabold text-emerald-400 font-mono">{prepPlan.readiness_summary.skill_overlap_pct}%</span>
                <Link to="/skill-gap" className="text-[11px] text-emerald-400 hover:underline font-semibold flex items-center gap-1">
                  Skill Gap Check ⚡
                </Link>
              </div>

            </div>
          </div>

          {/* 5. REQUIRED SKILLS & MISSING SKILLS GAP ANALYSIS */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            {/* Required Technical Skills */}
            <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
              <h2 className="text-base font-bold text-white flex items-center justify-between">
                <span>🎯 Role Required Competencies</span>
                <span className="text-xs font-mono text-slate-400">{prepPlan.skills_analysis.required_skills.length} Total Skills</span>
              </h2>

              <div className="flex flex-wrap gap-2">
                {prepPlan.skills_analysis.required_skills.map(s => {
                  const isMatched = prepPlan.skills_analysis.matched_skills.includes(s);
                  return (
                    <span
                      key={s}
                      className={`px-3 py-1 rounded-xl text-xs font-bold border flex items-center gap-1.5 ${
                        isMatched
                          ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                          : 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                      }`}
                    >
                      <span>{isMatched ? '✓' : '✕'}</span>
                      <span>{s}</span>
                    </span>
                  );
                })}
              </div>
            </div>

            {/* Missing Skills Recommendation Card */}
            <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md flex flex-col justify-between">
              <div className="space-y-3">
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  <span>🚨 Priority Skill Gaps</span>
                  <span className="text-xs font-mono px-2 py-0.5 bg-rose-500/10 text-rose-400 border border-rose-500/20 rounded-full">
                    {prepPlan.skills_analysis.missing_skills.length} Missing
                  </span>
                </h2>

                {prepPlan.skills_analysis.missing_skills.length > 0 ? (
                  <p className="text-xs text-slate-300 leading-relaxed">
                    To optimize your fit for <strong className="text-white">{prepPlan.company.name} ({prepPlan.target_role})</strong>, add the following key competencies to your technical profile and resume:
                  </p>
                ) : (
                  <p className="text-xs text-emerald-400 font-semibold">
                    🎉 Excellent! You possess all required technical skills for this role!
                  </p>
                )}

                <div className="flex flex-wrap gap-2 pt-1">
                  {prepPlan.skills_analysis.missing_skills.map(m => (
                    <span key={m} className="px-3 py-1 bg-rose-500/10 text-rose-300 border border-rose-500/30 text-xs font-bold rounded-xl font-mono">
                      + {m}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
                <span className="text-xs text-slate-400">Update resume keywords:</span>
                <Link
                  to="/resume-analyzer"
                  className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-xl shadow transition"
                >
                  Optimize Resume 📄
                </Link>
              </div>
            </div>

          </div>

          {/* 6. ROUND-BY-ROUND INTERVIEW RECRUITMENT PROCESS */}
          <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <span>📋 Company Interview Process & Round Breakdown</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {(prepPlan.rounds_breakdown || []).map(r => (
                <div key={r.round} className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="px-2 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded font-bold">
                      Round {r.round}
                    </span>
                    <span className="text-slate-500">⏱️ {r.duration}</span>
                  </div>
                  <h3 className="text-sm font-bold text-white">{r.name}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{r.type}</p>
                </div>
              ))}
            </div>
          </div>

          {/* 7. RECOMMENDED CODING PRACTICE QUESTIONS */}
          <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h2 className="text-base font-bold text-white flex items-center gap-2">
                  <span>💻 Recommended Coding Arena Practice Questions</span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Hand-picked from existing Coding Arena question bank based on {prepPlan.company.name}'s key DSA topics ({prepPlan.preparation_topics.coding_topics.join(', ')}).
                </p>
              </div>

              <Link
                to="/coding-arena"
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl shadow transition shrink-0 self-start sm:self-auto"
              >
                Open Coding Arena ⚡
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {(prepPlan.recommended_questions || []).map(q => (
                <div key={q.id} className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex flex-col justify-between space-y-3">
                  <div>
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono px-2 py-0.5 bg-slate-800 text-blue-300 rounded border border-slate-700">
                        #{q.category || 'DSA'}
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded font-mono ${
                        q.difficulty === 'Easy' ? 'bg-emerald-500/20 text-emerald-400' : (q.difficulty === 'Medium' ? 'bg-amber-500/20 text-amber-400' : 'bg-red-500/20 text-red-400')
                      }`}>
                        {q.difficulty}
                      </span>
                    </div>

                    <h3 className="text-sm font-bold text-white mt-2">{q.title}</h3>
                  </div>

                  <Link
                    to="/coding-arena"
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-lg border border-slate-700 transition flex items-center justify-between"
                  >
                    <span>Solve Challenge</span>
                    <ExternalLinkIcon />
                  </Link>
                </div>
              ))}
            </div>
          </div>

          {/* 8. TECHNICAL, SQL, CS FUNDAMENTALS & BEHAVIORAL TOPICS */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

            {/* CS Fundamentals */}
            <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-3 backdrop-blur-md">
              <h2 className="text-sm font-bold text-white flex items-center gap-2">
                <span>📚 Core CS Fundamentals</span>
              </h2>
              <ul className="space-y-2 text-xs text-slate-300">
                {(prepPlan.preparation_topics.cs_fundamentals || []).map((cs, i) => (
                  <li key={i} className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between">
                    <span>{cs}</span>
                    <span className="text-slate-500">Focus</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* SQL Topics */}
            <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-3 backdrop-blur-md">
              <h2 className="text-sm font-bold text-white flex items-center gap-2">
                <span>🗄️ SQL & Database Topics</span>
              </h2>
              <ul className="space-y-2 text-xs text-slate-300">
                {(prepPlan.preparation_topics.sql_topics || []).map((sql, i) => (
                  <li key={i} className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between">
                    <span>{sql}</span>
                    <span className="text-slate-500">Query</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Behavioral & STAR Topics */}
            <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-3 backdrop-blur-md flex flex-col justify-between">
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <span>⭐ Behavioral & Leadership Principles</span>
                </h2>
                <ul className="space-y-2 text-xs text-slate-300 mt-3">
                  {(prepPlan.preparation_topics.behavioral_topics || []).map((b, i) => (
                    <li key={i} className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 text-slate-200">
                      • {b}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="pt-3 border-t border-slate-800">
                <Link
                  to="/interview-simulator"
                  className="w-full px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold rounded-xl shadow transition text-center block"
                >
                  Practice in AI Mock Interview 🎙️
                </Link>
              </div>
            </div>

          </div>

          {/* 9. CONNECTED PLATFORM MODULE QUICK LINKS */}
          <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400">
              Connected Platform Preparation Modules:
            </h2>

            <div className="flex flex-wrap items-center gap-3">
              <Link to="/placement-roadmap" className="px-4 py-2 bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-200 text-xs font-bold rounded-xl transition">
                🧠 Adaptive Career Roadmap
              </Link>
              <Link to="/coding-arena" className="px-4 py-2 bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-200 text-xs font-bold rounded-xl transition">
                💻 Coding Arena Compiler
              </Link>
              <Link to="/interview-simulator" className="px-4 py-2 bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-200 text-xs font-bold rounded-xl transition">
                🎙️ AI Mock Interview
              </Link>
              <Link to="/resume-analyzer" className="px-4 py-2 bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-200 text-xs font-bold rounded-xl transition">
                📄 ATS Resume Analyzer
              </Link>
              <Link to="/oa-simulator" className="px-4 py-2 bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-200 text-xs font-bold rounded-xl transition">
                ⏱️ Mock OA Exam Simulator
              </Link>
              <Link to="/job-readiness" className="px-4 py-2 bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-200 text-xs font-bold rounded-xl transition">
                🎯 Job Readiness Index
              </Link>
              <Link to="/company-insights" className="px-4 py-2 bg-slate-950 hover:bg-slate-800 border border-slate-800 text-slate-200 text-xs font-bold rounded-xl transition">
                🏢 Company Archives
              </Link>
            </div>
          </div>

        </div>
      ) : null}

    </div>
  );
};

export default CompanyPrep;
