export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    ME: '/auth/me',
    LOGOUT: '/auth/logout',
  },
  CHAT: {
    SEND: '/chat',
    CONVERSATIONS: '/conversations',
    STREAM: '/chat/stream',
  },
  VOICE: {
    TRANSCRIBE: '/voice/transcribe',
    SPEAK: '/voice/speak',
    PROVIDERS: '/voice/providers',
  },
  CONSENT: {
    PENDING: '/consent/pending',
    APPROVE: '/consent/approve',
    DENY: '/consent/deny',
  },
  WORKSPACE: {
    LIST: '/workspaces',
    GET: '/workspaces/:id',
  },
  OBSERVABILITY: {
    LOGS: '/observability/logs',
    TRACE: '/observability/trace',
  },
} as const;

export default API_ENDPOINTS;
