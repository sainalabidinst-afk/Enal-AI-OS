export interface ChatRequest {
  message: string;
  conversation_id?: string;
  workspace_id?: string;
  stream?: boolean;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  agent: string;
  tasks_completed: number;
  metadata: Record<string, any>;
}

export interface Message {
  id?: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
  agent?: string;
  metadata?: Record<string, any>;
}

export interface Conversation {
  conversation_id: string;
  messages: Message[];
}
