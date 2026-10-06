import { apiClient } from '@/lib/api-client';

export async function getADRList() {
  return apiClient.get('/api/v1/packs');
}

export async function getADRDetail(id: string) {
  return apiClient.get(`/api/v1/packs/${id}`);
}

export async function getQualityGates() {
  return apiClient.get('/api/v1/packs');
}

export async function getGovernanceStatus() {
  return apiClient.get('/api/v1/packs');
}
