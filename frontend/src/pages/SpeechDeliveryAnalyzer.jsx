import React, { useState, useEffect, useRef } from 'react';
import { api } from '../services/api';
import { PageHeader, AnimatedProgressBar } from '../components/common/DesignSystemComponents';

const SpeechDeliveryAnalyzer = () => {
  const [activeTab, setActiveTab] = useState('studio'); // 'studio', 'interview', 'history'
  const [transcript, setTranscript] = useState("In my previous internship, basically we had an issue where, you know, the database latency spiked. So I actually implemented Redis caching, which um reduced response time by 45%.");
  const [duration, setDuration] = useState(45);
  const [interviewQuestion, setInterviewQuestion] = useState("Tell me about a time you solved a critical technical bottleneck under pressure.");
  
  // Recording State
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);

  // Results & History State
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [history, setHistory] = useState([]);
  const [progress, setProgress] = useState(null);

  // Refs for Web MediaRecorder & Timers
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    fetchHistoryAndProgress();
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const fetchHistoryAndProgress = async () => {
    try {
      const histRes = await api.speech.getHistory();
      if (histRes.status === 'success') {
        setHistory(histRes.history || []);
      }
      const progRes = await api.speech.getProgress();
      if (progRes.status === 'success') {
        setProgress(progRes.progress || null);
      }
    } catch (e) {
      console.error("Failed to load speech history:", e);
    }
  };

  // Browser Microphone Recording Handlers
  const startRecording = async () => {
    setErrorMsg(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunksRef.current = [];
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setAudioBlob(blob);
        setAudioUrl(URL.createObjectURL(blob));
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorder.start(100);
      setIsRecording(true);
      setIsPaused(false);
      setRecordingTime(0);

      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } catch (err) {
      setErrorMsg("Microphone access denied or browser recording unavailable. You can still type/paste your transcript or upload an audio file.");
    }
  };

  const pauseRecording = () => {
    if (mediaRecorderRef.current && isRecording && !isPaused) {
      mediaRecorderRef.current.pause();
      setIsPaused(true);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  const resumeRecording = () => {
    if (mediaRecorderRef.current && isRecording && isPaused) {
      mediaRecorderRef.current.resume();
      setIsPaused(false);
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsPaused(false);
      if (timerRef.current) clearInterval(timerRef.current);
      if (recordingTime > 0) setDuration(recordingTime);
    }
  };

  const clearRecording = () => {
    setAudioBlob(null);
    setAudioUrl(null);
    setUploadedFile(null);
    setRecordingTime(0);
    setErrorMsg(null);
  };

  // Audio File Upload Validation
  const handleFileUpload = (e) => {
    setErrorMsg(null);
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 25 * 1024 * 1024) {
      setErrorMsg("Audio file exceeds 25MB size limit.");
      return;
    }

    const ext = file.name.split('.').pop().toLowerCase();
    const validExts = ['wav', 'mp3', 'm4a', 'ogg', 'webm', 'flac'];
    if (!validExts.includes(ext)) {
      setErrorMsg(`Unsupported file format (.${ext}). Please upload WAV, MP3, M4A, OGG, WEBM, or FLAC.`);
      return;
    }

    setUploadedFile(file);
    setAudioUrl(URL.createObjectURL(file));
  };

  // Analysis Submission
  const handleAnalyze = async (e) => {
    if (e) e.preventDefault();
    setIsLoading(true);
    setErrorMsg(null);

    try {
      let data;
      if (audioBlob || uploadedFile) {
        const formData = new FormData();
        formData.append('file', uploadedFile || audioBlob, uploadedFile ? uploadedFile.name : 'recording.wav');
        if (transcript.trim()) formData.append('transcript', transcript);
        formData.append('duration_seconds', recordingTime > 0 ? recordingTime : duration);
        if (activeTab === 'interview' && interviewQuestion) {
          formData.append('question', interviewQuestion);
        }

        const res = await api.speech.analyzeAudio(formData);
        data = res.data;
      } else if (activeTab === 'interview') {
        const res = await api.speech.analyzeInterviewAnswer({
          question: interviewQuestion,
          transcript,
          duration_seconds: Number(duration)
        });
        data = res.data;
      } else {
        const res = await api.speech.analyzeSpeech({
          transcript,
          duration_seconds: Number(duration)
        });
        data = res.data;
      }

      setResult(data);
      fetchHistoryAndProgress();
    } catch (err) {
      setErrorMsg(err.message || "Failed to analyze speech. Please check audio recording or transcript.");
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <PageHeader
        category="Speech & Prosody"
        badgeText="PROSODY ANALYZER"
        title="AI Voice & Speech Delivery Prosody Analyzer 🎙️"
        subtitle="Real-time acoustic signal & text prosody engine: Pace (WPM), Pitch variation (F0), Loudness dynamics, Pause fillers, and Poise scoring."
        actions={
          <div className="flex bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 p-1 rounded-xl text-xs">
            <button
              onClick={() => setActiveTab('studio')}
              className={`px-4 py-2 rounded-lg font-bold transition ${activeTab === 'studio' ? 'bg-blue-600 text-white shadow' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
            >
              🎙️ Prosody Studio
            </button>
            <button
              onClick={() => setActiveTab('interview')}
              className={`px-4 py-2 rounded-lg font-bold transition ${activeTab === 'interview' ? 'bg-blue-600 text-white shadow' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
            >
              💼 Interview Mode
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`px-4 py-2 rounded-lg font-bold transition ${activeTab === 'history' ? 'bg-blue-600 text-white shadow' : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'}`}
            >
              📈 Progress & History
            </button>
          </div>
        }
      />

      {errorMsg && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/20 text-rose-600 dark:text-rose-300 rounded-xl text-xs flex items-center justify-between">
          <span>⚠️ {errorMsg}</span>
          <button onClick={() => setErrorMsg(null)} className="text-xs font-bold underline ml-2">Dismiss</button>
        </div>
      )}

      {/* Main Studio Tab */}
      {activeTab !== 'history' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Controls Panel */}
          <div className="lg:col-span-5 space-y-6">
            {/* Interview Question Selector (if in interview mode) */}
            {activeTab === 'interview' && (
              <div className="prof-card p-5 space-y-3">
                <label className="block text-xs font-bold text-blue-600 dark:text-blue-400">Target Interview Question</label>
                <input
                  type="text"
                  value={interviewQuestion}
                  onChange={(e) => setInterviewQuestion(e.target.value)}
                  placeholder="Enter or select interview question..."
                  className="w-full p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white"
                />
                <div className="flex flex-wrap gap-1 text-[11px]">
                  {["Tell me about yourself", "Explain a difficult bug", "Why should we hire you?"].map(q => (
                    <button
                      key={q}
                      onClick={() => setInterviewQuestion(q)}
                      className="px-2 py-1 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded border border-slate-200 dark:border-slate-700"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Audio Recording & File Upload Component */}
            <div className="prof-card p-5 space-y-4">
              <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center justify-between">
                <span>Microphone & Audio Input</span>
                {isRecording && <span className="flex items-center gap-1.5 text-rose-500 text-[11px] animate-pulse">🔴 Recording ({formatTime(recordingTime)})</span>}
              </h3>

              {/* Live Waveform Indicator & Controls */}
              <div className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-center space-y-3">
                <div className="h-10 flex items-center justify-center gap-1">
                  {[40, 70, 30, 90, 50, 80, 60, 100, 45, 85, 35, 65, 95, 40].map((h, idx) => (
                    <div
                      key={idx}
                      className={`w-1.5 rounded-full transition-all duration-300 ${isRecording && !isPaused ? 'bg-blue-500 animate-pulse' : 'bg-slate-300 dark:bg-slate-700'}`}
                      style={{ height: isRecording && !isPaused ? `${Math.max(15, (h * Math.random()).toFixed(0))}%` : '20%' }}
                    />
                  ))}
                </div>

                <div className="flex items-center justify-center gap-2">
                  {!isRecording ? (
                    <button
                      onClick={startRecording}
                      className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white font-bold rounded-xl text-xs flex items-center gap-1.5 shadow"
                    >
                      🎙️ Start Recording
                    </button>
                  ) : (
                    <>
                      {!isPaused ? (
                        <button
                          onClick={pauseRecording}
                          className="px-3 py-2 bg-amber-600 hover:bg-amber-500 text-white font-bold rounded-xl text-xs"
                        >
                          ⏸️ Pause
                        </button>
                      ) : (
                        <button
                          onClick={resumeRecording}
                          className="px-3 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl text-xs"
                        >
                          ▶️ Resume
                        </button>
                      )}
                      <button
                        onClick={stopRecording}
                        className="px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white font-bold rounded-xl text-xs"
                      >
                        ⏹️ Stop
                      </button>
                    </>
                  )}

                  {(audioBlob || uploadedFile) && (
                    <button
                      onClick={clearRecording}
                      className="btn-secondary"
                    >
                      🔄 Clear
                    </button>
                  )}
                </div>
              </div>

              {/* Audio Playback Element */}
              {audioUrl && (
                <div className="space-y-1">
                  <label className="block text-[11px] font-bold text-slate-500 dark:text-slate-400">Audio Preview Playback:</label>
                  <audio controls src={audioUrl} className="w-full h-8 rounded-lg" />
                </div>
              )}

              {/* Audio File Upload */}
              <div className="pt-2 border-t border-slate-200 dark:border-slate-800">
                <label className="block text-xs font-bold text-slate-500 dark:text-slate-400 mb-1">Or Upload Audio File (.wav, .mp3, .m4a, .webm):</label>
                <input
                  type="file"
                  accept="audio/*"
                  onChange={handleFileUpload}
                  className="w-full text-xs text-slate-500 dark:text-slate-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-slate-100 dark:file:bg-slate-800 file:text-blue-600 dark:file:text-blue-400 hover:file:bg-slate-200"
                />
              </div>
            </div>

            {/* Transcript & Duration Controls */}
            <div className="prof-card p-5 space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Spoken Answer Transcript</label>
                <textarea
                  rows={6}
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  placeholder="Paste or edit spoken answer transcript..."
                  className="w-full p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-900 dark:text-white resize-none"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">
                  <span>Speaking Duration:</span>
                  <span className="text-blue-600 dark:text-blue-400">{duration} seconds ({formatTime(duration)})</span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="180"
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  className="w-full accent-blue-600"
                />
              </div>

              <button
                onClick={handleAnalyze}
                disabled={isLoading}
                className="w-full btn-primary py-3 flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <span className="animate-spin">🌀</span> Computing Prosody Signal Metrics...
                  </>
                ) : (
                  <>⚡ Evaluate Speech & Acoustic Delivery</>
                )}
              </button>
            </div>
          </div>

          {/* Results Display Panel */}
          <div className="lg:col-span-7 space-y-6">
            {result ? (
              <div className="space-y-6">
                {/* Scorecard Hero Banner */}
                <div className="prof-card p-6 grid grid-cols-1 md:grid-cols-3 gap-4 items-center">
                  <div className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-center space-y-1">
                    <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Speech Delivery Score</p>
                    <p className={`text-4xl font-extrabold ${result.overall_delivery_score >= 85 ? 'text-emerald-600 dark:text-emerald-400' : result.overall_delivery_score >= 70 ? 'text-blue-600 dark:text-blue-400' : 'text-rose-600 dark:text-rose-400'}`}>
                      {result.overall_delivery_score}/100
                    </p>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 font-semibold">{result.metrics?.pace_category} Pace</p>
                  </div>

                  <div className="md:col-span-2 space-y-2">
                    <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">Executive Poise & Delivery Assessment</h3>
                    <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed bg-slate-50 dark:bg-slate-950 p-3 border border-slate-200 dark:border-slate-800 rounded-xl">
                      {result.delivery_indicators?.confidence_assessment}
                    </p>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-950/60 p-2 border border-slate-200 dark:border-slate-800/60 rounded-lg">
                      {result.delivery_indicators?.nervousness_assessment}
                    </p>
                  </div>
                </div>

                {/* 6-Pillar Transparent Score Breakdown Grid */}
                <div className="prof-card p-5 space-y-3">
                  <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">Transparent 6-Pillar Score Breakdown</h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                    <div className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl">
                      <p className="text-slate-500 dark:text-slate-400 text-[11px]">Pace (20%)</p>
                      <p className="text-base font-bold text-blue-600 dark:text-blue-400 mt-1">{result.score_breakdown?.pace_score}/100</p>
                      <p className="text-[10px] text-slate-500">{result.metrics?.words_per_minute} WPM</p>
                    </div>
                    <div className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl">
                      <p className="text-slate-500 dark:text-slate-400 text-[11px]">Clarity (20%)</p>
                      <p className="text-base font-bold text-emerald-600 dark:text-emerald-400 mt-1">{result.score_breakdown?.clarity_score}/100</p>
                      <p className="text-[10px] text-slate-500">{result.metrics?.clarity_rating}</p>
                    </div>
                    <div className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl">
                      <p className="text-slate-500 dark:text-slate-400 text-[11px]">Filler Control (20%)</p>
                      <p className="text-base font-bold text-amber-500 mt-1">{result.score_breakdown?.filler_control_score}/100</p>
                      <p className="text-[10px] text-slate-500">{result.metrics?.filler_words_count} fillers ({result.metrics?.filler_ratio_percentage}%)</p>
                    </div>
                    <div className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl">
                      <p className="text-slate-500 dark:text-slate-400 text-[11px]">Pause Control (15%)</p>
                      <p className="text-base font-bold text-blue-600 dark:text-blue-400 mt-1">{result.score_breakdown?.pause_control_score}/100</p>
                      <p className="text-[10px] text-slate-500">{result.audio_prosody?.pause?.pause_classification}</p>
                    </div>
                    <div className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl">
                      <p className="text-slate-500 dark:text-slate-400 text-[11px]">Pitch Intonation (12.5%)</p>
                      <p className="text-base font-bold text-indigo-600 dark:text-indigo-400 mt-1">{result.score_breakdown?.pitch_score}/100</p>
                      <p className="text-[10px] text-slate-500">{result.audio_prosody?.pitch?.pitch_variation_hz ? `${result.audio_prosody.pitch.pitch_variation_hz} Hz StdDev` : 'Standard'}</p>
                    </div>
                    <div className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl">
                      <p className="text-slate-500 dark:text-slate-400 text-[11px]">Volume Dynamics (12.5%)</p>
                      <p className="text-base font-bold text-teal-600 dark:text-teal-400 mt-1">{result.score_breakdown?.volume_score}/100</p>
                      <p className="text-[10px] text-slate-500">{result.audio_prosody?.volume?.volume_consistency}</p>
                    </div>
                  </div>
                </div>

                {/* Acoustic Prosody Metrics Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Pitch Card */}
                  <div className="prof-card p-4 space-y-2 text-xs">
                    <div className="flex items-center justify-between text-indigo-600 dark:text-indigo-400 font-bold">
                      <span>🎵 Pitch & Intonation</span>
                    </div>
                    {result.audio_prosody?.pitch?.is_available ? (
                      <div className="space-y-1 text-slate-700 dark:text-slate-300">
                        <p className="text-[11px]">Avg Pitch: <strong className="text-slate-900 dark:text-white">{result.audio_prosody.pitch.average_pitch_hz} Hz</strong></p>
                        <p className="text-[11px]">Range: <strong className="text-slate-900 dark:text-white">{result.audio_prosody.pitch.pitch_range_hz}</strong></p>
                        <p className="text-[11px] text-blue-600 dark:text-blue-400 font-semibold">{result.audio_prosody.pitch.pitch_classification}</p>
                      </div>
                    ) : (
                      <p className="text-[11px] text-slate-500">{result.audio_prosody?.pitch?.reason || "Pitch detection unavailable"}</p>
                    )}
                  </div>

                  {/* Volume Card */}
                  <div className="prof-card p-4 space-y-2 text-xs">
                    <div className="flex items-center justify-between text-teal-600 dark:text-teal-400 font-bold">
                      <span>🔊 Volume & Energy</span>
                    </div>
                    <div className="space-y-1 text-slate-700 dark:text-slate-300">
                      <p className="text-[11px]">Avg Loudness: <strong className="text-slate-900 dark:text-white">{result.audio_prosody?.volume?.average_volume_db} dBFS</strong></p>
                      <p className="text-[11px]">Consistency: <strong className="text-slate-900 dark:text-white">{result.audio_prosody?.volume?.volume_consistency}</strong></p>
                    </div>
                  </div>

                  {/* Pause Card */}
                  <div className="prof-card p-4 space-y-2 text-xs">
                    <div className="flex items-center justify-between text-amber-500 font-bold">
                      <span>⏸️ Pause Analysis</span>
                    </div>
                    <div className="space-y-1 text-slate-700 dark:text-slate-300">
                      <p className="text-[11px]">Longest Pause: <strong className="text-slate-900 dark:text-white">{result.audio_prosody?.pause?.longest_pause}s</strong></p>
                      <p className="text-[11px]">Total Pauses: <strong className="text-slate-900 dark:text-white">{result.audio_prosody?.pause?.pause_count} pauses ({result.audio_prosody?.pause?.total_pause_duration}s total)</strong></p>
                      <p className="text-[11px] text-amber-500 font-semibold">{result.audio_prosody?.pause?.pause_classification}</p>
                    </div>
                  </div>
                </div>

                {/* Highlighted Transcript & Detected Fillers */}
                <div className="prof-card p-5 space-y-4">
                  <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center justify-between">
                    <span>Annotated Transcript & Detected Fillers</span>
                    <span className="text-amber-500 text-[11px] font-semibold">{result.metrics?.filler_words_count} fillers detected</span>
                  </h3>

                  <div
                    className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-800 dark:text-slate-200 leading-relaxed font-sans"
                    dangerouslySetInnerHTML={{ __html: result.highlighted_transcript || transcript }}
                  />

                  {/* Filler Breakdown Badges */}
                  {Object.keys(result.detected_filler_breakdown || {}).length > 0 && (
                    <div className="space-y-1">
                      <p className="text-[11px] font-bold text-slate-500 dark:text-slate-400">Detected Filler Word Breakdown:</p>
                      <div className="flex flex-wrap gap-1.5">
                        {Object.entries(result.detected_filler_breakdown).map(([word, count]) => (
                          <span key={word} className="px-2.5 py-1 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-600 dark:text-rose-300 text-xs font-semibold">
                            "{word}": {count}x
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Timeline Events */}
                  {result.timeline_events && result.timeline_events.length > 0 && (
                    <div className="pt-2 border-t border-slate-200 dark:border-slate-800 space-y-2">
                      <p className="text-[11px] font-bold text-slate-500 dark:text-slate-400">Timeline Highlights:</p>
                      <div className="space-y-1 text-xs">
                        {result.timeline_events.map((ev, idx) => (
                          <div key={idx} className="flex items-center gap-2 text-slate-700 dark:text-slate-300 text-[11px]">
                            <span className="font-mono text-blue-600 dark:text-blue-400 font-bold">{ev.time}</span>
                            <span>— {ev.event}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* AI Personalized Coaching Box */}
                <div className="prof-card p-5 space-y-4">
                  <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                    <span>💡</span> Personalized AI Speech Coaching & Action Plan
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    {/* Strengths */}
                    <div className="p-4 bg-emerald-500/5 border border-emerald-500/20 rounded-xl space-y-2">
                      <h4 className="font-bold text-emerald-600 dark:text-emerald-400 text-xs">Key Strengths Observed</h4>
                      <ul className="space-y-1 text-slate-700 dark:text-slate-300 text-[11px] list-disc list-inside">
                        {(result.ai_coaching?.top_strengths || []).map((st, idx) => (
                          <li key={idx}>{st}</li>
                        ))}
                      </ul>
                    </div>

                    {/* Areas for Improvement */}
                    <div className="p-4 bg-rose-500/5 border border-rose-500/20 rounded-xl space-y-2">
                      <h4 className="font-bold text-rose-600 dark:text-rose-400 text-xs">Areas to Refine</h4>
                      <ul className="space-y-1 text-slate-700 dark:text-slate-300 text-[11px] list-disc list-inside">
                        {(result.ai_coaching?.top_weaknesses || []).map((wk, idx) => (
                          <li key={idx}>{wk}</li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* Recommended Exercises */}
                  {result.ai_coaching?.recommended_exercises && (
                    <div className="space-y-2 pt-2 border-t border-slate-200 dark:border-slate-800">
                      <h4 className="text-xs font-bold text-blue-600 dark:text-blue-400">Targeted Delivery Exercises:</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                        {result.ai_coaching.recommended_exercises.map((ex, idx) => (
                          <div key={idx} className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl space-y-1">
                            <p className="font-bold text-slate-900 dark:text-white text-[11px]">{ex.title}</p>
                            <p className="text-slate-500 dark:text-slate-400 text-[10px] leading-normal">{ex.description}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Next Attempt Goal */}
                  <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl text-xs text-blue-600 dark:text-blue-300 flex items-center justify-between">
                    <span>🎯 <strong>Next Goal:</strong> {result.ai_coaching?.next_attempt_goals}</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full min-h-[400px] flex flex-col items-center justify-center text-slate-500 text-xs border border-dashed border-slate-300 dark:border-slate-800 rounded-2xl p-8 text-center space-y-3">
                <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center text-xl">
                  🎙️
                </div>
                <p className="font-bold text-slate-700 dark:text-slate-300">Ready to Evaluate Your Speech Prosody</p>
                <p className="max-w-md text-slate-500 dark:text-slate-400 text-[11px]">
                  Record your voice or paste a transcript to receive real-time WPM pace analysis, pitch intonation (F0), pause filler ratios, and AI speech coaching.
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Progress & History Tab */}
      {activeTab === 'history' && (
        <div className="space-y-6">
          {/* Historical Score Progress Timeline */}
          {progress && progress.attempts_count > 0 ? (
            <div className="prof-card p-6 space-y-4">
              <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center justify-between">
                <span>Delivery Score Performance Progress ({progress.attempts_count} Attempts Recorded)</span>
                <span className="text-emerald-600 dark:text-emerald-400 font-bold text-xs">Latest: {progress.latest_score}/100</span>
              </h3>

              {/* Bar / Trend Chart */}
              <div className="h-40 flex items-end gap-3 pt-6 pb-2 border-b border-slate-200 dark:border-slate-800">
                {progress.score_trend.map((pt, idx) => (
                  <div key={idx} className="flex-1 flex flex-col items-center gap-1 group">
                    <span className="text-[10px] font-bold text-blue-600 dark:text-blue-400 opacity-0 group-hover:opacity-100 transition">{pt.score}</span>
                    <div
                      className="w-full bg-gradient-to-t from-blue-600 to-emerald-400 rounded-t-lg transition-all duration-500"
                      style={{ height: `${pt.score}%` }}
                    />
                    <span className="text-[10px] text-slate-500 dark:text-slate-400 font-semibold">{pt.attempt}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="prof-card p-8 text-center text-xs text-slate-500 dark:text-slate-400">
              No historical speech attempts stored yet. Complete your first evaluation to start tracking score progress!
            </div>
          )}

          {/* Detailed Attempts History Table */}
          <div className="prof-card p-6 space-y-4">
            <h3 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">Past Speech Evaluation Log</h3>
            {history.length > 0 ? (
              <div className="divide-y divide-slate-200 dark:divide-slate-800">
                {history.map((item, idx) => (
                  <div key={item.id || idx} className="py-3 flex items-center justify-between text-xs">
                    <div>
                      <p className="font-bold text-slate-900 dark:text-white text-xs">{item.metrics?.pace_rating || "Speech Evaluation"}</p>
                      <p className="text-slate-500 dark:text-slate-400 text-[11px] truncate max-w-md">{item.metrics?.total_words_spoken} words • {item.metrics?.words_per_minute} WPM • {item.metrics?.filler_words_count} fillers</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-extrabold text-emerald-600 dark:text-emerald-400">{item.overall_delivery_score || item.score}/100</p>
                      <p className="text-[10px] text-slate-500">{item.created_at ? item.created_at.substring(0, 10) : 'Recent'}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500">No stored history entries found.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SpeechDeliveryAnalyzer;
