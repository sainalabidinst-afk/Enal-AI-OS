export const ROUTES = {
  HOME: 'Home',
  CHAT: 'Chat',
  OBSERVABILITY: 'Observability',
  SETTINGS: 'Settings',
} as const;

export type RootStackParamList = {
  Home: undefined;
  Chat: undefined;
  Observability: undefined;
  Settings: undefined;
};
