"use client";

import { useCognitiveStore } from "@/store/cognitive-store";
import type { ReasoningStep } from "@/types/cognitive";
import { cn } from "@/lib/utils";

export function ReasoningChain() {
  const thinkingMode = useCognitiveStore((s) => s.thinking_mode);

  if (!thinkingMode || thinkingMode.reasoning_chain.length === 0) {
    return (
      <div className="text-xs text-[var(--color-text-secondary)]">
        No reasoning chain available. Start an analysis to see step-by-step reasoning.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {thinkingMode.reasoning_chain.map((step: ReasoningStep, index: number) => (
        <div key={step.step_id} className="flex gap-3">
          <div className="flex flex-col items-center">
            <div
              className={cn(
                "w-3 h-3 rounded-full border-2",
                step.status === "completed" && "border-green-500 bg-green-500",
                step.status === "running" && "border-yellow-500 bg-yellow-500 animate-pulse",
                step.status === "failed" && "border-red-500 bg-red-500",
                step.status === "pending" && "border-gray-300 bg-transparent"
              )}
            />
            {index < thinkingMode.reasoning_chain.length - 1 && (
              <div className="w-0.5 h-6 bg-[var(--color-border)] mt-1" />
            )}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-[var(--color-text-primary)]">{step.service}</span>
              <span className="text-xs text-[var(--color-text-secondary)]">{step.duration_ms}ms</span>
            </div>
            <div className="text-xs text-[var(--color-text-secondary)] mt-0.5 capitalize">{step.status}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
