"use client";

import Link from "next/link";
import { AlertCircle, Check, Play, Sparkles, TrendingUp } from "lucide-react";
import { Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { Pill } from "@/components/console/ui/states";
import { formatNumber, titleCase } from "@/lib/format";
import type { EvaluationResult } from "@/types/console";

export function DimensionScore({ value, threshold }: { value: number; threshold: number }) {
  const pass = value >= threshold;
  return (
    <span
      className={
        pass
          ? "font-mono text-[11px] text-[var(--ecp-gov)]"
          : "font-mono text-[11px] text-[var(--ecp-alert)]"
      }
    >
      {formatNumber(value, 2)}
    </span>
  );
}

export function EvaluationSummary({
  result,
  title = "Evaluation Results",
  subtitle,
  running = false,
  onRun,
  runLabel = "Run evaluation",
  footer,
}: {
  result: EvaluationResult | null;
  title?: string;
  subtitle?: string;
  running?: boolean;
  onRun?: () => void;
  runLabel?: string;
  footer?: React.ReactNode;
}) {
  return (
    <Panel className="h-full">
      <PanelHeader
        title={title}
        subtitle={subtitle}
        actions={
          onRun ? (
            <button
              type="button"
              onClick={onRun}
              disabled={running}
              className="flex items-center gap-1.5 rounded-md bg-[var(--ecp-blue)] px-2.5 py-1.5 text-[11px] font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              <Play className="h-3 w-3" />
              {running ? "Evaluating…" : runLabel}
            </button>
          ) : null
        }
      />

      <PanelBody className="space-y-4">
        {!result ? (
          <div className="rounded-lg border border-dashed border-[var(--ecp-border)] px-4 py-8 text-center">
            <Sparkles className="mx-auto mb-2 h-5 w-5 text-[var(--ecp-text-dim)]" />
            <p className="text-xs text-[var(--ecp-text-muted)]">
              No evaluation output yet.
            </p>
            <p className="mx-auto mt-1 max-w-xs text-[11px] text-[var(--ecp-text-dim)]">
              Run the evaluator against an execution output to populate accuracy and
              improvement notes.
            </p>
          </div>
        ) : (
          <>
            <section>
              <div className="mb-2 flex items-center justify-between">
                <h3 className="text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
                  Accuracy
                </h3>
                <Pill tone={result.passed ? "good" : "bad"}>
                  {result.passed ? "passed" : "below threshold"} ·{" "}
                  {formatNumber(result.score, 2)}/{formatNumber(result.threshold, 2)}
                </Pill>
              </div>
              <ul className="space-y-1.5">
                {result.dimensions.map((dimension) => {
                  const pass = dimension.score >= result.threshold;
                  return (
                    <li
                      key={dimension.dimension}
                      className="flex items-start gap-2 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2"
                    >
                      {pass ? (
                        <Check className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[var(--ecp-gov)]" />
                      ) : (
                        <AlertCircle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[var(--ecp-alert)]" />
                      )}
                      <span className="min-w-0 flex-1">
                        <span className="flex items-center justify-between gap-2 text-xs text-[var(--ecp-text)]">
                          <span className="truncate">{titleCase(dimension.dimension)}</span>
                          <DimensionScore value={dimension.score} threshold={result.threshold} />
                        </span>
                        {dimension.feedback && (
                          <span className="mt-0.5 block text-[11px] text-[var(--ecp-text-dim)]">
                            {dimension.feedback}
                          </span>
                        )}
                      </span>
                    </li>
                  );
                })}
              </ul>
            </section>

            <section>
              <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
                Improvements
              </h3>
              {result.insights.length === 0 ? (
                <p className="text-[11px] text-[var(--ecp-text-dim)]">
                  The evaluator produced no improvement notes for this output.
                </p>
              ) : (
                <ul className="space-y-1.5">
                  {result.insights.map((insight) => (
                    <li
                      key={insight}
                      className="flex items-start gap-2 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2 text-[11px] text-[var(--ecp-text-muted)]"
                    >
                      <TrendingUp className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[var(--ecp-alert)]" />
                      <span className="min-w-0 flex-1">{insight}</span>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </>
        )}
      </PanelBody>

      {footer && (
        <div className="flex items-center gap-3 border-t border-[var(--ecp-border)] px-4 py-2.5 text-[11px]">
          {footer}
          <Link
            href="/console/evaluation"
            className="ml-auto text-[var(--ecp-gov)] hover:underline"
          >
            Open evaluation workspace
          </Link>
        </div>
      )}
    </Panel>
  );
}