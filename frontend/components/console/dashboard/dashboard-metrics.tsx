"use client";

import { useMemo } from "react";
import {
  Activity,
  CheckCircle2,
  Gauge,
  ShieldCheck,
  Timer,
} from "lucide-react";
import { MetricCard, MetricGrid } from "@/components/console/ui/metric-card";
import { useConsoleStore } from "@/store/console-store";
import { useGovernanceMetrics } from "@/features/console/use-console";
import { formatDurationMs, formatPercent } from "@/lib/format";

export function DashboardMetrics() {
  const metrics = useGovernanceMetrics();
  const packStatus = useConsoleStore((s) => s.packs.status);
  const lifecycleStatus = useConsoleStore((s) => s.lifecycle.status);
  const loading = packStatus === "loading" || lifecycleStatus === "loading";

  const gateCount = useConsoleStore((s) => Object.keys(s.gateResults.data ?? {}).length);

  const cards = useMemo(
    () => [
      {
        label: "Acceptance Rate",
        value: formatPercent(metrics.acceptanceRate),
        icon: <CheckCircle2 className="h-5 w-5" />,
        tone: "gov" as const,
        hint: gateCount
          ? `${gateCount} quality gate result${gateCount === 1 ? "" : "s"} evaluated`
          : `${metrics.acceptedPacks}/${metrics.totalPacks} packs approved or registered`,
      },
      {
        label: "Remediation Success",
        value: formatPercent(metrics.remediationSuccess, 1),
        icon: <Gauge className="h-5 w-5" />,
        tone: "sky" as const,
        hint: `mean success rate across ${metrics.totalCapabilities} capabilities`,
      },
      {
        label: "Compliance Coverage",
        value: formatPercent(metrics.complianceCoverage),
        icon: <ShieldCheck className="h-5 w-5" />,
        tone: "blue" as const,
        hint: `${metrics.healthyCapabilities}/${metrics.totalCapabilities} capabilities healthy`,
      },
      {
        label: "Avg Response Time",
        value: formatDurationMs(metrics.avgResponseMs),
        icon: <Timer className="h-5 w-5" />,
        tone: "alert" as const,
        hint: "mean capability latency reported by the runtime",
      },
    ],
    [metrics, gateCount]
  );

  return (
    <MetricGrid>
      {cards.map((card) => (
        <MetricCard
          key={card.label}
          label={card.label}
          value={card.value}
          hint={card.hint}
          icon={card.icon}
          tone={card.tone}
          loading={loading}
        />
      ))}
    </MetricGrid>
  );
}

export function RuntimeSignalStrip() {
  const telemetry = useConsoleStore((s) => s.telemetry.data);
  const policies = useConsoleStore((s) => s.policies.data);
  const guardrails = useConsoleStore((s) => s.guardrails.data);
  const connectors = useConsoleStore((s) => s.connectors.data);

  const items = [
    {
      label: "Analyses",
      value: telemetry ? String(telemetry.analysis.count) : "—",
      icon: <Activity className="h-3.5 w-3.5 text-[var(--ecp-sky)]" />,
    },
    {
      label: "Chat runs",
      value: telemetry ? String(telemetry.chat.count) : "—",
      icon: <Activity className="h-3.5 w-3.5 text-[var(--ecp-gov)]" />,
    },
    {
      label: "Policies",
      value: policies ? String(policies.length) : "—",
      icon: <ShieldCheck className="h-3.5 w-3.5 text-[var(--ecp-blue)]" />,
    },
    {
      label: "Guardrails",
      value: guardrails ? String(guardrails.length) : "—",
      icon: <ShieldCheck className="h-3.5 w-3.5 text-[var(--ecp-alert)]" />,
    },
    {
      label: "Connectors",
      value: connectors ? String(connectors.length) : "—",
      icon: <Activity className="h-3.5 w-3.5 text-[var(--ecp-text-dim)]" />,
    },
  ];

  return (
    <div className="flex flex-wrap items-center gap-x-5 gap-y-1.5 text-[11px] text-[var(--ecp-text-muted)]">
      {items.map((item) => (
        <span key={item.label} className="flex items-center gap-1.5">
          {item.icon}
          <span className="text-[var(--ecp-text-dim)]">{item.label}</span>
          <span className="font-medium text-[var(--ecp-text)]">{item.value}</span>
        </span>
      ))}
    </div>
  );
}