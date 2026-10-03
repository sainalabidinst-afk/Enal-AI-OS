import AsyncStorage from '@react-native-async-storage/async-storage';

const TOKEN_KEY = 'enal-auth-token';
const USER_KEY = 'enal-auth-user';

export async function getToken(): Promise<string | null> {
  try {
    return await AsyncStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export async function setToken(token: string): Promise<void> {
  await AsyncStorage.setItem(TOKEN_KEY, token);
}

export async function removeToken(): Promise<void> {
  await AsyncStorage.removeItem(TOKEN_KEY);
}

export async function getUser<T>(): Promise<T | null> {
  try {
    const raw = await AsyncStorage.getItem(USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export async function setUser<T>(user: T): Promise<void> {
  await AsyncStorage.setItem(USER_KEY, JSON.stringify(user));
}

export async function removeUser(): Promise<void> {
  await AsyncStorage.removeItem(USER_KEY);
}

export async function clearAll(): Promise<void> {
  await AsyncStorage.multiRemove([TOKEN_KEY, USER_KEY]);
}
