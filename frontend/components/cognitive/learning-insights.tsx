"use client";

import { useCognitiveStore } from "@/store/cognitive-store";
import type { LearningInsight, InsightPriority } from "@/types/cognitive";
import { cn } from "@/lib/utils";

export function LearningInsights() {
  const insights = useCognitiveStore((s) => s.learningInsights);
  const applyInsight = useCognitiveStore((s) => s.applyInsight);
  const dismissInsight = useCognitiveStore((s) => s.dismissInsight);

  const PRIORITY_LABELS: Record<InsightPriority, string> = {
    high: "High",
    medium: "Medium",
    low: "Low",
  };

  if (insights.length === 0) {
    return (
      <div className="text-xs text-[var(--color-text-secondary)]">
        No improvement suggestions available. Completed analyses will surface here.
      </div>
    );
  }

  const sorted = [...insights].sort((a, b) => {
    const order: Record<InsightPriority, number> = { high: 0, medium: 1, low: 2 };
    const diff = (order[b.priority] ?? 2) - (order[a.priority] ?? 2);
    if (diff !== 0) return diff;
    return b.created_at.localeCompare(a.created_at);
  });

  return (
    <div className="space-y-2">
      {sorted.map((insight: LearningInsight) => (
        <InsightItem
          key={insight.id}
          insight={insight}
          priorityLabel={PRIORITY_LABELS[insight.priority]}
          onApply={() => applyInsight(insight.id)}
          onDismiss={() => dismissInsight(insight.id)}
        />
      ))}
    </div>
  );
}

interface InsightItemProps {
  insight: LearningInsight;
  priorityLabel: string;
  onApply: () => void;
  onDismiss: () => void;
}

function InsightItem({ insight, priorityLabel, onApply, onDismiss }: InsightItemProps) {
  const priorityColor = {
    high: "bg-red-500",
    medium: "bg-yellow-500",
    low: "bg-green-500",
  }[insight.priority];

  return (
    <div className="flex items-start gap-2 rounded-lg border border-[var(--color-border)] p-3 bg-[var(--color-bg-primary)]">
      <div className={cn("mt-0.5 h-2 w-2 shrink-0 rounded-full", priorityColor)} />
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-[var(--color-text-primary)]">{priorityLabel} Priority</span>
          <span className="text-[10px] text-[var(--color-text-secondary)]">
            • {insight.source_capability}
          </span>
        </div>
        <p className="text-xs text-[var(--color-text-primary)] mt-1">{insight.text}</p>
      </div>

      {insight.applied ? (
        <span className="text-[10px] text-green-600">Applied</span>
      ) : (
        <div className="flex items-center gap-1">
          <button
            onClick={onApply}
            className="rounded bg-[var(--color-accent)]/10 px-2 py-0.5 text-[10px] text-[var(--color-accent)] hover:bg-[var(--color-accent)]/20"
          >
            Apply
          </button>
          <button
            onClick={onDismiss}
            className="rounded bg-[var(--color-bg-tertiary)] px-2 py-0.5 text-[10px] text-[var(--color-text-secondary)] hover:bg-[var(--color-border)]"
          >
            Dismiss
          </button>
        </div>
      )}
    </div>
  );
}
