import { apiClient } from '@/lib/api-client';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthUser {
  username: string;
  roles: string[];
  permissions: string[];
}

export async function login(username: string, password: string) {
  return apiClient.post<LoginResponse>('/api/v1/auth/login', { username, password });
}

export async function getMe() {
  return apiClient.get<AuthUser>('/api/v1/auth/me');
}

export async function logout() {
  return apiClient.post('/api/v1/auth/logout');
}
