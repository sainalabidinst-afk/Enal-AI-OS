import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { ROUTES, RootStackParamList } from './routes';
import { HomeScreen } from '../screens/HomeScreen';
import { ChatScreen } from '../screens/ChatScreen';
import { ObservabilityScreen } from '../screens/ObservabilityScreen';
import { SettingsScreen } from '../screens/SettingsScreen';

const Stack = createNativeStackNavigator<RootStackParamList>();

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName={ROUTES.HOME}>
        <Stack.Screen name={ROUTES.HOME} component={HomeScreen} options={{ title: 'Enal AI OS' }} />
        <Stack.Screen name={ROUTES.CHAT} component={ChatScreen} options={{ title: 'Chat' }} />
        <Stack.Screen
          name={ROUTES.OBSERVABILITY}
          component={ObservabilityScreen}
          options={{ title: 'Observability' }}
        />
        <Stack.Screen name={ROUTES.SETTINGS} component={SettingsScreen} options={{ title: 'Settings' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
