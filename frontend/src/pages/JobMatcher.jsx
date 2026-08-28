import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { PageHeader, AnimatedProgressBar } from '../components/common/DesignSystemComponents';

const JobMatcher = () => {
  const { user } = useAuth();

  // Filter States
  const [targetRole, setTargetRole] = useState(user?.target_role || 'Full Stack Developer');
  const [location, setLocation] = useState('All');
  const [remoteType, setRemoteType] = useState('All');
  const [experienceLevel, setExperienceLevel] = useState('All');
  const [minSalary, setMinSalary] = useState(0);
  const [requiredSkill, setRequiredSkill] = useState('All');
  const [sortBy, setSortBy] = useState('match_score');
  const [searchQuery, setSearchQuery] = useState('');

  // Data & Modal States
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [userContext, setUserContext] = useState(null);

  const fetchMatchedJobs = async () => {
    setLoading(true);
    try {
      const res = await api.jobs.matchJobs({
        target_role: targetRole,
        location: location === 'All' ? '' : location,
        remote_type: remoteType,
        experience_level: experienceLevel,
        min_salary: parseFloat(minSalary) || 0.0,
        required_skill: requiredSkill === 'All' ? '' : requiredSkill,
        sort_by: sortBy
      });

      if (res?.matched_jobs) {
        setJobs(res.matched_jobs);
      }
      if (res?.user_context_used) {
        setUserContext(res.user_context_used);
      }
    } catch (err) {
      console.error('Job Matching Error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMatchedJobs();
  }, [targetRole, location, remoteType, experienceLevel, minSalary, requiredSkill, sortBy]);

  const handleToggleSave = async (jobId, currentSaved) => {
    try {
      await api.jobs.saveJob(jobId, !currentSaved);
      setJobs(jobs.map(j => j.id === jobId ? { ...j, saved: !currentSaved } : j));
    } catch (err) {
      console.error(err);
    }
  };

  const filteredJobs = jobs.filter(j =>
    !searchQuery ||
    j.job_title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    j.company?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    j.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      
      {/* 1. HEADER & USER CONTEXT BANNER */}
      <PageHeader
        category="Opportunities"
        badgeText="JOB MATCHER"
        title="AI Personalized Job Matcher 🎯"
        subtitle="Real-world opportunities scored against your skills, education, experience, and projects."
        actions={
          <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-3 rounded-xl flex items-center gap-4 text-xs font-mono">
            <div>
              <p className="text-[10px] text-slate-500 uppercase">Target Role</p>
              <p className="font-bold text-slate-900 dark:text-slate-200">{targetRole}</p>
            </div>
            <div className="h-8 w-px bg-slate-200 dark:bg-slate-800" />
            <div>
              <p className="text-[10px] text-slate-500 uppercase">Detected Skills</p>
              <p className="font-bold text-emerald-600 dark:text-emerald-400">{userContext?.skills_count || user?.skills?.length || 5} Skills</p>
            </div>
            <div className="h-8 w-px bg-slate-200 dark:bg-slate-800" />
            <div>
              <p className="text-[10px] text-slate-500 uppercase">Experience</p>
              <p className="font-bold text-blue-600 dark:text-blue-400">{userContext?.experience_level || "Fresher / 0-2 yrs"}</p>
            </div>
          </div>
        }
      />

      {/* 2. FILTER & SORT CONTROLS BAR */}
      <div className="prof-card p-4 sm:p-6 space-y-4">
        
        <div className="flex flex-col lg:flex-row items-center justify-between gap-4">
          {/* Live Search Input */}
          <div className="w-full lg:w-96 relative">
            <input
              type="text"
              placeholder="Search by job title, company name, or keyword..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
            />
            <span className="absolute left-3 top-2.5 text-slate-400">🔍</span>
          </div>

          {/* Refresh Action */}
          <button
            onClick={fetchMatchedJobs}
            disabled={loading}
            className="w-full lg:w-auto btn-secondary"
          >
            {loading ? 'Re-calculating Matches...' : '🔄 Refresh Live Job Matches'}
          </button>
        </div>

        {/* Filters Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-xs">
          
          {/* Role Filter */}
          <div>
            <label className="block text-slate-500 dark:text-slate-400 font-semibold mb-1">Target Role</label>
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-200 focus:outline-none focus:border-blue-500"
            >
              <option value="Full Stack Developer">Full Stack Developer</option>
              <option value="Backend Developer">Backend Developer</option>
              <option value="Frontend Developer">Frontend Developer</option>
              <option value="Software Engineer">Software Engineer</option>
              <option value="AI/ML Engineer">AI/ML Engineer</option>
              <option value="DevOps / Cloud Engineer">DevOps / Cloud Engineer</option>
              <option value="Data Engineer">Data Engineer</option>
            </select>
          </div>

          {/* Location Filter */}
          <div>
            <label className="block text-slate-500 dark:text-slate-400 font-semibold mb-1">Location</label>
            <select
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-200 focus:outline-none focus:border-blue-500"
            >
              <option value="All">All Locations</option>
              <option value="Hyderabad">Hyderabad</option>
              <option value="Bengaluru">Bengaluru</option>
              <option value="Pune">Pune</option>
              <option value="Delhi NCR">Delhi NCR</option>
            </select>
          </div>

          {/* Remote / Hybrid / On-Site */}
          <div>
            <label className="block text-slate-500 dark:text-slate-400 font-semibold mb-1">Work Type</label>
            <select
              value={remoteType}
              onChange={(e) => setRemoteType(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-200 focus:outline-none focus:border-blue-500"
            >
              <option value="All">All Types</option>
              <option value="Remote">Remote</option>
              <option value="Hybrid">Hybrid</option>
              <option value="On-Site">On-Site</option>
            </select>
          </div>

          {/* Experience Filter */}
          <div>
            <label className="block text-slate-500 dark:text-slate-400 font-semibold mb-1">Experience</label>
            <select
              value={experienceLevel}
              onChange={(e) => setExperienceLevel(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-200 focus:outline-none focus:border-blue-500"
            >
              <option value="All">All Experience</option>
              <option value="0-1">0-1 Years (Fresher)</option>
              <option value="0-2">0-2 Years</option>
              <option value="1-3">1-3 Years</option>
              <option value="3+">3+ Years</option>
            </select>
          </div>

          {/* Min Salary Filter */}
          <div>
            <label className="block text-slate-500 dark:text-slate-400 font-semibold mb-1">Min Salary (LPA)</label>
            <select
              value={minSalary}
              onChange={(e) => setMinSalary(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-200 focus:outline-none focus:border-blue-500 font-mono"
            >
              <option value={0}>Any Compensation</option>
              <option value={12}>&gt; ₹12 LPA</option>
              <option value={18}>&gt; ₹18 LPA</option>
              <option value={24}>&gt; ₹24 LPA</option>
            </select>
          </div>

          {/* Sort By */}
          <div>
            <label className="block text-slate-500 dark:text-slate-400 font-semibold mb-1">Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-200 focus:outline-none focus:border-blue-500"
            >
              <option value="match_score">Match Score (Highest)</option>
              <option value="relevance">Role Relevance</option>
            </select>
          </div>

        </div>

      </div>

      {/* 3. RECOMMENDED JOBS GRID */}
      {loading ? (
        <div className="prof-card p-12 text-center text-slate-500 dark:text-slate-400 space-y-3">
          <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs font-mono">Running multi-factor job matching against candidate skills, education & experience...</p>
        </div>
      ) : filteredJobs.length === 0 ? (
        <div className="prof-card p-12 text-center text-slate-500 dark:text-slate-400 space-y-3">
          <p className="text-base font-bold text-slate-900 dark:text-white">No Matching Placement Opportunities Found</p>
          <p className="text-xs max-w-sm mx-auto">
            Try adjusting your location, work type, or experience filters to expand your search criteria.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredJobs.map((job) => {
            let scoreBadge = "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20";
            if (job.match_score < 65) scoreBadge = "bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20";
            else if (job.match_score < 80) scoreBadge = "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20";

            let workTypeBadge = "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300";
            if (job.work_type === "Remote") workTypeBadge = "bg-purple-500/10 text-purple-600 dark:text-purple-300 border-purple-500/20";
            if (job.work_type === "Hybrid") workTypeBadge = "bg-cyan-500/10 text-cyan-600 dark:text-cyan-300 border-cyan-500/20";

            return (
              <div key={job.id} className="prof-card p-6 space-y-4 flex flex-col justify-between">
                
                <div className="space-y-3">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <span className="text-[10px] uppercase font-bold tracking-wider text-blue-600 dark:text-blue-400">
                        {job.company}
                      </span>
                      <h3 className="text-base font-bold text-slate-900 dark:text-white mt-0.5">{job.job_title}</h3>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-xs text-slate-500 dark:text-slate-400">{job.location}</span>
                        <span className={`px-2 py-0.5 text-[10px] font-semibold rounded-md border ${workTypeBadge}`}>
                          {job.work_type}
                        </span>
                      </div>
                    </div>

                    <div className="text-right shrink-0">
                      <span className={`px-3 py-1 rounded-xl text-xs font-extrabold font-mono border ${scoreBadge}`}>
                        {job.match_score}% Match
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-2.5 rounded-xl">
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase">Salary:</span>
                      <p className="text-emerald-600 dark:text-emerald-400 font-bold">{job.salary}</p>
                    </div>
                    <div>
                      <span className="text-[10px] text-slate-500 uppercase">Experience:</span>
                      <p className="text-slate-700 dark:text-slate-300 font-bold">{job.experience_required}</p>
                    </div>
                  </div>

                  {/* Matching Skills */}
                  <div>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 font-semibold mb-1">Matching Competencies ({job.matching_skills?.length || 0}):</p>
                    <div className="flex flex-wrap gap-1">
                      {job.matching_skills?.map((s, i) => (
                        <span key={i} className="px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-700 dark:text-emerald-300 text-[10px] rounded font-mono">
                          ✓ {s}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Missing Skills */}
                  {job.missing_skills?.length > 0 && (
                    <div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 font-semibold mb-1">Missing Skill Gaps ({job.missing_skills?.length}):</p>
                      <div className="flex flex-wrap gap-1">
                        {job.missing_skills?.slice(0, 3).map((s, i) => (
                          <span key={i} className="px-2 py-0.5 bg-rose-500/10 border border-rose-500/20 text-rose-700 dark:text-rose-300 text-[10px] rounded font-mono">
                            + {s}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Card Footer Actions */}
                <div className="space-y-2 pt-3 border-t border-slate-200 dark:border-slate-800 text-xs">
                  <button
                    onClick={() => setSelectedJob(job)}
                    className="w-full btn-secondary text-center justify-center py-2"
                  >
                    📊 Detailed Match Breakdown & Analysis
                  </button>

                  <div className="flex items-center justify-between gap-2">
                    <a
                      href={job.job_url}
                      target="_blank"
                      rel="noreferrer"
                      className="btn-primary flex-1 text-center py-2"
                    >
                      🚀 Apply Link
                    </a>
                    <button
                      onClick={() => handleToggleSave(job.id, job.saved)}
                      className={`px-3 py-2 rounded-xl font-medium border transition shrink-0 ${
                        job.saved ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20' : 'btn-secondary'
                      }`}
                    >
                      {job.saved ? '★ Saved' : '☆ Save'}
                    </button>
                  </div>
                </div>

              </div>
            );
          })}
        </div>
      )}

      {/* 4. DETAILED MATCH BREAKDOWN MODAL */}
      {selectedJob && (
        <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="prof-card w-full max-w-2xl p-6 space-y-6 relative text-xs">
            
            <div className="flex items-start justify-between border-b border-slate-200 dark:border-slate-800 pb-4">
              <div>
                <span className="text-[10px] uppercase font-bold text-blue-600 dark:text-blue-400 font-mono">{selectedJob.company}</span>
                <h2 className="text-xl font-bold text-slate-900 dark:text-white mt-0.5">{selectedJob.job_title}</h2>
                <p className="text-slate-500 dark:text-slate-400">{selectedJob.location} • {selectedJob.salary}</p>
              </div>

              <div className="flex items-center gap-3">
                <span className="px-3.5 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-base font-extrabold font-mono rounded-xl">
                  {selectedJob.match_score}% Match
                </span>
                <button
                  onClick={() => setSelectedJob(null)}
                  className="w-8 h-8 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white font-bold flex items-center justify-center"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* 5-WEIGHT SUB-SCORES BREAKDOWN */}
            <div className="space-y-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-4 rounded-xl">
              <h4 className="font-bold text-slate-900 dark:text-white text-xs">5-Factor Match Weight Breakdown</h4>

              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-700 dark:text-slate-300">1. Skills Overlap (35%)</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-mono">{selectedJob.breakdown?.skills_score || 0}%</span>
                </div>
                <AnimatedProgressBar value={selectedJob.breakdown?.skills_score || 0} height="h-1.5" />
              </div>

              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-700 dark:text-slate-300">2. Target Role Alignment (25%)</span>
                  <span className="text-blue-600 dark:text-blue-400 font-mono">{selectedJob.breakdown?.role_score || 0}%</span>
                </div>
                <AnimatedProgressBar value={selectedJob.breakdown?.role_score || 0} height="h-1.5" />
              </div>

              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-700 dark:text-slate-300">3. Experience Fit (15%)</span>
                  <span className="text-amber-500 font-mono">{selectedJob.breakdown?.experience_score || 0}%</span>
                </div>
                <AnimatedProgressBar value={selectedJob.breakdown?.experience_score || 0} height="h-1.5" />
              </div>

              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-700 dark:text-slate-300">4. Education Match (15%)</span>
                  <span className="text-indigo-600 dark:text-indigo-400 font-mono">{selectedJob.breakdown?.education_score || 0}%</span>
                </div>
                <AnimatedProgressBar value={selectedJob.breakdown?.education_score || 0} height="h-1.5" />
              </div>

              <div>
                <div className="flex justify-between font-semibold mb-1">
                  <span className="text-slate-700 dark:text-slate-300">5. Project Tech Stack Depth (10%)</span>
                  <span className="text-purple-600 dark:text-purple-400 font-mono">{selectedJob.breakdown?.projects_score || 0}%</span>
                </div>
                <AnimatedProgressBar value={selectedJob.breakdown?.projects_score || 0} height="h-1.5" />
              </div>
            </div>

            {/* EXPERIENCE & EDUCATION STATUS */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl space-y-1">
                <p className="text-[10px] text-slate-500 uppercase font-bold">Experience Match</p>
                <p className="font-bold text-slate-900 dark:text-white">{selectedJob.experience_match?.status}</p>
                <p className="text-slate-500 dark:text-slate-400 text-[11px]">{selectedJob.experience_match?.details}</p>
              </div>

              <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-3.5 rounded-xl space-y-1">
                <p className="text-[10px] text-slate-500 uppercase font-bold">Education Match</p>
                <p className="font-bold text-slate-900 dark:text-white">{selectedJob.education_match?.status}</p>
                <p className="text-slate-500 dark:text-slate-400 text-[11px]">{selectedJob.education_match?.details}</p>
              </div>
            </div>

            {/* REASONS FOR RECOMMENDATION */}
            <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl space-y-2">
              <h4 className="font-bold text-emerald-700 dark:text-emerald-300 text-xs">Reasons for Recommendation:</h4>
              <div className="space-y-1">
                {selectedJob.reasons_for_recommendation?.map((r, i) => (
                  <p key={i} className="text-emerald-800 dark:text-emerald-200 text-xs">• {r}</p>
                ))}
              </div>
            </div>

            {/* CANDIDATE WEAKNESSES */}
            {selectedJob.weaknesses?.length > 0 && (
              <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl space-y-2">
                <h4 className="font-bold text-rose-700 dark:text-rose-300 text-xs">Areas Where Candidate is Weak:</h4>
                <div className="space-y-1">
                  {selectedJob.weaknesses?.map((w, i) => (
                    <p key={i} className="text-rose-800 dark:text-rose-200 text-xs">• {w}</p>
                  ))}
                </div>
              </div>
            )}

            <div className="pt-2 border-t border-slate-200 dark:border-slate-800 flex justify-end">
              <a
                href={selectedJob.job_url}
                target="_blank"
                rel="noreferrer"
                className="btn-primary py-2.5 px-5"
              >
                Apply Directly on Company Careers Portal 🚀
              </a>
            </div>

          </div>
        </div>
      )}

    </div>
  );
};

export default JobMatcher;
