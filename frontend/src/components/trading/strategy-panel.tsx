'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { StatusBadge } from '@/components/shared/status-badge';
import { useToast } from '@/components/shared/toast';
import { Loader2, Play } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

const strategies = [
  { name: 'RSI', status: 'active' as const },
  { name: 'EMA Cross', status: 'active' as const },
  { name: 'MACD', status: 'paused' as const },
];

export function StrategyPanel() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const testMutation = useMutation({
    mutationFn: () => apiClient.post('/api/v1/trading/analyze', { symbol: 'BTCUSDT', timeframes: ['15m', '1h', '4h', '1d'] }),
    onSuccess: () => {
      addToast('success', 'Strategy test started');
      queryClient.invalidateQueries({ queryKey: ['trading'] });
    },
    onError: () => addToast('error', 'Strategy test failed'),
  });

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold">Strategies</span>
        <button
          onClick={() => testMutation.mutate()}
          disabled={testMutation.isPending}
          className="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs text-white hover:bg-primary-hover disabled:opacity-70"
        >
          {testMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <Play size={14} />
          Start Strategy Test
        </button>
      </div>
      {strategies.map((strategy) => (
        <div key={strategy.name} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <span className="text-sm">{strategy.name}</span>
          <StatusBadge status={strategy.status === 'active' ? 'success' : 'warning'} label={strategy.status === 'active' ? 'Active' : 'Paused'} />
        </div>
      ))}
    </div>
  );
}
