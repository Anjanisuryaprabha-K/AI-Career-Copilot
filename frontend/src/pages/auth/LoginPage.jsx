import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const LoginPage = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [loading, setLoading] = useState(false);

  // Forgot Password Modal State
  const [showForgotModal, setShowForgotModal] = useState(false);
  const [forgotEmail, setForgotEmail] = useState('');
  const [forgotSubmitted, setForgotSubmitted] = useState(false);

  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMsg('');
    setLoading(true);
    try {
      if (isRegister) {
        await register(name, email, password, 'Software Engineer');
        setSuccessMsg('Registration successful! Please sign in with your email and password.');
        setIsRegister(false);
        setPassword('');
      } else {
        await login(email, password);
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.message || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleForgotSubmit = (e) => {
    e.preventDefault();
    if (!forgotEmail) return;
    setForgotSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex items-center justify-center p-4 sm:p-6 lg:p-10 relative overflow-hidden font-sans">
      
      {/* Background Subtle Gradient Shapes (Faint & Non-distracting) */}
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-blue-400/10 dark:bg-blue-600/10 rounded-full blur-3xl pointer-events-none -z-0" />
      <div className="absolute bottom-0 right-1/4 w-[450px] h-[450px] bg-cyan-400/10 dark:bg-cyan-600/10 rounded-full blur-3xl pointer-events-none -z-0" />

      {/* Main Centered Application Container */}
      <div className="w-full max-w-6xl mx-auto relative z-10">
        <div className="flex flex-col-reverse lg:flex-row items-center justify-center gap-8 lg:gap-12">
          
          {/* ================================================== */}
          {/* 2. LEFT SIDE — AI CAREER COPILOT (55% Desktop)     */}
          {/* ================================================== */}
          <div className="w-full lg:w-[55%] space-y-6 animate-fadeIn" style={{ animationDuration: '400ms' }}>
            
            {/* Header / Intro */}
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 text-blue-600 dark:text-blue-400 text-xs font-bold tracking-wide">
                <span>✨</span>
                <span>AI CAREER COPILOT</span>
              </div>

              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight">
                Your intelligent partner for becoming career-ready.
              </h1>

              <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed max-w-xl">
                From discovering your skill gaps to preparing for interviews and finding the right opportunities — everything is connected in one place.
              </p>
            </div>

            {/* 10. COMPACT AI DIAGRAM */}
            <div className="p-4 sm:p-5 bg-white/70 dark:bg-slate-900/70 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm backdrop-blur-md">
              <div className="flex flex-col items-center justify-center text-center space-y-3">
                {/* Node 1: AI Copilot Root */}
                <div className="px-4 py-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl text-xs font-bold shadow-md flex items-center gap-1.5">
                  <span>✨</span>
                  <span>AI CAREER COPILOT</span>
                </div>

                {/* Connecting Line Down */}
                <div className="w-0.5 h-4 bg-gradient-to-b from-blue-600 to-indigo-500 animate-pulse" />

                {/* Node Row: Skills, Coding, Interview */}
                <div className="w-full max-w-md grid grid-cols-3 gap-2 relative">
                  <div className="p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-center shadow-xs">
                    <p className="text-[10px] font-bold text-blue-600 dark:text-blue-400">🎯 Skills</p>
                  </div>
                  <div className="p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-center shadow-xs">
                    <p className="text-[10px] font-bold text-indigo-600 dark:text-indigo-400">💻 Coding</p>
                  </div>
                  <div className="p-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-center shadow-xs">
                    <p className="text-[10px] font-bold text-cyan-600 dark:text-cyan-400">🎤 Interview</p>
                  </div>
                </div>

                {/* Connecting Line Down */}
                <div className="w-0.5 h-4 bg-gradient-to-b from-indigo-500 to-emerald-500 animate-pulse" />

                {/* Node End: Career Ready */}
                <div className="px-4 py-1.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 rounded-xl text-xs font-extrabold font-mono">
                  🚀 Career Ready
                </div>
              </div>
            </div>

            {/* 4 Compact Capability Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
              
              {/* Card 1 */}
              <div className="p-4 bg-white/80 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-blue-300 dark:hover:border-blue-700 transition duration-200 space-y-1 shadow-xs">
                <div className="flex items-center gap-2">
                  <span className="text-base">🎯</span>
                  <h3 className="text-xs font-bold text-slate-900 dark:text-white">Personalized Roadmap</h3>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-normal">
                  Build a learning path based on your goals and skills.
                </p>
              </div>

              {/* Card 2 */}
              <div className="p-4 bg-white/80 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-blue-300 dark:hover:border-blue-700 transition duration-200 space-y-1 shadow-xs">
                <div className="flex items-center gap-2">
                  <span className="text-base">💻</span>
                  <h3 className="text-xs font-bold text-slate-900 dark:text-white">Smart Coding Practice</h3>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-normal">
                  Practice problems based on your performance.
                </p>
              </div>

              {/* Card 3 */}
              <div className="p-4 bg-white/80 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-blue-300 dark:hover:border-blue-700 transition duration-200 space-y-1 shadow-xs">
                <div className="flex items-center gap-2">
                  <span className="text-base">🎤</span>
                  <h3 className="text-xs font-bold text-slate-900 dark:text-white">AI Interview Coach</h3>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-normal">
                  Improve technical answers and communication.
                </p>
              </div>

              {/* Card 4 */}
              <div className="p-4 bg-white/80 dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 rounded-xl hover:border-blue-300 dark:hover:border-blue-700 transition duration-200 space-y-1 shadow-xs">
                <div className="flex items-center gap-2">
                  <span className="text-base">📈</span>
                  <h3 className="text-xs font-bold text-slate-900 dark:text-white">Career Readiness</h3>
                </div>
                <p className="text-[11px] text-slate-500 dark:text-slate-400 leading-normal">
                  Track your progress from preparation to placement.
                </p>
              </div>

            </div>

            {/* Bottom Stepper Flow with Subtle Lines */}
            <div className="pt-2 border-t border-slate-200 dark:border-slate-800">
              <div className="flex flex-wrap items-center justify-between text-[11px] font-mono text-slate-500 dark:text-slate-400 gap-1.5">
                <span className="font-semibold text-slate-700 dark:text-slate-300">Resume</span>
                <span className="text-blue-500">→</span>
                <span className="font-semibold text-slate-700 dark:text-slate-300">Skills</span>
                <span className="text-blue-500">→</span>
                <span className="font-semibold text-slate-700 dark:text-slate-300">Learn</span>
                <span className="text-blue-500">→</span>
                <span className="font-semibold text-slate-700 dark:text-slate-300">Code</span>
                <span className="text-blue-500">→</span>
                <span className="font-semibold text-slate-700 dark:text-slate-300">Interview</span>
                <span className="text-blue-500">→</span>
                <span className="font-bold text-emerald-600 dark:text-emerald-400">Jobs</span>
              </div>
            </div>

          </div>


          {/* ================================================== */}
          {/* 3. RIGHT SIDE — LOGIN CARD (45% Desktop)           */}
          {/* Primary Action Focus                               */}
          {/* ================================================== */}
          <div className="w-full lg:w-[45%] max-w-md mx-auto">
            <div 
              className="bg-[#FFFFFF] dark:bg-slate-900 border border-[#E2E8F0] dark:border-slate-800 rounded-[16px] p-6 sm:p-8 shadow-xl shadow-slate-200/50 dark:shadow-none space-y-6 transition duration-300 hover:shadow-2xl hover:shadow-blue-500/5 animate-fadeIn"
              style={{ animationDuration: '400ms' }}
            >
              {/* Card Header */}
              <div className="space-y-1.5">
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight flex items-center gap-2">
                  <span>Welcome back</span>
                  <span>👋</span>
                </h2>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  {isRegister ? 'Create your account to start your career journey.' : 'Sign in to continue your career journey.'}
                </p>
              </div>

              {/* Banners for Success / Error */}
              {successMsg && (
                <div className="p-3.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-xs text-emerald-600 dark:text-emerald-400 font-medium flex items-center gap-2">
                  <span>✓</span>
                  <span>{successMsg}</span>
                </div>
              )}

              {error && (
                <div className="p-3.5 bg-rose-500/10 border border-rose-500/20 rounded-xl text-xs text-rose-600 dark:text-rose-400 font-medium flex items-center gap-2">
                  <span>⚠️</span>
                  <span>{error}</span>
                </div>
              )}

              {/* Login / Register Form */}
              <form onSubmit={handleSubmit} className="space-y-4 text-xs">
                
                {/* Name Input (If Register Mode) */}
                {isRegister && (
                  <div className="space-y-1.5">
                    <label className="block text-slate-700 dark:text-slate-300 font-bold text-xs">Full Name</label>
                    <div className="relative">
                      <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm">👤</span>
                      <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Enter your full name"
                        required
                        className="w-full pl-10 pr-4 py-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20 transition font-sans text-xs"
                      />
                    </div>
                  </div>
                )}

                {/* Email Field with Icon */}
                <div className="space-y-1.5">
                  <label className="block text-slate-700 dark:text-slate-300 font-bold text-xs">Email Address</label>
                  <div className="relative">
                    <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm">✉</span>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="Enter your email"
                      required
                      className="w-full pl-10 pr-4 py-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20 transition font-sans text-xs"
                    />
                  </div>
                </div>

                {/* Password Field with Show/Hide Toggle */}
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between">
                    <label className="block text-slate-700 dark:text-slate-300 font-bold text-xs">Password</label>
                    {!isRegister && (
                      <button
                        type="button"
                        onClick={() => {
                          setForgotEmail(email);
                          setShowForgotModal(true);
                          setForgotSubmitted(false);
                        }}
                        className="text-xs text-blue-600 dark:text-blue-400 hover:underline font-semibold focus:outline-none focus:ring-2 focus:ring-blue-500/20 rounded"
                      >
                        Forgot password?
                      </button>
                    )}
                  </div>

                  <div className="relative">
                    <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm">🔒</span>
                    
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••••••••••••••"
                      required
                      className="w-full pl-10 pr-11 py-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20 transition font-sans text-xs"
                    />

                    {/* Show/Hide Password Eye Button */}
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      aria-label={showPassword ? "Hide password" : "Show password"}
                      className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-600/30 rounded-lg transition"
                    >
                      {showPassword ? (
                        /* Hide Password Icon (Eye Off) */
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858-5.908a10.046 10.046 0 013.122-.463c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m-7.228-3.097a3 3 0 11-4.243-4.243m4.243 4.243L3 3l18 18" />
                        </svg>
                      ) : (
                        /* Show Password Icon (Eye Open) */
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                      )}
                    </button>
                  </div>
                </div>

                {/* Primary Blue Button */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full group relative py-3.5 px-4 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md hover:shadow-lg hover:shadow-blue-600/25 active:scale-[0.99] active:translate-y-0 hover:-translate-y-0.5 transition-all duration-150 disabled:opacity-70 disabled:pointer-events-none flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      <span>{isRegister ? 'Creating account...' : 'Signing in...'}</span>
                    </>
                  ) : (
                    <>
                      <span>{isRegister ? 'Create Account' : 'Sign In'}</span>
                      <span className="group-hover:translate-x-1 transition-transform duration-150">→</span>
                    </>
                  )}
                </button>
              </form>

              {/* Divider */}
              <div className="relative flex items-center justify-center my-4">
                <div className="border-t border-slate-200 dark:border-slate-800 w-full" />
                <span className="bg-white dark:bg-slate-900 px-3 text-[10px] uppercase font-mono font-bold text-slate-400 shrink-0">
                  OR
                </span>
                <div className="border-t border-slate-200 dark:border-slate-800 w-full" />
              </div>

              {/* Toggle Register / Sign In */}
              <div className="text-center text-xs">
                <span className="text-slate-500 dark:text-slate-400">
                  {isRegister ? 'Already have an account?' : "Don't have an account?"}
                </span>{' '}
                <button
                  type="button"
                  onClick={() => {
                    setIsRegister(!isRegister);
                    setError('');
                    setSuccessMsg('');
                  }}
                  className="text-blue-600 dark:text-blue-400 font-bold hover:underline ml-1 focus:outline-none focus:ring-2 focus:ring-blue-500/20 rounded"
                >
                  {isRegister ? 'Sign In' : 'Create an account'}
                </button>
              </div>

            </div>
          </div>

        </div>
      </div>

      {/* Forgot Password Modal */}
      {showForgotModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-6 max-w-sm w-full space-y-4 shadow-2xl">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-slate-900 dark:text-white">Reset Password</h3>
              <button
                onClick={() => setShowForgotModal(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 font-bold"
              >
                ✕
              </button>
            </div>

            {!forgotSubmitted ? (
              <form onSubmit={handleForgotSubmit} className="space-y-4 text-xs">
                <p className="text-slate-500 dark:text-slate-400">
                  Enter your email address and we'll send you instructions to reset your password.
                </p>
                <div>
                  <label className="block text-slate-700 dark:text-slate-300 font-bold mb-1">Email Address</label>
                  <input
                    type="email"
                    value={forgotEmail}
                    onChange={(e) => setForgotEmail(e.target.value)}
                    required
                    placeholder="Enter your email"
                    className="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-900 dark:text-white text-xs"
                  />
                </div>
                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setShowForgotModal(false)}
                    className="flex-1 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 py-2 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl"
                  >
                    Send Instructions
                  </button>
                </div>
              </form>
            ) : (
              <div className="space-y-3 text-xs text-center py-2">
                <div className="w-10 h-10 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 flex items-center justify-center mx-auto text-lg font-bold">
                  ✓
                </div>
                <p className="font-bold text-slate-900 dark:text-white">Instructions Sent!</p>
                <p className="text-slate-500 dark:text-slate-400">
                  If an account exists for <strong className="text-slate-700 dark:text-slate-200">{forgotEmail}</strong>, password reset steps have been dispatched.
                </p>
                <button
                  onClick={() => setShowForgotModal(false)}
                  className="w-full py-2 bg-blue-600 text-white font-bold rounded-xl mt-2"
                >
                  Back to Sign In
                </button>
              </div>
            )}
          </div>
        </div>
      )}

    </div>
  );
};

export default LoginPage;
