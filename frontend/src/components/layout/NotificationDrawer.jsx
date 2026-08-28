import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';

const NotificationDrawer = ({ isOpen, onClose }) => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    if (isOpen) {
      const fetchNotifs = async () => {
        try {
          const res = await api.notifications.list();
          if (res?.notifications) {
            setNotifications(res.notifications);
          }
        } catch (err) {
          console.error(err);
        }
      };
      fetchNotifs();
    }
  }, [isOpen]);

  const handleMarkAllRead = async () => {
    try {
      await api.notifications.markAllRead();
      setNotifications(notifications.map(n => ({ ...n, read: true })));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.notifications.delete(id);
      setNotifications(notifications.filter(n => (n.id !== id && n._id !== id)));
    } catch (err) {
      console.error(err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-sm bg-gray-900 border-l border-gray-800 h-full p-6 flex flex-col space-y-4 shadow-2xl">
        <div className="flex items-center justify-between pb-3 border-b border-gray-800">
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            🔔 Placement Notifications
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-xs">✕</button>
        </div>

        <div className="flex items-center justify-between text-xs text-gray-400">
          <span>{notifications.filter(n => !n.read).length} unread</span>
          <button onClick={handleMarkAllRead} className="text-cyan-400 hover:underline">
            Mark all read
          </button>
        </div>

        <div className="flex-1 overflow-y-auto space-y-3">
          {notifications.map((n) => (
            <div
              key={n.id || n._id}
              className={`p-3.5 rounded-xl border text-xs space-y-1 relative ${
                n.read ? 'bg-gray-950/60 border-gray-800 text-gray-400' : 'bg-gray-950 border-cyan-900/60 text-gray-200'
              }`}
            >
              <div className="flex items-start justify-between">
                <h4 className="font-bold text-white text-[11px]">{n.title}</h4>
                <button onClick={() => handleDelete(n.id || n._id)} className="text-gray-600 hover:text-rose-400 text-[10px]">✕</button>
              </div>
              <p className="text-[11px] leading-relaxed">{n.message}</p>
              <span className="text-[9px] text-gray-500">{new Date(n.created_at || Date.now()).toLocaleDateString()}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default NotificationDrawer;
