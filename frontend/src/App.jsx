import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { UserProfileProvider } from './contexts/UserProfileContext';
import { ToastProvider } from './contexts/ToastContext';
import { ThemeProvider } from './contexts/ThemeContext';
import ProtectedRoute from './components/common/ProtectedRoute';

import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';
import FloatingAI from './components/layout/FloatingAI';
import NotificationDrawer from './components/layout/NotificationDrawer';

import LoginPage from './pages/auth/LoginPage';
import DashboardHub from './pages/DashboardHub';
import ResumeAnalyzer from './pages/ResumeAnalyzer';
import AIInterviewSimulator from './pages/AIInterviewSimulator';
import SpeechDeliveryAnalyzer from './pages/SpeechDeliveryAnalyzer';
import SystemDesignCanvas from './pages/SystemDesignCanvas';
import CodingArena from './pages/CodingArena';
import SkillGapAnalyzer from './pages/SkillGapAnalyzer';
import LearningRoadmap from './pages/LearningRoadmap';
import GitHubAnalyzer from './pages/GitHubAnalyzer';
import JobReadiness from './pages/JobReadiness';
import CompanyInsights from './pages/CompanyInsights';
import OASimulator from './pages/OASimulator';
import BehavioralSTARBuilder from './pages/BehavioralSTARBuilder';
import JobMatcher from './pages/JobMatcher';
import ApplicationKanban from './pages/ApplicationKanban';
import ResumeExporter from './pages/ResumeExporter';
import PlacementAdminPortal from './pages/PlacementAdminPortal';
import AICoverLetterGenerator from './pages/AICoverLetterGenerator';
import AILinkedInOptimizer from './pages/AILinkedInOptimizer';
import ProjectRecommendations from './pages/ProjectRecommendations';
import AIJobSalaryPredictor from './pages/AIJobSalaryPredictor';
import PortfolioBuilder from './pages/PortfolioBuilder';
import AIChatAssistant from './pages/AIChatAssistant';
import Analytics from './pages/Analytics';
import CodingProfilesTracker from './pages/CodingProfilesTracker';
import PlacementRoadmapTracker from './pages/PlacementRoadmapTracker';
import WeaknessDetector from './pages/WeaknessDetector';
import CompanyPrep from './pages/CompanyPrep';
import GDSimulator from './pages/GDSimulator';
import StudyPlanner from './pages/StudyPlanner';
import CareerSkillRadar from './pages/CareerSkillRadar';
import UserProfile from './pages/UserProfile';
import Settings from './pages/Settings';

const AppLayout = ({ children }) => {
  const [isNotifOpen, setIsNotifOpen] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col font-sans transition-colors duration-200">
      <Navbar 
        onOpenNotifications={() => setIsNotifOpen(true)} 
        onToggleMobileSidebar={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
      />
      <div className="flex flex-1">
        <Sidebar 
          isMobileOpen={isMobileSidebarOpen} 
          onCloseMobile={() => setIsMobileSidebarOpen(false)} 
        />
        <main className="flex-1 p-4 md:p-6 overflow-y-auto page-fade-in">
          {children}
        </main>
      </div>
      <FloatingAI />
      <NotificationDrawer isOpen={isNotifOpen} onClose={() => setIsNotifOpen(false)} />
    </div>
  );
};

const App = () => {
  return (
    <ThemeProvider>
      <AuthProvider>
        <UserProfileProvider>
          <ToastProvider>
            <BrowserRouter>
              <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route
                  path="/*"
                  element={
                    <ProtectedRoute>
                      <AppLayout>
                        <Routes>
                          <Route path="/dashboard" element={<DashboardHub />} />
                          <Route path="/weakness-detector" element={<WeaknessDetector />} />
                          <Route path="/resume-analyzer" element={<ResumeAnalyzer />} />
                          <Route path="/interview-simulator" element={<AIInterviewSimulator />} />
                          <Route path="/speech-analyzer" element={<SpeechDeliveryAnalyzer />} />
                          <Route path="/coding-arena" element={<CodingArena />} />
                          <Route path="/coding-tracker" element={<CodingProfilesTracker />} />
                          <Route path="/skill-gap" element={<SkillGapAnalyzer />} />
                          <Route path="/roadmap" element={<LearningRoadmap />} />
                          <Route path="/placement-roadmap" element={<PlacementRoadmapTracker />} />
                          <Route path="/github-analyzer" element={<GitHubAnalyzer />} />
                          <Route path="/job-readiness" element={<JobReadiness />} />
                          <Route path="/company-prep" element={<CompanyPrep />} />
                          <Route path="/gd-simulator" element={<GDSimulator />} />
                          <Route path="/study-planner" element={<StudyPlanner />} />
                          <Route path="/skill-radar" element={<CareerSkillRadar />} />
                          <Route path="/company-insights" element={<CompanyInsights />} />
                          <Route path="/oa-simulator" element={<OASimulator />} />
                          <Route path="/star-builder" element={<BehavioralSTARBuilder />} />
                          <Route path="/job-matcher" element={<JobMatcher />} />
                          <Route path="/applications" element={<ApplicationKanban />} />
                          <Route path="/resume-export" element={<ResumeExporter />} />
                          <Route path="/admin-portal" element={<PlacementAdminPortal />} />
                          <Route path="/cover-letter" element={<AICoverLetterGenerator />} />
                          <Route path="/linkedin-optimizer" element={<AILinkedInOptimizer />} />
                          <Route path="/project-recommendations" element={<ProjectRecommendations />} />
                          <Route path="/salary-predictor" element={<AIJobSalaryPredictor />} />
                          <Route path="/portfolio-builder" element={<PortfolioBuilder />} />
                          <Route path="/chat-assistant" element={<AIChatAssistant />} />
                          <Route path="/analytics" element={<Analytics />} />
                          <Route path="/profile" element={<UserProfile />} />
                          <Route path="/settings" element={<Settings />} />
                          <Route path="/" element={<Navigate to="/login" replace />} />
                        </Routes>
                      </AppLayout>
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </BrowserRouter>
          </ToastProvider>
        </UserProfileProvider>
      </AuthProvider>
    </ThemeProvider>
  );
};

export default App;
