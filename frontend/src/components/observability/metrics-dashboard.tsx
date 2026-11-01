'use client';

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';
import { MetricsCard } from '@/components/shared/metrics-card';
import { CardSkeleton } from '@/components/shared/loading-skeleton';
import { JsonViewer } from '@/components/shared/json-viewer';

interface PlatformMetrics {
  analysis?: {
    total_analyses?: number;
    avg_findings?: number;
    avg_risk_score?: number;
  };
  chat?: {
    total_messages?: number;
    avg_latency_ms?: number;
  };
  parser?: {
    total_parses?: number;
    success_rate?: number;
  };
  reasoning?: {
    total_queries?: number;
    avg_steps?: number;
    avg_duration_ms?: number;
  };
  trading?: {
    total_regime_checks?: number;
    avg_confidence?: number;
  };
}

export function MetricsDashboard() {
  const { data, isLoading, isError } = useQuery<PlatformMetrics>({
    queryKey: ['metrics', 'all'],
    queryFn: () => apiClient.get('/api/v1/metrics'),
  });

  const metrics = data ?? {};
  const formatNumber = (value?: number) =>
    typeof value === 'number' ? value.toLocaleString() : '—';
  const formatPercent = (value?: number) =>
    typeof value === 'number' ? `${(value * 100).toFixed(0)}%` : '—';

  return (
    <div className="space-y-6">
      <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4" aria-label="Telemetry summary">
        {isLoading ? (
          Array.from({ length: 4 }, (_, index) => <CardSkeleton key={index} />)
        ) : (
          <>
            <MetricsCard title="Analyses" value={formatNumber(data?.analysis?.total_analyses)} />
            <MetricsCard title="Chat requests" value={formatNumber(data?.chat?.total_messages)} />
            <MetricsCard title="Parser success" value={formatPercent(data?.parser?.success_rate)} />
            <MetricsCard
              title="Average chat latency"
              value={typeof data?.chat?.avg_latency_ms === 'number' ? `${data.chat.avg_latency_ms} ms` : '—'}
            />
          </>
        )}
      </section>
      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="text-sm font-semibold">Metrics Explorer</h3>
            <p className="mt-1 text-xs text-text-muted">Telemetry reported by the backend</p>
          </div>
          <span
            className={`rounded-full px-2.5 py-1 text-xs ${
              isError
                ? 'bg-danger/10 text-danger'
                : isLoading
                  ? 'bg-surface-tertiary text-text-muted'
                  : 'bg-success/10 text-success'
            }`}
          >
            {isError ? 'Unavailable' : isLoading ? 'Loading' : 'Live telemetry'}
          </span>
        </div>
        {isError ? (
          <p className="mt-4 rounded-lg border border-warning/30 bg-warning/10 px-3 py-3 text-sm text-warning" role="status">
            Metrics could not be loaded. Confirm the API is reachable, then refresh this page.
          </p>
        ) : isLoading ? (
          <CardSkeleton />
        ) : (
          <JsonViewer data={metrics} className="mt-4" />
        )}
      </section>
    </div>
  );
}
