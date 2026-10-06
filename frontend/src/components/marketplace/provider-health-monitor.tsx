'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { useToast } from '@/components/shared/toast';
import { Loader2, RefreshCw } from 'lucide-react';

export function ProviderHealthMonitor() {
  const queryClient = useQueryClient();
  const { addToast } = useToast();

  const { data, isLoading } = useQuery({
    queryKey: ['providers', 'health'],
    queryFn: () => apiClient.get('/api/v1/models/health'),
  });

  const refreshMutation = useMutation({
    mutationFn: () => apiClient.get('/api/v1/models/health'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['providers', 'health'] });
      addToast('success', 'Provider health refreshed');
    },
    onError: () => addToast('error', 'Failed to refresh provider health'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const providers = data ?? {};

  return (
    <div className="mt-4 space-y-3">
      <div className="flex justify-end">
        <button
          onClick={() => refreshMutation.mutate()}
          disabled={refreshMutation.isPending}
          className="flex items-center gap-2 rounded-md bg-primary px-3 py-1.5 text-xs text-white hover:bg-primary-hover disabled:opacity-70"
        >
          {refreshMutation.isPending && <Loader2 size={14} className="animate-spin" />}
          <RefreshCw size={14} />
          Refresh Health
        </button>
      </div>
      {Object.entries(providers).map(([name, info]: [string, { status?: string; latency_ms?: number; last_checked?: string }]) => (
        <div key={name} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{name}</p>
            <p className="text-xs text-text-muted">Latency: {info?.latency_ms ?? '-'}ms</p>
          </div>
          <div className="text-right">
            <StatusBadge status={info?.status === 'ok' ? 'success' : 'warning'} label={info?.status ?? 'unknown'} />
            <p className="mt-1 text-xs text-text-secondary">
              {info?.last_checked ? new Date(info.last_checked).toLocaleString() : '-'}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
