'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { MarketChart } from '@/components/trading/market-chart';

export function MarketFeedWidget({ symbol = 'BTCUSDT' }: { symbol?: string }) {
  const { data, isLoading } = useQuery({
    queryKey: ['trading', 'analysis', symbol],
    queryFn: () => apiClient.post('/api/v1/trading/analyze', { symbol, timeframes: ['15m', '1h', '4h', '1d'] }),
  });

  if (isLoading) return <div className="mt-4 h-64 w-full animate-pulse rounded-md bg-surface-tertiary" />;

  return (
    <div className="mt-4">
      <MarketChart symbol={symbol} data={data} />
    </div>
  );
}
