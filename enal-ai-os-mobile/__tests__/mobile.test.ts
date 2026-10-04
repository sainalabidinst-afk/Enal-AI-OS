import { ROUTES } from '../src/navigation/routes';
import { ENDPOINTS } from '../src/api/endpoints';

describe('Enal AI OS Mobile App Test Suite', () => {
  describe('Navigation Routes', () => {
    it('defines correct screen routes', () => {
      expect(ROUTES.LOGIN).toBe('Login');
      expect(ROUTES.HOME).toBe('Home');
      expect(ROUTES.CHAT).toBe('Chat');
      expect(ROUTES.OBSERVABILITY).toBe('Observability');
      expect(ROUTES.SETTINGS).toBe('Settings');
    });
  });

  describe('API Endpoints', () => {
    it('defines valid endpoint URIs', () => {
      expect(ENDPOINTS.AUTH.LOGIN).toBe('/api/v1/auth/token');
      expect(ENDPOINTS.CHAT.SEND).toBe('/api/v1/chat');
      expect(ENDPOINTS.OBSERVABILITY.LOGS).toBe('/api/v1/observability/logs');
      expect(ENDPOINTS.OBSERVABILITY.TRACES).toBe('/api/v1/observability/traces');
    });
  });
});
