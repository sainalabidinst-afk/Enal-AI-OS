import { apiClient } from '@/lib/api-client';

export async function getTelemetryMetrics() {
  return apiClient.get('/api/v1/metrics');
}

export async function getParserMetrics() {
  return apiClient.get('/api/v1/metrics/parser');
}

export async function getReasoningMetrics() {
  return apiClient.get('/api/v1/metrics/reasoning');
}

export async function getTradingMetrics() {
  return apiClient.get('/api/v1/metrics/trading');
}

export async function getCrossPackMetrics() {
  return apiClient.get('/api/v1/metrics/cross-pack');
}
