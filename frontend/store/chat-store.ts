import { create } from "zustand";
import type { Message, Conversation, StreamEvent } from "@/types";
import { getConversation, deleteConversation as apiDeleteConversation } from "@/services/chat";

interface ChatState {
  conversations: Record<string, Conversation>;
  activeConversationId: string | null;
  isStreaming: boolean;
  error: string | null;
  loadConversation: (conversationId: string) => Promise<void>;
  appendMessage: (conversationId: string, message: Message) => void;
  replaceLastAssistant: (conversationId: string, message: Message) => void;
  setActiveConversation: (conversationId: string | null) => void;
  appendStreamEvent: (conversationId: string, event: StreamEvent) => void;
  setStreaming: (streaming: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
  deleteConversation: (conversationId: string) => Promise<void>;
}

export const useChatStore = create<ChatState>()((set, get) => ({
  conversations: {},
  activeConversationId: null,
  isStreaming: false,
  error: null,

  loadConversation: async (conversationId: string) => {
    const data = await getConversation(conversationId);
    set((state) => ({
      conversations: {
        ...state.conversations,
        [conversationId]: data,
      },
      activeConversationId: conversationId,
    }));
  },

  appendMessage: (conversationId: string, message: Message) => {
    set((state) => {
      const conversation = state.conversations[conversationId] || { conversation_id: conversationId, messages: [] };
      return {
        conversations: {
          ...state.conversations,
          [conversationId]: {
            ...conversation,
            messages: [...conversation.messages, message],
          },
        },
      };
    });
  },

  replaceLastAssistant: (conversationId: string, message: Message) => {
    set((state) => {
      const conversation = state.conversations[conversationId];
      if (!conversation) return state;
      const messages = [...conversation.messages];
      const last = messages[messages.length - 1];
      if (last && last.role === "assistant") {
        messages[messages.length - 1] = message;
      } else {
        messages.push(message);
      }
      return {
        conversations: {
          ...state.conversations,
          [conversationId]: { ...conversation, messages },
        },
      };
    });
  },

  setActiveConversation: (conversationId: string | null) => {
    set({ activeConversationId: conversationId });
  },

  appendStreamEvent: (conversationId: string, event: StreamEvent) => {
    const state = get();
    const conversation = state.conversations[conversationId];
    if (!conversation) return;

    switch (event.type) {
      case "final": {
        const assistantMessage: Message = {
          id: `msg-${Date.now()}`,
          role: "assistant",
          content: event.message,
          timestamp: new Date().toISOString(),
          metadata: {
            domain: event.domain,
            intent: event.intent,
          },
        };
        get().replaceLastAssistant(conversationId, assistantMessage);
        break;
      }
      case "error": {
        const errorMessage: Message = {
          id: `msg-${Date.now()}`,
          role: "assistant",
          content: `Error: ${event.message}`,
          timestamp: new Date().toISOString(),
        };
        get().replaceLastAssistant(conversationId, errorMessage);
        set({ error: event.message, isStreaming: false });
        break;
      }
      case "execution_started":
      case "phase":
      case "progress":
      case "artifact":
      case "log":
      case "execution_complete":
      default:
        break;
    }
  },

  setStreaming: (streaming: boolean) => set({ isStreaming: streaming }),
  setError: (error: string | null) => set({ error }),
  clearError: () => set({ error: null }),

  deleteConversation: async (conversationId: string) => {
    await apiDeleteConversation(conversationId);
    set((state) => {
      const newConversations = { ...state.conversations };
      delete newConversations[conversationId];
      return {
        conversations: newConversations,
        activeConversationId: state.activeConversationId === conversationId ? null : state.activeConversationId,
      };
    });
  },
}));
