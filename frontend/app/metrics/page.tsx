"use client";

import { useEffect, useState, useCallback } from "react";
import { getMetrics, type MetricsResponse } from "@/services/metrics";
import { ErrorBoundary } from "@/components/ui/error-boundary";
import { CardSkeleton } from "@/components/ui/loading-skeleton";
import { useToast } from "@/components/ui/toast";

// --- Metric Card ---
function MetricCard({ title, value, sub, icon }: { title: string; value: string | number; sub?: string; icon?: string }) {
  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 transition-colors hover:border-[var(--color-text-secondary)]">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-[var(--color-text-secondary)]">{title}</p>
          <p className="text-2xl font-semibold mt-1 text-[var(--color-text-primary)]">{value}</p>
          {sub && <p className="text-xs text-[var(--color-text-secondary)] mt-1">{sub}</p>}
        </div>
        {icon && <span className="text-xl">{icon}</span>}
      </div>
    </div>
  );
}

// --- Loading Card ---
function MetricCardSkeleton() {
  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-4 animate-pulse">
      <div className="h-3 w-20 bg-[var(--color-bg-tertiary)] rounded mb-2" />
      <div className="h-8 w-16 bg-[var(--color-bg-tertiary)] rounded mb-1" />
      <div className="h-3 w-28 bg-[var(--color-bg-tertiary)] rounded" />
    </div>
  );
}

// --- Bar Chart Row ---
function BarRow({ label, value, max }: { label: string; value: number; max: number }) {
  const width = max > 0 ? Math.round((value / max) * 100) : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="w-36 text-xs text-[var(--color-text-secondary)] truncate" title={label}>
        {label}
      </span>
      <div className="flex-1 h-2.5 rounded-full bg-[var(--color-bg-primary)]">
        <div
          className="h-2.5 rounded-full bg-[var(--color-accent)] transition-all duration-500"
          style={{ width: `${width}%` }}
        />
      </div>
      <span className="w-10 text-right text-xs font-mono text-[var(--color-text-primary)]">{value}</span>
    </div>
  );
}

