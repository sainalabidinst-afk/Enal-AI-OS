import { apiClient } from '@/lib/api-client';

export async function getPacks(status?: string) {
  return apiClient.get('/api/v1/packs', { params: status ? { status } : undefined });
}

export async function getPack(packId: string) {
  return apiClient.get(`/api/v1/packs/${packId}`);
}

export async function registerPack(payload: Record<string, unknown>) {
  return apiClient.post('/api/v1/packs', payload);
}

export async function getAuditTrail(packId?: string) {
  return apiClient.get('/api/v1/audit', { params: packId ? { pack_id: packId } : undefined });
}

export async function getGovernanceStatus() {
  return apiClient.get('/api/v1/packs');
}
