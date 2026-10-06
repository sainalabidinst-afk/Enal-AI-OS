import { apiClient } from '@/lib/api-client';

export async function getADRList() {
  return apiClient.get('/api/v1/governance/adr');
}

export async function getADRDetail(id: string) {
  return apiClient.get(`/api/v1/governance/adr/${id}`);
}

export async function getQualityGates() {
  return apiClient.get('/api/v1/governance/quality-gates');
}

export async function getGovernanceStatus() {
  return apiClient.get('/api/v1/governance/status');
}
