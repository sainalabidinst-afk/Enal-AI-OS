"use client";

import { useState, useMemo } from "react";
import { useCognitiveStore } from "@/store/cognitive-store";
import type { ThinkingMode, ReasoningStep } from "@/types/cognitive";
import { cn } from "@/lib/utils";

export function ComparisonView() {
  const thinkingHistory = useCognitiveStore((s) => s.thinkingHistory);
  const setLayer = useCognitiveStore((s) => s.setLayer);
  const [selectedA, setSelectedA] = useState<string | null>(null);
  const [selectedB, setSelectedB] = useState<string | null>(null);

  const completed = useMemo(
    () => thinkingHistory.filter((t) => t.completed_at),
    [thinkingHistory]
  );

  const autoSelect = (index: number, side: "A" | "B") => {
    if (completed.length === 0) return;
    const idx = Math.min(index, completed.length - 1);
    const id = completed[idx]?.started_at ?? null;
    if (side === "A") setSelectedA(id);
    else setSelectedB(id);
  };

  if (completed.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-xs text-[var(--color-text-secondary)] mb-3">
          No completed thinking modes available for comparison.
        </p>
        <p className="text-xs text-[var(--color-text-secondary)]">
          Complete an analysis in System 2 to see side-by-side comparison here.
        </p>
      </div>
    );
  }

  if (completed.length === 1) {
    autoSelect(0, "A");
    autoSelect(0, "B");
  } else {
    if (!selectedA) autoSelect(0, "A");
    if (!selectedB) autoSelect(1, "B");
  }

  const modeA = completed.find((t) => t.started_at === selectedA);
  const modeB = completed.find((t) => t.started_at === selectedB);

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-xs">
        <span className="text-[var(--color-text-secondary)]">Compare:</span>
        <select
          value={selectedA ?? ""}
          onChange={(e) => setSelectedA(e.target.value || null)}
          className="text-[10px] rounded border border-[var(--color-border)] bg-[var(--color-bg-primary)] text-[var(--color-text-primary)] px-1.5 py-0.5"
        >
          {completed.map((t) => (
            <option key={`A-${t.started_at}`} value={t.started_at}>
              {formatModeLabel(t)}
            </option>
          ))}
        </select>
        <span className="text-[var(--color-text-secondary)]">vs</span>
        <select
          value={selectedB ?? ""}
          onChange={(e) => setSelectedB(e.target.value || null)}
          className="text-[10px] rounded border border-[var(--color-border)] bg-[var(--color-bg-primary)] text-[var(--color-text-primary)] px-1.5 py-0.5"
        >
          {completed.map((t) => (
            <option key={`B-${t.started_at}`} value={t.started_at}>
              {formatModeLabel(t)}
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {modeA && <ComparisonCard mode={modeA} label="Option A" color="border-blue-500/50" />}
        {modeB && <ComparisonCard mode={modeB} label="Option B" color="border-pink-500/50" />}
      </div>
    </div>
  );
}

function formatModeLabel(mode: ThinkingMode): string {
  const date = new Date(mode.started_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  return `${mode.mode} @ ${date}`;
}

interface ComparisonCardProps {
  mode: ThinkingMode;
  label: string;
  color: string;
}

function ComparisonCard({ mode, label, color }: ComparisonCardProps) {
  const stepCount = mode.reasoning_chain.length;
  const completedSteps = mode.reasoning_chain.filter((s) => s.status === "completed").length;
  const avgDuration =
    stepCount > 0
      ? mode.reasoning_chain.reduce((sum, s) => sum + s.duration_ms, 0) / stepCount
      : 0;

  return (
    <div className={cn("rounded-lg border-2 bg-[var(--color-bg-secondary)] p-3", color)}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-medium text-[var(--color-text-primary)]">{label}</span>
        <span className="text-xs text-[var(--color-text-secondary)]">
          {Math.round(mode.confidence * 100)}% confidence
        </span>
      </div>

      <div className="space-y-1.5 mb-3">
        <div className="flex justify-between text-[10px]">
          <span className="text-[var(--color-text-secondary)]">Steps</span>
          <span className="text-[var(--color-text-primary)]">{stepCount}</span>
        </div>
        <div className="flex justify-between text-[10px]">
          <span className="text-[var(--color-text-secondary)]">Completed</span>
          <span className="text-[var(--color-text-primary)]">{completedSteps}</span>
        </div>
        <div className="flex justify-between text-[10px]">
          <span className="text-[var(--color-text-secondary)]">Avg Duration</span>
          <span className="text-[var(--color-text-primary)]">{Math.round(avgDuration)}ms</span>
        </div>
      </div>

      <div className="space-y-1">
        {mode.reasoning_chain.slice(0, 4).map((step: ReasoningStep) => (
          <div key={step.step_id} className="flex items-center gap-2 text-[10px]">
            <div
              className={cn(
                "w-1.5 h-1.5 rounded-full shrink-0",
                step.status === "completed" && "bg-green-500",
                step.status === "running" && "bg-yellow-500",
                step.status === "failed" && "bg-red-500",
                step.status === "pending" && "bg-gray-400"
              )}
            />
            <span className="truncate text-[var(--color-text-secondary)]">{step.service}</span>
            <span className="ml-auto text-[var(--color-text-tertiary)]">{step.duration_ms}ms</span>
          </div>
        ))}
        {stepCount > 4 && (
          <div className="text-[10px] text-[var(--color-text-tertiary)]">
            +{stepCount - 4} more steps
          </div>
        )}
      </div>
    </div>
  );
}
