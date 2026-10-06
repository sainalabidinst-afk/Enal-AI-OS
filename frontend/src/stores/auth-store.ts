'use client';

import { create } from 'zustand';
import { apiClient } from '@/lib/api-client';
import { login as loginService } from '@/services/auth';

export interface User {
  username: string;
  roles: string[];
  permissions: string[];
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: typeof window !== 'undefined' ? localStorage.getItem('access_token') : null,
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (username: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await loginService(username, password);

      const token = response.access_token;
      apiClient.setToken(token);

      const user = await apiClient.get<User>('/api/v1/auth/me');

      set({
        user,
        token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Login failed';
      set({ error: message, isLoading: false, isAuthenticated: false, user: null, token: null });
      apiClient.setToken(null);
      throw error;
    }
  },

  logout: () => {
    apiClient.setToken(null);
    set({ user: null, token: null, isAuthenticated: false, error: null });
  },

  fetchMe: async () => {
    set({ isLoading: true });
    try {
      const user = await apiClient.get<User>('/api/v1/auth/me');
      set({ user, isAuthenticated: true, isLoading: false });
    } catch {
      set({ isLoading: false, isAuthenticated: false, user: null });
    }
  },
}));
