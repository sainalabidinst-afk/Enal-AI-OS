export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatRequest {
  message: string;
  conversationId?: string;
  workspaceId?: string;
}

export interface ChatResponse {
  message: string;
  conversationId: string;
  domain?: string;
  intent?: string;
}
