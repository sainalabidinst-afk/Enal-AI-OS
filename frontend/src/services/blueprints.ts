import { apiClient } from '@/lib/api-client';

export async function createAgentBlueprint(data: Record<string, unknown>) {
  return apiClient.post('/api/v1/blueprints/agent', data);
}

export async function listAgentBlueprints() {
  return apiClient.get('/api/v1/blueprints/agent');
}

export async function getAgentBlueprint(id: string) {
  return apiClient.get(`/api/v1/blueprints/agent/${id}`);
}

export async function updateAgentBlueprint(id: string, data: Record<string, unknown>) {
  return apiClient.put(`/api/v1/blueprints/agent/${id}`, data);
}

export async function deleteAgentBlueprint(id: string) {
  return apiClient.delete(`/api/v1/blueprints/agent/${id}`);
}

export async function createToolBlueprint(data: Record<string, unknown>) {
  return apiClient.post('/api/v1/blueprints/tool', data);
}

export async function listToolBlueprints() {
  return apiClient.get('/api/v1/blueprints/tool');
}
