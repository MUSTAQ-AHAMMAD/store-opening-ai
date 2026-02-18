export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
  },
  STORES: {
    LIST: '/stores',
    CREATE: '/stores',
    GET: (id: number) => `/stores/${id}`,
    UPDATE: (id: number) => `/stores/${id}`,
    DELETE: (id: number) => `/stores/${id}`,
  },
  TEAM: {
    LIST: '/team',
    CREATE: '/team',
    DELETE: (id: number) => `/team/${id}`,
  },
  CHECKLISTS: {
    LIST: '/checklists',
    CREATE: '/checklists',
    TASKS: (id: number) => `/checklists/${id}/tasks`,
  },
  ANALYTICS: {
    DASHBOARD: '/analytics/dashboard',
    STORE_PROGRESS: (id: number) => `/analytics/store/${id}/progress`,
  },
  AI: {
    PREDICT_COMPLETION: (id: number) => `/ai/predict/completion-date/${id}`,
    TASK_PRIORITIZATION: (id: number) => `/ai/store/${id}/task-prioritization`,
    INSIGHTS: '/ai/insights/dashboard',
  },
  WHATSAPP: {
    GROUPS: '/whatsapp/groups',
    CREATE_GROUP: '/whatsapp/groups',
    ARCHIVE: (id: number) => `/whatsapp/groups/${id}/archive`,
  },
  WORKFLOW: {
    STAGES: (id: number) => `/workflow/store/${id}/stages`,
    ADVANCE: (id: number) => `/workflow/store/${id}/advance`,
  },
  ML: {
    PREDICTIONS: (id: number) => `/ml/store/${id}/predictions`,
    RISK_ASSESSMENT: (id: number) => `/ml/store/${id}/risk-assessment`,
  },
};
