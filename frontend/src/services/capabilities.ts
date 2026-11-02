import { apiClient } from '@/lib/api-client';

export async function getCapabilities() {
  return apiClient.get('/api/v1/capability-packs');
}

export async function getCapability(id: string) {
  return apiClient.get(`/api/v1/capability-packs/${id}`);
}

export async function executeCapability(id: string, payload: { message: string; workspace_id?: string }) {
  return apiClient.post(`/api/v1/capability-packs/${id}/execute`, payload);
}

export async function getCapabilityLifecycle() {
  return apiClient.get('/api/v1/capabilities/lifecycle');
}
