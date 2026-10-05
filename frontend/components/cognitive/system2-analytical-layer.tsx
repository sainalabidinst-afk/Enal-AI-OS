"use client";

import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { useCognitiveStore } from "@/store/cognitive-store";
import type { ReasoningStep, ThinkingMode } from "@/types/cognitive";
import { CognitiveLayer } from "@/types/cognitive";
import { cn } from "@/lib/utils";
import { ReasoningChain } from "./reasoning-chain";
import { ConfidenceMeter } from "./confidence-meter";
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
  const metaFlags = useCognitiveStore((s) => s.meta_cognitive_flags);
  const reasoningChain = useCognitiveStore((s) => thinkingMode?.reasoning_chain ?? []);
  const confidence = useCognitiveStore((s) => thinkingMode?.confidence ?? 0);

  const executions = useExecutionStore((s) => s.executions);
  const activeExecutionId = useExecutionStore((s) => s.activeExecutionId);
  const loadExecutions = useExecutionStore((s) => s.loadExecutions);
  const loadLogs = useExecutionStore((s) => s.loadLogs);
  const loadArtifacts = useExecutionStore((s) => s.loadArtifacts);
  const [executionsList, setExecutionsList] = useState<ExecutionSession[]>([]);
  const [activeLogs, setActiveLogs] = useState<Array<Record<string, any>>>([]);
  const [activeArtifacts, setActiveArtifacts] = useState<any[]>([]);
  const [isLoadingArtifacts, setIsLoadingArtifacts] = useState(false);

  useEffect(() => {
    void loadExecutions();
  }, [loadExecutions]);

  useEffect(() => {
    const list = Object.values(executions);
    setExecutionsList(list);
  }, [executions]);

  useEffect(() => {
    if (activeExecutionId) {
      void loadLogs(activeExecutionId);
    }
  }, [activeExecutionId, loadLogs]);

  const activeExecution = activeExecutionId
    ? executions[activeExecutionId]
    : executionsList.find((e) => ["pending", "planning", "running", "waiting_approval", "paused"].includes(e.status));

  const handleArtifactLoad = async () => {
    if (!activeExecution?.id) return;
    setIsLoadingArtifacts(true);
    try {
      const artifacts = await loadArtifacts(activeExecution.id);
      setActiveArtifacts(artifacts || []);
    } catch {
      setActiveArtifacts([]);
    } finally {
      setIsLoadingArtifacts(false);
    }
  };

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

  const phases = activeExecution?.phases ?? [];
  const progress = activeExecution?.progress ?? 0;
  const eta = activeExecution?.eta_seconds;

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
              <ReasoningAnalysisCard steps={reasoningChain} />
              <DecisionAnalysisCard
                thinkingMode={thinkingMode}
                execution={activeExecution}
                confidence={confidence}
              />
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Execution Timeline</CardTitle>
            <CardDescription>
              Phase-based progress{eta !== undefined && eta !== null ? ` • ETA: ${eta}s` : ""}
            </CardDescription>
          </CardHeader>
          <div className="p-4">
            {phases.length > 0 ? (
              <div className="space-y-2">
                {phases.map((phase: any, i: number) => (
                  <div key={phase.id ?? i} className="flex items-center gap-3 text-xs">
                    <div className="flex-1">
                      <div className="flex justify-between">
                        <span className="font-medium text-[var(--color-text-primary)]">{phase.name ?? `Phase ${i + 1}`}</span>
                        <span className={`capitalize ${
                          phase.status === "completed" ? "text-green-600" :
                          phase.status === "running" ? "text-blue-600" :
                          phase.status === "failed" ? "text-red-600" : "text-[var(--color-text-secondary)]"
                        }`}>{phase.status ?? "pending"}</span>
                      </div>
                      <div className="text-[var(--color-text-tertiary)] mt-1">
                        Progress: {phase.progress ?? 0}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <span className="text-xs text-[var(--color-text-secondary)]">
                {progress > 0 ? `Overall progress: ${progress}%` : "No execution phases recorded yet."}
              </span>
            )}
            {progress > 0 && (
              <div className="mt-3">
                <div className="flex justify-between text-xs mb-1">
                  <span>Overall Progress</span>
                  <span>{progress}%</span>
                </div>
                <div className="w-full h-2 bg-[var(--color-bg-tertiary)] rounded-full overflow-hidden">
                  <div
                    className="h-full bg-[var(--color-secondary-500)] transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              </div>
            )}
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Execution Artifacts</CardTitle>
            <CardDescription>Generated outputs and evidence</CardDescription>
          </CardHeader>
          <div className="p-4">
            <button
              onClick={handleArtifactLoad}
              disabled={isLoadingArtifacts || !activeExecution?.id}
              className="px-3 py-1.5 rounded text-xs font-medium bg-[var(--color-bg-tertiary)] hover:bg-[var(--color-border)] disabled:opacity-50 transition-colors"
            >
              {isLoadingArtifacts ? "Loading..." : "Load Artifacts"}
            </button>
            {activeArtifacts.length > 0 && (
              <div className="mt-3 space-y-2">
                {activeArtifacts.map((artifact) => (
                  <div key={artifact.id} className="text-xs">
                    <span className="font-medium text-[var(--color-text-primary)]">{artifact.name}</span>
                    <span className="text-[var(--color-text-tertiary)]"> ({artifact.type})</span>
                  </div>
                ))}
              </div>
            )}
            {activeArtifacts.length === 0 && !isLoadingArtifacts && (
              <span className="text-xs text-[var(--color-text-secondary)] mt-2 block">
                No artifacts loaded. Click &quot;Load Artifacts&quot; to fetch.
              </span>
            )}
          </div>
        </Card>
      </div>

      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Analysis Metrics</CardTitle>
            <CardDescription>Performance indicators</CardDescription>
          </CardHeader>
          <div className="p-4 space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <StatusItem label="Steps" value={reasoningChain.length.toString()} />
              <StatusItem label="Confidence" value={confidence > 0 ? `${Math.round(confidence * 100)}%` : "—"} />
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

        <Card>
          <CardHeader>
            <CardTitle>Recent Executions</CardTitle>
            <CardDescription>History ({executionsList.length})</CardDescription>
          </CardHeader>
          <div className="p-4">
            {executionsList.length > 0 ? (
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {executionsList.slice(0, 5).map((exec) => (
                  <div key={exec.id} className="text-xs">
                    <div className="font-medium text-[var(--color-text-primary)] truncate">{exec.goal}</div>
                    <div className="flex justify-between text-[var(--color-text-tertiary)]">
                      <span>{new Date(exec.created_at).toLocaleTimeString()}</span>
                      <span className={`capitalize ${
                        exec.status === "completed" ? "text-green-600" :
                        exec.status === "failed" ? "text-red-600" :
                        exec.status === "running" ? "text-blue-600" : "text-[var(--color-text-tertiary)]"
                      }`}>{exec.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <span className="text-xs text-[var(--color-text-secondary)]">No recent executions.</span>
            )}
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Execution Logs</CardTitle>
            <CardDescription>Real-time execution output</CardDescription>
          </CardHeader>
          <div className="p-4">
            {activeLogs.length > 0 ? (
              <div className="space-y-1 max-h-40 overflow-y-auto">
                {activeLogs.slice(-10).map((log, i) => (
                  <div key={i} className="text-xs">
                    <span className={`[${log.level ?? "info"}]`} /> {log.message}
                  </div>
                ))}
              </div>
            ) : (
              <span className="text-xs text-[var(--color-text-secondary)]">
                {activeExecutionId ? "No logs loaded." : "Select an execution to view logs."}
              </span>
            )}
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

function ReasoningAnalysisCard({ steps }: { steps: ReasoningStep[] }) {
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
  confidence,
}: {
  thinkingMode: ThinkingMode | null;
  execution?: ExecutionSession;
  confidence: number;
}) {
  const alternatives = thinkingMode?.alternatives ?? [];
  const phaseCount = execution?.phases?.length ?? 0;
  const progress = execution?.progress ?? 0;
  const decisionConfidence = confidence;

  return (
    <div className="rounded-lg border border-[var(--color-border)] p-3 bg-[var(--color-bg-primary)]">
      <div className="text-xs font-medium text-[var(--color-text-primary)] mb-1">Decision Output</div>
      <div className="text-xs text-[var(--color-text-secondary)] mb-2">Selected option with confidence</div>
      {decisionConfidence > 0 && (
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
      {!(decisionConfidence > 0) && !alternatives.length && !phaseCount && (
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
