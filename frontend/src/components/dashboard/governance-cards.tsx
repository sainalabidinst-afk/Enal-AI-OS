'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { MetricsCard } from '@/components/shared/metrics-card';
import { apiClient } from '@/lib/api-client';
import { useToast } from '@/components/shared/toast';
import { Loader2, RefreshCw } from 'lucide-react';

interface PlatformMetrics {
  analysis?: {
    total_analyses?: number;
  };
  chat?: {
    total_messages?: number;
    avg_latency_ms?: number;
  };
  parser?: {
    success_rate?: number;
  };
}

export function GovernanceCards() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading, isError } = useQuery<PlatformMetrics>({
    queryKey: ['metrics'],
    queryFn: () => apiClient.get('/api/v1/metrics'),
  });

  const refreshMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/metrics'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['metrics'] });
      addToast('success', 'Metrics refreshed');
    },
    onError: () => addToast('error', 'Failed to refresh metrics'),
  });

  const formatNumber = (value?: number) =>
    typeof value === 'number' ? value.toLocaleString() : '—';

  const formatPercent = (value?: number) =>
    typeof value === 'number' ? `${(value * 100).toFixed(0)}%` : '—';

  return (
    <section aria-label="Platform metrics">
      <div className="mb-3 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold">Platform activity</h3>
          <p className="mt-1 text-xs text-text-muted">Live values from the telemetry API</p>
        </div>
        <button
          onClick={() => refreshMutation.mutate()}
          disabled={refreshMutation.isPending}
          className="icon-button rounded-lg p-2 disabled:opacity-70"
          aria-label="Refresh platform metrics"
        >
          {refreshMutation.isPending ? <Loader2 size={16} className="animate-spin" /> : <RefreshCw size={16} />}
        </button>
      </div>
      {isError && (
        <p className="mb-3 rounded-lg border border-warning/30 bg-warning/10 px-3 py-2 text-sm text-warning" role="status">
          Live metrics are unavailable. Check the backend connection.
        </p>
      )}
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <MetricsCard title="Analyses" value={isLoading ? '…' : formatNumber(data?.analysis?.total_analyses)} />
        <MetricsCard title="Chat requests" value={isLoading ? '…' : formatNumber(data?.chat?.total_messages)} />
        <MetricsCard title="Parser success" value={isLoading ? '…' : formatPercent(data?.parser?.success_rate)} />
        <MetricsCard
          title="Average chat latency"
          value={isLoading ? '…' : typeof data?.chat?.avg_latency_ms === 'number' ? `${data.chat.avg_latency_ms} ms` : '—'}
        />
      </div>
    </section>
  );
}
