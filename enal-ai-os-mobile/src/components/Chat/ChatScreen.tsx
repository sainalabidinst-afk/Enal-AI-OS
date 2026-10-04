import React, { useState, useRef } from 'react';
import { View, FlatList, KeyboardAvoidingView, Platform, Alert } from 'react-native';
import { MessageBubble } from './MessageBubble';
import { InputBar } from './InputBar';
import { useSTT } from '../../hooks/useSTT';
import { useTTS } from '../../hooks/useSTT';
import { apiClient } from '../../api/client';
import { API_ENDPOINTS } from '../../api/endpoints';

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Good morning. I am Jenny, your personal AI assistant. What should we work on today?',
      timestamp: new Date().toISOString(),
    },
  ]);
  const [isSending, setIsSending] = useState(false);
  const flatListRef = useRef<FlatList>(null);
  const { isListening, transcript, startListening, stopListening } = useSTT();
  const { speak } = useTTS();

  const handleSend = async (text: string) => {
    if (!text.trim() || isSending) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsSending(true);

    try {
      const response = await apiClient.post(API_ENDPOINTS.CHAT.SEND, { message: text });
      const content = response.data?.reply ?? response.data?.message ?? 'No response.';

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      speak(content);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          role: 'system',
          content: 'Failed to send message. Please try again.',
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const handleMicPress = async () => {
    if (isListening) {
      stopListening();
    } else {
      try {
        await startListening();
      } catch (error) {
        Alert.alert('Microphone Error', 'Unable to access microphone.');
      }
    }
  };

  React.useEffect(() => {
    if (transcript && transcript !== 'Listening...') {
      handleSend(transcript);
    }
  }, [transcript]);

  return (
    <KeyboardAvoidingView
      className="flex-1 bg-background"
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => <MessageBubble message={item} />}
        contentContainerStyle={{ padding: 16 }}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
      />
      <InputBar
        onSend={handleSend}
        isSending={isSending}
        onMicPress={handleMicPress}
        isListening={isListening}
      />
    </KeyboardAvoidingView>
  );
}
