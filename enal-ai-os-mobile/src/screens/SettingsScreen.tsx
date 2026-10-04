import React from 'react';
import { View, Text, Switch, TouchableOpacity } from 'react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { ROUTES, RootStackParamList } from '../navigation/routes';

type SettingsScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Settings'>;
  onLogout?: () => void;
};

export function SettingsScreen({ navigation, onLogout }: SettingsScreenProps) {
  const [notifications, setNotifications] = React.useState(true);
  const [voiceEnabled, setVoiceEnabled] = React.useState(true);

  return (
    <View className="flex-1 bg-background p-4">
      <Text className="text-text-primary text-2xl font-bold mb-4">Settings</Text>

      <View className="bg-surface rounded-lg p-4 mb-4 border border-gray-800">
        <View className="flex-row justify-between items-center mb-4">
          <Text className="text-text-primary text-base">Notifications</Text>
          <Switch value={notifications} onValueChange={setNotifications} />
        </View>
        <View className="flex-row justify-between items-center">
          <Text className="text-text-primary text-base">Voice Enabled</Text>
          <Switch value={voiceEnabled} onValueChange={setVoiceEnabled} />
        </View>
      </View>

      <TouchableOpacity
        onPress={() => {}}
        className="bg-surface rounded-lg p-4 mb-3 border border-gray-800"
      >
        <Text className="text-text-primary text-base">Clear Cache</Text>
      </TouchableOpacity>

      {onLogout && (
        <TouchableOpacity
          onPress={onLogout}
          className="bg-red-900/30 rounded-lg p-4 border border-red-800"
        >
          <Text className="text-red-400 text-center font-semibold">Logout</Text>
        </TouchableOpacity>
      )}
    </View>
  );
}
