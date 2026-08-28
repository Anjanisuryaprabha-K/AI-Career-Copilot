import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { PageHeader } from '../components/common/DesignSystemComponents';

const STAGES = ['Wishlist', 'Applied', 'Online Assessment', 'Interview', 'Offer', 'Rejected'];

const ApplicationKanban = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [newCompany, setNewCompany] = useState('');
  const [newRole, setNewRole] = useState('');
  const [newSalary, setNewSalary] = useState('₹18 LPA');
  const [newDeadline, setNewDeadline] = useState('Sep 15, 2026');

  const fetchApplications = async () => {
    setLoading(true);
    try {
      const res = await api.applications.list();
      if (res?.data) {
        setApplications(res.data);
      }
    } catch (err) {
      console.error('Error fetching applications:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  const handleStageChange = async (appId, newStage) => {
    try {
      await api.applications.updateStage(appId, newStage);
      setApplications(applications.map(a => 
        (a.id === appId || a._id === appId) ? { ...a, stage: newStage, status: newStage } : a
      ));
    } catch (err) {
      console.error('Error updating stage in MongoDB:', err);
    }
  };

  const handleCreateApplication = async (e) => {
    e.preventDefault();
    if (!newCompany || !newRole) return;
    try {
      const res = await api.applications.create({
        company: newCompany,
        role: newRole,
        salary: newSalary,
        deadline: newDeadline,
        status: 'Applied',
        match_score: 88
      });
      if (res?.data) {
        setApplications([res.data, ...applications]);
        setIsAdding(false);
        setNewCompany('');
        setNewRole('');
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <PageHeader
        category="CRM Tracking"
        badgeText="KANBAN CRM"
        title="Placement Application Kanban CRM 📋"
        subtitle="Persisted live in MongoDB with multi-stage workflow tracking."
        actions={
          <button
            onClick={() => setIsAdding(!isAdding)}
            className="btn-primary"
          >
            {isAdding ? '✕ Cancel' : '+ Add New Application'}
          </button>
        }
      />

      {/* Add Modal / Form */}
      {isAdding && (
        <form onSubmit={handleCreateApplication} className="prof-card p-6 grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Company Name (e.g. Google)"
            value={newCompany}
            onChange={(e) => setNewCompany(e.target.value)}
            required
            className="px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white"
          />
          <input
            type="text"
            placeholder="Role (e.g. SDE-1 Full Stack)"
            value={newRole}
            onChange={(e) => setNewRole(e.target.value)}
            required
            className="px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white"
          />
          <input
            type="text"
            placeholder="Salary / CTC (e.g. ₹22 LPA)"
            value={newSalary}
            onChange={(e) => setNewSalary(e.target.value)}
            className="px-3 py-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white"
          />
          <button type="submit" className="btn-primary">
            ✓ Save to MongoDB
          </button>
        </form>
      )}

      {/* Kanban Columns */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {STAGES.map((stage) => {
          const stageApps = applications.filter(a => (a.stage || a.status) === stage);
          return (
            <div key={stage} className="prof-card p-4 flex flex-col space-y-3 min-h-[400px]">
              <div className="flex items-center justify-between pb-2 border-b border-slate-200 dark:border-slate-800">
                <span className="text-xs font-bold text-slate-900 dark:text-slate-200">{stage}</span>
                <span className="px-2 py-0.5 bg-slate-100 dark:bg-slate-800 text-blue-600 dark:text-blue-400 text-[10px] font-bold rounded-full">
                  {stageApps.length}
                </span>
              </div>

              <div className="space-y-3 flex-1">
                {stageApps.map((app) => (
                  <div key={app.id || app._id} className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl p-3.5 space-y-2 shadow-sm">
                    <div className="flex items-start justify-between">
                      <h4 className="text-xs font-bold text-slate-900 dark:text-white">{app.company}</h4>
                      <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono font-bold">{app.ctc || app.salary}</span>
                    </div>
                    <p className="text-[11px] text-slate-700 dark:text-slate-300">{app.role}</p>
                    <p className="text-[10px] text-slate-500">📅 {app.deadline || app.next_deadline}</p>

                    {/* Move stage dropdown */}
                    <div className="pt-2 border-t border-slate-200 dark:border-slate-800">
                      <select
                        value={app.stage || app.status || stage}
                        onChange={(e) => handleStageChange(app.id || app._id, e.target.value)}
                        className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-[10px] text-slate-700 dark:text-slate-300 rounded px-1.5 py-1 focus:outline-none"
                      >
                        {STAGES.map((s) => (
                          <option key={s} value={s}>{s}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ApplicationKanban;
