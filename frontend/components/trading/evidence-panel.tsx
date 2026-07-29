"use client";

import type { TradingEvidence } from "@/types/trading";

interface EvidenceCardProps {
  ev: TradingEvidence;
}

function EvidenceCard({ ev }: EvidenceCardProps) {
  const directionColor =
    ev.direction === "bullish" ? "border-l-green-500" :
    ev.direction === "bearish" ? "border-l-red-500" :
    "border-l-yellow-500";

  const directionBadge =
    ev.direction === "bullish" ? "bg-green-500/10 text-green-600" :
    ev.direction === "bearish" ? "bg-red-500/10 text-red-600" :
    "bg-yellow-500/10 text-yellow-600";

  return (
    <div className={`border-l-4 ${directionColor} bg-[var(--color-bg-secondary)] rounded-lg p-3 space-y-2`}>
      <div className="flex items-start justify-between gap-2">
        <p className="text-sm font-medium text-[var(--color-text-primary)]">
          {ev.description}
        </p>
        <span className={`shrink-0 text-[10px] px-2 py-0.5 rounded-full font-medium ${directionBadge}`}>
          {ev.direction}
        </span>
      </div>
      <div className="flex items-center gap-3 text-xs text-[var(--color-text-secondary)]">
        <span className="bg-[var(--color-bg-tertiary)] px-2 py-0.5 rounded">
          {ev.timeframe}
        </span>
        <span>Strength: {(ev.strength * 100).toFixed(0)}%</span>
        <span>Confidence: {(ev.confidence * 100).toFixed(0)}%</span>
      </div>
      <p className="text-[10px] text-[var(--color-text-secondary)]">
        Source: {ev.source}
      </p>
    </div>
  );
}

interface EvidencePanelProps {
  evidence: TradingEvidence[];
}

export function EvidencePanel({ evidence }: EvidencePanelProps) {
  if (evidence.length === 0) {
    return (
      <div className="rounded-lg bg-[var(--color-bg-secondary)] p-4 text-center">
        <p className="text-sm text-[var(--color-text-secondary)]">No evidence available.</p>
      </div>
    );
  }

  // Group by type
  const grouped: Record<string, TradingEvidence[]> = {};
  for (const ev of evidence) {
    if (!grouped[ev.type]) grouped[ev.type] = [];
    grouped[ev.type].push(ev);
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-[var(--color-text-primary)]">
        Evidence ({evidence.length})
      </h3>
      {Object.entries(grouped).map(([type, evs]) => (
        <div key={type} className="space-y-2">
          <p className="text-xs font-medium text-[var(--color-text-secondary)] capitalize">
            {type.replace(/_/g, " ")}
          </p>
          {evs.map((ev) => (
            <EvidenceCard key={ev.id} ev={ev} />
          ))}
        </div>
      ))}
    </div>
  );
}
