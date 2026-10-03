import React from 'react';
import { View, Text, FlatList } from 'react-native';
import { TraceList } from '../components/Observability/TraceList';
import { LogViewer } from '../components/Observability/LogViewer';

const MOCK_TRACES = [
  {
    id: '1',
    timestamp: new Date().toISOString(),
    service: 'chat',
    duration_ms: 120,
    status: 'success',
  },
  {
    id: '2',
    timestamp: new Date().toISOString(),
    service: 'voice',
    duration_ms: 350,
    status: 'success',
  },
];

const MOCK_LOGS = [
  { id: '1', timestamp: new Date().toISOString(), level: 'info' as const, message: 'App started' },
  { id: '2', timestamp: new Date().toISOString(), level: 'info' as const, message: 'Backend connected' },
];

export function ObservabilityScreen() {
  return (
    <View className="flex-1 bg-background p-4">
      <Text className="text-text-primary text-2xl font-bold mb-4">Observability</Text>
      <TraceList traces={MOCK_TRACES} />
      <LogViewer logs={MOCK_LOGS} />
    </View>
  );
}
