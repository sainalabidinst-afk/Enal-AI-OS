"use client";

import { useCognitiveStore } from "@/store/cognitive-store";
import { cn } from "@/lib/utils";

export function ConfidenceMeter() {
  const thinkingMode = useCognitiveStore((s) => s.thinking_mode);
  const metaFlags = useCognitiveStore((s) => s.meta_cognitive_flags);

  if (!thinkingMode) {
    return (
      <div className="text-xs text-[var(--color-text-secondary)]">
        Start a thinking mode to see confidence.
      </div>
    );
  }

  const confidence = thinkingMode.confidence;
  const getConfidenceColor = (value: number) => {
    if (value >= 0.8) return "bg-green-500";
    if (value >= 0.6) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs text-[var(--color-text-secondary)]">Confidence</span>
        <span className="text-xs font-medium text-[var(--color-text-primary)]">
          {Math.round(confidence * 100)}%
        </span>
      </div>
      <div className="h-2 w-full rounded-full bg-[var(--color-bg-primary)] overflow-hidden">
        <div
          className={cn("h-full rounded-full transition-all duration-500", getConfidenceColor(confidence))}
          style={{ width: `${confidence * 100}%` }}
        />
      </div>

      {metaFlags.uncertainty && (
        <div className="flex items-center gap-2 mt-2">
          <div className="h-2 w-2 rounded-full bg-yellow-500 animate-pulse" />
          <span className="text-xs text-yellow-600">High uncertainty — consider alternatives</span>
        </div>
      )}

      <div className="text-xs text-[var(--color-text-secondary)] mt-2">
        Trend: {metaFlags.confidence_trend}
      </div>
    </div>
  );
}
