import React, { useState } from 'react';
import { View, TextInput, TouchableOpacity, Text } from 'react-native';

interface InputBarProps {
  onSend: (text: string) => void;
  isSending: boolean;
}

export function InputBar({ onSend, isSending }: InputBarProps) {
  const [text, setText] = useState('');

  const handleSend = () => {
    if (text.trim()) {
      onSend(text);
      setText('');
    }
  };

  return (
    <View className="border-t border-gray-800 bg-surface p-3">
      <View className="flex-row items-center gap-2">
        <TextInput
          value={text}
          onChangeText={setText}
          placeholder="Message Jenny..."
          placeholderTextColor="#9ca3af"
          className="flex-1 rounded-lg border border-gray-700 bg-background px-3 py-2 text-text-primary text-sm"
          onSubmitEditing={handleSend}
          returnKeyType="send"
        />
        <TouchableOpacity
          onPress={handleSend}
          disabled={!text.trim() || isSending}
          className="bg-primary rounded-lg p-2 opacity-80"
        >
          <Text className="text-white font-bold">➤</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}
