import { apiClient } from '@/lib/api-client';

export async function startSTT() {
  return apiClient.post('/api/v1/voice/stt/start');
}

export async function sendTranscript(text: string) {
  return apiClient.post('/api/v1/voice/transcript', { text });
}

export async function getVoiceContext() {
  return apiClient.get('/api/v1/voice/providers');
}

export async function updateVoiceContext(context: Record<string, unknown>) {
  return apiClient.post('/api/v1/voice/providers', context);
}
