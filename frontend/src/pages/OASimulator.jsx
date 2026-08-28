import { api } from '../services/api';
import React, { useState, useEffect } from 'react';

const OASimulator = () => {
  const [config, setConfig] = useState(null);
  const [isTestActive, setIsTestActive] = useState(false);
  const [result, setResult] = useState(null);
  const [answers, setAnswers] = useState({ aptitude_score: 13, coding_tests_passed: 6, total_coding_tests: 6 });

  useEffect(() => {
    api.tools.oaConfig('Amazon')
      .then((d) => setConfig(d.data))
      .catch(() => {});
  }, []);

  const handleSubmitTest = async () => {
    try {
      const data = await api.tools.oaEvaluate(answers);
      setResult(data.data);
      setIsTestActive(false);
    } catch {}
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6 text-slate-100">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>⏱️</span> Mock Online Assessment (OA) Placement Exam
        </h1>
        <p className="text-sm text-slate-400 mt-1">Simulate real-world 75-minute company hiring assessments with timed aptitude and coding sections.</p>
      </div>

      {!isTestActive && !result && config && (
        <div className="p-8 bg-slate-900 border border-slate-800 rounded-2xl space-y-6 text-center">
          <div className="text-4xl">🎯</div>
          <h2 className="text-xl font-bold text-white">{config.test_title}</h2>
          <p className="text-xs text-slate-400 max-w-lg mx-auto">
            This test mirrors real hiring assessments for Tier-1 companies. Includes Section 1 (Core CS / Logic) and Section 2 (Algorithmic Problems).
          </p>
          <div className="flex justify-center gap-6 text-xs text-slate-300">
            <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">⏱️ Duration: 75 Mins</div>
            <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">💻 2 Coding Challenges</div>
            <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">🧠 15 CS Core MCQs</div>
          </div>
          <button
            onClick={() => setIsTestActive(true)}
            className="px-8 py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold rounded-xl text-sm transition shadow-lg shadow-cyan-500/20"
          >
            Start Mock Assessment →
          </button>
        </div>
      )}

      {isTestActive && (
        <div className="p-8 bg-slate-900 border border-slate-800 rounded-2xl space-y-6">
          <div className="flex justify-between items-center pb-4 border-b border-slate-800">
            <span className="text-sm font-bold text-white">Section 2: Algorithmic Problem Solving</span>
            <span className="px-3 py-1 rounded bg-rose-500/10 border border-rose-500/30 text-rose-400 font-mono text-xs">
              ⏱️ Time Remaining: 48:32
            </span>
          </div>

          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
            <h3 className="font-bold text-sm text-cyan-400">Problem 1: Minimum Operations to Balance Server Loads</h3>
            <p className="text-xs text-slate-400">Given an array of server capacities, determine the minimum rebalancing operations to ensure no server exceeds the median load by more than K.</p>
            <textarea
              defaultValue="def minServerOperations(servers: list[int]) -> int:
    servers.sort()
    median = servers[len(servers)//2]
    return sum(abs(s - median) for s in servers)"
              className="w-full h-40 p-3 bg-slate-900 border border-slate-700 rounded-xl font-mono text-xs text-slate-200 resize-none focus:outline-none"
            />
          </div>

          <button
            onClick={handleSubmitTest}
            className="w-full py-3.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl text-sm transition"
          >
            Submit Assessment for Evaluation
          </button>
        </div>
      )}

      {result && (
        <div className="p-8 bg-slate-900 border border-slate-800 rounded-2xl space-y-6">
          <div className="text-center space-y-2">
            <p className="text-xs font-bold uppercase text-slate-400">Assessment Scorecard</p>
            <p className="text-4xl font-extrabold text-emerald-400">{result.overall_score_percentage}%</p>
            <p className="text-sm font-bold text-cyan-400">{result.qualification_status}</p>
            <p className="text-xs text-slate-400">{result.percentile_rank}</p>
          </div>

          <div className="grid grid-cols-2 gap-4 text-xs">
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl">
              <p className="text-slate-400 font-semibold">Core CS / Aptitude</p>
              <p className="text-base font-bold text-white mt-1">{result.section_breakdown?.aptitude_score}</p>
            </div>
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl">
              <p className="text-slate-400 font-semibold">Coding Test Cases</p>
              <p className="text-base font-bold text-white mt-1">{result.section_breakdown?.coding_score}</p>
            </div>
          </div>

          <button
            onClick={() => setResult(null)}
            className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold"
          >
            Take Another Assessment
          </button>
        </div>
      )}
    </div>
  );
};

export default OASimulator;
