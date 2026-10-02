"use client";

import { useEffect, useCallback } from "react";
import { useCognitiveStore } from "@/store/cognitive-store";
import type {
  CapabilityStatusInfo,
  CapabilityRunStatus,
  TranslationConfidenceMetric,
} from "@/types/cognitive";
import { cn } from "@/lib/utils";
import { CAPABILITY_APPS, type CapabilityApp } from "@/components/apps/capability-registry";

const STATUS_COLORS: Record<CapabilityRunStatus, string> = {
  ready: "bg-green-500",
  running: "bg-yellow-500",
  idle: "bg-gray-400",
  failed: "bg-red-500",
  pending: "bg-blue-500",
};

export function CrossCapabilityView() {
  const orchestration = useCognitiveStore((s) => s.orchestration);
  const setOrchestration = useCognitiveStore((s) => s.setOrchestration);
  const setCapabilityStatus = useCognitiveStore((s) => s.setCapabilityStatus);

  const syncCapabilities = useCallback(() => {
    const caps: CapabilityStatusInfo[] = CAPABILITY_APPS.map((app) => {
      const existing = orchestration.capabilities.find((c) => c.id === app.id);
      return {
        id: app.id,
        name: app.name,
        domain: app.domain,
        status: (existing?.status ?? "ready") as CapabilityRunStatus,
        last_active: existing?.last_active ?? "",
        success_rate: existing?.success_rate ?? 100,
        executions: existing?.executions ?? 0,
      };
    });

    setOrchestration({
      capabilities: caps,
      active_execution: orchestration.active_execution,
      cross_capability_metrics: orchestration.cross_capability_metrics,
      last_sync: new Date().toISOString(),
      translation_confidences: orchestration.translation_confidences ?? [],
    });
  }, [orchestration, setOrchestration]);

  useEffect(() => {
    syncCapabilities();
  }, [syncCapabilities]);

  const grouped = groupByDomain(orchestration.capabilities);
  const activeCaps = orchestration.capabilities.filter((c) => c.status === "running");
  const translationConfidences = orchestration.translation_confidences ?? [];
  const translatorCap = orchestration.capabilities.find((c) => c.id === "translator");

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs">
          <span className="h-2 w-2 rounded-full bg-green-500" />
          <span className="text-[var(--color-text-secondary)]">
            {activeCaps.length} active capability{activeCaps.length !== 1 ? "ies" : ""}
          </span>
          {orchestration.last_sync && (
            <span className="text-[var(--color-text-tertiary)]">
              Last sync: {new Date(orchestration.last_sync).toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>

      <div className="space-y-3">
        {Object.entries(grouped).map(([domain, caps]) => (
          <CapabilityDomainGroup
            key={domain}
            domain={domain}
            capabilities={caps}
            onStatusChange={setCapabilityStatus}
          />
        ))}
      </div>

      {translatorCap && translationConfidences.length > 0 && (
        <TranslationCrossCapabilityView
          confidences={translationConfidences}
          capability={translatorCap}
        />
      )}
    </div>
  );
}

function groupByDomain(caps: CapabilityStatusInfo[]): Record<string, CapabilityStatusInfo[]> {
  return caps.reduce(
    (acc, cap) => {
      const domain = cap.domain;
      if (!acc[domain]) acc[domain] = [];
      acc[domain].push(cap);
      return acc;
    },
    {} as Record<string, CapabilityStatusInfo[]>,
  );
}

interface CapabilityDomainGroupProps {
  domain: string;
  capabilities: CapabilityStatusInfo[];
  onStatusChange: (id: string, status: CapabilityRunStatus) => void;
}

function CapabilityDomainGroup({ domain, capabilities, onStatusChange }: CapabilityDomainGroupProps) {
  return (
    <div>
      <div className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-secondary)] mb-2">
        {domain.replace(/_/g, " ")}
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {capabilities.map((cap) => (
          <CapabilityStatusCard
            key={cap.id}
            capability={cap}
            app={CAPABILITY_APPS.find((a) => a.id === cap.id)}
            onStatusChange={onStatusChange}
          />
        ))}
      </div>
    </div>
  );
}

interface CapabilityStatusCardProps {
  capability: CapabilityStatusInfo;
  app?: CapabilityApp;
  onStatusChange: (id: string, status: CapabilityRunStatus) => void;
}

function CapabilityStatusCard({ capability, app, onStatusChange }: CapabilityStatusCardProps) {
  const dotColor = STATUS_COLORS[capability.status] ?? "bg-gray-400";

  return (
    <div className="flex items-center justify-between rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-3">
      <div className="flex items-center gap-2 min-w-0">
        <span className="text-base">{app?.icon ?? "🧩"}</span>
        <div className="truncate">
          <div className="text-xs font-medium text-[var(--color-text-primary)]">{capability.name}</div>
          <div className="text-[10px] text-[var(--color-text-secondary)]">
            {capability.executions} runs · {Math.round(capability.success_rate)}% success
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 shrink-0">
        <div className="text-right">
          <select
            value={capability.status}
            onChange={(e) => onStatusChange(capability.id, e.target.value as CapabilityRunStatus)}
            className="text-[10px] text-[var(--color-text-primary)] bg-[var(--color-bg-secondary)] border border-[var(--color-border)] rounded px-1.5 py-0.5"
          >
            {(["ready", "running", "idle", "failed", "pending"] as const).map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <div className={cn("h-2 w-2 rounded-full", dotColor)} />
      </div>
    </div>
  );
}

interface TranslationCrossCapabilityViewProps {
  confidences: TranslationConfidenceMetric[];
  capability: CapabilityStatusInfo;
}

function TranslationCrossCapabilityView({ confidences, capability }: TranslationCrossCapabilityViewProps) {
  const latest = confidences[confidences.length - 1];
  if (!latest) return null;

  const avgConfidence =
    confidences.reduce((sum, m) => sum + m.confidence, 0) / confidences.length;
  const avgLatency =
    confidences.reduce((sum, m) => sum + m.latency_ms, 0) / confidences.length;
  const avgThroughput =
    confidences.reduce((sum, m) => sum + m.throughput_cps, 0) / confidences.length;

  const confidenceColor =
    avgConfidence >= 0.8
      ? "text-green-500"
      : avgConfidence >= 0.6
      ? "text-yellow-500"
      : "text-red-500";

  return (
    <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-4">
      <div className="flex items-center justify-between mb-3">
        <div>
          <div className="text-xs font-semibold text-[var(--color-text-primary)]">
            {capability.name} — Translation Confidence
          </div>
          <div className="text-[10px] text-[var(--color-text-secondary)]">
            {latest.source_lang}→{latest.target_lang} · {latest.domain}
          </div>
        </div>
        <div className={cn("text-sm font-semibold", confidenceColor)}>
          {Math.round(avgConfidence * 100)}%
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 text-center">
        <div>
          <div className="text-[10px] text-[var(--color-text-secondary)]">Avg Latency</div>
          <div className="text-xs font-medium text-[var(--color-text-primary)]">
            {Math.round(avgLatency)}ms
          </div>
        </div>
        <div>
          <div className="text-[10px] text-[var(--color-text-secondary)]">Throughput</div>
          <div className="text-xs font-medium text-[var(--color-text-primary)]">
            {Math.round(avgThroughput)} cps
          </div>
        </div>
        <div>
          <div className="text-[10px] text-[var(--color-text-secondary)]">Samples</div>
          <div className="text-xs font-medium text-[var(--color-text-primary)]">
            {confidences.length}
          </div>
        </div>
      </div>
    </div>
  );
}
