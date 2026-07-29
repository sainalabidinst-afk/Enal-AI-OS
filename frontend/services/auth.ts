import { api } from './api';
import type { LoginRequest, LoginResponse, AuthUser } from '@/types/auth';

const TOKEN_KEY = 'enal-auth-token';
const USER_KEY = 'enal-auth-user';

export function getStoredToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function getStoredUser(): AuthUser | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function storeAuth(token: string, user: AuthUser): void {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export async function login(request: LoginRequest): Promise<LoginResponse> {
  // Backend expects form-encoded for OAuth2-compatible token endpoint
  const formData = new URLSearchParams();
  formData.append('username', request.username);
  formData.append('password', request.password);

  const url = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/auth/login`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData,
  });

  if (!response.ok) {
    let message = 'Login failed';
    try {
      const error = await response.json();
      message = error.detail || error.message || message;
    } catch {
      // use default
    }
    throw new Error(message);
  }

  return response.json();
}

export async function getCurrentUser(): Promise<AuthUser> {
  return api.get<AuthUser>('/api/v1/auth/me');
}

export async function logout(): Promise<void> {
  try {
    await api.post('/api/v1/auth/logout');
  } catch {
    // Best-effort logout on server side
  }
  clearAuth();
}

