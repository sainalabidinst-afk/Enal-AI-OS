"use client";

import { PageHeader, Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { MetricCard, MetricGrid } from "@/components/console/ui/metric-card";
import { EmptyBlock, Pill } from "@/components/console/ui/states";
import { BarChart, LineChart, CHART_PALETTE } from "@/components/console/charts/charts";
import { useConsoleStore } from "@/store/console-store";
import { useCapabilityLatency, useConsoleHydration } from "@/features/console/use-console";
import { formatNumber, formatPercent, relativeTime } from "@/lib/format";

export function ObservabilityView() {
  useConsoleHydration("settings", "governance");
  const telemetry = useConsoleStore((s) => s.telemetry);
  const observability = useConsoleStore((s) => s.observability);
  const latency = useCapabilityLatency(10);

  const data = telemetry.data;
  const snapshot = observability.data ?? {};

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

      <div className="grid gap-4 xl:grid-cols-2">
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