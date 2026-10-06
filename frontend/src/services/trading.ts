import { apiClient } from '@/lib/api-client';

export async function analyzeMarket(symbol: string, timeframes?: string[]) {
  return apiClient.post('/api/v1/trading/analyze', { symbol, timeframes });
}

export async function getLiveRegime(symbol: string, lookback = 20) {
  return apiClient.get('/api/v1/trading/regime/live', { params: { symbol, lookback } });
}

export async function startLiveFeed(symbol: string, timeframes?: string[]) {
  return apiClient.post('/api/v1/trading/feed/start', { symbol, timeframes });
}

export async function stopLiveFeed() {
  return apiClient.post('/api/v1/trading/feed/stop');
}

export function getFeedStreamUrl(symbol: string, interval = 5, lookback = 20) {
  return `/api/v1/trading/feed/stream?symbol=${encodeURIComponent(symbol)}&interval=${interval}&lookback=${lookback}`;
}
