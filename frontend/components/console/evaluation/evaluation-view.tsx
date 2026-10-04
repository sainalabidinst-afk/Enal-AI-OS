"use client";

import { useState } from "react";
import Link from "next/link";
import { Download, Play, Trash2 } from "lucide-react";
import { PageHeader, Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { ConsoleTabs, type TabItem } from "@/components/console/ui/console-tabs";
import { EmptyBlock, Pill } from "@/components/console/ui/states";
import { EvaluationSummary } from "@/components/console/evaluation/evaluation-summary";
import { RadarChart, ChartLegend } from "@/components/console/charts/charts";
import { Field, inputClass } from "@/components/console/ui/controls";
import { useConsoleStore } from "@/store/console-store";
import { useConsoleHydration } from "@/features/console/use-console";
import { formatNumber, relativeTime, titleCase } from "@/lib/format";
import type { EvaluationResult } from "@/types/console";

const TABS: TabItem[] = [
  { id: "run", label: "Run evaluation" },
  { id: "history", label: "Stored results" },
  { id: "schedule", label: "Schedules" },
];

export function EvaluationView() {
  useConsoleHydration("evaluation");
  const evaluation = useConsoleStore((s) => s.evaluation);
  const results = useConsoleStore((s) => s.evaluationResults);
  const schedules = useConsoleStore((s) => s.schedules.data);
  const running = useConsoleStore((s) => s.loading.includes("evaluation"));
  const runEvaluation = useConsoleStore((s) => s.runEvaluation);
  const [tab, setTab] = useState("run");
  const [output, setOutput] = useState("");
  const [selected, setSelected] = useState<EvaluationResult | null>(null);

  const active = selected ?? evaluation.data;

  function exportReport(result: EvaluationResult | null) {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `evaluation-${result.vendor ?? "generic"}-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="space-y-4">
      <PageHeader
        title="Evaluation Results"
        description="Scenario scoring from the evaluator engine with per-dimension feedback"
        actions={
          <button
            type="button"
            onClick={() => exportReport(active)}
            disabled={!active}
            className="flex items-center gap-1.5 rounded-md border border-[var(--ecp-border)] px-3 py-1.5 text-[11px] text-[var(--ecp-text-muted)] transition-colors hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)] disabled:opacity-40"
          >
            <Download className="h-3.5 w-3.5" />
            Export report
          </button>
        }
      />

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_360px]">
        <div className="space-y-4">
          <EvaluationSummary
            result={active}
            running={running}
            onRun={() => runEvaluation(output)}
            subtitle={
              active
                ? `${active.vendor ?? "generic"} · ${active.scenario ?? "scenario"} · threshold ${formatNumber(
                    active.threshold,
                    2
                  )}`
                : "Run the evaluator to populate accuracy dimensions"
            }
          />

          {active && (
            <Panel>
              <PanelHeader
                title="Capability radar"
                subtitle="Score per evaluation dimension against the gate threshold"
              />
              <PanelBody className="grid gap-4 lg:grid-cols-[1fr_220px]">
                <RadarChart
                  labels={active.dimensions.map((dimension) => titleCase(dimension.dimension))}
                  series={[
                    {
                      label: "Score",
                      values: active.dimensions.map((dimension) => dimension.score),
                      color: "#2dd4bf",
                    },
                    {
                      label: "Threshold",
                      values: active.dimensions.map(() => active.threshold),
                      color: "#f59e0b",
                    },
                  ]}
                  max={1}
                />
                <ChartLegend
                  items={[
                    { label: "Dimension score", color: "#2dd4bf" },
                    { label: "Gate threshold", color: "#f59e0b" },
                  ]}
                />
              </PanelBody>
            </Panel>
          )}

          <Panel>
            <ConsoleTabs tabs={TABS} active={tab} onChange={setTab} className="px-2" />
            <PanelBody>
              {tab === "run" && (
                <div className="space-y-3">
                  <Field
                    label="Execution output"
                    hint="Paste the agent output that should be graded against the vendor rubric"
                  >
                    <textarea
                      value={output}
                      onChange={(event) => setOutput(event.target.value)}
                      rows={6}
                      placeholder="Paste configuration review, remediation plan, executive report…"
                      className={inputClass()}
                    />
                  </Field>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => runEvaluation(output)}
                      disabled={running}
                      className="flex items-center gap-1.5 rounded-lg bg-[var(--ecp-blue)] px-3 py-2 text-xs font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
                    >
                      <Play className="h-3.5 w-3.5" />
                      {running ? "Evaluating…" : "Evaluate output"}
                    </button>
                    <Link
                      href="/console/packs/benchmark"
                      className="text-[11px] text-[var(--ecp-gov)] hover:underline"
                    >
                      Browse benchmark dashboard
                    </Link>
                  </div>
                  {evaluation.error && (
                    <p className="text-[11px] text-[var(--ecp-danger)]">{evaluation.error}</p>
                  )}
                </div>
              )}

              {tab === "history" && (
                <ResultHistory
                  results={results.data?.results ?? []}
                  onSelect={(result) => {
                    setSelected(result);
                    setTab("run");
                  }}
                />
              )}

              {tab === "schedule" && (
                <div className="space-y-2">
                  {(schedules ?? []).length === 0 ? (
                    <EmptyBlock
                      title="No evaluation schedules"
                      hint="Register a cron schedule through POST /api/v1/schedule to automate evaluation runs."
                    />
                  ) : (
                    (schedules ?? []).map((job) => (
                      <div
                        key={job.job_id}
                        className="flex items-center gap-3 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2 text-[11px]"
                      >
                        <Pill tone="info">{job.cron}</Pill>
                        <span className="flex-1 text-[var(--ecp-text-muted)]">
                          next {relativeTime(job.next_run)}
                        </span>
                        <Trash2 className="h-3.5 w-3.5 text-[var(--ecp-text-dim)]" />
                      </div>
                    ))
                  )}
                </div>
              )}
            </PanelBody>
          </Panel>
        </div>

        <aside>
          <Panel>
            <PanelHeader title="Evaluation notes" subtitle="How scoring works" />
            <PanelBody className="space-y-2 text-[11px] text-[var(--ecp-text-muted)]">
              <p>
                Scores come from the backend evaluator engine
                (<code className="text-[var(--ecp-sky)]">POST /api/v1/evaluate</code>).
                The console only renders the returned dimensions, insights and threshold.
              </p>
              <p>
                Vendor rules are applied server-side; improvement notes are the engine&apos;s
                recommendations for the evaluated output.
              </p>
              <p className="text-[var(--ecp-text-dim)]">
                Nothing on this page is computed locally — refresh after a run to pull the
                latest result set.
              </p>
            </PanelBody>
          </Panel>
        </aside>
      </div>
    </div>
  );
}

function ResultHistory({
  results,
  onSelect,
}: {
  results: EvaluationResult[];
  onSelect: (result: EvaluationResult) => void;
}) {
  if (results.length === 0) {
    return (
      <EmptyBlock
        title="No stored evaluation results"
        hint="Scheduled evaluations persist here once they run."
      />
    );
  }
  return (
    <ul className="space-y-2">
      {results
        .slice()
        .reverse()
        .map((result, index) => (
          <li key={`${result.case_id ?? "case"}-${index}`}>
            <button
              type="button"
              onClick={() => onSelect(result)}
              className="flex w-full items-center gap-3 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2 text-left transition-colors hover:border-[var(--ecp-border-strong)]"
            >
              <span className="min-w-0 flex-1">
                <span className="block truncate text-[11px] font-medium text-[var(--ecp-text)]">
                  {result.case_id ?? result.scenario ?? "evaluation"}
                </span>
                <span className="block truncate text-[10px] text-[var(--ecp-text-dim)]">
                  {result.vendor ?? "generic"} · {result.dimensions.length} dimensions
                </span>
              </span>
              <Pill tone={result.passed ? "good" : "bad"}>
                {formatNumber(result.score, 2)}
              </Pill>
            </button>
          </li>
        ))}
    </ul>
  );
}