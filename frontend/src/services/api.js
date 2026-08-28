const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
    const token = localStorage.getItem('access_token');

    const headers = {
      ...(!options.isFormData && { 'Content-Type': 'application/json' }),
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    };

    const config = {
      ...options,
      headers,
    };

    if (options.body && !options.isFormData && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);

      if (response.status === 401) {
        // Token invalid or expired
        if (token && !endpoint.includes('/login') && !endpoint.includes('/register')) {
          console.warn('[API] Session token expired or invalid.');
        }
      }

      const isJson = (response.headers.get('content-type') || '').includes('application/json');
      const data = isJson ? await response.json() : await response.text();

      if (!response.ok) {
        const errorMsg = data?.detail || data?.message || `Request failed with status ${response.status}`;
        throw new Error(errorMsg);
      }

      return data;
    } catch (error) {
      console.error(`[API Error] ${options.method || 'GET'} ${endpoint}:`, error.message);
      throw error;
    }
  }

  get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'GET' });
  }

  post(endpoint, body, options = {}) {
    return this.request(endpoint, { ...options, method: 'POST', body });
  }

  put(endpoint, body, options = {}) {
    return this.request(endpoint, { ...options, method: 'PUT', body });
  }

  delete(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: 'DELETE' });
  }

  // Auth & Profile
  auth = {
    login: (email, password) => this.post('/api/v1/auth/login', { email, password }),
    register: (name, email, password, target_role) => this.post('/api/v1/auth/register', { name, email, password, target_role }),
    getMe: () => this.get('/api/v1/auth/me'),
    updateProfile: (profileData) => this.put('/api/v1/auth/profile', profileData),
    getSettings: () => this.get('/api/v1/auth/settings'),
    updateSettings: (settingsData) => this.put('/api/v1/auth/settings', settingsData),
  };

  // Google Search & Intelligence
  search = {
    web: (query, type = 'all', page = 1, limit = 10) =>
      this.get(`/api/v1/search?query=${encodeURIComponent(query)}&type=${type}&page=${page}&limit=${limit}`),
  };

  // Resume & ATS
  resume = {
    analyzeText: (resume_text, target_role, custom_jd, company_name) =>
      this.post('/api/v1/resume/analyze-text', { resume_text, target_role, custom_jd, company_name }),
    analyzeFile: (formData) =>
      this.post('/api/v1/resume/analyze-file', formData, { isFormData: true }),
    getHistory: () => this.get('/api/v1/resume/history'),
    getScanById: (scanId) => this.get(`/api/v1/resume/history/${encodeURIComponent(scanId)}`),
    benchmarkSearch: (target_role, company_name, custom_jd) =>
      this.post('/api/v1/resume/benchmark-search', { target_role, company_name, custom_jd }),
    rewriteBullet: (bullet_point, action_verb) =>
      this.post('/api/v1/resume/rewrite-bullet', { bullet_point, action_verb }),
    generateLatex: (userData) =>
      this.post('/api/v1/resume-export/generate-latex', userData),
  };

  // Jobs & Matching
  roadmap = {
    getTracks: () => this.get('/api/v1/skills/roadmap/tracks'),
    getTrack: (track_name) => this.get(`/api/v1/skills/roadmap/${encodeURIComponent(track_name)}`),
    toggleVideo: (payload) => this.post('/api/v1/skills/roadmap/progress/toggle', payload),
    getUserProgress: (userId, trackId) => this.get(`/api/v1/skills/roadmap/user-progress/${encodeURIComponent(userId)}/${encodeURIComponent(trackId)}`),

    // Adaptive Roadmap Endpoints
    getAdaptive: () => this.get('/api/v1/skills/roadmap/adaptive'),
    getAdaptiveRoles: () => this.get('/api/v1/skills/roadmap/adaptive/roles'),
    configureAdaptive: (payload) => this.post('/api/v1/skills/roadmap/adaptive/configure', payload),
    toggleAdaptiveItem: (itemId, is_completed) => this.post(`/api/v1/skills/roadmap/adaptive/toggle-item/${encodeURIComponent(itemId)}`, { is_completed }),
    recalculateAdaptive: () => this.post('/api/v1/skills/roadmap/adaptive/recalculate'),

    // YouTube Learning Resources & Bookmarks
    getResources: (params = {}) => {
      const q = new URLSearchParams();
      if (params.topic) q.append('topic', params.topic);
      if (params.role) q.append('role', params.role);
      if (params.difficulty) q.append('difficulty', params.difficulty);
      if (params.resource_type) q.append('resource_type', params.resource_type);
      return this.get(`/api/v1/skills/resources?${q.toString()}`);
    },
    getRecommendedResources: (role) => this.get(`/api/v1/skills/resources/recommended${role ? `?role=${encodeURIComponent(role)}` : ''}`),
    getBookmarks: () => this.get('/api/v1/skills/resources/bookmarks'),
    bookmarkResource: (resourceId, payload) => this.post(`/api/v1/skills/resources/${encodeURIComponent(resourceId)}/bookmark`, payload || {}),
    unbookmarkResource: (resourceId) => this.delete(`/api/v1/skills/resources/${encodeURIComponent(resourceId)}/bookmark`),
    updateResourceProgress: (resourceId, status, topic) => this.post(`/api/v1/skills/resources/${encodeURIComponent(resourceId)}/complete`, { status, topic }),
    adminSaveResource: (payload) => this.post('/api/v1/skills/admin/resources', payload),
    adminDeleteResource: (resourceId) => this.delete(`/api/v1/skills/admin/resources/${encodeURIComponent(resourceId)}`),
  };

  weakness = {
    getAnalysis: () => this.get('/api/v1/weakness/analysis'),
    runAnalysis: () => this.post('/api/v1/weakness/analyze'),
  };

  companyPrep = {
    getCatalog: () => this.get('/api/v1/company-prep/catalog'),
    getPlan: (companyId, targetRole) =>
      this.get(`/api/v1/company-prep/plan?company_id=${encodeURIComponent(companyId || 'ibm')}${targetRole ? `&target_role=${encodeURIComponent(targetRole)}` : ''}`),
    selectTarget: (companyId, targetRole) =>
      this.post('/api/v1/company-prep/select', { company_id: companyId, target_role: targetRole }),
  };

  gd = {
    getCategories: () => this.get('/api/v1/gd/categories'),
    getTopics: (category, difficulty) =>
      this.get(`/api/v1/gd/topics?${category ? `category=${encodeURIComponent(category)}` : ''}${difficulty ? `&difficulty=${encodeURIComponent(difficulty)}` : ''}`),
    generateTopic: (category, difficulty, duration_minutes) =>
      this.post('/api/v1/gd/generate-topic', { category, difficulty, duration_minutes }),
    evaluateGD: (payload) =>
      this.post('/api/v1/gd/evaluate', payload),
    getHistory: () => this.get('/api/v1/gd/history'),
  };

  studyPlanner = {
    getPlan: () => this.get('/api/v1/study-planner/plan'),
    generatePlan: (payload) => this.post('/api/v1/study-planner/generate', payload),
    completeTask: (task_id) => this.post('/api/v1/study-planner/complete-task', { task_id }),
    reschedule: () => this.post('/api/v1/study-planner/reschedule', {}),
  };

  skillRadar = {
    getRadar: (target_role) =>
      this.get(`/api/v1/skill-radar/radar?target_role=${encodeURIComponent(target_role || 'Software Engineer')}`),
    getTargets: () => this.get('/api/v1/skill-radar/targets'),
    getHistory: () => this.get('/api/v1/skill-radar/history'),
  };

  persona = {
    getProfile: () => this.get('/api/v1/persona/me'),
    detectRole: (resume_text, target_role_override) =>
      this.post('/api/v1/persona/detect-role', { resume_text, target_role_override }),
    updateRole: (role_name, track_id) =>
      this.post('/api/v1/persona/update-role', { role_name, track_id }),
  };

  jobs = {
    getRoles: () => this.get('/api/v1/jobs/roles'),
    getRecommendations: () => this.get('/api/v1/jobs/recommendations'),
    matchJobs: (payload) => this.post('/api/v1/matching/match-jobs', payload),
    saveJob: (job_id, saved) => this.post('/api/v1/jobs/save-job', { job_id, saved }),
    calculateReadiness: (scores) => this.post('/api/v1/jobs/calculate-readiness', scores),
    predictSalary: (payload) => this.post('/api/v1/jobs/predict-salary', payload),
  };

  // Applications Kanban
  applications = {
    list: () => this.get('/api/v1/applications/'),
    create: (appData) => this.post('/api/v1/applications/', appData),
    updateStage: (app_id, new_stage) => this.put('/api/v1/applications/update-stage', { app_id, new_stage }),
    delete: (app_id) => this.delete(`/api/v1/applications/${app_id}`),
  };

  // Chat & AI Mentor
  chat = {
    send: (message, conversation_id) => this.post('/api/v1/chat/send', { message, conversation_id }),
    getConversations: () => this.get('/api/v1/chat/conversations'),
    deleteConversation: (conv_id) => this.delete(`/api/v1/chat/conversations/${conv_id}`),
    getMentorSummary: () => this.get('/api/v1/chat/mentor-summary'),
  };

  // Coding Arena & Profiles
  coding = {
    getTopics: () => this.get('/api/v1/coding/topics'),
    getProblems: () => this.get('/api/v1/coding/problems'),
    getProblemsFiltered: (params = {}) => {
      const q = new URLSearchParams();
      if (params.role) q.append('role', params.role);
      if (params.category) q.append('category', params.category);
      if (params.topic) q.append('topic', params.topic);
      if (params.difficulty) q.append('difficulty', params.difficulty);
      if (params.language) q.append('language', params.language);
      if (params.status) q.append('status', params.status);
      if (params.search) q.append('search', params.search);
      if (params.page) q.append('page', params.page);
      if (params.limit) q.append('limit', params.limit);
      return this.get(`/api/v1/coding/problems?${q.toString()}`);
    },
    getProblem: (pid) => this.get(`/api/v1/coding/problems/${pid}`),
    toggleBookmark: (pid) => this.post(`/api/v1/coding/bookmark/${pid}`),
    getBookmarks: () => this.get('/api/v1/coding/bookmarks'),
    getRandomPractice: (params = {}) => {
      const q = new URLSearchParams();
      if (params.role) q.append('role', params.role);
      if (params.category) q.append('category', params.category);
      if (params.difficulty) q.append('difficulty', params.difficulty);
      return this.get(`/api/v1/coding/random-practice?${q.toString()}`);
    },
    startInterviewPrep: (data) => this.post('/api/v1/coding/interview-prep/start', data),
    submitInterviewPrep: (data) => this.post('/api/v1/coding/interview-prep/submit-session', data),
    runCode: (problem_id, language, code) => this.post('/api/v1/coding/run', { problem_id, language, code }),
    submitCode: (problem_id, language, code) => this.post('/api/v1/coding/submit', { problem_id, language, code }),
    getHistory: () => this.get('/api/v1/coding/history'),
    getProgress: () => this.get('/api/v1/coding/progress'),
    getDailyChallenge: () => this.get('/api/v1/coding/daily'),
    getLeetCodeStats: (username) => this.get(`/api/v1/coding/leetcode/${encodeURIComponent(username)}`),
    getHackerRankStats: (username) => this.get(`/api/v1/coding/hackerrank/${encodeURIComponent(username)}`),
    connectProfiles: (payload) => this.post('/api/v1/coding/connect', payload),
    
    // Adaptive Practice Engine Endpoints
    getNextAdaptive: (params = {}) => {
      const q = new URLSearchParams(params).toString();
      return this.get(`/api/v1/coding/adaptive/next${q ? `?${q}` : ''}`);
    },
    getAdaptiveQueue: (params = {}) => {
      const q = new URLSearchParams(params).toString();
      return this.get(`/api/v1/coding/adaptive/queue${q ? `?${q}` : ''}`);
    },
    getAdaptiveStats: () => this.get('/api/v1/coding/adaptive/stats'),
  };

  // Interview & Behavioral
  interview = {
    getQuestions: (role, seniority = 'Mid-Level') => this.get(`/api/v1/interview/questions?role=${encodeURIComponent(role)}&seniority=${encodeURIComponent(seniority)}`),
    startSession: (payload) => this.post('/api/v1/interview/start-session', payload),
    submitAnswer: (payload) => this.post('/api/v1/interview/submit-answer', payload),
    getScorecard: (session_id) => this.get(`/api/v1/interview/scorecard/${encodeURIComponent(session_id)}`),
    evaluate: (question, user_answer, role) => this.post('/api/v1/interview/evaluate', { question, user_answer, role }),
    getHistory: () => this.get('/api/v1/interview/history'),
    evaluateSTAR: (payload) => this.post('/api/v1/behavioral/evaluate-star', payload),
    analyzeSpeech: (payload) => this.post('/api/v1/speech/analyze-delivery', payload),
  };

  speech = {
    analyzeSpeech: (payload) => this.post('/api/v1/speech/analyze-delivery', payload),
    analyzeAudio: (formData) => this.post('/api/v1/speech/analyze-audio', formData),
    transcribeAudio: (formData) => this.post('/api/v1/speech/transcribe', formData),
    analyzeInterviewAnswer: (payload) => this.post('/api/v1/speech/analyze-interview-answer', payload),
    getHistory: () => this.get('/api/v1/speech/history'),
    getProgress: () => this.get('/api/v1/speech/progress'),
  };

  mockInterview = {
    start: (payload) => this.post('/api/v1/mock-interview/start', payload),
    getQuestion: (session_id) => this.post(`/api/v1/mock-interview/${session_id}/question`),
    submitAnswer: (session_id, question, user_answer) => this.post(`/api/v1/mock-interview/${session_id}/answer`, { question, user_answer }),
    transcribe: (session_id, formData) => this.post(`/api/v1/mock-interview/${session_id}/transcribe`, formData),
    nextQuestion: (session_id) => this.post(`/api/v1/mock-interview/${session_id}/next`),
    pause: (session_id) => this.post(`/api/v1/mock-interview/${session_id}/pause`),
    resume: (session_id) => this.post(`/api/v1/mock-interview/${session_id}/resume`),
    end: (session_id) => this.post(`/api/v1/mock-interview/${session_id}/end`),
    getSession: (session_id) => this.get(`/api/v1/mock-interview/${session_id}`),
    getHistory: () => this.get('/api/v1/mock-interview/history'),
    getReport: (session_id) => this.get(`/api/v1/mock-interview/${session_id}/report`),
  };

  // Companies
  companies = {
    list: () => this.get('/api/v1/companies/'),
    getDetails: (comp_id) => this.get(`/api/v1/companies/${comp_id}`),
  };

  // Skills & Roadmap
  skills = {
    analyzeGap: (user_skills, target_role) => this.post('/api/v1/skills/analyze-gap', { user_skills, target_role }),
    getRoadmaps: () => this.get('/api/v1/skills/roadmaps'),
    updateProgress: (completed_milestones, progress_percentage) =>
      this.put('/api/v1/skills/progress', { completed_milestones, progress_percentage }),
    getCategories: () => this.get('/api/v1/skills/categories'),
    getRecommendations: () => this.get('/api/v1/skills/recommendations'),

    // Technical Topics Learning Catalog
    getTechnicalTopics: () => this.get('/api/v1/skills/topics'),
    getTechnicalTopicDetail: (topicId) => this.get(`/api/v1/skills/topics/${encodeURIComponent(topicId)}`),
    setTopicResourceProgress: (resourceId, status, topic) => this.post('/api/v1/skills/topics/progress', { resource_id: resourceId, status, topic }),
  };

  // Notifications
  notifications = {
    list: () => this.get('/api/v1/notifications/'),
    markRead: (notif_id) => this.put(`/api/v1/notifications/${notif_id}/read`, {}),
    markAllRead: () => this.put('/api/v1/notifications/read-all', {}),
    delete: (notif_id) => this.delete(`/api/v1/notifications/${notif_id}`),
  };

  // Analytics
  analytics = {
    getSummary: () => this.get('/api/v1/analytics/summary'),
    getAdminBatch: () => this.get('/api/v1/admin/batch-analytics'),
  };

  // Additional Tools
  tools = {
    githubScorer: (username) => this.post('/api/v1/github/score', { username }),
    linkedinOptimizer: (payload) => this.post('/api/v1/linkedin/optimize', payload),
    coverLetter: (payload) => this.post('/api/v1/cover-letter/generate', payload),
    portfolioBuilder: (payload) => this.post('/api/v1/portfolio/generate', payload),
    systemDesign: (payload) => this.post('/api/v1/system-design/evaluate-architecture', payload),
    oaConfig: (company) => this.get(`/api/v1/oa/config?company=${encodeURIComponent(company)}`),
    oaEvaluate: (payload) => this.post('/api/v1/oa/evaluate', payload),
  };
}

export const api = new ApiClient(API_BASE_URL);
export default api;
