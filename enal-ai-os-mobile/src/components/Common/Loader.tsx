import React from 'react';
import { View, ActivityIndicator, Text } from 'react-native';

export function Loader({ message = 'Loading...' }: { message?: string }) {
  return (
    <View className="flex-1 items-center justify-center bg-background">
      <ActivityIndicator size="large" color="#3b82f6" />
      <Text className="text-text-secondary mt-4 text-sm">{message}</Text>
    </View>
  );
}
