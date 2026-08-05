import { create } from "zustand";
import type { WorkspaceMemory } from "../memory/memory-types";
import type { ConversationThread } from "../context/conversation-types";

interface MemoryState {
  memories: Map<string, WorkspaceMemory>;
  getMemory: (workspaceId: string, capabilityId: string) => WorkspaceMemory | undefined;
  updateMemory: (workspaceId: string, capabilityId: string, updates: Partial<WorkspaceMemory>) => void;
  addThread: (workspaceId: string, capabilityId: string, thread: ConversationThread) => void;
}

export const useMemoryStore = create<MemoryState>((set, get) => ({
  memories: new Map(),

  getMemory: (workspaceId, capabilityId) => {
    const key = `${workspaceId}:${capabilityId}`;
    return get().memories.get(key);
  },

  updateMemory: (workspaceId, capabilityId, updates) => {
    const key = `${workspaceId}:${capabilityId}`;
    set((state) => {
      const memories = new Map(state.memories);
      const existing = memories.get(key) || {
        workspaceId,
        capabilityId,
        conversationHistory: [],
        preferences: {},
      };
      memories.set(key, { ...existing, ...updates });
      return { memories };
    });
  },

  addThread: (workspaceId, capabilityId, thread) => {
    const key = `${workspaceId}:${capabilityId}`;
    set((state) => {
      const memories = new Map(state.memories);
      const existing = memories.get(key) || {
        workspaceId,
        capabilityId,
        conversationHistory: [],
        preferences: {},
      };
      memories.set(key, {
        ...existing,
        conversationHistory: [...existing.conversationHistory, thread],
      });
      return { memories };
    });
  },
}));

