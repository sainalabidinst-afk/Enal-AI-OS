'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { MarketChart } from '@/components/trading/market-chart';
import { useToast } from '@/components/shared/toast';
import { Loader2, Play } from 'lucide-react';

export function MarketFeedWidget({ symbol = 'BTCUSDT' }: { symbol?: string }) {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery({
    queryKey: ['trading', 'analysis', symbol],
    queryFn: () => apiClient.post<{ success: boolean; data?: Record<string, unknown>; error?: string }>('/api/v1/trading/analyze', { symbol, timeframes: ['15m', '1h', '4h', '1d'] }),
  });

  const tradeMutation = useMutation({
    mutationFn: () => apiClient.post('/api/v1/trading/analyze', { symbol, timeframes: ['15m', '1h', '4h', '1d'] }),
    onSuccess: () => {
      addToast('success', 'Trade simulation executed');
      queryClient.invalidateQueries({ queryKey: ['trading'] });
    },
    onError: () => addToast('error', 'Trade simulation failed'),
  });

  if (isLoading) return <div className="mt-4 h-64 w-full animate-pulse rounded-md bg-surface-tertiary" />;

  const inner = data?.data as { confidence?: number; timeframes?: string[]; regimes?: Record<string, { regime?: string; confidence?: number }> } | undefined;

  return (
    <div className="mt-4 space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs text-text-secondary">Symbol: {symbol}</p>
          <p className="text-xs text-text-secondary">Confidence trend streamed from trading module.</p>
        </div>
        <button
          onClick={() => tradeMutation.mutate()}
          disabled={tradeMutation.isPending}
          className="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs text-white hover:bg-primary-hover disabled:opacity-70"
        >
          {tradeMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <Play size={14} />
          Execute Trade Simulation
        </button>
      </div>
      <MarketChart symbol={symbol} data={inner} />
    </div>
  );
}
