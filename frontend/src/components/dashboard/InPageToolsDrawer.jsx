import React, { useState } from 'react';
import PomodoroWidget from '../common/PomodoroWidget';
import LogCodingModal from './LogCodingModal';

const InPageToolsDrawer = ({ isOpen, onClose }) => {
  const [isLogModalOpen, setIsLogModalOpen] = useState(false);

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="fixed right-0 top-0 bottom-0 z-50 w-full max-w-md bg-gray-900 border-l border-gray-800 p-6 shadow-2xl overflow-y-auto space-y-6">
        <div className="flex items-center justify-between border-b border-gray-800 pb-4">
          <div className="flex items-center gap-2">
            <span className="text-xl">🛠️</span>
            <h3 className="text-lg font-bold text-white">Focus & Quick Tools</h3>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white text-lg p-1 rounded-lg"
          >
            ✕
          </button>
        </div>

        {/* Pomodoro Focus Timer */}
        <div className="bg-gray-800/60 border border-gray-700/60 p-4 rounded-xl space-y-3">
          <h4 className="text-sm font-semibold text-gray-200">Pomodoro Study Timer</h4>
          <PomodoroWidget />
        </div>

        {/* Quick Log Coding Activity */}
        <div className="bg-gray-800/60 border border-gray-700/60 p-4 rounded-xl space-y-3">
          <h4 className="text-sm font-semibold text-gray-200">Log External Coding Activity</h4>
          <p className="text-xs text-gray-400">
            Log problems solved on LeetCode, HackerRank, or Codeforces to keep your streak active.
          </p>
          <button
            onClick={() => setIsLogModalOpen(true)}
            className="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg transition"
          >
            + Log Coding Problem
          </button>
        </div>
      </div>

      <LogCodingModal
        isOpen={isLogModalOpen}
        onClose={() => setIsLogModalOpen(false)}
      />
    </>
  );
};

export default InPageToolsDrawer;
