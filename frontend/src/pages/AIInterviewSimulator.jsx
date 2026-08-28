import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { useUserProfile } from '../contexts/UserProfileContext';
import { PageHeader, AnimatedProgressBar } from '../components/common/DesignSystemComponents';

const PRESET_ROLES = [
  "Software Developer", "Full Stack Developer", "Frontend Developer", "Backend Developer",
  "Python Developer", "Java Developer", "JavaScript Developer", "React Developer",
  "Node.js Developer", "Data Analyst", "Data Scientist", "AI/ML Engineer",
  "DevOps Engineer", "Cloud Engineer", "Custom Role"
];

const PRESET_TECHS = [
  "Python", "Java", "JavaScript", "React", "Node.js", "Express", "MongoDB",
  "SQL", "AWS", "Docker", "Kubernetes", "Machine Learning", "Data Structures",
  "Algorithms", "System Design"
];

const AIInterviewSimulator = () => {
  const { detectedRole } = useUserProfile();

  // Phase: 'setup' | 'room' | 'report'
  const [phase, setPhase] = useState('setup');

  // Setup Form States
  const [role, setRole] = useState(detectedRole || 'Full Stack Developer');
  const [customRole, setCustomRole] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('Fresher');
  const [interviewType, setInterviewType] = useState('Technical');
  const [difficulty, setDifficulty] = useState('Adaptive');
  const [duration, setDuration] = useState('20 minutes');
  const [selectedTechs, setSelectedTechs] = useState(['React', 'Node.js', 'MongoDB']);
  const [customTech, setCustomTech] = useState('');
  const [isStarting, setIsStarting] = useState(false);

  // Interview Room States
  const [sessionId, setSessionId] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [questionCount, setQuestionCount] = useState(1);
  const [userTranscript, setUserTranscript] = useState('');
  const [isPaused, setIsPaused] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [ttsEnabled, setTtsEnabled] = useState(true);
  const [showEndModal, setShowEndModal] = useState(false);

  // STT Microphone Recording States
  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [sttStatus, setSttStatus] = useState('');
  const recognitionRef = useRef(null);
  const timerRef = useRef(null);

  // Report State
  const [finalReport, setFinalReport] = useState(null);
  const [loadingReport, setLoadingReport] = useState(false);

  // Initialize Speech Recognition & TTS
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const rec = new SpeechRecognition();
      rec.continuous = true;
      rec.interimResults = true;
      rec.lang = 'en-US';

      rec.onstart = () => {
        setIsRecording(true);
        setSttStatus('🎙️ Listening to speech...');
      };

      rec.onresult = (event) => {
        let text = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          text += event.results[i][0].transcript;
        }
        setUserTranscript(prev => (prev ? prev.trim() + ' ' + text : text));
      };

      rec.onerror = (err) => {
        setIsRecording(false);
        setSttStatus(`Microphone warning: ${err.error}. You can type manually.`);
      };

      rec.onend = () => {
        setIsRecording(false);
      };

      recognitionRef.current = rec;
    }
  }, []);

  // Timer for audio recording
  useEffect(() => {
    if (isRecording) {
      timerRef.current = setInterval(() => {
        setRecordingSeconds(prev => prev + 1);
      }, 1000);
    } else {
      clearInterval(timerRef.current);
      setRecordingSeconds(0);
    }
    return () => clearInterval(timerRef.current);
  }, [isRecording]);

  // Speak AI Question using Text-To-Speech (TTS)
  const speakQuestion = (text) => {
    if (!ttsEnabled || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  };

  const toggleTech = (t) => {
    if (selectedTechs.includes(t)) {
      setSelectedTechs(selectedTechs.filter(item => item !== t));
    } else {
      setSelectedTechs([...selectedTechs, t]);
    }
  };

  // Phase 1: Start Session
  const handleStartInterview = async (e) => {
    e.preventDefault();
    setIsStarting(true);
    try {
      const res = await api.mockInterview.start({
        role,
        custom_role: customRole,
        experience_level: experienceLevel,
        interview_type: interviewType,
        difficulty,
        duration_minutes: duration,
        technologies: selectedTechs,
        custom_technology: customTech
      });

      if (res?.session_id && res?.current_question) {
        setSessionId(res.session_id);
        setCurrentQuestion(res.current_question);
        setQuestionCount(1);
        setUserTranscript('');
        setPhase('room');
        speakQuestion(res.current_question.question);
      }
    } catch (err) {
      console.error('Failed to start interview:', err);
    } finally {
      setIsStarting(false);
    }
  };

  // Voice Controls
  const startRecording = () => {
    if (recognitionRef.current) {
      setUserTranscript('');
      try {
        recognitionRef.current.start();
      } catch (e) {}
    }
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsRecording(false);
      setSttStatus('Recording stopped. Processing transcript...');
    }
  };

  // Phase 2: Submit Answer & Evaluate
  const handleSubmitAnswer = async () => {
    if (!userTranscript.trim() || !currentQuestion) return;
    stopRecording();
    setIsAnalyzing(true);

    try {
      const res = await api.mockInterview.submitAnswer(sessionId, currentQuestion.question, userTranscript);
      if (res?.evaluation) {
        // Automatically fetch next adaptive question
        const nextRes = await api.mockInterview.nextQuestion(sessionId);
        if (nextRes?.question) {
          setCurrentQuestion(nextRes.question);
          setQuestionCount(prev => prev + 1);
          setUserTranscript('');
          speakQuestion(nextRes.question.question);
        }
      }
    } catch (err) {
      console.error('Error submitting answer:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Session Action Controls
  const handlePauseToggle = async () => {
    if (isPaused) {
      await api.mockInterview.resume(sessionId);
      setIsPaused(false);
    } else {
      await api.mockInterview.pause(sessionId);
      setIsPaused(true);
    }
  };

  const handleSkipQuestion = async () => {
    stopRecording();
    setUserTranscript('');
    try {
      const res = await api.mockInterview.nextQuestion(sessionId);
      if (res?.question) {
        setCurrentQuestion(res.question);
        setQuestionCount(prev => prev + 1);
        speakQuestion(res.question.question);
      }
    } catch (err) {
      console.error('Skip error:', err);
    }
  };

  const handleEndInterviewConfirmed = async () => {
    setShowEndModal(false);
    stopRecording();
    setPhase('report');
    setLoadingReport(true);

    try {
      const res = await api.mockInterview.end(sessionId);
      if (res?.report) {
        setFinalReport(res.report);
      }
    } catch (err) {
      console.error('End interview error:', err);
    } finally {
      setLoadingReport(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* TOP HEADER */}
      <PageHeader
        category="Interview Preparation"
        badgeText="AI SIMULATOR"
        title="AI Technical Mock Interview Room 🎙️"
        subtitle="Practice adaptive live interviews with real-time speech transcription, text-to-speech audio, and verified answer evaluations."
        actions={
          phase === 'room' && (
            <div className="flex items-center gap-3">
              <button
                onClick={() => setTtsEnabled(!ttsEnabled)}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold border transition ${
                  ttsEnabled ? 'bg-blue-500/10 border-blue-500/20 text-blue-600 dark:text-blue-400' : 'bg-slate-100 dark:bg-slate-950 border-slate-200 dark:border-slate-800 text-slate-500'
                }`}
              >
                {ttsEnabled ? '🔊 Voice TTS On' : '🔇 Voice TTS Off'}
              </button>
              <button
                onClick={() => setShowEndModal(true)}
                className="px-4 py-1.5 bg-rose-500/10 border border-rose-500/20 hover:bg-rose-600 hover:text-white text-rose-600 dark:text-rose-400 text-xs font-bold rounded-xl transition"
              >
                🛑 End Interview
              </button>
            </div>
          )
        }
      />

      {/* PHASE 1: PROFESSIONAL SETUP SCREEN */}
      {phase === 'setup' && (
        <div className="max-w-4xl mx-auto prof-card p-8 space-y-6">
          <div className="border-b border-slate-200 dark:border-slate-800 pb-4">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <span>🎙️</span> Customize Personalized AI Technical Interview
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Configure your role, seniority, interview type, and stack. AI retrieves your resume to personalize questions and evaluate semantic accuracy.
            </p>
          </div>

          <form onSubmit={handleStartInterview} className="space-y-6 text-xs">
            {/* Role & Experience */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1.5">Target Discipline Role</label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 font-semibold focus:outline-none focus:border-blue-500"
                >
                  {PRESET_ROLES.map(r => <option key={r} value={r}>{r}</option>)}
                </select>
                {role === 'Custom Role' && (
                  <input
                    type="text"
                    value={customRole}
                    onChange={(e) => setCustomRole(e.target.value)}
                    placeholder="Enter custom role title..."
                    className="w-full mt-2 px-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 font-mono"
                  />
                )}
              </div>

              <div>
                <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1.5">Experience Level</label>
                <select
                  value={experienceLevel}
                  onChange={(e) => setExperienceLevel(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 font-semibold focus:outline-none focus:border-blue-500"
                >
                  <option value="Beginner / Fresher">Beginner / Fresher (0-1 Yrs)</option>
                  <option value="Junior">Junior (1-3 Yrs)</option>
                  <option value="Intermediate">Intermediate (3-5 Yrs)</option>
                  <option value="Senior">Senior (5+ Yrs)</option>
                </select>
              </div>
            </div>

            {/* Type, Difficulty & Duration */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              <div>
                <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1.5">Interview Type</label>
                <select
                  value={interviewType}
                  onChange={(e) => setInterviewType(e.target.value)}
                  className="w-full px-3 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 font-medium"
                >
                  <option value="Technical">Technical</option>
                  <option value="Coding">Coding</option>
                  <option value="System Design">System Design</option>
                  <option value="Behavioral">Behavioral</option>
                  <option value="Mixed Technical + Behavioral">Mixed Technical + Behavioral</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1.5">Difficulty Mode</label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="w-full px-3 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 font-medium"
                >
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                  <option value="Adaptive">Adaptive (Auto-scales)</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1.5">Interview Duration</label>
                <select
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  className="w-full px-3 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 font-medium"
                >
                  <option value="10 minutes">10 minutes</option>
                  <option value="20 minutes">20 minutes</option>
                  <option value="30 minutes">30 minutes</option>
                  <option value="Custom">Custom</option>
                </select>
              </div>
            </div>

            {/* Technologies Selector */}
            <div className="space-y-2">
              <label className="block text-slate-700 dark:text-slate-300 font-bold">Focus Technologies & Stack</label>
              <div className="flex flex-wrap gap-2">
                {PRESET_TECHS.map(t => {
                  const isSel = selectedTechs.includes(t);
                  return (
                    <button
                      key={t}
                      type="button"
                      onClick={() => toggleTech(t)}
                      className={`px-3 py-1.5 rounded-xl border text-xs font-semibold transition ${
                        isSel
                          ? 'bg-blue-600 text-white border-blue-500 shadow-md'
                          : 'bg-slate-50 dark:bg-slate-950 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                      }`}
                    >
                      {t} {isSel ? '✓' : ''}
                    </button>
                  );
                })}
              </div>

              <input
                type="text"
                value={customTech}
                onChange={(e) => setCustomTech(e.target.value)}
                placeholder="Add custom technology tag..."
                className="w-full mt-2 px-4 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 font-mono"
              />
            </div>

            <button
              type="submit"
              disabled={isStarting}
              className="w-full btn-primary py-4 text-sm"
            >
              {isStarting ? 'Initializing Personalized AI Interviewer...' : 'Start Personalized AI Technical Interview 🚀'}
            </button>
          </form>
        </div>
      )}

      {/* PHASE 2: LIVE VOICE INTERVIEW ROOM */}
      {phase === 'room' && currentQuestion && (
        <div className="max-w-4xl mx-auto space-y-6">
          
          {/* Room Controls Bar */}
          <div className="prof-card p-4 flex items-center justify-between text-xs font-mono">
            <div className="flex items-center gap-3">
              <span className="px-3 py-1 bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20 rounded-lg font-bold">
                Question {questionCount}
              </span>
              <span className="text-slate-500 dark:text-slate-400">Topic: {currentQuestion.topic || 'Technical'}</span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handlePauseToggle}
                className="btn-secondary"
              >
                {isPaused ? '▶ Resume' : '⏸ Pause'}
              </button>
              <button
                onClick={handleSkipQuestion}
                className="btn-secondary"
              >
                ⏭️ Skip
              </button>
            </div>
          </div>

          {/* AI INTERVIEWER CARD */}
          <div className="prof-card p-8 space-y-6 text-center">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center mx-auto text-3xl shadow-lg shadow-blue-600/20 text-white">
              🤖
            </div>

            <div className="space-y-2 max-w-2xl mx-auto">
              <p className="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider">AI Technical Interviewer:</p>
              <h2 className="text-lg lg:text-xl font-bold text-slate-900 dark:text-white leading-snug">
                "{currentQuestion.question}"
              </h2>
              {currentQuestion.personalized_note && (
                <p className="text-[11px] text-slate-500 font-mono italic">{currentQuestion.personalized_note}</p>
              )}
            </div>

            {/* Microphone Recording Status & Controls */}
            <div className="p-6 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-4 max-w-xl mx-auto">
              <div className="flex items-center justify-center gap-3">
                {!isRecording ? (
                  <button
                    onClick={startRecording}
                    className="btn-primary flex items-center gap-2"
                  >
                    <span>🎙️</span> Start Voice Answer
                  </button>
                ) : (
                  <button
                    onClick={stopRecording}
                    className="px-6 py-3 bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-rose-600/30 animate-pulse flex items-center gap-2"
                  >
                    <span>⏹</span> Stop Recording ({String(Math.floor(recordingSeconds / 60)).padStart(2, '0')}:{String(recordingSeconds % 60).padStart(2, '0')})
                  </button>
                )}

                <button
                  onClick={() => speakQuestion(currentQuestion.question)}
                  className="btn-secondary"
                >
                  🔊 Replay
                </button>
              </div>

              {sttStatus && <p className="text-[11px] text-slate-500 dark:text-slate-400 font-mono">{sttStatus}</p>}

              {/* Editable Transcript Fallback */}
              <div className="space-y-2 text-left">
                <label className="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase">Spoken Transcript Preview:</label>
                <textarea
                  value={userTranscript}
                  onChange={(e) => setUserTranscript(e.target.value)}
                  placeholder="Your spoken response transcript will auto-populate here. You can edit manually before submitting..."
                  rows="4"
                  className="w-full p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-200 font-sans text-xs focus:outline-none focus:border-blue-500"
                />
              </div>

              <button
                onClick={handleSubmitAnswer}
                disabled={isAnalyzing || !userTranscript.trim()}
                className="w-full btn-primary py-3"
              >
                {isAnalyzing ? 'Analyzing Answer...' : 'Submit Answer & Evaluate 🚀'}
              </button>
            </div>
          </div>

        </div>
      )}

      {/* PHASE 3: FINAL REPORT & QUESTION-BY-QUESTION REVIEW */}
      {phase === 'report' && (
        <div className="max-w-4xl mx-auto space-y-6">
          {loadingReport ? (
            <div className="py-16 text-center text-slate-500 dark:text-slate-400 font-mono text-sm animate-pulse">
              Synthesizing overall score and performance metrics...
            </div>
          ) : finalReport ? (
            <div className="space-y-6">
              
              {/* Overall Score Banner */}
              <div className="prof-card p-8 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                <div>
                  <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold rounded-full font-mono uppercase">
                    🎯 Interview Completed
                  </span>
                  <h2 className="text-xl font-bold text-slate-900 dark:text-white mt-2">Overall Candidate Readiness Performance</h2>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">{finalReport.experience_level} {finalReport.role}</p>
                </div>

                <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl text-center min-w-[160px] shrink-0">
                  <p className="text-xs text-slate-500 dark:text-slate-400 font-bold uppercase">Overall Score</p>
                  <p className="text-4xl font-extrabold text-emerald-600 dark:text-emerald-400 font-mono mt-1">{finalReport.overall_score}</p>
                  <p className="text-[10px] text-slate-500 font-mono">out of 100</p>
                </div>
              </div>

              {/* Performance Radar Bars */}
              <div className="prof-card p-6 space-y-4">
                <h3 className="text-base font-bold text-slate-900 dark:text-white">Performance Breakdown</h3>
                <div className="space-y-3 text-xs font-mono">
                  {Object.entries(finalReport.performance_bars || {}).map(([key, val]) => (
                    <div key={key}>
                      <div className="flex justify-between mb-1">
                        <span className="text-slate-700 dark:text-slate-300 capitalize">{key.replace(/_/g, ' ')}</span>
                        <span className="text-blue-600 dark:text-blue-400 font-bold">{val} / 100</span>
                      </div>
                      <AnimatedProgressBar value={val} height="h-2" />
                    </div>
                  ))}
                </div>
              </div>

              {/* Strong & Weak Areas */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
                <div className="prof-card p-6 space-y-2">
                  <h4 className="font-bold text-emerald-600 dark:text-emerald-400 uppercase">✓ Strong Areas:</h4>
                  <ul className="list-disc list-inside text-slate-700 dark:text-slate-300 space-y-1">
                    {(finalReport.strong_areas || []).map((s, i) => <li key={i}>{s}</li>)}
                  </ul>
                </div>

                <div className="prof-card p-6 space-y-2">
                  <h4 className="font-bold text-amber-500 uppercase">⚠️ Weak Areas:</h4>
                  <ul className="list-disc list-inside text-amber-600 dark:text-amber-300 space-y-1">
                    {(finalReport.weak_areas || []).map((w, i) => <li key={i}>{w}</li>)}
                  </ul>
                </div>
              </div>

              {/* Question-by-Question Review */}
              <div className="prof-card p-6 space-y-4">
                <h3 className="text-base font-bold text-slate-900 dark:text-white">Question-by-Question Review</h3>
                <div className="space-y-4 text-xs">
                  {(finalReport.question_reviews || []).map((qr) => (
                    <div key={qr.question_number} className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl space-y-2">
                      <div className="flex justify-between font-bold">
                        <span className="text-slate-900 dark:text-slate-200">Question {qr.question_number}: {qr.question}</span>
                        <span className="text-emerald-600 dark:text-emerald-400 font-mono text-sm">{qr.score} / 100</span>
                      </div>
                      <p className="text-slate-500 dark:text-slate-400 italic">" Your Answer: {qr.candidate_transcript} "</p>
                      <p className="text-slate-700 dark:text-slate-300 font-medium">{qr.evaluation_text}</p>
                      {qr.correct_explanation && (
                        <div className="p-2.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg text-[11px] text-blue-600 dark:text-blue-300 font-mono">
                          {qr.correct_explanation}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Verified Sources */}
              {finalReport.verified_sources && finalReport.verified_sources.length > 0 && (
                <div className="prof-card p-6 space-y-3 text-xs">
                  <h4 className="font-bold text-slate-900 dark:text-white uppercase">Sources Used for Verification:</h4>
                  <ul className="space-y-2">
                    {finalReport.verified_sources.map((src, idx) => (
                      <li key={idx} className="p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl flex items-center justify-between">
                        <span className="text-blue-600 dark:text-blue-400 font-bold">{src.source_name || src.title}</span>
                        <a href={src.url} target="_blank" rel="noreferrer" className="text-slate-500 hover:text-slate-900 dark:hover:text-white underline">
                          {src.url} ↗
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <button
                onClick={() => {
                  setPhase('setup');
                  setFinalReport(null);
                }}
                className="w-full btn-primary py-4 text-sm"
              >
                Start New Mock Interview 🚀
              </button>

            </div>
          ) : null}
        </div>
      )}

      {/* CONFIRMATION END MODAL */}
      {showEndModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="prof-card p-6 max-w-sm w-full space-y-4 text-center">
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">End Interview Early?</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">Are you sure you want to end the interview? Your current progress will be saved into your final report.</p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowEndModal(false)}
                className="btn-secondary flex-1"
              >
                Cancel
              </button>
              <button
                onClick={handleEndInterviewConfirmed}
                className="flex-1 py-2.5 bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs rounded-xl shadow transition"
              >
                End & Save
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default AIInterviewSimulator;
