"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, BookOpen, Boxes, Gauge, Plug, RefreshCw, ShieldCheck, Table2, Trophy } from "lucide-react";
import { PageHeader, Panel, PanelBody } from "@/components/console/ui/panel";
import { ConsoleTabs, type TabItem } from "@/components/console/ui/console-tabs";
import { MetricCard } from "@/components/console/ui/metric-card";
import { Pill } from "@/components/console/ui/states";
import { usePackDetail } from "@/features/console/use-pack-detail";
import { useConsoleStore } from "@/store/console-store";
import { formatDurationMs, formatPercent, relativeTime } from "@/lib/format";
import {
  BenchmarksTab,
} from "./pack-benchmarks-tab";
import { RealCasesTab } from "./pack-cases-tab";
import { DocsTab, IntegrationTab } from "./pack-integration-tab";
import { OverviewTab } from "./pack-overview-tab";

const TABS: TabItem[] = [
  { id: "overview", label: "Overview", icon: <Boxes className="h-3.5 w-3.5" /> },
  { id: "benchmarks", label: "Benchmarks", icon: <Trophy className="h-3.5 w-3.5" /> },
  { id: "cases", label: "Real Cases", icon: <Table2 className="h-3.5 w-3.5" /> },
  { id: "integration", label: "Integration", icon: <Plug className="h-3.5 w-3.5" /> },
  { id: "docs", label: "Docs", icon: <BookOpen className="h-3.5 w-3.5" /> },
];

export function PackDetailView({
  packId,
  focusCase,
}: {
  packId: string;
  focusCase?: string | null;
}) {
  const [tab, setTab] = useState("overview");
  const detail = usePackDetail(packId);
  const runQualityGate = useConsoleStore((s) => s.runQualityGate);
  const gateResults = useConsoleStore((s) => s.gateResults.data);
  const gate = gateResults?.[packId];

  const lifecycle = detail.lifecycle;
  const title = detail.governance?.name ?? lifecycle?.name ?? packId;
  const grade = detail.governance?.benchmark_score
    ? `Grade ${Math.round(detail.governance.benchmark_score * 100)}`
    : "Ungraded";

  return (
    <div className="space-y-4">
      <Link
        href="/console/packs"
        className="inline-flex items-center gap-1 text-[11px] text-[var(--ecp-text-muted)] hover:text-[var(--ecp-text)]"
      >
        <ArrowLeft className="h-3 w-3" />
        All capability packs
      </Link>

      <PageHeader
        title={title}
        description={`${packId} · ${lifecycle?.category ?? detail.governance?.domain ?? "unclassified"}`}
        actions={
          <>
            <Pill tone={lifecycle?.health === "healthy" ? "good" : "warn"}>
              {lifecycle?.health ?? detail.governance?.status ?? "untracked"}
            </Pill>
            <span className="rounded-md border border-[var(--ecp-border)] px-2 py-1 text-[11px] text-[var(--ecp-text-muted)]">
              {grade}
            </span>
            <button
              type="button"
              onClick={() => {
                detail.refresh();
              }}
              className="grid h-7 w-7 place-items-center rounded-md border border-[var(--ecp-border)] text-[var(--ecp-text-muted)] transition-colors hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)]"
              title="Reload pack data"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${detail.loading ? "animate-spin" : ""}`} />
            </button>
          </>
        }
      />

      {detail.errors.length > 0 && (
        <div className="rounded-lg border border-[var(--ecp-alert)]/40 bg-[var(--ecp-alert-soft)] px-3 py-2 text-[11px] text-[var(--ecp-alert)]">
          Partial data — {detail.errors.join(" · ")}
        </div>
      )}

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_320px]">
        <div className="min-w-0 space-y-4">
          <ConsoleTabs tabs={TABS} active={tab} onChange={setTab} />
          <Panel>
            <PanelBody>
              {detail.loading ? (
                <p className="py-10 text-center text-xs text-[var(--ecp-text-dim)]">
                  Loading pack detail…
                </p>
              ) : tab === "overview" ? (
                <OverviewTab detail={detail} />
              ) : tab === "benchmarks" ? (
                <BenchmarksTab detail={detail} />
              ) : tab === "cases" ? (
                <RealCasesTab focusCase={focusCase} />
              ) : tab === "integration" ? (
                <IntegrationTab detail={detail} />
              ) : (
                <DocsTab detail={detail} />
              )}
            </PanelBody>
          </Panel>
        </div>

        <aside className="space-y-3">
          <Panel>
            <PanelBody className="space-y-3">
              <h3 className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
                <ShieldCheck className="h-3.5 w-3.5" />
                Governance metrics
              </h3>
              <MetricCard
                label="Benchmark score"
                value={formatPercent(detail.governance?.benchmark_score)}
                tone="gov"
                hint="quality gate input"
              />
              <MetricCard
                label="Test coverage"
                value={formatPercent(detail.governance?.coverage)}
                tone="sky"
                hint={`${detail.governance?.tests_passed ?? 0}/${
                  detail.governance?.tests_total ?? 0
                } tests passing`}
              />
              <MetricCard
                label="Avg response"
                value={formatDurationMs(lifecycle?.metrics.avg_latency_ms ?? null)}
                tone="alert"
                hint="reported by the runtime"
              />
            </PanelBody>
          </Panel>

          <Panel>
            <PanelBody className="space-y-3">
              <h3 className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
                <Gauge className="h-3.5 w-3.5" />
                Quality gate
              </h3>
              {gate ? (
                <div className="space-y-2 text-[11px]">
                  <Pill tone={gate.passed ? "good" : "bad"}>
                    {gate.passed ? "gate passed" : "gate rejected"}
                  </Pill>
                  <p className="text-[var(--ecp-text-muted)]">
                    Min score {formatPercent(gate.min_benchmark_score)} · min coverage{" "}
                    {formatPercent(gate.min_coverage)} · min pass rate{" "}
                    {formatPercent(gate.min_test_pass_rate)}
                  </p>
                  <p className="text-[var(--ecp-text-dim)]">
                    Observed {formatPercent(gate.benchmark_score)} /{" "}
                    {formatPercent(gate.coverage)} / {formatPercent(gate.test_pass_rate)}
                  </p>
                </div>
              ) : (
                <>
                  <p className="text-[11px] text-[var(--ecp-text-dim)]">
                    No gate evaluation recorded for this pack yet.
                  </p>
                  <button
                    type="button"
                    onClick={() => runQualityGate(packId)}
                    className="w-full rounded-lg bg-[var(--ecp-gov)] px-3 py-2 text-[11px] font-semibold text-[#04121a] transition-opacity hover:opacity-90"
                  >
                    Evaluate quality gate
                  </button>
                </>
              )}
            </PanelBody>
          </Panel>

          <Panel>
            <PanelBody className="space-y-2 text-[11px] text-[var(--ecp-text-muted)]">
              <h3 className="text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
                Audit trail
              </h3>
              <p>
                Last updated {relativeTime(detail.governance?.updated_at ?? lifecycle?.updated_at)}
              </p>
              <Link
                href={`/console/evaluation?pack=${encodeURIComponent(packId)}`}
                className="block text-[var(--ecp-gov)] hover:underline"
              >
                Evaluate this pack
              </Link>
            </PanelBody>
          </Panel>
        </aside>
      </div>
    </div>
  );
}