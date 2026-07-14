"use client";

import { useEffect, useState } from "react";
import { getMetrics, type MetricsResponse } from "@/services/metrics";

function MetricCard({ title, value, sub }: { title: string; value: string | number; sub?: string }) {
  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4">
      <p className="text-xs text-[var(--color-text-secondary)]">{title}</p>
      <p className="text-2xl font-semibold mt-1">{value}</p>
      {sub && <p className="text-xs text-[var(--color-text-secondary)] mt-1">{sub}</p>}
    </div>
  );
}

function Bar({ label, value, max }: { label: string; value: number; max: number }) {
  const width = max > 0 ? Math.round((value / max) * 100) : 0;
  return (
    <div className="flex items-center gap-2 text-sm">
      <span className="w-40 truncate text-[var(--color-text-secondary)]">{label}</span>
      <div className="flex-1 h-2 rounded bg-[var(--color-bg-tertiary)]">
        <div className="h-2 rounded bg-[var(--color-accent)]" style={{ width: `${width}%` }} />
      </div>
      <span className="w-10 text-right">{value}</span>
    </div>
  );
}

export default function MetricsPage() {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getMetrics()
      .then((data) => {
        if (!cancelled) setMetrics(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load metrics");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="mx-auto max-w-5xl p-4 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold">Product Metrics</h1>
          <p className="text-sm text-[var(--color-text-secondary)]">Real-time instrumentation from backend telemetry</p>
        </div>
        <button
          onClick={() => getMetrics().then(setMetrics).catch((err) => setError(err instanceof Error ? err.message : "Failed"))}
          className="rounded-lg bg-[var(--color-accent)] px-3 py-1 text-sm text-white hover:opacity-90"
        >
          Refresh
        </button>
      </div>

      {error && (
        <div className="rounded-lg border border-[var(--color-danger)] bg-[var(--color-bg-secondary)] px-4 py-2 text-sm text-[var(--color-danger)]">
          {error}
        </div>
      )}

      {loading && <p className="text-sm text-[var(--color-text-secondary)]">Loading metrics...</p>}

      {!loading && metrics && (
        <>
          <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <MetricCard title="Analysis Count" value={metrics.analysis.count} sub={`${metrics.analysis.success_count} success`} />
            <MetricCard title="Chat Count" value={metrics.chat.count} sub={`${metrics.chat.success_count} success`} />
            <MetricCard title="Parser Count" value={metrics.parser.count} />
          </section>

          <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <MetricCard title="Avg Analysis Time" value={`${metrics.analysis.avg_total_time_ms.toFixed(0)} ms`} />
            <MetricCard title="Avg Chat Time" value={`${metrics.chat.avg_total_time_ms.toFixed(0)} ms`} />
            <MetricCard title="Avg Confidence" value={`${(metrics.analysis.avg_confidence * 100).toFixed(0)}%`} sub={`${metrics.analysis.avg_findings.toFixed(1)} avg findings`} />
          </section>

          <section className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-2">
            <h2 className="text-sm font-semibold">Vendor Distribution</h2>
            {Object.entries(metrics.analysis.vendor_distribution).length === 0 && (
              <p className="text-xs text-[var(--color-text-secondary)]">No vendor data yet.</p>
            )}
            <div className="space-y-1">
              {Object.entries(metrics.analysis.vendor_distribution)
                .sort((a, b) => b[1] - a[1])
                .map(([vendor, count]) => (
                  <Bar key={vendor} label={vendor} value={count} max={Math.max(...Object.values(metrics.analysis.vendor_distribution))} />
                ))}
            </div>
          </section>

          <section className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 space-y-2">
            <h2 className="text-sm font-semibold">Parser Distribution</h2>
            {Object.entries(metrics.analysis.parser_distribution).length === 0 && (
              <p className="text-xs text-[var(--color-text-secondary)]">No parser data yet.</p>
            )}
            <div className="space-y-1">
              {Object.entries(metrics.analysis.parser_distribution)
                .sort((a, b) => b[1] - a[1])
                .map(([parser, count]) => (
                  <Bar key={parser} label={parser} value={count} max={Math.max(...Object.values(metrics.analysis.parser_distribution))} />
                ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}
