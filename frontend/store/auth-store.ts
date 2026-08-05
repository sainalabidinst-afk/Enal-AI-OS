import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { AuthUser, AuthState } from '@/types/auth';
import type { LoginRequest } from '@/types/auth';
import {
  login as apiLogin,
  logout as apiLogout,
  getCurrentUser,
  getStoredToken,
  getStoredUser,
  storeAuth,
  clearAuth,
} from '@/services/auth';

interface AuthActions {
  login: (request: LoginRequest) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<boolean>;
  initialize: () => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState & AuthActions>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      initialize: () => {
        const token = getStoredToken();
        const user = getStoredUser();
        if (token && user) {
          set({ token, user, isAuthenticated: true });
        }
      },

login: async (request: LoginRequest) => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiLogin(request);
          const token = response.access_token;

          // Persist the token to localStorage immediately so that any
          // subsequent API calls (e.g. /me) carry the Authorization header.
          // This prevents the 401 hard-redirect in services/api.ts from firing
          // and causing a login loop.
          const user: AuthUser = { username: request.username };
          storeAuth(token, user);
          set({ token, user });

          // Try to enrich the user from the backend, but never fail the login
          // if the backend is unreachable or /me is not available.
          try {
            const currentUser = await getCurrentUser();
            storeAuth(token, currentUser);
            set({ user: currentUser });
          } catch {
            // Fall back to basic user from login (already stored).
          }

          set({
            token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          clearAuth();
          set({
            token: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: error instanceof Error ? error.message : 'Login failed',
          });
          throw error;
        }
      },

      logout: async () => {
        try {
          await apiLogout();
        } catch {
          // Best-effort
        }
        clearAuth();
        set({
          token: null,
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        });
      },

      checkAuth: async () => {
        const { token } = get();
        if (!token) {
          set({ isAuthenticated: false, user: null });
          return false;
        }

        try {
          const user = await getCurrentUser();
          set({ user, isAuthenticated: true });
          return true;
        } catch {
          clearAuth();
          set({ isAuthenticated: false, user: null, token: null });
          return false;
        }
      },

      setError: (error: string | null) => set({ error }),
      clearError: () => set({ error: null }),
    }),
    {
      name: 'enal-auth-storage',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

