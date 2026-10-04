import axios from 'axios';
import Constants from 'expo-constants';
import { getToken, setToken, removeToken } from '../utils/storage';

const extraApiUrl =
  (Constants?.expoConfig?.extra as any)?.apiUrl ||
  process.env.EXPO_PUBLIC_API_URL ||
  'http://localhost:8000/api/v1';

const API_BASE_URL = extraApiUrl.replace(/\/$/, '');

let currentToken: string | null = null;

export async function initAuthToken() {
  currentToken = await getToken();
}

export function getAuthToken() {
  return currentToken;
}

export async function updateAuthToken(token: string | null) {
  currentToken = token;
  if (token) {
    await setToken(token);
  } else {
    await removeToken();
  }
}

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    if (currentToken) {
      config.headers.Authorization = `Bearer ${currentToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      currentToken = await getToken();
      if (currentToken) {
        originalRequest.headers.Authorization = `Bearer ${currentToken}`;
        return apiClient(originalRequest);
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
