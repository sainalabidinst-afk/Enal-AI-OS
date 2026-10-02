"use client";

import { useCognitiveStore } from "@/store/cognitive-store";
import type { MetaCognitiveFlags } from "@/types/cognitive";
import { cn } from "@/lib/utils";

export function MetaCognitiveState() {
  const thinkingMode = useCognitiveStore((s) => s.thinking_mode);
  const metaFlags = useCognitiveStore((s) => s.meta_cognitive_flags);
  const activeCapability = useCognitiveStore((s) => s.active_capability);

  const confidence = thinkingMode?.confidence ?? 0;
  const hasData = thinkingMode !== null;

  return (
    <div className="space-y-4">
      <ConfidenceGauge value={confidence} active={hasData} />

      <MetaFlagsGrid metaFlags={metaFlags} activeCapability={activeCapability} />

      {metaFlags.last_reflection && (
        <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-3">
          <div className="text-[10px] font-semibold uppercase tracking-wide text-[var(--color-text-secondary)] mb-1">
            Last Reflection
          </div>
          <p className="text-xs text-[var(--color-text-primary)]">{metaFlags.last_reflection}</p>
        </div>
      )}
    </div>
  );
}

interface ConfidenceGaugeProps {
  value: number;
  active: boolean;
}

function ConfidenceGauge({ value, active }: ConfidenceGaugeProps) {
  const pct = Math.round(value * 100);

  const colorClass =
    value >= 0.8
      ? "bg-green-500"
      : value >= 0.6
      ? "bg-yellow-500"
      : value >= 0.4
      ? "bg-orange-500"
      : "bg-red-500";

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-[var(--color-text-secondary)]">Confidence</span>
        <span className="text-xs font-semibold text-[var(--color-text-primary)]">
          {active ? `${pct}%` : "—"}
        </span>
      </div>

      <div className="relative h-4 w-full rounded-full bg-[var(--color-bg-primary)] overflow-hidden">
        <div
          className={cn(
            "h-full rounded-full transition-all duration-500",
            active ? colorClass : "bg-gray-300",
          )}
          style={active ? { width: `${pct}%` } : { width: "100%" }}
        />
      </div>

      <div className="grid grid-cols-5 gap-1 text-[10px]">
        <span className="text-[var(--color-text-secondary)]">Low</span>
        <span className="text-center text-[var(--color-text-secondary)]">Medium</span>
        <span className="text-[var(--color-text-secondary)]">High</span>
      </div>
    </div>
  );
}

interface MetaFlagsGridProps {
  metaFlags: MetaCognitiveFlags;
  activeCapability: string | null;
}

function MetaFlagsGrid({ metaFlags, activeCapability }: MetaFlagsGridProps) {
  const trendColor = {
    increasing: "text-green-500",
    stable: "text-blue-500",
    decreasing: "text-red-500",
  }[metaFlags.confidence_trend];

  const statusItems = [
    { label: "Active Capability", value: activeCapability || "—" },
    {
      label: "Uncertainty",
      value: metaFlags.uncertainty ? "High" : "Low",
      valueClass: metaFlags.uncertainty ? "text-yellow-500" : "text-green-500",
    },
    { label: "Confidence Trend", value: metaFlags.confidence_trend, valueClass: trendColor },
    { label: "Alternatives Considered", value: metaFlags.alternatives_considered.toString() },
  ];

  return (
    <div className="grid grid-cols-2 gap-2">
      {statusItems.map((item) => (
        <div
          key={item.label}
          className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-primary)] p-2.5"
        >
          <div className="text-[10px] font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">
            {item.label}
          </div>
          <div className={cn("text-xs font-medium text-[var(--color-text-primary)]", item.valueClass)}>
            {item.value}
          </div>
        </div>
      ))}
    </div>
  );
}
