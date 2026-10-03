import React, { useState, useRef } from 'react';
import { View, Text, FlatList, KeyboardAvoidingView, Platform } from 'react-native';
import { MessageBubble } from './MessageBubble';
import { InputBar } from './InputBar';

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
      // TODO: Replace with actual API call
      // const response = await apiClient.post('/chat', { message: text });
      
      // Simulated response for now
      await new Promise((resolve) => setTimeout(resolve, 1000));
      
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: `I received: "${text}". This is a demo response.`,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
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
      <InputBar onSend={handleSend} isSending={isSending} />
    </KeyboardAvoidingView>
  );
}
