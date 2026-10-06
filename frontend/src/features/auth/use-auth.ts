'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { login, getMe, logout } from '@/services/auth';
import { useAuthStore } from '@/stores/auth-store';

export function useAuth() {
  const { user, isAuthenticated, isLoading, error, login: loginStore, logout: logoutStore, fetchMe } = useAuthStore();

  const loginMutation = useMutation({
    mutationFn: ({ username, password }: { username: string; password: string }) => login(username, password),
    onSuccess: (_, { username, password }) => {
      loginStore(username, password);
    },
    onError: () => {
      // error handled by store
    },
  });

  const logoutMutation = useMutation({
    mutationFn: () => logout(),
    onSuccess: () => {
      logoutStore();
    },
  });

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login: loginMutation.mutate,
    logout: logoutMutation.mutate,
    fetchMe,
  };
}
