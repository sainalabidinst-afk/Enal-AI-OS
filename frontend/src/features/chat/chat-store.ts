'use client';

import { create } from 'zustand';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface ChatState {
  messages: ChatMessage[];
  conversationId: string | null;
  isStreaming: boolean;
  addMessage: (message: ChatMessage) => void;
  setConversationId: (conversationId: string | null) => void;
  setStreaming: (streaming: boolean) => void;
  reset: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  conversationId: null,
  isStreaming: false,
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setConversationId: (conversationId) => set({ conversationId }),
  setStreaming: (isStreaming) => set({ isStreaming }),
  reset: () => set({ messages: [], conversationId: null, isStreaming: false }),
}));
