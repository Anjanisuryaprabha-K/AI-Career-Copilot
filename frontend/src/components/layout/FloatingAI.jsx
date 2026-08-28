import { api } from '../../services/api';
import React, { useState } from 'react';

const FloatingAI = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'ai', text: 'Hi Preetham! How can I assist your placement preparation today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg = input.trim();
    setMessages((prev) => [...prev, { sender: 'user', text: userMsg }]);
    setInput('');
    setIsLoading(true);

    try {
      const data = await api.chat.send(userMsg, undefined, messages);
      setMessages((prev) => [...prev, { sender: 'ai', text: data.response }]);
    } catch {
      setMessages((prev) => [...prev, { sender: 'ai', text: 'Career Mentor AI is ready to help you optimize your resume, practice coding problems, and prepare for interviews.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-40">
      {!isOpen ? (
        <button
          onClick={() => setIsOpen(true)}
          className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-500 to-blue-600 text-white flex items-center justify-center shadow-xl shadow-cyan-500/25 hover:scale-105 transition active:scale-95"
        >
          🤖
        </button>
      ) : (
        <div className="w-96 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl flex flex-col h-[500px] overflow-hidden">
          <div className="p-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-xl">🤖</span>
              <div>
                <p className="text-sm font-bold text-slate-100">AI Career Mentor</p>
                <p className="text-[10px] text-cyan-400">Online & Ready</p>
              </div>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-slate-400 hover:text-white text-lg">✕</button>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-3">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div
                  className={`max-w-[80%] p-3 rounded-xl text-xs ${
                    m.sender === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-bl-none'
                  }`}
                >
                  {m.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="text-xs text-slate-500 italic">AI Mentor is thinking...</div>
            )}
          </div>

          <form onSubmit={handleSend} className="p-3 bg-slate-950 border-t border-slate-800 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything (e.g. ATS tips, STAR method)..."
              className="flex-1 px-3 py-2 bg-slate-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
            <button type="submit" className="px-3 py-2 bg-cyan-600 text-white rounded-xl text-xs font-semibold hover:bg-cyan-500">
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default FloatingAI;
