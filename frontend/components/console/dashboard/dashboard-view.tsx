"use client";

import { useState } from "react";
import { DashboardMetrics, RuntimeSignalStrip } from "@/components/console/dashboard/dashboard-metrics";
import { PackCatalogPanel } from "@/components/console/dashboard/pack-catalog-panel";
import { BenchmarkOverviewPanel } from "@/components/console/dashboard/benchmark-overview-panel";
import { ActiveWorkflowPanel } from "@/components/console/dashboard/active-workflow-panel";
import { TradingPanel } from "@/components/console/dashboard/trading-panel";
import { EvaluationSummary } from "@/components/console/evaluation/evaluation-summary";
import { PageHeader } from "@/components/console/ui/panel";
import { useConsoleStore } from "@/store/console-store";
import { useConsoleHydration } from "@/features/console/use-console";
import { relativeTime } from "@/lib/format";

export function DashboardView() {
  useConsoleHydration("governance", "benchmark", "evaluation");
  const [blueprintId, setBlueprintId] = useState<string | undefined>();
  const evaluation = useConsoleStore((s) => s.evaluation);
  const evaluationResults = useConsoleStore((s) => s.evaluationResults.data);
  const running = useConsoleStore((s) => s.loading.includes("evaluation"));
  const runEvaluation = useConsoleStore((s) => s.runEvaluation);
  const lastSyncAt = useConsoleStore((s) => s.lastSyncAt);

  const latestResult =
    evaluation.data ?? evaluationResults?.results?.[evaluationResults.results.length - 1] ?? null;

  return (
    <div className="space-y-4">
      <PageHeader
        title="Governance Dashboard"
        description="Live capability governance, benchmark health and pipeline state from the ECP backend"
        actions={<RuntimeSignalStrip />}
      />

      <DashboardMetrics />

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_minmax(0,1.55fr)]">
        <PackCatalogPanel />
        <BenchmarkOverviewPanel />
      </div>

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)]">
        <ActiveWorkflowPanel blueprintId={blueprintId} onSelect={setBlueprintId} />
        <EvaluationSummary
          result={latestResult}
          running={running}
          onRun={() => runEvaluation("")}
          footer={
            <span className="text-[var(--ecp-text-dim)]">
              Synced {relativeTime(lastSyncAt)}
            </span>
          }
        />
      </div>
    </div>
  );
}