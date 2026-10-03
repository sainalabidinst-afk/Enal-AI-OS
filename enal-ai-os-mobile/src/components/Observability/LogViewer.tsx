import React from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';

interface Log {
  id: string;
  timestamp: string;
  level: 'info' | 'warn' | 'error' | 'debug';
  message: string;
}

interface LogViewerProps {
  logs: Log[];
}

export function LogViewer({ logs }: LogViewerProps) {
  const levelColors = {
    info: 'text-blue-400',
    warn: 'text-yellow-400',
    error: 'text-red-400',
    debug: 'text-gray-400',
  };

  return (
    <View className="flex-1">
      <Text className="text-text-primary text-lg font-semibold mb-4">Logs</Text>
      <ScrollView className="flex-1 bg-background rounded-lg p-3">
        {logs.map((log) => (
          <View key={log.id} className="mb-2">
            <Text className={`text-xs ${levelColors[log.level]}`}>
              [{log.level.toUpperCase()}] {new Date(log.timestamp).toLocaleString()}
            </Text>
            <Text className="text-text-secondary text-xs">{log.message}</Text>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}
