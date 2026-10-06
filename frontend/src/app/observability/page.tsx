'use client';

import { MetricsDashboard } from '@/components/observability/metrics-dashboard';
import { LogViewer } from '@/components/observability/log-viewer';
import { TracingPanel } from '@/components/observability/tracing-panel';
import { AlertRulesNotifications } from '@/components/observability/alert-rules-notifications';

export default function ObservabilityPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Observability</h2>
        <p className="text-sm text-text-secondary">Metrics, logs, and tracing.</p>
      </div>

      <MetricsDashboard />

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Logs</h3>
          <LogViewer />
        </div>
        <div className="rounded-lg border border-border bg-surface-secondary p-4">
          <h3 className="text-sm font-semibold">Tracing</h3>
          <TracingPanel />
        </div>
      </section>

      <section className="rounded-lg border border-border bg-surface-secondary p-4">
        <h3 className="text-sm font-semibold">Alert Rules & Notifications</h3>
        <AlertRulesNotifications />
      </section>
    </div>
  );
}
