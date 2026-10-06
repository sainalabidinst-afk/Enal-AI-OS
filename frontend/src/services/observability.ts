import { apiClient } from '@/lib/api-client';

export async function getAllMetrics() {
  return apiClient.get('/api/v1/metrics');
}

export async function getMetricsByDomain(domain: string) {
  return apiClient.get(`/api/v1/metrics/${domain}`);
}

export async function getAlerts() {
  return apiClient.get('/api/v1/metrics/alerts');
}

export async function getPrometheusMetrics() {
  return apiClient.get('/api/v1/metrics/prometheus', { responseType: 'text' });
}
