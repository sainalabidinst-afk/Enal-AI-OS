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

          // Try to get user info
          let user: AuthUser = { username: request.username };
          try {
            // Temporarily set token for API calls
            const prevToken = get().token;
            set({ token });
            user = await getCurrentUser();
          } catch {
            // Fall back to basic user from login
          }

          storeAuth(token, user);
          set({
            token,
            user,
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

