import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const UserProfile = () => {
  const { user, updateProfile } = useAuth();
  const [name, setName] = useState(user?.name || '');
  const [targetRole, setTargetRole] = useState(user?.target_role || 'Software Engineer');
  const [skills, setSkills] = useState(Array.isArray(user?.skills) ? user.skills.join(', ') : '');
  const [location, setLocation] = useState(user?.location || '');
  const [experience, setExperience] = useState(user?.experience || '');
  const [education, setEducation] = useState(user?.education || '');
  const [github, setGithub] = useState(user?.github || '');
  const [linkedin, setLinkedin] = useState(user?.linkedin || '');
  const [portfolio, setPortfolio] = useState(user?.portfolio || '');
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setTargetRole(user.target_role || 'Software Engineer');
      setSkills(Array.isArray(user.skills) ? user.skills.join(', ') : (user.skills || ''));
      setLocation(user.location || '');
      setExperience(user.experience || '');
      setEducation(user.education || '');
      setGithub(user.github || '');
      setLinkedin(user.linkedin || '');
      setPortfolio(user.portfolio || '');
    }
    const fetchMe = async () => {
      try {
        const res = await api.auth.getMe();
        if (res?.user) {
          setName(res.user.name || '');
          setTargetRole(res.user.target_role || 'Software Engineer');
          setSkills(Array.isArray(res.user.skills) ? res.user.skills.join(', ') : (res.user.skills || ''));
          setLocation(res.user.location || '');
          setExperience(res.user.experience || '');
          setEducation(res.user.education || '');
          setGithub(res.user.github || '');
          setLinkedin(res.user.linkedin || '');
          setPortfolio(res.user.portfolio || '');
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchMe();
  }, [user]);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const skillsArray = skills.split(',').map(s => s.trim()).filter(Boolean);
      await updateProfile({
        name,
        target_role: targetRole,
        skills: skillsArray,
        location,
        experience,
        education,
        github,
        linkedin,
        portfolio
      });
      setMsg('Profile successfully updated in MongoDB!');
      setTimeout(() => setMsg(''), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-10 space-y-6">
      
      {/* Logged-in User Profile Header Card */}
      <div className="bg-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center text-2xl font-extrabold text-white shadow-lg shadow-blue-600/20 border border-blue-400/20">
            {name ? name[0].toUpperCase() : (user?.name ? user.name[0].toUpperCase() : 'U')}
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-white tracking-tight">
                {name || user?.name || 'Logged-in Candidate'}
              </h1>
              <span className="px-2.5 py-0.5 bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold rounded-md font-mono">
                {targetRole || user?.target_role || 'Software Engineer'}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 flex items-center gap-3">
              <span>📧 {user?.email || 'Logged-in Account'}</span>
              <span>•</span>
              <span className="text-emerald-400 font-medium flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Active Session
              </span>
            </p>
          </div>
        </div>

        <Link
          to="/dashboard"
          className="self-start md:self-auto px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl border border-slate-700 transition"
        >
          ← Back to Dashboard
        </Link>
      </div>

      <form onSubmit={handleSave} className="bg-slate-900/90 border border-slate-800 rounded-2xl p-8 shadow-xl max-w-3xl space-y-6 backdrop-blur-md">
        <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-800/80 pb-3">
          Candidate Profile & Credentials
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block text-slate-300 font-bold mb-1">Full Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your Full Name"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label className="block text-slate-300 font-bold mb-1">Target Role</label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. Full Stack Developer"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-slate-300 font-bold mb-1">Skills (comma-separated)</label>
            <input
              type="text"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
              placeholder="Python, FastAPI, React, MongoDB"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label className="block text-slate-300 font-bold mb-1">Location</label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. India / Remote"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label className="block text-slate-300 font-bold mb-1">Experience Level</label>
            <input
              type="text"
              value={experience}
              onChange={(e) => setExperience(e.target.value)}
              placeholder="e.g. Student / Fresh Graduate"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label className="block text-slate-300 font-bold mb-1">Education & University</label>
            <input
              type="text"
              value={education}
              onChange={(e) => setEducation(e.target.value)}
              placeholder="e.g. B.Tech Computer Science"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label className="block text-slate-300 font-bold mb-1">GitHub Profile URL</label>
            <input
              type="text"
              value={github}
              onChange={(e) => setGithub(e.target.value)}
              placeholder="github.com/username"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label className="block text-slate-300 font-bold mb-1">LinkedIn Profile URL</label>
            <input
              type="text"
              value={linkedin}
              onChange={(e) => setLinkedin(e.target.value)}
              placeholder="linkedin.com/in/username"
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            />
          </div>
        </div>

        <div className="flex items-center gap-4 pt-4 border-t border-slate-800/80">
          <button
            type="submit"
            disabled={saving}
            className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-600/20 transition duration-200"
          >
            {saving ? 'Saving...' : 'Update Profile in MongoDB'}
          </button>
          {msg && <span className="text-xs text-emerald-400 font-bold">✓ {msg}</span>}
        </div>
      </form>
    </div>
  );
};

export default UserProfile;