// --- Distribution Section ---
function DistributionSection({
  title,
  data,
  emptyText,
}: {
  title: string;
  data: Record<string, number>;
  emptyText: string;
}) {
  const entries = Object.entries(data);
  const max = Math.max(...entries.map(([, v]) => v), 1);

  if (entries.length === 0) {
    return (
      <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-5">
        <h3 className="text-sm font-semibold text-[var(--color-text-primary)] mb-1">{title}</h3>
        <p className="text-xs text-[var(--color-text-secondary)]">{emptyText}</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-5">
      <h3 className="text-sm font-semibold text-[var(--color-text-primary)] mb-3">{title}</h3>
      <div className="space-y-2">
        {entries.sort((a, b) => b[1] - a[1]).map(([key, val]) => (
          <BarRow key={key} label={key} value={val} max={max} />
        ))}
      </div>
    </div>
  );
}

// --- Main Content ---
function MetricsPageContent() {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const { showError: showToastError } = useToast();

  const fetchMetrics = useCallback(async (showLoading = false) => {
    if (showLoading) setLoading(true);
    setError(null);
    try {
      const data = await getMetrics();
      setMetrics(data);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Failed to load metrics";
      setError(msg);
      if (showLoading) showToastError("Failed to load metrics", msg);
    } finally {
      if (showLoading) setLoading(false);
    }
  }, [showToastError]);

  // Initial load
  useEffect(() => {
    const controller = new AbortController();
    fetchMetrics(true);
    return () => controller.abort();
  }, [fetchMetrics]);

  // Auto-refresh toggle
  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => fetchMetrics(), 30000);
    return () => clearInterval(interval);
  }, [autoRefresh, fetchMetrics]);

  // Loading state
  if (loading && !metrics) {
    return (
      <div className="mx-auto max-w-5xl p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <div className="h-8 w-48 bg-[var(--color-bg-tertiary)] rounded animate-pulse" />
            <div className="h-4 w-64 bg-[var(--color-bg-tertiary)] rounded animate-pulse mt-2" />
          </div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <MetricCardSkeleton key={i} />
          ))}
        </div>
        <div className="h-40 bg-[var(--color-bg-tertiary)] rounded-xl animate-pulse" />
      </div>
    );
  }

  // Error with no data
  if (error && !metrics) {
    return (
      <div className="mx-auto max-w-5xl p-6">
        <div className="rounded-xl border border-[var(--color-danger)] bg-[var(--color-bg-secondary)] p-6 text-center">
          <p className="text-lg mb-2">⚠️</p>
          <p className="text-sm font-medium text-[var(--color-text-primary)]">Failed to load metrics</p>
          <p className="text-xs text-[var(--color-text-secondary)] mt-1">{error}</p>
          <button
            onClick={() => fetchMetrics(true)}
            className="mt-4 rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm text-white hover:opacity-90"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // No data yet
  if (!metrics) {
    return (
      <div className="mx-auto max-w-5xl p-6 text-center py-12">
        <p className="text-sm text-[var(--color-text-secondary)]">No metrics data available.</p>
      </div>
    );
  }

  const analysis = metrics.analysis;
  const chat = metrics.chat;
  const parser = metrics.parser;

  return (
    <div className="mx-auto max-w-5xl p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-primary)]">
            Platform Metrics
          </h1>
          <p className="text-sm text-[var(--color-text-secondary)] mt-1">
            Real-time instrumentation from backend telemetry
          </p>
        </div>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 text-xs text-[var(--color-text-secondary)] cursor-pointer">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="rounded border-[var(--color-border)]"
            />
            Auto-refresh
          </label>
          <button
            onClick={() => fetchMetrics(true)}
            disabled={loading}
            className="rounded-lg bg-[var(--color-accent)] px-4 py-2 text-sm font-medium text-white hover:opacity-90 disabled:opacity-50 transition-opacity"
          >
            {loading ? "Loading..." : "Refresh"}
          </button>
        </div>
      </div>

      {/* Error banner */}
      {error && (
        <div className="rounded-lg border border-[var(--color-danger)] bg-red-900/20 px-4 py-2.5 text-sm text-[var(--color-danger)]">
          {error}
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <MetricCard
          title="Analysis Executions"
          value={analysis.count}
          sub={`${analysis.success_count} succeeded · ${analysis.error_count} failed`}
          icon="🔬"
        />
        <MetricCard
          title="Chat Interactions"
          value={chat.count}
          sub={`${chat.success_count} succeeded · ${chat.error_count} failed`}
          icon="💬"
        />
        <MetricCard
          title="Parser Runs"
          value={parser.count}
          sub={`${Object.keys(parser.parser_distribution).length} parser types`}
          icon="📄"
        />
      </div>

      {/* Performance Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <MetricCard
          title="Avg Analysis Time"
          value={`${analysis.avg_total_time_ms.toFixed(0)} ms`}
          sub={`${(analysis.avg_total_time_ms / 1000).toFixed(2)} seconds`}
          icon="⏱️"
        />
        <MetricCard
          title="Avg Chat Response"
          value={`${chat.avg_total_time_ms.toFixed(0)} ms`}
          sub={`${(chat.avg_total_time_ms / 1000).toFixed(2)} seconds`}
          icon="⚡"
        />
        <MetricCard
          title="Avg Confidence Score"
          value={`${(analysis.avg_confidence * 100).toFixed(1)}%`}
          sub={`${analysis.avg_findings.toFixed(1)} avg findings · ${(analysis.avg_compliance_score * 100).toFixed(0)}% compliance`}
          icon="🎯"
        />
      </div>

      {/* Vendor Distribution */}
      <DistributionSection
        title="Vendor Distribution"
        data={analysis.vendor_distribution}
        emptyText="No vendor data yet."
      />

      {/* Parser Distribution */}
      <DistributionSection
        title="Parser Distribution"
        data={parser.parser_distribution}
        emptyText="No parser data yet."
      />

      {/* Footer */}
      <p className="text-xs text-[var(--color-text-secondary)] text-center">
        Metrics are aggregated from backend telemetry. Data refreshes {autoRefresh ? "every 30s" : "manually"}.
      </p>
    </div>
  );
}

// --- Export with ErrorBoundary ---
export default function MetricsPage() {
  return (
    <ErrorBoundary>
      <MetricsPageContent />
    </ErrorBoundary>
  );
}

