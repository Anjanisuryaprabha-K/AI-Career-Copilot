import React, { useState, useEffect } from 'react';

const PomodoroWidget = () => {
  const [minutes, setMinutes] = useState(25);
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [mode, setMode] = useState('work'); // 'work' or 'break'

  useEffect(() => {
    let interval = null;
    if (isActive) {
      interval = setInterval(() => {
        if (seconds > 0) {
          setSeconds(seconds - 1);
        } else if (seconds === 0) {
          if (minutes === 0) {
            clearInterval(interval);
            setIsActive(false);
            if (mode === 'work') {
              setMode('break');
              setMinutes(5);
            } else {
              setMode('work');
              setMinutes(25);
            }
          } else {
            setMinutes(minutes - 1);
            setSeconds(59);
          }
        }
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive, minutes, seconds, mode]);

  const toggleTimer = () => setIsActive(!isActive);

  const resetTimer = () => {
    setIsActive(false);
    setMode('work');
    setMinutes(25);
    setSeconds(0);
  };

  return (
    <div className="text-center space-y-3">
      <div className="flex justify-center gap-2">
        <button
          onClick={() => { setMode('work'); setMinutes(25); setSeconds(0); setIsActive(false); }}
          className={`px-2.5 py-1 text-xs rounded-lg font-medium transition ${
            mode === 'work' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'
          }`}
        >
          Work (25m)
        </button>
        <button
          onClick={() => { setMode('break'); setMinutes(5); setSeconds(0); setIsActive(false); }}
          className={`px-2.5 py-1 text-xs rounded-lg font-medium transition ${
            mode === 'break' ? 'bg-emerald-600 text-white' : 'bg-gray-700 text-gray-300'
          }`}
        >
          Break (5m)
        </button>
      </div>

      <div className="text-3xl font-mono font-bold text-white tracking-wider">
        {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
      </div>

      <div className="flex justify-center gap-2">
        <button
          onClick={toggleTimer}
          className="px-3.5 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg transition"
        >
          {isActive ? 'Pause' : 'Start'}
        </button>
        <button
          onClick={resetTimer}
          className="px-3.5 py-1.5 bg-gray-700 hover:bg-gray-600 text-gray-300 text-xs font-semibold rounded-lg transition"
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default PomodoroWidget;
