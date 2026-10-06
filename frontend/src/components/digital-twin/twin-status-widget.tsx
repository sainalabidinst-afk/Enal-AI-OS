'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { MetricsCard } from '@/components/shared/metrics-card';
import { StatusBadge } from '@/components/shared/status-badge';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';

export function TwinStatusWidget() {
  const { data, isLoading } = useQuery({
    queryKey: ['twin', 'status'],
    queryFn: () => apiClient.get('/api/v1/twin/status'),
    refetchInterval: 5000,
  });

  if (isLoading) {
    return (
      <div className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Decision Twin Status</h3>
        <LoadingSkeleton className="mt-4 h-24 w-full" />
      </div>
    );
  }

  const healthStatus = data?.mirror_health === 'healthy' ? 'success' : 'warning';

  return (
    <div className="rounded-lg border border-border bg-surface-secondary p-4">
      <h3 className="text-sm font-semibold">Decision Twin Status</h3>
      <div className="mt-4 grid gap-3 md:grid-cols-3">
        <MetricsCard
          title="Twin ID"
          value={data?.twin_id?.slice(0, 8) || '—'}
        />
        <MetricsCard
          title="Active Simulations"
          value={data?.active_simulations ?? 0}
        />
        <MetricsCard
          title="Pending Tests"
          value={data?.pending_adversarial_tests ?? 0}
        />
      </div>
      <div className="mt-3 flex items-center gap-4">
        <StatusBadge status={healthStatus} label={data?.mirror_health || 'unknown'} />
        <span className="text-xs text-text-secondary">
          Last sync: {data?.last_sync || '—'}
        </span>
      </div>
      {data?.system_state_keys?.length > 0 && (
        <p className="mt-2 text-xs text-text-secondary">
          State keys: {data.system_state_keys.slice(0, 10).join(', ')}
        </p>
      )}
    </div>
  );
}
