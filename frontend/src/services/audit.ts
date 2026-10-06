import { apiClient } from '@/lib/api-client';

export async function getAuditTrail(filters?: { pack_id?: string; user?: string; date_range?: string }) {
  return apiClient.get('/api/v1/audit', { params: filters });
}

export async function getPackProgression(packId: string) {
  return apiClient.get(`/api/v1/packs/${packId}`);
}

export async function getChangelog() {
  return apiClient.get('/api/v1/audit');
}
