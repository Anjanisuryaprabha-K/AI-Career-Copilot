import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const QUICK_QUESTIONS = [
  "Am I ready for a Software Engineer interview?",
  "What should I study today?",
  "What are my biggest weaknesses?",
  "Which coding topic should I practice?",
  "Which jobs match my current skills?",
  "How can I improve my resume?"
];

const AIChatAssistant = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I am your Unified AI Placement Mentor. I have access to your live platform performance metrics across Resume ATS, Coding Arena, Mock Interviews, Speech Prosody, and Job Readiness. How can I guide your preparation today?',
      actionable_recommendations: []
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [mentorSummary, setMentorSummary] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    fetchMentorSummary();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchMentorSummary = async () => {
    try {
      const res = await api.chat.getMentorSummary();
      if (res?.context) {
        setMentorSummary(res.context);
      }
    } catch (err) {
      console.error('Error fetching mentor summary:', err);
    }
  };

  const handleSendMessage = async (textToSend) => {
    const userText = textToSend || inputMessage.trim();
    if (!userText || loading) return;

    if (!textToSend) setInputMessage('');
    setMessages((prev) => [...prev, { role: 'user', content: userText }]);
    setLoading(true);

    try {
      const res = await api.chat.send(userText, conversationId);
      if (res) {
        if (res.conversation_id) setConversationId(res.conversation_id);
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: res.reply || res.message,
            sources: res.sources || [],
            actionable_recommendations: res.actionable_recommendations || []
          }
        ]);
        fetchMentorSummary();
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an issue connecting to the AI Placement Mentor. Please try again.'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-10 flex flex-col space-y-6">
      
      {/* 1. TOP HEADER & CANDIDATE CONTEXT BAR */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl backdrop-blur-md space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <Link to="/dashboard" className="text-xs font-semibold text-blue-400 hover:underline">
              ← Back to Dashboard
            </Link>
            <h1 className="text-2xl font-bold text-white mt-1 flex items-center gap-2 tracking-tight">
              Unified AI Placement Mentor 🤖
            </h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Personalized career mentor grounded in your actual platform metrics across all modules.
            </p>
          </div>
        </div>

        {/* Live Candidate Context Summary Bar */}
        {mentorSummary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3 border-t border-slate-800/80 text-xs font-mono">
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400 text-[10px] uppercase font-semibold block">Job Readiness</span>
              <span className="text-lg font-extrabold text-emerald-400">
                {mentorSummary.job_readiness?.overall_readiness_score || 0}/100
              </span>
            </div>

            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400 text-[10px] uppercase font-semibold block">ATS Resume Score</span>
              <span className="text-lg font-extrabold text-blue-400">
                {mentorSummary.resume?.ats_score || 0}%
              </span>
            </div>

            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400 text-[10px] uppercase font-semibold block">Coding Solved</span>
              <span className="text-lg font-extrabold text-purple-400">
                {mentorSummary.coding?.overall_solved || 0} Solved
              </span>
            </div>

            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400 text-[10px] uppercase font-semibold block">Weakest Area</span>
              <span className="text-xs font-bold text-amber-400 truncate block mt-1">
                {mentorSummary.weaknesses?.weakest_dsa_topic || 'Arrays'}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* 2. QUICK QUESTION CHIPS */}
      <div className="space-y-2">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
          Suggested Mentor Questions:
        </span>
        <div className="flex flex-wrap gap-2">
          {QUICK_QUESTIONS.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSendMessage(q)}
              disabled={loading}
              className="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 hover:text-white rounded-xl text-xs font-medium transition shadow-sm"
            >
              💡 {q}
            </button>
          ))}
        </div>
      </div>

      {/* 3. CHAT MESSAGES WINDOW */}
      <div className="flex-1 bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between overflow-hidden min-h-[500px] backdrop-blur-md">
        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          {messages.map((m, idx) => (
            <div key={idx} className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div
                className={`max-w-2xl px-5 py-4 rounded-2xl text-xs leading-relaxed ${
                  m.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none shadow-md shadow-blue-600/20'
                    : 'bg-slate-950 border border-slate-800 text-slate-200 rounded-bl-none shadow-lg'
                }`}
              >
                <p className="font-bold text-[11px] mb-1 opacity-75 flex items-center gap-1.5">
                  <span>{m.role === 'user' ? '👤 Candidate' : '🤖 AI Placement Mentor'}</span>
                </p>
                <div className="whitespace-pre-wrap leading-relaxed">{m.content}</div>

                {/* Actionable Recommendations with Direct Module Routes */}
                {m.actionable_recommendations?.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-slate-800 space-y-2">
                    <p className="text-[10px] font-bold uppercase tracking-wider text-indigo-400">
                      ⚡ Actionable Next Steps:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {m.actionable_recommendations.map((rec, ri) => (
                        <Link
                          key={ri}
                          to={rec.route}
                          className="px-3 py-1.5 bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 border border-blue-500/30 rounded-lg text-xs font-bold transition inline-flex items-center gap-1"
                        >
                          <span>{rec.label}</span>
                          <span>→</span>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}

                {/* Live Grounding Sources if present */}
                {m.sources?.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-slate-800 space-y-1">
                    <p className="text-[10px] font-bold text-cyan-400">🌐 Live Google Grounding Sources:</p>
                    {m.sources.map((s, si) => (
                      <a
                        key={si}
                        href={s.url}
                        target="_blank"
                        rel="noreferrer"
                        className="block text-[10px] text-slate-400 hover:text-cyan-300 underline truncate"
                      >
                        • {s.title} ({s.source})
                      </a>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-xs text-blue-400 font-bold animate-pulse">
              <span>🌀</span> AI Placement Mentor is gathering platform data and synthesizing response...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }} className="mt-4 flex gap-3 pt-3 border-t border-slate-800">
          <input
            type="text"
            placeholder="Ask your mentor about interview readiness, resume improvements, DSA topics..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            disabled={loading}
            className="flex-1 px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500 font-medium"
          />
          <button
            type="submit"
            disabled={loading || !inputMessage.trim()}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 text-white rounded-xl text-xs font-bold transition shadow-lg shadow-blue-600/25 disabled:opacity-50"
          >
            Ask Mentor ⚡
          </button>
        </form>
      </div>
    </div>
  );
};

export default AIChatAssistant;
