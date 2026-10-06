'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function ProviderHealthMonitor() {
  const { data, isLoading } = useQuery({
    queryKey: ['providers', 'health'],
    queryFn: () => apiClient.get('/api/v1/models/health'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const providers = data ?? {};

  return (
    <div className="mt-4 space-y-3">
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
