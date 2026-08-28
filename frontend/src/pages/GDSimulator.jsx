import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const CATEGORIES = [
  "Technology", "AI", "Business", "Education",
  "Environment", "Current Affairs", "Workplace", "Ethics", "Software Industry"
];

const GDSimulator = () => {
  // Control Panel States
  const [selectedCategory, setSelectedCategory] = useState("Technology");
  const [selectedDifficulty, setSelectedDifficulty] = useState("Medium");
  const [selectedDuration, setSelectedDuration] = useState(5);

  // Discussion Session States
  const [currentTopic, setCurrentTopic] = useState(null);
  const [participants, setParticipants] = useState([]);
  const [userTranscript, setUserTranscript] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [loadingTopic, setLoadingTopic] = useState(false);
  const [evaluating, setEvaluating] = useState(false);

  // History State
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState("simulator"); // "simulator" | "history"

  const timerRef = useRef(null);

  // Initial Load: Fetch history and generate first topic
  useEffect(() => {
    fetchHistory();
    handleGenerateTopic();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await api.gd.getHistory();
      if (res?.history) {
        setHistory(res.history);
      }
    } catch (err) {
      console.error("Error fetching GD history:", err);
    }
  };

  const handleGenerateTopic = async () => {
    setLoadingTopic(true);
    setEvaluationResult(null);
    setUserTranscript("");
    setRecordingSeconds(0);
    if (isRecording) stopRecording();

    try {
      const res = await api.gd.generateTopic(selectedCategory, selectedDifficulty, selectedDuration);
      if (res?.topic) {
        setCurrentTopic(res.topic);
        setParticipants(res.participants || []);
      }
    } catch (err) {
      console.error("Error generating GD topic:", err);
    } finally {
      setLoadingTopic(false);
    }
  };

  // Recording Studio Controls
  const startRecording = () => {
    setIsRecording(true);
    setRecordingSeconds(0);
    timerRef.current = setInterval(() => {
      setRecordingSeconds((prev) => prev + 1);
    }, 1000);

    // Browser Speech Recognition fallback if supported
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.onresult = (event) => {
        let currentText = '';
        for (let i = 0; i < event.results.length; i++) {
          currentText += event.results[i][0].transcript;
        }
        setUserTranscript(currentText);
      };
      recognition.start();
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
  };

  // Evaluate GD Session
  const handleEvaluateSession = async () => {
    if (!currentTopic || !userTranscript.trim()) return;

    setEvaluating(true);
    try {
      const payload = {
        topic_title: currentTopic.title,
        category: selectedCategory,
        difficulty: selectedDifficulty,
        duration_minutes: selectedDuration,
        user_transcript: userTranscript
      };

      const res = await api.gd.evaluateGD(payload);
      if (res?.session) {
        setEvaluationResult(res.session);
        fetchHistory();
      }
    } catch (err) {
      console.error("Error evaluating GD session:", err);
    } finally {
      setEvaluating(false);
    }
  };

  const formatTime = (secs) => {
    const mins = Math.floor(secs / 60);
    const s = secs % 60;
    return `${mins.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
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
              COMMUNICATION & LEADERSHIP SIMULATOR
            </span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-bold text-white mt-2 tracking-tight flex items-center gap-2">
            AI Group Discussion Simulator 🎙️
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            Practice multi-participant group discussions, improve speech prosody, structure arguments, and build collaborative communication poise.
          </p>
        </div>

        {/* View Switcher Tabs */}
        <div className="bg-slate-950 p-1 border border-slate-800 rounded-xl flex items-center gap-1 text-xs shrink-0 self-start md:self-auto">
          <button
            onClick={() => setActiveTab("simulator")}
            className={`px-4 py-2 rounded-lg font-bold transition ${
              activeTab === "simulator" ? "bg-blue-600 text-white shadow" : "text-slate-400 hover:text-white"
            }`}
          >
            🎙️ GD Arena
          </button>
          <button
            onClick={() => setActiveTab("history")}
            className={`px-4 py-2 rounded-lg font-bold transition ${
              activeTab === "history" ? "bg-blue-600 text-white shadow" : "text-slate-400 hover:text-white"
            }`}
          >
            📊 Session History ({history.length})
          </button>
        </div>
      </div>

      {/* 2. DISCLAIMER BANNER */}
      <div className="bg-slate-900/60 border border-slate-800/80 p-4 rounded-xl flex items-start gap-3 text-xs text-slate-400">
        <span className="text-amber-400 text-base shrink-0">ℹ️</span>
        <div>
          <strong className="text-slate-200 font-semibold block">Practice Framework Notice:</strong>
          Group discussion topics and simulated participant turns are designed for communication and argument structure practice. They do not represent exact company exam questions. Speech feedback uses measurable prosody metrics and non-diagnostic indicators.
        </div>
      </div>

      {activeTab === "simulator" && (
        <div className="space-y-8">

          {/* 3. CONTROL PANEL TOOLBAR */}
          <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
            <label className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Configure Discussion Session:
            </label>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              
              {/* Category Dropdown */}
              <div>
                <label className="text-xs font-semibold text-slate-400 mb-1 block">Topic Category:</label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 text-slate-200 px-3.5 py-2.5 rounded-xl text-xs font-bold focus:outline-none focus:border-blue-500"
                >
                  {CATEGORIES.map(c => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              {/* Difficulty Dropdown */}
              <div>
                <label className="text-xs font-semibold text-slate-400 mb-1 block">Difficulty:</label>
                <select
                  value={selectedDifficulty}
                  onChange={(e) => setSelectedDifficulty(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 text-slate-200 px-3.5 py-2.5 rounded-xl text-xs font-bold focus:outline-none focus:border-blue-500"
                >
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              {/* Duration Dropdown */}
              <div>
                <label className="text-xs font-semibold text-slate-400 mb-1 block">Duration:</label>
                <select
                  value={selectedDuration}
                  onChange={(e) => setSelectedDuration(parseInt(e.target.value, 10))}
                  className="w-full bg-slate-950 border border-slate-800 text-slate-200 px-3.5 py-2.5 rounded-xl text-xs font-bold focus:outline-none focus:border-blue-500"
                >
                  <option value={3}>3 Minutes (Short Round)</option>
                  <option value={5}>5 Minutes (Standard Round)</option>
                  <option value={10}>10 Minutes (In-Depth Round)</option>
                </select>
              </div>

            </div>

            <button
              onClick={handleGenerateTopic}
              disabled={loadingTopic}
              className="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-bold rounded-xl shadow-lg transition flex items-center gap-2"
            >
              <span>{loadingTopic ? "Generating Topic..." : "⚡ Generate New GD Topic"}</span>
            </button>
          </div>

          {/* 4. CURRENT DISCUSSION TOPIC CARD */}
          {currentTopic && (
            <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md shadow-xl">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="px-3 py-1 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full text-xs font-mono font-bold">
                    {selectedCategory}
                  </span>
                  <span className={`px-3 py-1 rounded-full text-xs font-mono font-bold ${
                    selectedDifficulty === 'Easy' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : (selectedDifficulty === 'Medium' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30')
                  }`}>
                    {selectedDifficulty}
                  </span>
                </div>
                <span className="text-xs text-slate-400 font-mono">⏱️ Target Time: {selectedDuration} mins</span>
              </div>

              <h2 className="text-lg lg:text-xl font-bold text-white tracking-tight">
                "{currentTopic.title}"
              </h2>

              <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/60 p-4 rounded-xl border border-slate-800">
                <strong className="text-slate-200">Context:</strong> {currentTopic.background}
              </p>

              {currentTopic.key_angles && (
                <div className="space-y-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Key Focus Angles:</span>
                  <div className="flex flex-wrap gap-2">
                    {currentTopic.key_angles.map((angle, idx) => (
                      <span key={idx} className="px-3 py-1 bg-slate-950 border border-slate-800 text-slate-300 text-xs font-medium rounded-lg">
                        • {angle}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* 5. SIMULATED PARTICIPANTS DISCUSSION FEED */}
          <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
              <span>👥 Simulated Discussion Participants ({participants.length})</span>
              <span className="text-xs font-normal text-slate-500">Listen to viewpoints before delivering your contribution</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {participants.map((p) => (
                <div key={p.participant_id} className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2 flex flex-col justify-between">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                      <span className="text-sm font-bold text-white flex items-center gap-2">
                        <span>{p.avatar}</span>
                        <span>{p.name}</span>
                      </span>
                    </div>
                    <span className="text-[10px] font-mono px-2 py-0.5 bg-slate-900 text-indigo-300 border border-slate-800 rounded font-semibold inline-block">
                      {p.perspective}
                    </span>
                    <p className="text-xs text-slate-300 leading-relaxed italic">
                      "{p.statement}"
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* 6. USER RECORDING STUDIO & TRANSCRIPT EDITOR */}
          <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
                🎙️ Your Discussion Turn & Response
              </h3>
              {isRecording && (
                <div className="flex items-center gap-2 text-xs font-mono text-rose-400 animate-pulse">
                  <span className="w-2.5 h-2.5 bg-rose-500 rounded-full"></span>
                  <span>RECORDING: {formatTime(recordingSeconds)}</span>
                </div>
              )}
            </div>

            {/* Recording Trigger Buttons */}
            <div className="flex items-center gap-3">
              {!isRecording ? (
                <button
                  onClick={startRecording}
                  className="px-5 py-2.5 bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold rounded-xl shadow-lg transition flex items-center gap-2"
                >
                  <span className="w-2.5 h-2.5 bg-white rounded-full"></span>
                  <span>Start Microphone Recording 🎙️</span>
                </button>
              ) : (
                <button
                  onClick={stopRecording}
                  className="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold rounded-xl border border-slate-700 transition flex items-center gap-2"
                >
                  <span>⏹️ Stop Recording</span>
                </button>
              )}
            </div>

            {/* Live Transcript Area */}
            <div>
              <label className="text-xs font-semibold text-slate-400 mb-1 block">
                Your Speech Transcript (auto-recorded or type manually):
              </label>
              <textarea
                value={userTranscript}
                onChange={(e) => setUserTranscript(e.target.value)}
                rows={5}
                placeholder="Speak using the microphone or type your response contribution here..."
                className="w-full bg-slate-950 border border-slate-800 text-slate-200 p-4 rounded-xl text-xs font-sans focus:outline-none focus:border-blue-500 leading-relaxed"
              />
            </div>

            <div className="flex items-center justify-between pt-2">
              <span className="text-xs font-mono text-slate-500">
                Word Count: {userTranscript.trim() ? userTranscript.trim().split(/\s+/).length : 0} words
              </span>

              <button
                onClick={handleEvaluateSession}
                disabled={evaluating || !userTranscript.trim()}
                className="px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold rounded-xl shadow-lg transition disabled:opacity-50"
              >
                {evaluating ? "Evaluating Discussion Performance..." : "Submit GD Contribution 🚀"}
              </button>
            </div>
          </div>

          {/* 7. GD EVALUATION SCORECARD RESULT */}
          {evaluationResult && (
            <div className="space-y-6">
              
              {/* Overall GD Score Card */}
              <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl backdrop-blur-md shadow-xl grid grid-cols-1 lg:grid-cols-4 gap-6">
                
                <div className="lg:col-span-1 border-b lg:border-b-0 lg:border-r border-slate-800 pb-4 lg:pb-0 lg:pr-6 flex flex-col justify-between">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Overall GD Performance</span>
                    <div className="flex items-baseline gap-2 mt-2">
                      <span className="text-4xl font-extrabold text-emerald-400 font-mono">
                        {evaluationResult.gd_score}
                      </span>
                      <span className="text-xs text-slate-400 font-mono">/ 100</span>
                    </div>

                    <div className="h-3 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800 mt-3">
                      <div
                        className="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-emerald-400 transition-all duration-500 rounded-full"
                        style={{ width: `${evaluationResult.gd_score}%` }}
                      />
                    </div>
                  </div>

                  <div className="text-xs text-slate-400 pt-3 mt-4 border-t border-slate-800 font-mono">
                    Category: <strong className="text-white">{evaluationResult.category}</strong>
                  </div>
                </div>

                {/* 7-Component Pillar Breakdown Grid */}
                <div className="lg:col-span-3 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                  {Object.entries(evaluationResult.score_breakdown || {}).map(([key, score]) => (
                    <div key={key} className="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-1">
                      <span className="text-[10px] text-slate-400 font-semibold uppercase block truncate">
                        {key.replace(/_/g, ' ')}
                      </span>
                      <span className="text-lg font-bold text-blue-400 font-mono">{score}%</span>
                    </div>
                  ))}
                </div>

              </div>

              {/* Audio Prosody & Non-Diagnostic Indicators */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                {/* Prosody Metrics */}
                <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-3 backdrop-blur-md">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <span>🗣️ Audio & Delivery Prosody Metrics</span>
                  </h3>

                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                      <span className="text-[10px] text-slate-400">Pace (WPM)</span>
                      <div className="text-base font-bold text-emerald-400 font-mono mt-1">
                        {evaluationResult.speech_prosody?.wpm} WPM
                      </div>
                    </div>

                    <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                      <span className="text-[10px] text-slate-400">Filler Words</span>
                      <div className="text-base font-bold text-amber-400 font-mono mt-1">
                        {evaluationResult.speech_prosody?.filler_count} detected
                      </div>
                    </div>

                    <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                      <span className="text-[10px] text-slate-400">Pause Quality</span>
                      <div className="text-xs font-bold text-blue-400 mt-1">
                        {evaluationResult.speech_prosody?.pause_classification}
                      </div>
                    </div>

                    <div className="bg-slate-950 p-3 rounded-xl border border-slate-800">
                      <span className="text-[10px] text-slate-400">Intonation</span>
                      <div className="text-xs font-bold text-purple-400 mt-1">
                        {evaluationResult.speech_prosody?.pitch_classification}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Non-Diagnostic Indicators */}
                <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-3 backdrop-blur-md flex flex-col justify-between">
                  <div className="space-y-3">
                    <h3 className="text-sm font-bold text-white flex items-center gap-2">
                      <span>📊 Objective Speech Indicators</span>
                    </h3>

                    <p className="text-xs text-slate-300 leading-relaxed bg-slate-950 p-3 rounded-xl border border-slate-800">
                      • {evaluationResult.non_diagnostic_indicators?.confidence_indicator}
                    </p>

                    <p className="text-xs text-slate-300 leading-relaxed bg-slate-950 p-3 rounded-xl border border-slate-800">
                      • {evaluationResult.non_diagnostic_indicators?.nervousness_indicator}
                    </p>
                  </div>
                </div>

              </div>

              {/* Strengths, Weaknesses & Recommended Improvements */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                {/* Strengths */}
                <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-3 backdrop-blur-md">
                  <h3 className="text-sm font-bold text-emerald-400 flex items-center gap-2">
                    <span>✓ Key Strengths</span>
                  </h3>
                  <ul className="space-y-2 text-xs text-slate-300">
                    {(evaluationResult.strengths || []).map((s, idx) => (
                      <li key={idx} className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-start gap-2">
                        <span className="text-emerald-400 font-bold">•</span>
                        <span>{s}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Weaknesses */}
                <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-3 backdrop-blur-md">
                  <h3 className="text-sm font-bold text-rose-400 flex items-center gap-2">
                    <span>✕ Areas for Improvement</span>
                  </h3>
                  <ul className="space-y-2 text-xs text-slate-300">
                    {(evaluationResult.weaknesses || []).map((w, idx) => (
                      <li key={idx} className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-start gap-2">
                        <span className="text-rose-400 font-bold">•</span>
                        <span>{w}</span>
                      </li>
                    ))}
                  </ul>
                </div>

              </div>

              {/* Example Better Response */}
              <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-3 backdrop-blur-md">
                <h3 className="text-sm font-bold text-indigo-400 flex items-center gap-2">
                  <span>💡 Exemplary Response Model</span>
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed italic bg-slate-950 p-4 rounded-xl border border-slate-800">
                  "{evaluationResult.example_better_response}"
                </p>
              </div>

            </div>
          )}

        </div>
      )}

      {/* 8. SESSION HISTORY VIEW */}
      {activeTab === "history" && (
        <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl space-y-4 backdrop-blur-md">
          <h2 className="text-base font-bold text-white flex items-center justify-between">
            <span>📜 Past Group Discussion Sessions</span>
            <span className="text-xs font-mono text-slate-400">{history.length} Sessions Completed</span>
          </h2>

          {history.length > 0 ? (
            <div className="space-y-3">
              {history.map((sess) => (
                <div key={sess.id} className="bg-slate-950 p-4 rounded-xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full font-bold font-mono text-[10px]">
                        {sess.category}
                      </span>
                      <span className="text-slate-500 font-mono text-[10px]">{sess.created_at?.split('T')[0]}</span>
                    </div>
                    <div className="font-bold text-white">{sess.topic_title}</div>
                  </div>

                  <div className="flex items-center gap-4 shrink-0">
                    <div className="text-right">
                      <span className="text-[10px] text-slate-400 block font-mono">GD Score</span>
                      <span className="text-lg font-bold text-emerald-400 font-mono">{sess.gd_score} / 100</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-slate-500 text-xs">
              No Group Discussion sessions completed yet. Generate a topic above to begin!
            </div>
          )}
        </div>
      )}

    </div>
  );
};

export default GDSimulator;
