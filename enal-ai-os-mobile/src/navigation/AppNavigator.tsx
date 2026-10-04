import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { ROUTES, RootStackParamList } from './routes';
import { LoginScreen } from '../screens/LoginScreen';
import { HomeScreen } from '../screens/HomeScreen';
import { ChatScreen } from '../screens/ChatScreen';
import { ObservabilityScreen } from '../screens/ObservabilityScreen';
import { SettingsScreen } from '../screens/SettingsScreen';
import { initAuthToken, getAuthToken, updateAuthToken } from '../api/client';

const Stack = createNativeStackNavigator<RootStackParamList>();

export function AppNavigator() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      await initAuthToken();
      const token = getAuthToken();
      setIsAuthenticated(!!token);
    } catch {
      setIsAuthenticated(false);
    } finally {
      setCheckingAuth(false);
    }
  };

  const handleLoginSuccess = async () => {
    const token = getAuthToken();
    setIsAuthenticated(!!token);
  };

  const handleLogout = async () => {
    await updateAuthToken(null);
    setIsAuthenticated(false);
  };

  if (checkingAuth) {
    return null;
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!isAuthenticated ? (
          <Stack.Screen name={ROUTES.LOGIN}>
            {() => <LoginScreen onLoginSuccess={handleLoginSuccess} />}
          </Stack.Screen>
        ) : (
          <>
            <Stack.Screen name={ROUTES.HOME} options={{ title: 'Enal AI OS', headerShown: true }}>
              {(props) => <HomeScreen {...props} onLogout={handleLogout} />}
            </Stack.Screen>
            <Stack.Screen name={ROUTES.CHAT} component={ChatScreen} options={{ title: 'Chat' }} />
            <Stack.Screen
              name={ROUTES.OBSERVABILITY}
              component={ObservabilityScreen}
              options={{ title: 'Observability' }}
            />
            <Stack.Screen name={ROUTES.SETTINGS} options={{ title: 'Settings', headerShown: true }}>
              {(props) => <SettingsScreen {...props} onLogout={handleLogout} />}
            </Stack.Screen>
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
