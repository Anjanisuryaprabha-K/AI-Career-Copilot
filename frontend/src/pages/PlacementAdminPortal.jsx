import { api } from '../services/api';
import React, { useState, useEffect } from 'react';

const PlacementAdminPortal = () => {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    api.analytics.getAdminBatch()
      .then((d) => setAnalytics(d.data))
      .catch(() => {});
  }, []);

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6 text-slate-100">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>🏛️</span> College Placement Cell & Recruiter Portal
        </h1>
        <p className="text-sm text-slate-400 mt-1">Batch readiness oversight, student shortlisting, and drive eligibility filters.</p>
      </div>

      {analytics && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl">
              <p className="text-xs font-bold text-slate-400 uppercase">Enrolled Students</p>
              <p className="text-3xl font-extrabold text-white mt-1">{analytics.total_students_enrolled}</p>
              <p className="text-xs text-emerald-400 mt-1">{analytics.placement_ready_students} Placement Ready (65%)</p>
            </div>
            <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl">
              <p className="text-xs font-bold text-slate-400 uppercase">Average Batch Score</p>
              <p className="text-3xl font-extrabold text-cyan-400 mt-1">{analytics.average_batch_readiness_score}%</p>
              <p className="text-xs text-slate-400 mt-1">Top Tier: 38 Students</p>
            </div>
            <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl">
              <p className="text-xs font-bold text-slate-400 uppercase">Upcoming Recruiter Drives</p>
              <p className="text-3xl font-extrabold text-indigo-400 mt-1">{analytics.top_recruiter_drives?.length}</p>
              <p className="text-xs text-slate-400 mt-1">Next: Amazon Drive</p>
            </div>
          </div>

          <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-white">Tier 1 Shortlisted Candidates</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-xs text-left text-slate-300">
                <thead className="bg-slate-950 text-slate-400 font-bold border-b border-slate-800">
                  <tr>
                    <th className="p-3">Student Name</th>
                    <th className="p-3">CGPA</th>
                    <th className="p-3">Readiness Index</th>
                    <th className="p-3">DSA Solved</th>
                    <th className="p-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {analytics.shortlisted_students?.map((s) => (
                    <tr key={s.id} className="hover:bg-slate-800/50">
                      <td className="p-3 font-bold text-white">{s.name}</td>
                      <td className="p-3">{s.cgpa}</td>
                      <td className="p-3 text-cyan-400 font-semibold">{s.readiness}%</td>
                      <td className="p-3">{s.solved_dsa}</td>
                      <td className="p-3">
                        <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold">
                          {s.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlacementAdminPortal;
