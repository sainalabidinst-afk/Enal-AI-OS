import { api } from "./api";
import type { ChatRequest, ChatResponse, Conversation } from "@/types/chat";

export async function sendChat(request: ChatRequest): Promise<ChatResponse> {
  return api.post<ChatResponse>("/api/v1/chat", request);
}

export async function getConversation(conversationId: string): Promise<Conversation> {
  return api.get<Conversation>(`/api/v1/conversations/${conversationId}`);
}

export async function deleteConversation(conversationId: string): Promise<{ deleted: boolean }> {
  return api.delete<{ deleted: boolean }>(`/api/v1/conversations/${conversationId}`);
}
