import type { ConversationThread } from "../context/conversation-types";

export interface WorkspaceMemory {
  workspaceId: string;
  capabilityId: string;
  lastSymbol?: string;
  lastTimeframe?: string;
  pinnedAnalysis?: string;
  conversationHistory: ConversationThread[];
  preferences: Record<string, unknown>;
}
