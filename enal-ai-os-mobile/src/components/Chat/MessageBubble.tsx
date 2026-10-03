import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Message } from '../Chat/ChatScreen';

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  return (
    <View className={`mb-4 ${isUser ? 'items-end' : 'items-start'}`}>
      <View
        className={`max-w-[80%] rounded-lg p-3 ${
          isUser
            ? 'bg-primary'
            : isSystem
            ? 'bg-danger'
            : 'bg-surface border border-gray-800'
        }`}
      >
        <Text className={`text-sm ${isUser ? 'text-white' : 'text-text-primary'}`}>
          {message.content}
        </Text>
        <Text className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-text-secondary'}`}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </Text>
      </View>
    </View>
  );
}
