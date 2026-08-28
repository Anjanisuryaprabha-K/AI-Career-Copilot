import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const TARGET_ROLES = [
  "Software Engineer", "Full Stack Developer", "Frontend Developer",
  "Backend Developer", "Data Engineer", "Data Scientist", "Machine Learning Eng"
];

const TARGET_COMPANIES = ["Amazon", "Google", "Microsoft", "IBM", "Stripe", "Swiggy", "Meta"];

const StudyPlanner = () => {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  // Config Form States
  const [targetRole, setTargetRole] = useState("Software Engineer");
  const [targetCompany, setTargetCompany] = useState("");
  const [interviewDate, setInterviewDate] = useState("");
  const [hoursPerDay, setHoursPerDay] = useState(2);
  const [daysPerWeek, setDaysPerWeek] = useState(5);
  const [studyTime, setStudyTime] = useState("Evening");
  const [skillLevel, setSkillLevel] = useState("Intermediate");

  const [activeDayIdx, setActiveDayIdx] = useState(0);

  useEffect(() => {
    fetchPlan();
  }, []);

  const fetchPlan = async () => {
    setLoading(true);
    try {
      const res = await api.studyPlanner.getPlan();
      if (res?.plan) {
        setPlan(res.plan);
        if (res.plan.target_role) setTargetRole(res.plan.target_role);
        if (res.plan.target_company) setTargetCompany(res.plan.target_company);
        if (res.plan.interview_date) setInterviewDate(res.plan.interview_date);
        if (res.plan.available_hours_per_day) setHoursPerDay(res.plan.available_hours_per_day);
      }
    } catch (err) {
      console.error("Error fetching study plan:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePlan = async (e) => {
    e.preventDefault();
    setGenerating(true);
    try {
      const payload = {
        target_role: targetRole,
        target_company: targetCompany || null,
        interview_date: interviewDate || null,
        available_hours_per_day: hoursPerDay,
        days_per_week: daysPerWeek,
        preferred_study_time: studyTime,
        current_skill_level: skillLevel
      };
      const res = await api.studyPlanner.generatePlan(payload);
      if (res?.plan) {
        setPlan(res.plan);
      }
    } catch (err) {
      console.error("Error generating study plan:", err);
    } finally {
      setGenerating(false);
    }
  };

  const handleCompleteTask = async (taskId) => {
    try {
      const res = await api.studyPlanner.completeTask(taskId);
      if (res?.status === "success") {
        fetchPlan();
      }
    } catch (err) {
      console.error("Error completing task:", err);
    }
  };

  const handleReschedule = async () => {
    try {
      const res = await api.studyPlanner.reschedule();
      if (res?.plan) {
        setPlan(res.plan);
      }
    } catch (err) {
      console.error("Error rescheduling tasks:", err);
    }
  };

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
            <span className="px-2.5 py-0.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold rounded-full font-mono">
              ADAPTIVE PREPARATION ENGINE
            </span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white mt-2 tracking-tight flex items-center gap-2">
            AI Study Planner & Schedule 📅
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Personalized daily preparation schedule generated from your actual platform weaknesses, target role, and interview target date.
          </p>
        </div>
      </div>

      {/* 2. TARGET INTERVIEW COUNTDOWN BANNER */}
      {plan?.interview_date && (
        <div className="bg-gradient-to-r from-amber-500/10 via-indigo-500/10 to-blue-500/10 border border-amber-500/30 p-5 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4 shadow-lg">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🎯</span>
            <div>
              <strong className="text-sm font-bold text-amber-300 block">
                Target Interview Date Set: {plan.interview_date}
              </strong>
              <span className="text-xs text-slate-300">
                {plan.days_remaining ? `${plan.days_remaining} Days Remaining` : 'Upcoming Round'} • Target: {plan.target_company || 'Tier 1'} ({plan.target_role})
              </span>
            </div>
          </div>
          {plan.is_accelerated && (
            <span className="px-3 py-1 bg-amber-500/20 border border-amber-500/40 text-amber-300 text-xs font-bold font-mono rounded-full shrink-0">
              ⚡ ACCELERATED PREP MODE ACTIVE
            </span>
          )}
        </div>
      )}

      {/* 3. CONFIGURATOR TOOLBAR */}
      <form onSubmit={handleGeneratePlan} className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
        <label className="text-xs font-bold uppercase tracking-wider text-slate-400 block">
          Configure Your Study Parameters:
        </label>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          
          <div>
            <label className="text-slate-400 mb-1 block font-semibold">Target Role:</label>
            <select
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 text-slate-200 p-2.5 rounded-xl font-bold focus:outline-none focus:border-blue-500"
            >
              {TARGET_ROLES.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>

          <div>
            <label className="text-slate-400 mb-1 block font-semibold">Target Company (Optional):</label>
            <select
              value={targetCompany}
              onChange={(e) => setTargetCompany(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 text-slate-200 p-2.5 rounded-xl font-bold focus:outline-none focus:border-blue-500"
            >
              <option value="">General Industry</option>
              {TARGET_COMPANIES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>

          <div>
            <label className="text-slate-400 mb-1 block font-semibold">Available Hours / Day:</label>
            <select
              value={hoursPerDay}
              onChange={(e) => setHoursPerDay(parseInt(e.target.value, 10))}
              className="w-full bg-slate-950 border border-slate-800 text-slate-200 p-2.5 rounded-xl font-bold focus:outline-none focus:border-blue-500"
            >
              <option value={1}>1 Hour / Day</option>
              <option value={2}>2 Hours / Day</option>
              <option value={3}>3 Hours / Day</option>
              <option value={4}>4 Hours / Day</option>
            </select>
          </div>

          <div>
            <label className="text-slate-400 mb-1 block font-semibold">Target Interview Date:</label>
            <input
              type="date"
              value={interviewDate}
              onChange={(e) => setInterviewDate(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 text-slate-200 p-2.5 rounded-xl font-bold focus:outline-none focus:border-blue-500"
            />
          </div>

        </div>

        <button
          type="submit"
          disabled={generating}
          className="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 text-white text-xs font-bold rounded-xl shadow-lg transition disabled:opacity-50"
        >
          {generating ? "Generating Plan..." : "⚡ Generate Personalized Study Schedule"}
        </button>
      </form>

      {/* 4. PLAN OVERVIEW STATS CARDS */}
      {plan && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl backdrop-blur-md">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Schedule Completion</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-3xl font-extrabold text-emerald-400 font-mono">
                {plan.completion_percentage}%
              </span>
              <span className="text-xs text-slate-400">({plan.completed_tasks_count}/{plan.total_tasks_count} Tasks)</span>
            </div>
            <div className="h-2 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800 mt-2">
              <div className="h-full bg-emerald-400 transition-all duration-300" style={{ width: `${plan.completion_percentage}%` }} />
            </div>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl backdrop-blur-md">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Current Focus</span>
            <div className="text-sm font-bold text-white mt-2 truncate">
              {plan.current_focus}
            </div>
            <span className="text-[10px] text-indigo-400 font-mono mt-1 block">Driven by AI Weakness Detector</span>
          </div>

          <div className="bg-slate-900/90 border border-slate-800 p-5 rounded-2xl backdrop-blur-md flex items-center justify-between">
            <div>
              <span className="text-[10px] text-slate-400 uppercase font-semibold block">Missed Tasks Management</span>
              <span className="text-xs font-bold text-slate-300 mt-1 block">Auto-reschedule uncompleted items</span>
            </div>
            <button
              onClick={handleReschedule}
              className="px-3.5 py-2 bg-slate-950 hover:bg-slate-800 border border-slate-700 text-blue-300 text-xs font-bold rounded-xl transition shrink-0"
            >
              🔄 Reschedule
            </button>
          </div>
        </div>
      )}

      {/* 5. DAILY TIMELINE SCHEDULE TABS & TASK LIST */}
      {plan?.days_schedule && (
        <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-6 backdrop-blur-md">
          
          {/* Day Switcher Tabs */}
          <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-800 text-xs font-bold">
            {plan.days_schedule.map((day, idx) => (
              <button
                key={day.day_number}
                onClick={() => setActiveDayIdx(idx)}
                className={`px-4 py-2 rounded-xl transition shrink-0 ${
                  activeDayIdx === idx
                    ? "bg-blue-600 text-white shadow-md"
                    : "bg-slate-950 text-slate-400 hover:text-white border border-slate-800"
                }`}
              >
                {day.day_name}
              </button>
            ))}
          </div>

          {/* Active Day Tasks List */}
          <div className="space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center justify-between">
              <span>{plan.days_schedule[activeDayIdx]?.day_name} Tasks</span>
              <span className="text-xs font-mono text-slate-400">
                {plan.days_schedule[activeDayIdx]?.tasks?.length || 0} Tasks Scheduled
              </span>
            </h3>

            <div className="space-y-3">
              {plan.days_schedule[activeDayIdx]?.tasks.map((task) => (
                <div
                  key={task.task_id}
                  className={`p-4 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4 transition ${
                    task.status === "completed"
                      ? "bg-emerald-950/20 border-emerald-500/30"
                      : "bg-slate-950 border-slate-800"
                  }`}
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full font-bold font-mono text-[10px]">
                        {task.category}
                      </span>
                      <span className="text-slate-500 text-xs font-mono">⏱️ {task.duration_minutes} mins</span>
                    </div>

                    <div className={`text-sm font-bold ${task.status === "completed" ? "line-through text-slate-400" : "text-white"}`}>
                      {task.title}
                    </div>
                  </div>

                  {/* Task Actions */}
                  <div className="flex items-center gap-3 shrink-0">
                    <Link
                      to={task.route}
                      className="px-3.5 py-1.5 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 text-blue-300 text-xs font-bold rounded-lg transition inline-flex items-center gap-1"
                    >
                      <span>Open Feature</span>
                      <span>→</span>
                    </Link>

                    {task.status !== "completed" ? (
                      <button
                        onClick={() => handleCompleteTask(task.task_id)}
                        className="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow"
                      >
                        ✓ Complete
                      </button>
                    ) : (
                      <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 text-xs font-bold rounded-lg font-mono">
                        ✓ Completed
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
};

export default StudyPlanner;
