'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { cn } from '@/lib/cn';
import { useToast } from '@/components/shared/toast';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { Loader2 } from 'lucide-react';

export function BacktestingModule({ symbol = 'BTCUSDT' }: { symbol?: string }) {
  const [capital, setCapital] = useState('10000');
  const [start, setStart] = useState('2026-01-01');
  const [end, setEnd] = useState('2026-10-06');
  const { addToast } = useToast();

  const mutation = useMutation({
    mutationFn: async () => {
      const response = await apiClient.post('/api/v1/trading/analyze', {
        symbol,
        timeframes: ['15m', '1h', '4h', '1d'],
      });
      return response;
    },
    onSuccess: () => addToast('success', 'Backtest completed'),
    onError: () => addToast('error', 'Backtest failed'),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate();
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 space-y-4 rounded-lg border border-border bg-surface-secondary p-4">
      <h3 className="text-sm font-semibold">Backtest Configuration</h3>
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className="block text-sm font-medium">Initial Capital</label>
          <input
            type="number"
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={capital}
            onChange={(e) => setCapital(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Symbol</label>
          <input
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={symbol}
            disabled
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Start Date</label>
          <input
            type="date"
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={start}
            onChange={(e) => setStart(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium">End Date</label>
          <input
            type="date"
            className="mt-1 w-full rounded-md border border-border bg-surface-primary px-3 py-2 text-sm outline-none focus:border-primary"
            value={end}
            onChange={(e) => setEnd(e.target.value)}
            required
          />
        </div>
      </div>
      <div className="flex items-center justify-between">
        <p className="text-xs text-text-secondary">Results include equity curve and trade list.</p>
        <button
          type="submit"
          disabled={mutation.isPending}
          className={cn('flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm text-white hover:bg-primary-hover disabled:opacity-70')}
        >
          {mutation.isPending && <Loader2 size={14} className="animate-spin" />}
          {mutation.isPending ? 'Running...' : 'Run Backtest'}
        </button>
      </div>
      {mutation.isPending && <LoadingSkeleton className="h-48 w-full" />}
    </form>
  );
}
