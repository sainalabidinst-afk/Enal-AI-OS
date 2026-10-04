export const ROUTES = {
  LOGIN: 'Login',
  HOME: 'Home',
  CHAT: 'Chat',
  OBSERVABILITY: 'Observability',
  SETTINGS: 'Settings',
} as const;

export type RootStackParamList = {
  Login: undefined;
  Home: undefined;
  Chat: undefined;
  Observability: undefined;
  Settings: undefined;
};
