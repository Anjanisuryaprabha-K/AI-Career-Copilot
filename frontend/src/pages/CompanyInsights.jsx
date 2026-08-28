import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const CompanyInsights = () => {
  const [companyName, setCompanyName] = useState('Amazon');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchInsights = async (cName) => {
    setLoading(true);
    try {
      const res = await api.companies.getDetails(cName || companyName);
      if (res?.company) {
        setData(res.company);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInsights('Amazon');
  }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-6 lg:p-10 space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gray-900 border border-gray-800 p-6 rounded-2xl shadow-xl">
        <div>
          <Link to="/dashboard" className="text-gray-400 hover:text-white text-sm">
            ← Back to Dashboard
          </Link>
          <h1 className="text-2xl font-bold text-white mt-2 flex items-center gap-2">
            Company Placement Intelligence & Round Breakdown 🏢
          </h1>
          <p className="text-xs text-gray-400 mt-1">
            Real-world hiring patterns, tech stacks, round structures, and interview tips.
          </p>
        </div>

        <div className="flex gap-2">
          {['Amazon', 'Microsoft', 'Google', 'Swiggy'].map((c) => (
            <button
              key={c}
              onClick={() => {
                setCompanyName(c);
                fetchInsights(c);
              }}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition ${
                companyName.toLowerCase() === c.toLowerCase()
                  ? 'bg-cyan-500 text-white'
                  : 'bg-gray-800 text-gray-400 hover:text-white'
              }`}
            >
              {c}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-gray-400">Loading intelligence for {companyName}...</div>
      ) : data ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7 bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-xl space-y-4">
            <div>
              <span className="text-[10px] uppercase font-bold tracking-wider text-cyan-400">Company Dossier</span>
              <h2 className="text-2xl font-extrabold text-white mt-1">{data.company_name}</h2>
              <p className="text-xs text-gray-300 mt-2 leading-relaxed">{data.overview}</p>
            </div>

            <div className="space-y-3 pt-3 border-t border-gray-800 text-xs">
              <div>
                <span className="text-gray-400 font-bold">Interview & Placement Rounds:</span>
                <p className="text-gray-200 mt-1">{data.interview_process}</p>
              </div>

              <div>
                <span className="text-gray-400 font-bold">Core Tech Stack:</span>
                <div className="flex flex-wrap gap-1.5 mt-1.5">
                  {(data.tech_stack || []).map((t, i) => (
                    <span key={i} className="px-2.5 py-1 bg-gray-950 border border-gray-800 text-cyan-300 rounded-lg text-[11px]">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="lg:col-span-5 bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-xl space-y-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-gray-400">Compensation & Locations</h3>
            <div className="p-4 bg-gray-950 rounded-xl border border-gray-800 space-y-2 text-xs">
              <p><span className="text-gray-500 font-medium">Placement CTC:</span> <strong className="text-emerald-400">{data.salary_range}</strong></p>
              <p><span className="text-gray-500 font-medium">Hiring Hubs:</span> <span className="text-gray-300">{(data.locations || []).join(', ')}</span></p>
              <p><span className="text-gray-500 font-medium">Official Portal:</span> <a href={data.careers_url} target="_blank" rel="noreferrer" className="text-cyan-400 hover:underline">{data.careers_url}</a></p>
            </div>

            {data.sources?.length > 0 && (
              <div className="space-y-1.5 pt-2 border-t border-gray-800 text-xs">
                <p className="text-[11px] font-bold text-gray-400">Live Search Sources:</p>
                {data.sources.map((s, i) => (
                  <a key={i} href={s.url} target="_blank" rel="noreferrer" className="block text-[10px] text-cyan-400 hover:underline truncate">
                    • {s.title}
                  </a>
                ))}
              </div>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
};

export default CompanyInsights;
