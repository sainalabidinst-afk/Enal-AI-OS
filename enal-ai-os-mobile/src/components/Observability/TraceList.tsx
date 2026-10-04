import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';

interface Trace {
  id: string;
  timestamp: string;
  service: string;
  duration_ms: number;
  status: string;
}

interface TraceListProps {
  traces: Trace[];
}

export function TraceList({ traces }: TraceListProps) {
  const renderItem = ({ item }: { item: Trace }) => (
    <View className="bg-surface rounded-lg p-3 mb-2 border border-gray-800">
      <View className="flex-row justify-between items-center mb-1">
        <Text className="text-text-primary font-medium text-sm">{item.service}</Text>
        <Text className="text-text-secondary text-xs">{item.duration_ms}ms</Text>
      </View>
      <Text className="text-text-secondary text-xs">{item.status}</Text>
      <Text className="text-text-secondary text-xs opacity-60">
        {new Date(item.timestamp).toLocaleString()}
      </Text>
    </View>
  );

  return (
    <View className="flex-1">
      <Text className="text-text-primary text-lg font-semibold mb-4">Trace Logs</Text>
      <FlatList
        data={traces}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        ListEmptyComponent={<Text className="text-text-secondary text-center py-4">No traces available</Text>}
      />
    </View>
  );
}
