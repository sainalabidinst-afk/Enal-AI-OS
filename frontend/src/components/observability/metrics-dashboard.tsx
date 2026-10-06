'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { MetricsCard } from '@/components/shared/metrics-card';
import { LoadingSkeleton } from '@/components/shared/loading-skeleton';
import { JsonViewer } from '@/components/shared/json-viewer';

export function MetricsDashboard() {
  const { data, isLoading } = useQuery({
    queryKey: ['metrics', 'all'],
    queryFn: () => apiClient.get('/api/v1/metrics'),
  });

  const metrics = data?.analysis ?? data ?? {};

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-3">
        <MetricsCard title="CPU" value={isLoading ? '-' : '34%'} />
        <MetricsCard title="Memory" value={isLoading ? '-' : '62%'} />
        <MetricsCard title="Latency" value={isLoading ? '-' : '120ms'} />
      </section>
      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Metrics Explorer</h3>
        {isLoading ? (
          <LoadingSkeleton className="mt-4 h-64 w-full" />
        ) : (
          <JsonViewer data={metrics} className="mt-4" />
        )}
      </section>
    </div>
  );
}
