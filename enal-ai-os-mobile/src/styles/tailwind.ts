import { StyleSheet } from 'react-native';

export const colors = {
  primary: '#3b82f6',
  secondary: '#10b981',
  danger: '#ef4444',
  warning: '#f59e0b',
  success: '#22c55e',
  background: '#0a0a0a',
  surface: '#171717',
  text: {
    primary: '#f3f4f6',
    secondary: '#9ca3af',
  },
};

export const globalStyles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
});
