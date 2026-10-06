'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { StatusBadge } from '@/components/shared/status-badge';

export function AlertRulesNotifications() {
  const { data, isLoading } = useQuery<{ trading_regime?: Array<{ event_id?: string; symbol?: string; regime?: string; confidence?: number; status?: string }> }>({
    queryKey: ['metrics', 'alerts'],
    queryFn: () => apiClient.get('/api/v1/metrics/alerts'),
  });

  if (isLoading) return <LoadingSkeleton className="mt-4 h-64 w-full" />;

  const alerts = data?.trading_regime ?? [];

  return (
    <div className="mt-4 space-y-2">
      {alerts.map((alert: { event_id?: string; symbol?: string; regime?: string; confidence?: number; status?: string }) => (
        <div key={alert.event_id} className="flex items-center justify-between rounded-md border border-border px-3 py-2">
          <div>
            <p className="text-sm font-medium">{alert.symbol ?? 'Alert'}</p>
            <p className="text-xs text-text-muted">Regime: {alert.regime} · Confidence: {alert.confidence}</p>
          </div>
          <StatusBadge status={alert.status === 'active' ? 'danger' : 'success'} label={alert.status ?? 'unknown'} />
        </div>
      ))}
    </div>
  );
}
