import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

const Settings = () => {
  const [theme, setTheme] = useState('dark');
  const [notifications, setNotifications] = useState(true);
  const [remotePreference, setRemotePreference] = useState(true);
  const [preferredLocations, setPreferredLocations] = useState('Hyderabad, Bengaluru, Remote');
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState(false);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const res = await api.auth.getSettings();
        if (res?.settings) {
          setTheme(res.settings.theme || 'dark');
          setNotifications(res.settings.notifications ?? true);
          setRemotePreference(res.settings.remote_preference ?? true);
          if (res.settings.preferred_locations) {
            setPreferredLocations(res.settings.preferred_locations.join(', '));
          }
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.auth.updateSettings({
        theme,
        notifications,
        remote_preference: remotePreference,
        preferred_locations: preferredLocations.split(',').map(s => s.trim())
      });
      setSavedMsg(true);
      setTimeout(() => setSavedMsg(false), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-6 lg:p-10 space-y-6">
      <div className="flex items-center justify-between bg-gray-900 border border-gray-800 p-6 rounded-2xl shadow-xl">
        <div>
          <Link to="/dashboard" className="text-gray-400 hover:text-white text-sm">
            ← Back to Dashboard
          </Link>
          <h1 className="text-2xl font-bold text-white mt-2">Settings & Preferences ⚙️</h1>
          <p className="text-xs text-gray-400 mt-1">Configured settings are stored directly in MongoDB.</p>
        </div>
      </div>

      <form onSubmit={handleSave} className="bg-gray-900 border border-gray-800 rounded-2xl p-8 shadow-xl max-w-2xl space-y-6">
        <div className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-gray-300 mb-1">Theme Mode</label>
            <select
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
              className="w-full px-3.5 py-2.5 bg-gray-950 border border-gray-800 rounded-xl text-xs text-white"
            >
              <option value="dark">Dark Theme (Professional Slate / Cyan)</option>
              <option value="system">System Default</option>
            </select>
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-950 rounded-xl border border-gray-800">
            <div>
              <p className="text-xs font-bold text-white">Placement & Interview Notifications</p>
              <p className="text-[11px] text-gray-400">Receive alerts for upcoming deadlines and assessment links.</p>
            </div>
            <input
              type="checkbox"
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
              className="w-4 h-4 text-cyan-600 rounded bg-gray-900 border-gray-700"
            />
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-950 rounded-xl border border-gray-800">
            <div>
              <p className="text-xs font-bold text-white">Remote Placement Preference</p>
              <p className="text-[11px] text-gray-400">Prioritize remote & hybrid engineering opportunities.</p>
            </div>
            <input
              type="checkbox"
              checked={remotePreference}
              onChange={(e) => setRemotePreference(e.target.checked)}
              className="w-4 h-4 text-cyan-600 rounded bg-gray-900 border-gray-700"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-gray-300 mb-1">Preferred Job Locations (comma-separated)</label>
            <input
              type="text"
              value={preferredLocations}
              onChange={(e) => setPreferredLocations(e.target.value)}
              className="w-full px-3.5 py-2.5 bg-gray-950 border border-gray-800 rounded-xl text-xs text-white"
            />
          </div>
        </div>

        <div className="flex items-center gap-4 pt-4 border-t border-gray-800">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 text-white rounded-xl text-xs font-bold shadow-lg transition"
          >
            {saving ? 'Saving...' : 'Save Settings to MongoDB'}
          </button>
          {savedMsg && (
            <span className="text-xs text-emerald-400 font-bold">✓ Settings saved successfully in MongoDB!</span>
          )}
        </div>
      </form>
    </div>
  );
};

export default Settings;
