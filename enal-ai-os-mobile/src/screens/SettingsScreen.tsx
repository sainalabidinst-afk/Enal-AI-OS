import React from 'react';
import { View, Text, Switch } from 'react-native';
import { Button } from '../components/Common/Button';

export function SettingsScreen() {
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

      <Button title="Clear Cache" onPress={() => {}} variant="secondary" />
    </View>
  );
}
