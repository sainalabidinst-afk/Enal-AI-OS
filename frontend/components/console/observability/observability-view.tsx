"use client";

import { useState, useCallback, useEffect } from "react";
import { PageHeader, Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { MetricCard, MetricGrid } from "@/components/console/ui/metric-card";
import { EmptyBlock, Pill } from "@/components/console/ui/states";
import { BarChart, LineChart, CHART_PALETTE } from "@/components/console/charts/charts";
import { LearningProgressPanel } from "@/components/console/observability/learning-progress-panel";
import { useConsoleStore } from "@/store/console-store";
import { useCapabilityLatency, useConsoleHydration } from "@/features/console/use-console";
import { TradingPanel } from "@/components/console/dashboard/trading-panel";
import {
  getTelemetryAlerts,
  getTelemetryMetrics,
  getPrometheusMetrics,
  type AlertFeedResponse,
  type TradingRegimeAlert,
  type CrossPackCorrelationAlert,
} from "@/services/observability";
import { formatNumber, formatPercent, relativeTime } from "@/lib/format";

export function ObservabilityView() {
  useConsoleHydration("settings", "governance");
  const telemetry = useConsoleStore((s) => s.telemetry);
  const observability = useConsoleStore((s) => s.observability);
  const latency = useCapabilityLatency(10);

  const [alertFeed, setAlertFeed] = useState<AlertFeedResponse | null>(null);
  const [alertsLoading, setAlertsLoading] = useState(false);
  const [prometheusUrl, setPrometheusUrl] = useState<string | null>(null);

  const data = telemetry.data;
  const snapshot = observability.data ?? {};

  const loadAlerts = useCallback(async () => {
    setAlertsLoading(true);
    try {
      const [alerts, metrics] = await Promise.all([
        getTelemetryAlerts(),
        getTelemetryMetrics(),
      ]);
      setAlertFeed(alerts);
      const base = typeof window !== "undefined" ? window.location.origin : "";
      setPrometheusUrl(`${base}/api/v1/telemetry/metrics/prometheus`);
    } catch (error) {
      // silent refresh
    } finally {
      setAlertsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAlerts();
    const interval = setInterval(loadAlerts, 10000);
    return () => clearInterval(interval);
  }, [loadAlerts]);

  const counters = [
    {
      label: "Analyses",
      value: data ? String(data.analysis.count) : "—",
      tone: "gov" as const,
      hint: data ? `avg ${formatNumber(data.analysis.avg_total_time_ms)} ms` : "—",
    },
    {
      label: "Chat runs",
      value: data ? String(data.chat.count) : "—",
      tone: "sky" as const,
      hint: data ? `avg ${formatNumber(data.chat.avg_total_time_ms)} ms` : "—",
    },
    {
      label: "Avg confidence",
      value: data ? formatNumber(data.analysis.avg_confidence) : "—",
      tone: "blue" as const,
      hint: "analysis confidence",
    },
    {
      label: "Compliance score",
      value: data ? formatNumber(data.analysis.avg_compliance_score) : "—",
      tone: "alert" as const,
      hint: "analysis compliance",
    },
  ];

  return (
    <div className="space-y-4">
      <PageHeader
        title="Observability"
        description="Runtime telemetry, capability latency profile and agent metrics"
      />

      <MetricGrid>
        {counters.map((counter) => (
          <MetricCard
            key={counter.label}
            label={counter.label}
            value={counter.value}
            hint={counter.hint}
            tone={counter.tone}
            loading={telemetry.status === "loading"}
          />
        ))}
      </MetricGrid>

      <TradingPanel />

      <div className="grid gap-4 xl:grid-cols-2">
        <LearningProgressPanel />

        <Panel>
          <PanelHeader
            title="Trading + Governance Alerts"
            subtitle="Cross-pack correlation and trading regime alerts"
            actions={
              prometheusUrl ? (
                <a
                  href={prometheusUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="text-[11px] text-[var(--ecp-gov)] hover:underline"
                >
                  Prometheus metrics
                </a>
              ) : null
            }
          />
          <PanelBody>
            {alertsLoading && !alertFeed ? (
              <EmptyBlock title="Loading alerts" hint="Fetching telemetry alerts..." />
            ) : (
              <div className="space-y-4">
                <div>
                  <h3 className="text-xs font-semibold text-[var(--ecp-text-dim)] uppercase tracking-wide">
                    Trading regime alerts
                  </h3>
                  <div className="mt-2 space-y-2">
                    {(alertFeed?.trading_regime ?? []).length === 0 ? (
                      <p className="text-xs text-[var(--ecp-text-muted)]">No trading regime alerts yet.</p>
                    ) : (
                      alertFeed?.trading_regime.slice(0, 10).map((alert) => (
                        <div
                          key={alert.event_id}
                          className="flex items-center justify-between rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2"
                        >
                          <div className="min-w-0">
                            <p className="text-xs font-medium text-[var(--ecp-text)]">
                              {alert.symbol} · {alert.timeframe}
                            </p>
                            <p className="text-[11px] text-[var(--ecp-text-muted)]">
                              Regime: {alert.regime} · Confidence: {(alert.confidence * 100).toFixed(0)}%
                            </p>
                          </div>
                          <span
                            className={`text-[10px] font-medium ${
                              alert.confidence < 0.5
                                ? "text-[var(--ecp-alert)]"
                                : "text-green-500"
                            }`}
                          >
                            {alert.status}
                          </span>
                        </div>
                      ))
                    )}
                  </div>
                </div>
                <div>
                  <h3 className="text-xs font-semibold text-[var(--ecp-text-dim)] uppercase tracking-wide">
                    Cross-pack correlations
                  </h3>
                  <div className="mt-2 space-y-2">
                    {(alertFeed?.cross_pack_correlations ?? []).length === 0 ? (
                      <p className="text-xs text-[var(--ecp-text-muted)]">No cross-pack correlations yet.</p>
                    ) : (
                      alertFeed?.cross_pack_correlations.slice(0, 10).map((alert) => (
                        <div
                          key={alert.event_id}
                          className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2"
                        >
                          <div className="flex items-center justify-between">
                            <p className="text-xs font-medium text-[var(--ecp-text)]">
                              {alert.source_pack} → {alert.target_pack}
                            </p>
                            <span className="text-[10px] text-[var(--ecp-text-muted)]">
                              {(alert.confidence * 100).toFixed(0)}%
                            </span>
                          </div>
                          <p className="mt-1 text-[11px] text-[var(--ecp-text-secondary)]">{alert.details}</p>
                          <p className="mt-1 text-[10px] text-[var(--ecp-text-dim)]">
                            {alert.correlation_type} · {relativeTime(alert.timestamp)}
                          </p>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            )}
          </PanelBody>
        </Panel>

        <Panel>
          <PanelHeader
            title="Capability latency"
            subtitle="Average latency reported per capability"
          />
          <PanelBody>
            {latency.labels.length === 0 ? (
              <EmptyBlock
                title="No latency reported"
                hint="Capabilities report latency after their first execution."
              />
            ) : (
              <BarChart
                labels={latency.labels}
                series={[
                  {
                    label: "avg latency",
                    values: latency.values,
                    color: CHART_PALETTE.sky,
                  },
                ]}
                horizontal
                height={300}
                yTitle="ms"
              />
            )}
          </PanelBody>
        </Panel>

        <Panel>
          <PanelHeader
            title="Throughput"
            subtitle="Counter trend per subsystem (current snapshot)"
          />
          <PanelBody>
            {data ? (
              <LineChart
                labels={["analysis", "chat", "parser", "reasoning"]}
                series={[
                  {
                    label: "runs",
                    values: [
                      data.analysis.count,
                      data.chat.count,
                      data.parser.count,
                      data.reasoning.count,
                    ],
                    color: CHART_PALETTE.gov,
                  },
                ]}
                fill
                height={300}
                yTitle="runs"
              />
            ) : (
              <EmptyBlock
                title="No telemetry snapshot"
                hint={telemetry.error ?? "Telemetry endpoint returned no data."}
              />
            )}
          </PanelBody>
        </Panel>
      </div>

      <Panel>
        <PanelHeader
          title="Agent metrics"
          subtitle="Observability snapshot from /api/v1/observability/metrics"
          actions={<Pill>{relativeTime(observability.updatedAt)}</Pill>}
        />
        <PanelBody>
          {Object.keys(snapshot).length === 0 ? (
            <EmptyBlock
              title="No agent metrics"
              hint={observability.error ?? "No agents have reported metrics yet."}
            />
          ) : (
            <dl className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {Object.entries(snapshot)
                .slice(0, 12)
                .map(([key, value]) => (
                  <div
                    key={key}
                    className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2"
                  >
                    <dt className="text-[10px] uppercase tracking-wide text-[var(--ecp-text-dim)]">
                      {key}
                    </dt>
                    <dd className="mt-1 truncate text-xs font-medium text-[var(--ecp-text)]">
                      {typeof value === "object"
                        ? JSON.stringify(value).slice(0, 60)
                        : String(value)}
                    </dd>
                  </div>
                ))}
            </dl>
          )}
        </PanelBody>
      </Panel>
    </div>
  );
}