"use client";

import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useCognitiveStore } from "@/store/cognitive-store";
import type { ThinkingMode } from "@/types/cognitive";
import { CognitiveLayer } from "@/types/cognitive";
import { cn } from "@/lib/utils";
import { ReasoningChain } from "./reasoning-chain";
import { ConfidenceMeter } from "./confidence-meter";
import { ComparisonView } from "./comparison-view";
import { ThinkingModeIndicator } from "./thinking-mode-indicator";
import { useEffect, useState } from "react";
import type { ExecutionSession } from "@/types/execution";
import { useExecutionStore } from "@/store/execution-store";

interface System2AnalyticalLayerProps {
  className?: string;
}

export function System2AnalyticalLayer({ className }: System2AnalyticalLayerProps) {
  const currentLayer = useCognitiveStore((s) => s.current_layer);
  const setLayer = useCognitiveStore((s) => s.setLayer);
  const thinkingMode = useCognitiveStore((s) => s.thinking_mode);
  const activeCapability = useCognitiveStore((s) => s.active_capability);
  const executionContext = useCognitiveStore((s) => s.execution_context);
  const metaFlags = useCognitiveStore((s) => s.meta_cognitive_flags);

  const executions = useExecutionStore((s) => s.executions);
  const activeExecutionId = useExecutionStore((s) => s.activeExecutionId);
  const loadExecutions = useExecutionStore((s) => s.loadExecutions);
  const [executionsList, setExecutionsList] = useState<ExecutionSession[]>([]);

  useEffect(() => {
    void loadExecutions();
  }, [loadExecutions]);

  useEffect(() => {
    const list = Object.values(executions);
    setExecutionsList(list);
  }, [executions]);

  const activeExecution = activeExecutionId
    ? executions[activeExecutionId]
    : executionsList.find((e) => ["pending", "planning", "running", "waiting_approval", "paused"].includes(e.status));

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
              {thinkingMode
                ? `Analyzing: ${thinkingMode.mode}`
                : activeExecution
                ? `Execution: ${activeExecution.goal}`
                : "No active analysis"}
            </CardDescription>
          </CardHeader>
          <div className="p-4">
            <div className="space-y-3">
              <InputAnalysisCard
                label="Input Analysis"
                description="Perception and input processing"
                activeCapability={activeCapability ?? undefined}
                execution={activeExecution}
              />
              <ReasoningAnalysisCard thinkingMode={thinkingMode} />
              <DecisionAnalysisCard thinkingMode={thinkingMode} execution={activeExecution} />
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Comparison View</CardTitle>
            <CardDescription>Side-by-side capability and reasoning comparison</CardDescription>
          </CardHeader>
          <div className="p-4">
            <ComparisonView />
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
            <ReasoningChain />
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Analysis Metrics</CardTitle>
            <CardDescription>Performance indicators</CardDescription>
          </CardHeader>
          <div className="p-4 space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <StatusItem label="Steps" value={thinkingMode?.reasoning_chain.length?.toString() || "0"} />
              <StatusItem label="Confidence" value={thinkingMode ? `${Math.round(thinkingMode.confidence * 100)}%` : "—"} />
              <StatusItem label="Alternatives" value={thinkingMode?.alternatives.length?.toString() || "0"} />
              <StatusItem label="Uncertainty" value={metaFlags.uncertainty ? "High" : "Low"} />
            </div>
            <div className="pt-2">
              <ThinkingModeIndicator />
            </div>
            <div className="pt-2">
              <ConfidenceMeter />
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

function InputAnalysisCard({
  label,
  description,
  activeCapability,
  execution,
}: {
  label: string;
  description: string;
  activeCapability?: string;
  execution?: ExecutionSession;
}) {
  return (
    <div className="rounded-lg border border-dashed border-[var(--color-border)] p-3 bg-[var(--color-bg-primary)]">
      <div className="text-xs font-medium text-[var(--color-text-primary)] mb-1">{label}</div>
      <div className="text-xs text-[var(--color-text-secondary)] mb-2">{description}</div>
      {activeCapability && (
        <div className="text-xs">
          <span className="text-[var(--color-text-secondary)]">Capability:</span>{" "}
          <span className="text-[var(--color-text-primary)]">{activeCapability}</span>
        </div>
      )}
      {execution && (
        <div className="text-xs mt-1">
          <span className="text-[var(--color-text-secondary)]">Goal:</span>{" "}
          <span className="text-[var(--color-text-primary)]">{execution.goal}</span>
        </div>
      )}
    </div>
  );
}

function ReasoningAnalysisCard({ thinkingMode }: { thinkingMode: ThinkingMode | null }) {
  const steps = thinkingMode?.reasoning_chain ?? [];
  const hasSteps = steps.length > 0;

  return (
    <div className="rounded-lg border border-[var(--color-border)] p-3 bg-[var(--color-bg-primary)]">
      <div className="text-xs font-medium text-[var(--color-text-primary)] mb-1">Reasoning Chain</div>
      <div className="text-xs text-[var(--color-text-secondary)] mb-2">Step-by-step logic from cognitive services</div>
      {hasSteps ? (
        <div className="space-y-1">
          {steps.map((step, i) => (
            <div key={step.step_id} className="flex items-center gap-2 text-xs">
              <span className="text-[var(--color-text-tertiary)]">{i + 1}.</span>
              <span className="text-[var(--color-text-primary)]">{step.service}</span>
              <span className="text-[var(--color-text-tertiary)] capitalize">({step.status})</span>
            </div>
          ))}
        </div>
      ) : (
        <span className="text-xs text-[var(--color-text-secondary)]">No reasoning steps recorded yet.</span>
      )}
    </div>
  );
}

function DecisionAnalysisCard({
  thinkingMode,
  execution,
}: {
  thinkingMode: ThinkingMode | null;
  execution?: ExecutionSession;
}) {
  const alternatives = thinkingMode?.alternatives ?? [];
  const decisionConfidence = thinkingMode?.confidence;
  const phaseCount = execution?.phases?.length ?? 0;
  const progress = execution?.progress ?? 0;

  return (
    <div className="rounded-lg border border-[var(--color-border)] p-3 bg-[var(--color-bg-primary)]">
      <div className="text-xs font-medium text-[var(--color-text-primary)] mb-1">Decision Output</div>
      <div className="text-xs text-[var(--color-text-secondary)] mb-2">Selected option with confidence</div>
      {decisionConfidence !== undefined && (
        <div className="text-xs">
          <span className="text-[var(--color-text-secondary)]">Confidence:</span>{" "}
          <span className="text-[var(--color-text-primary)]">{Math.round(decisionConfidence * 100)}%</span>
        </div>
      )}
      {alternatives.length > 0 && (
        <div className="text-xs mt-1">
          <span className="text-[var(--color-text-secondary)]">Alternatives considered:</span>{" "}
          <span className="text-[var(--color-text-primary)]">{alternatives.join(", ")}</span>
        </div>
      )}
      {phaseCount > 0 && (
        <div className="text-xs mt-1">
          <span className="text-[var(--color-text-secondary)]">Execution phases:</span>{" "}
          <span className="text-[var(--color-text-primary)]">{phaseCount}</span>
        </div>
      )}
      {progress > 0 && (
        <div className="text-xs mt-1">
          <span className="text-[var(--color-text-secondary)]">Progress:</span>{" "}
          <span className="text-[var(--color-text-primary)]">{progress}%</span>
        </div>
      )}
      {!decisionConfidence && !alternatives.length && !phaseCount && (
        <span className="text-xs text-[var(--color-text-secondary)]">No decision recorded yet.</span>
      )}
    </div>
  );
}

function StatusItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col">
      <span className="text-xs text-[var(--color-text-secondary)]">{label}</span>
      <span className="text-sm font-medium text-[var(--color-text-primary)] transition-colors duration-150">{value}</span>
    </div>
  );
}
