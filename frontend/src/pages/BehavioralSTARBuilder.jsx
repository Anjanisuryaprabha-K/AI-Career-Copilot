import { api } from '../services/api';
import React, { useState } from 'react';

const BehavioralSTARBuilder = () => {
  const [form, setForm] = useState({
    situation: 'During the high-traffic annual festival sale, our microservice experienced sudden database connection spikes.',
    task: 'As lead backend engineer, I was responsible for preventing cascading service timeouts and ensuring 100% order capture.',
    action: 'I profiled slow database transactions, configured Redis cluster caching for product catalogs, and implemented circuit breaker retries.',
    result: 'Reduced database CPU utilization from 94% to 32% and successfully processed 50,000 orders with zero downtime.'
  });
  const [evaluation, setEvaluation] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleEvaluate = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const data = await api.interview.evaluateSTAR(form);
      setEvaluation(data.data);
    } catch {}
    finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6 text-slate-100">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>⭐</span> Behavioral Interview STAR Method Builder
        </h1>
        <p className="text-sm text-slate-400 mt-1">Structure and evaluate your behavioral interview responses against Amazon LP & Google culture standards.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <form onSubmit={handleEvaluate} className="p-6 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
          <div>
            <label className="block text-xs font-bold text-cyan-400 mb-1">S - Situation (Context & Background)</label>
            <textarea
              rows={2}
              value={form.situation}
              onChange={(e) => setForm({ ...form, situation: e.target.value })}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white resize-none"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-indigo-400 mb-1">T - Task (Your Responsibility & Challenge)</label>
            <textarea
              rows={2}
              value={form.task}
              onChange={(e) => setForm({ ...form, task: e.target.value })}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white resize-none"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-purple-400 mb-1">A - Action (Specific Individual Steps Taken)</label>
            <textarea
              rows={3}
              value={form.action}
              onChange={(e) => setForm({ ...form, action: e.target.value })}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white resize-none"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-emerald-400 mb-1">R - Result (Quantifiable Measurable Impact)</label>
            <textarea
              rows={2}
              value={form.result}
              onChange={(e) => setForm({ ...form, result: e.target.value })}
              className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded-xl text-xs text-white resize-none"
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-xl text-xs transition"
          >
            {isLoading ? 'Evaluating STAR...' : 'Evaluate STAR Response'}
          </button>
        </form>

        <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col justify-between space-y-4">
          <div>
            <h3 className="text-sm font-bold text-white mb-3">AI Evaluation & Scorecard</h3>
            {evaluation ? (
              <div className="space-y-3 text-xs">
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-center">
                  <p className="text-slate-400">STAR Compliance Score</p>
                  <p className="text-3xl font-extrabold text-emerald-400 my-1">{evaluation.star_compliance_score}/100</p>
                  <p className="text-cyan-400 font-bold">{evaluation.hiring_verdict}</p>
                </div>
                <div className="space-y-1.5">
                  <p className="text-slate-300"><b>Action Depth:</b> {evaluation.breakdown?.action_depth}</p>
                  <p className="text-slate-300"><b>Measurable Result:</b> {evaluation.breakdown?.quantifiable_result}</p>
                </div>
                <div className="p-3 bg-blue-500/10 border border-blue-500/30 rounded-xl text-blue-300 text-[11px]">
                  💡 {evaluation.suggested_enhancement}
                </div>
              </div>
            ) : (
              <div className="h-64 flex items-center justify-center text-slate-500 text-xs border border-dashed border-slate-800 rounded-xl">
                Fill the STAR segments and click evaluate to review feedback.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BehavioralSTARBuilder;
