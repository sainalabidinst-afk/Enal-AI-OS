import { apiClient } from '@/lib/api-client';

export async function sendChatMessage(message: string, conversationId?: string, workspaceId?: string) {
  return apiClient.post('/api/v1/chat', { message, conversationId, workspaceId });
}

export function getChatStreamUrl(message: string, conversationId?: string, workspaceId?: string) {
  const url = new URL('/api/v1/chat/stream', apiClient['baseUrl']);
  url.searchParams.set('message', message);
  if (conversationId) url.searchParams.set('conversationId', conversationId);
  if (workspaceId) url.searchParams.set('workspaceId', workspaceId);
  return url.toString();
}

export async function getConversation(conversationId: string) {
  return apiClient.get(`/api/v1/conversations/${conversationId}`);
}

export async function deleteConversation(conversationId: string) {
  return apiClient.delete(`/api/v1/conversations/${conversationId}`);
}
