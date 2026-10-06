import { apiClient } from '@/lib/api-client';

export async function getProviders() {
  return apiClient.get('/api/v1/models/providers');
}

export async function getProviderHealth(provider?: string) {
  return apiClient.get('/api/v1/models/health', { params: provider ? { provider } : undefined });
}

export async function routeModel(taskType: string, capability: string, context?: Record<string, unknown>) {
  return apiClient.post('/api/v1/models/route', { taskType, capability, context });
}

export async function getMarketplaceListings() {
  return apiClient.get('/api/v1/marketplace');
}

export async function cloneAgent(agentId: string, targetProject = 'default') {
  return apiClient.post('/api/v1/marketplace/clone', { agent_id: agentId, target_project: targetProject });
}
