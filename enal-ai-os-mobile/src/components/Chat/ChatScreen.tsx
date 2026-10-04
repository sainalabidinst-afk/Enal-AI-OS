import React, { useState, useRef, useEffect } from 'react';
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
  const [conversationId, setConversationId] = useState<string | null>(null);
  const { isListening, transcript, startListening, stopListening } = useSTT();
  const { speak } = useTTS();

  useEffect(() => {
    if (transcript && transcript !== 'Listening...') {
      handleSend(transcript);
    }
  }, [transcript]);

  const handleSend = async (text: string) => {
    if (!text.trim() || isSending) return;

    const trimmedText = text.trim();
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: trimmedText,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsSending(true);

    try {
      const payload: any = { message: trimmedText };
      if (conversationId) {
        payload.conversation_id = conversationId;
      }

      const response = await apiClient.post(API_ENDPOINTS.CHAT.SEND, payload);
      const data = response.data || {};
      const content = data.message || data.reply || 'No response.';
      const newConversationId = data.conversation_id || conversationId;

      if (newConversationId && !conversationId) {
        setConversationId(newConversationId);
      }

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      speak(content);
    } catch (error: any) {
      const detail = error?.response?.data?.detail || 'Failed to send message. Please try again.';
      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          role: 'system',
          content: detail,
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
