import { apiClient } from '@/lib/api-client';

export async function runBenchmark() {
  return apiClient.post('/api/v1/benchmark/run');
}

export async function getBenchmarkSuite() {
  return apiClient.get('/api/v1/benchmark/suite');
}

export async function getCapabilityScores() {
  return apiClient.get('/api/v1/benchmark/capability-scores');
}

export async function getBenchmarkDashboard() {
  return apiClient.get('/api/v1/benchmark/capability-scores');
}

export async function getBenchmarkHistory() {
  return apiClient.get('/api/v1/benchmark/capability-scores');
}

export async function getCCEStatus() {
  return apiClient.get('/api/v1/benchmark/cce/status');
}
