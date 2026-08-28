import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';
import { useAuth } from './AuthContext';

const UserProfileContext = createContext(null);

export const UserProfileProvider = ({ children }) => {
  const { user } = useAuth();
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  // Re-hydrate profile state from user details or persona endpoint
  const rehydrateProfile = async () => {
    setLoading(true);
    try {
      if (user?.profile?.isInitialized) {
        setUserProfile(user.profile);
      } else {
        const res = await api.persona.getProfile();
        if (res?.profile) {
          setUserProfile(res.profile);
        } else {
          setUserProfile({
            detectedRole: user?.target_role || '',
            experienceLevel: 'Not Analyzed',
            topSkills: user?.skills || [],
            skillGaps: [],
            recommendedTrack: 'dsa',
            isInitialized: false
          });
        }
      }
    } catch (err) {
      console.warn('Error fetching persona profile:', err);
      setUserProfile({
        detectedRole: user?.target_role || '',
        experienceLevel: 'Not Analyzed',
        topSkills: user?.skills || [],
        skillGaps: [],
        recommendedTrack: 'dsa',
        isInitialized: false
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    rehydrateProfile();
  }, [user]);

  // Role Override Handler
  const overrideRole = async (roleName, trackId) => {
    setLoading(true);
    try {
      const res = await api.persona.updateRole(roleName, trackId);
      if (res?.profile) {
        setUserProfile(res.profile);
        return res.profile;
      }
    } catch (err) {
      console.error('Failed to override target role persona:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <UserProfileContext.Provider value={{
      userProfile,
      detectedRole: userProfile?.detectedRole || user?.target_role || '',
      isInitialized: !!(userProfile?.isInitialized),
      experienceLevel: userProfile?.experienceLevel || 'Intermediate',
      topSkills: userProfile?.topSkills || [],
      skillGaps: userProfile?.skillGaps || [],
      recommendedTrack: userProfile?.recommendedTrack || 'dsa',
      loading,
      rehydrateProfile,
      overrideRole
    }}>
      {children}
    </UserProfileContext.Provider>
  );
};

export const useUserProfile = () => useContext(UserProfileContext);
export default UserProfileContext;

