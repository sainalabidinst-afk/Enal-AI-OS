import { create } from "zustand";
import type { ConversationThread, AIMessage } from "../context/conversation-types";
import type { CapabilityContext } from "../adapters/capability-adapter.interface";
import type { EvidencePayload } from "../evidence/evidence-types";

interface ConversationState {
  currentThread: ConversationThread | null;
  threads: ConversationThread[];
  isLoading: boolean;
  error: string | null;
  currentCapabilityContext: CapabilityContext | null;
  lastEvidence: EvidencePayload | null;
  setCurrentThread: (thread: ConversationThread | null) => void;
  addMessage: (message: AIMessage) => void;
  updateLastMessage: (message: Partial<AIMessage>) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setCapabilityContext: (context: CapabilityContext) => void;
  setLastEvidence: (evidence: EvidencePayload | null) => void;
}

export const useConversationStore = create<ConversationState>((set, get) => ({
  currentThread: null,
  threads: [],
  isLoading: false,
  error: null,
  currentCapabilityContext: null,
  lastEvidence: null,

  setCurrentThread: (currentThread) => set({ currentThread }),
  addMessage: (message) =>
    set((state) => {
      if (!state.currentThread) return state;

      const updatedThread = {
        ...state.currentThread,
        messages: [...state.currentThread.messages, message],
        updatedAt: Date.now(),
      };

      return {
        currentThread: updatedThread,
        threads: state.threads.map((t) => (t.id === updatedThread.id ? updatedThread : t)),
      };
    }),
  updateLastMessage: (message) =>
    set((state) => {
      if (!state.currentThread || state.currentThread.messages.length === 0) return state;

      const messages = [...state.currentThread.messages];
      messages[messages.length - 1] = { ...messages[messages.length - 1], ...message };

      const updatedThread = { ...state.currentThread, messages, updatedAt: Date.now() };

      return {
        currentThread: updatedThread,
        threads: state.threads.map((t) => (t.id === updatedThread.id ? updatedThread : t)),
      };
    }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  setCapabilityContext: (currentCapabilityContext) => set({ currentCapabilityContext }),
  setLastEvidence: (lastEvidence) => set({ lastEvidence }),
}));

