"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useCognitiveStore } from "@/store/cognitive-store";
import { CognitiveLayer } from "@/types/cognitive";
import { cn } from "@/lib/utils";

interface System2AnalyticalLayerProps {
  className?: string;
}

export function System2AnalyticalLayer({ className }: System2AnalyticalLayerProps) {
  const currentLayer = useCognitiveStore((s) => s.current_layer);
  const setLayer = useCognitiveStore((s) => s.setLayer);
  const thinkingMode = useCognitiveStore((s) => s.thinking_mode);

  if (currentLayer !== CognitiveLayer.ANALYTICAL) {
    return (
      <div className={cn("flex items-center justify-center h-full", className)}>
        <div className="text-center">
          <p className="text-sm text-[var(--color-text-secondary)] mb-3">
            System 2 is inactive. Switch to L2 for analytical workspace.
          </p>
          <button
            onClick={() => setLayer(CognitiveLayer.ANALYTICAL)}
            className="px-4 py-2 rounded-lg bg-[var(--color-secondary-500)] text-white text-sm font-medium hover:bg-[var(--color-secondary-600)] transition-colors"
          >
            Activate System 2
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={cn("grid grid-cols-1 lg:grid-cols-3 gap-4 p-4 h-full overflow-y-auto", className)}>
      <div className="lg:col-span-2 space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Execution Workspace</CardTitle>
            <CardDescription>
              {thinkingMode ? `Analyzing: ${thinkingMode.mode}` : "No active analysis"}
            </CardDescription>
          </CardHeader>
          <div className="p-4">
            <div className="space-y-3">
              <WorkspacePlaceholder label="Input Analysis" description="Perception output" />
              <WorkspacePlaceholder label="Reasoning Chain" description="Step-by-step logic" />
              <WorkspacePlaceholder label="Decision Output" description="Selected option with confidence" />
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Comparison View</CardTitle>
            <CardDescription>Side-by-side capability results</CardDescription>
          </CardHeader>
          <div className="p-4">
            <div className="grid grid-cols-2 gap-4">
              <WorkspacePlaceholder label="Option A" description="Alternative 1" />
              <WorkspacePlaceholder label="Option B" description="Alternative 2" />
            </div>
          </div>
        </Card>
      </div>

      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Reasoning Chain</CardTitle>
            <CardDescription>Step-by-step analysis</CardDescription>
          </CardHeader>
          <div className="p-4">
            <ReasoningChainPlaceholder />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Analysis Metrics</CardTitle>
            <CardDescription>Performance indicators</CardDescription>
          </CardHeader>
          <div className="p-4 grid grid-cols-2 gap-3">
            <StatusItem label="Steps" value={thinkingMode?.reasoning_chain.length?.toString() || "0"} />
            <StatusItem label="Confidence" value={thinkingMode ? `${Math.round(thinkingMode.confidence * 100)}%` : "—"} />
            <StatusItem label="Alternatives" value={thinkingMode?.alternatives.length?.toString() || "0"} />
            <StatusItem label="Status" value="Analyzing" />
          </div>
        </Card>
      </div>
    </div>
  );
}

function WorkspacePlaceholder({ label, description }: { label: string; description: string }) {
  return (
    <div className="rounded-lg border border-dashed border-[var(--color-border)] p-4 bg-[var(--color-bg-primary)]">
      <div className="text-xs font-medium text-[var(--color-text-primary)] mb-1">{label}</div>
      <div className="text-xs text-[var(--color-text-secondary)]">{description}</div>
    </div>
  );
}

function ReasoningChainPlaceholder() {
  return (
    <div className="space-y-2">
      {[
        { service: "perception", status: "completed" },
        { service: "memory", status: "completed" },
        { service: "reasoning", status: "running" },
        { service: "planning", status: "pending" },
        { service: "decision", status: "pending" },
      ].map((step, i) => (
        <div key={i} className="flex items-center gap-2 text-xs">
          <div
            className={cn(
              "w-2 h-2 rounded-full",
              step.status === "completed" && "bg-green-500",
              step.status === "running" && "bg-yellow-500 animate-pulse",
              step.status === "pending" && "bg-gray-300"
            )}
          />
          <span className="text-[var(--color-text-primary)]">{step.service}</span>
          <span className="text-[var(--color-text-secondary)] capitalize">{step.status}</span>
        </div>
      ))}
    </div>
  );
}

function StatusItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="text-xs text-[var(--color-text-secondary)]">{label}</span>
      <span className="text-sm font-medium text-[var(--color-text-primary)]">{value}</span>
    </div>
  );
}
