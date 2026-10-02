"use client";

import { useCognitiveStore } from "@/store/cognitive-store";
import type { MetaCognitiveFlags, TranslationConfidenceMetric } from "@/types/cognitive";
import { cn } from "@/lib/utils";

export function MetaCognitiveState() {
  const thinkingMode = useCognitiveStore((s) => s.thinking_mode);
  const metaFlags = useCognitiveStore((s) => s.meta_cognitive_flags);
  const activeCapability = useCognitiveStore((s) => s.active_capability);
  const translationConfidences = useCognitiveStore(
    (s) => s.orchestration.translation_confidences,
  );

  const confidence = thinkingMode?.confidence ?? metaFlags.translation_confidence ?? 0;
  const hasData = thinkingMode !== null || metaFlags.translation_confidence !== undefined;

  const isTranslatorActive = activeCapability === "translator" || activeCapability === "translator-expert";

  return (
    <div className="space-y-4">
      <ConfidenceGauge
        value={confidence}
        active={hasData}
        warning={metaFlags.translation_warning && isTranslatorActive}
      />

      <MetaFlagsGrid metaFlags={metaFlags} activeCapability={activeCapability} />

      {isTranslatorActive && translationConfidences && translationConfidences.length > 0 && (
        <TranslationMetrics confidenceHistory={translationConfidences} />
      )}

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
  warning?: boolean;
}

function ConfidenceGauge({ value, active, warning }: ConfidenceGaugeProps) {
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
        <span className="text-xs font-medium text-[var(--color-text-secondary)]">
          {active ? "Confidence" : "No Active Thinker"}
        </span>
        <span className="text-xs font-semibold text-[var(--color-text-primary)]">
          {active ? `${pct}%` : "—"}
        </span>
      </div>

      <div className="relative h-4 w-full rounded-full bg-[var(--color-bg-primary)] overflow-hidden">
        <div
          className={cn(
            "h-full rounded-full transition-all duration-500",
            active ? colorClass : "bg-gray-300",
            warning ? "animate-pulse" : "",
          )}
          style={active ? { width: `${pct}%` } : { width: "100%" }}
        />
      </div>

      {warning && (
        <div className="flex items-center gap-1 text-xs text-yellow-600">
          <span className="h-2 w-2 rounded-full bg-yellow-500 animate-pulse" />
          Low translation confidence — consider alternate models
        </div>
      )}

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

interface TranslationMetricsProps {
  confidenceHistory: TranslationConfidenceMetric[];
}

function TranslationMetrics({ confidenceHistory }: TranslationMetricsProps) {
  const latest = confidenceHistory[confidenceHistory.length - 1];
  if (!latest) return null;

  const avgConfidence =
    confidenceHistory.reduce((sum, m) => sum + m.confidence, 0) / confidenceHistory.length;
  const avgLatency =
    confidenceHistory.reduce((sum, m) => sum + m.latency_ms, 0) / confidenceHistory.length;
  const avgThroughput =
    confidenceHistory.reduce((sum, m) => sum + m.throughput_cps, 0) / confidenceHistory.length;

  return (
    <div className="space-y-3">
      <div className="text-[10px] font-semibold uppercase tracking-wide text-[var(--color-text-secondary)]">
        Translation Metrics
      </div>
      <div className="grid grid-cols-2 gap-2">
        <MetricRow
          label="Avg Confidence"
          value={`${Math.round(avgConfidence * 100)}%`}
        />
        <MetricRow label="Avg Latency" value={`${Math.round(avgLatency)}ms`} />
        <MetricRow label="Avg Throughput" value={`${Math.round(avgThroughput)} cps`} />
        <MetricRow
          label="Glossary Terms"
          value={latest.glossary_terms_used.toString()}
        />
        <MetricRow label="Model" value={latest.model_used ?? "—"} />
        <MetricRow
          label="Last Pair"
          value={`${latest.source_lang}→${latest.target_lang}`}
        />
      </div>
    </div>
  );
}

function MetricRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-secondary)] p-2">
      <div className="text-[10px] text-[var(--color-text-secondary)]">{label}</div>
      <div className="text-xs font-medium text-[var(--color-text-primary)] truncate">
        {value}
      </div>
    </div>
  );
}
