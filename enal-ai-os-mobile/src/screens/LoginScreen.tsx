import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, Alert } from 'react-native';
import { apiClient, updateAuthToken, initAuthToken, getAuthToken } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

interface LoginScreenProps {
  onLoginSuccess: () => void;
}

export function LoginScreen({ onLoginSuccess }: LoginScreenProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    initAuthToken();
  }, []);

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      Alert.alert('Error', 'Please enter both username and password');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const token = response.data?.access_token;
      if (token) {
        await updateAuthToken(token);
        onLoginSuccess();
      } else {
        Alert.alert('Error', 'Login failed. Please try again.');
      }
    } catch (error: any) {
      Alert.alert('Login Failed', error?.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="flex-1 bg-background p-6 justify-center">
      <Text className="text-text-primary text-3xl font-bold mb-2">Enal AI OS</Text>
      <Text className="text-text-secondary text-sm mb-8">Mobile Beta v3.2.0</Text>

      <View className="bg-surface rounded-lg p-6 border border-gray-800">
        <Text className="text-text-primary text-lg font-semibold mb-4">Sign In</Text>

        <TextInput
          value={username}
          onChangeText={setUsername}
          placeholder="Username"
          placeholderTextColor="#9ca3af"
          autoCapitalize="none"
          className="bg-background rounded-lg border border-gray-700 px-4 py-3 text-text-primary text-sm mb-3"
        />

        <TextInput
          value={password}
          onChangeText={setPassword}
          placeholder="Password"
          placeholderTextColor="#9ca3af"
          secureTextEntry
          className="bg-background rounded-lg border border-gray-700 px-4 py-3 text-text-primary text-sm mb-4"
        />

        <TouchableOpacity
          onPress={handleLogin}
          disabled={loading}
          className={`rounded-lg p-4 ${loading ? 'bg-gray-600' : 'bg-primary'}`}
        >
          <Text className="text-white text-center font-semibold">
            {loading ? 'Signing in...' : 'Sign In'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
