import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const [loading, setLoading] = useState(true);

  // Initialize session on mount (always start unauthenticated so app opens on login page)
  useEffect(() => {
    const initAuth = async () => {
      localStorage.removeItem('access_token');
      setToken(null);
      setUser(null);
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    const res = await api.auth.login(email, password);
    if (res?.access_token) {
      localStorage.setItem('access_token', res.access_token);
      setToken(res.access_token);
      setUser(res.user);
      return res.user;
    }
  };

  const register = async (name, email, password, target_role) => {
    const res = await api.auth.register(name, email, password, target_role);
    // Do NOT log in automatically on registration; return response so UI can prompt user to log in
    return res;
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setToken(null);
    setUser(null);
  };

  const updateProfile = async (profileData) => {
    const res = await api.auth.updateProfile(profileData);
    if (res?.user) {
      setUser(res.user);
      return res.user;
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      token,
      loading,
      isLoading: loading,
      login,
      register,
      logout,
      updateProfile,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
export default AuthContext;
