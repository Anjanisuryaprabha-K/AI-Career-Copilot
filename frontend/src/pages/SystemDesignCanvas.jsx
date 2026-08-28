import React, { useState } from 'react';
import { api } from '../services/api';

const SystemDesignCanvas = () => {
  const [selectedComponents, setSelectedComponents] = useState([
    'Client (Web/Mobile)',
    'Nginx Load Balancer',
    'FastAPI Microservices',
    'Redis Cache',
    'MongoDB Database'
  ]);
  const [prompt, setPrompt] = useState('Design a Scalable URL Shortener Service (10k req/sec)');
  const [evaluation, setEvaluation] = useState(null);

  const availableBlocks = [
    'Nginx Load Balancer',
    'API Gateway',
    'FastAPI Microservices',
    'Redis Cache',
    'MongoDB Database',
    'PostgreSQL Shards',
    'Kafka Message Queue',
    'Cloudflare CDN',
    'ElasticSearch Cluster'
  ];

  const toggleComponent = (block) => {
    if (selectedComponents.includes(block)) {
      setSelectedComponents(selectedComponents.filter((c) => c !== block));
    } else {
      setSelectedComponents([...selectedComponents, block]);
    }
  };

  const handleEvaluate = async () => {
    try {
      const data = await api.tools.systemDesign({ prompt, components: selectedComponents });
      setEvaluation(data.data);
    } catch {}
  };

  return (
    <div className="p-6 lg:p-10 max-w-5xl mx-auto space-y-6 text-slate-900 dark:text-slate-100">
      <div className="prof-card p-6 rounded-2xl">
        <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
          <span>📐</span> System Design Architecture Whiteboard
        </h1>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
          Compose multi-tier distributed architectures and receive automated scalability and bottleneck evaluations.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="prof-card p-6 rounded-2xl space-y-4">
          <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Available System Blocks</h3>
          <div className="space-y-2">
            {availableBlocks.map((b) => (
              <button
                key={b}
                onClick={() => toggleComponent(b)}
                className={`w-full text-left p-2.5 rounded-xl border text-xs font-semibold transition ${
                  selectedComponents.includes(b)
                    ? 'bg-[#EEF2FF] dark:bg-[#1E1B2E] border-indigo-200 dark:border-indigo-800 text-[#4F46E5] dark:text-[#6366F1]'
                    : 'bg-white dark:bg-[#151522] border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100'
                }`}
              >
                {selectedComponents.includes(b) ? '✓ ' : '+ '} {b}
              </button>
            ))}
          </div>
          <button
            onClick={handleEvaluate}
            className="w-full btn-ai"
          >
            Evaluate Architecture →
          </button>
        </div>

        <div className="md:col-span-2 space-y-6">
          <div className="prof-card p-6 rounded-2xl space-y-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white">Active Architecture Canvas</h3>
            <div className="p-6 bg-slate-50 dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-xl min-h-[160px] flex flex-wrap gap-2 items-center">
              {selectedComponents.map((c, i) => (
                <div key={i} className="px-3.5 py-2 rounded-xl bg-white dark:bg-[#151522] border border-indigo-200 dark:border-indigo-800 text-[#4F46E5] dark:text-[#6366F1] text-xs font-mono shadow-xs font-bold">
                  📦 {c}
                </div>
              ))}
            </div>
          </div>

          {evaluation && (
            <div className="ai-insight-card p-6 rounded-2xl space-y-4 text-xs">
              <div className="flex justify-between items-center pb-3 border-b border-[#DDD6FE] dark:border-[#3B2D54]">
                <span className="text-base font-bold text-[#059669]">{evaluation.evaluation_tier}</span>
                <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 rounded-full font-bold">
                  {evaluation.architecture_score}/100 Score
                </span>
              </div>
              <p className="text-slate-800 dark:text-slate-200"><b>Throughput Capacity:</b> {evaluation.estimated_capacity}</p>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(evaluation.scalability_checklist || {}).map(([k, v]) => (
                  <div key={k} className="p-2.5 bg-white dark:bg-[#151522] border border-slate-200 dark:border-slate-800 rounded-lg">
                    <p className="text-slate-500 dark:text-slate-400 capitalize text-[10px]">{k.replace('_', ' ')}</p>
                    <p className="text-slate-900 dark:text-slate-100 font-semibold mt-0.5">{v}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SystemDesignCanvas;
