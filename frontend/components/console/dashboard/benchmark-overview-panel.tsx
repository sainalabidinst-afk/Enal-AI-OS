"use client";

import { BarChart3, Play, RefreshCw } from "lucide-react";
import { Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { DataTable, type Column } from "@/components/console/ui/data-table";
import { Pill } from "@/components/console/ui/states";
import { BarChart, ChartLegend, CHART_PALETTE } from "@/components/console/charts/charts";
import { useConsoleStore } from "@/store/console-store";
import { formatNumber } from "@/lib/format";
import type { VendorCapabilityScore } from "@/types/console";

export function BenchmarkOverviewPanel() {
  const scores = useConsoleStore((s) => s.capabilityScores);
  const suite = useConsoleStore((s) => s.benchmarkSuite.data);
  const cce = useConsoleStore((s) => s.cceStatus.data);
  const running = useConsoleStore((s) => s.loading.includes("benchmarkRun"));
  const scoresLoading = useConsoleStore((s) => s.loading.includes("capabilityScores"));
  const run = useConsoleStore((s) => s.executeBenchmarkRun);
  const loadScores = useConsoleStore((s) => s.loadCapabilityScores);
  const loadBenchmark = useConsoleStore((s) => s.loadBenchmark);

  const vendors = Object.values(scores.data?.capabilities ?? {});
  const suiteTotals = vendors.reduce(
    (total, vendor) => ({
      cases: total.cases + vendor.cases,
      passed: total.passed + vendor.passed,
      failed: total.failed + vendor.failed,
      avgScore: total.avgScore + vendor.avg_score,
    }),
    { cases: 0, passed: 0, failed: 0, avgScore: 0 }
  );
  const avgScore = vendors.length ? suiteTotals.avgScore / vendors.length : null;

  const columns: Column<VendorCapabilityScore>[] = [
    {
      key: "vendor",
      header: "Component",
      sortable: true,
      sortValue: (row) => row.vendor,
      render: (row) => <span className="text-[var(--ecp-text)]">{row.vendor}</span>,
    },
    {
      key: "cases",
      header: "Scenarios",
      align: "right",
      sortable: true,
      sortValue: (row) => row.cases,
      render: (row) => `${row.cases} tests`,
    },
    {
      key: "score",
      header: "Avg Score",
      align: "right",
      sortable: true,
      sortValue: (row) => row.avg_score,
      render: (row) => formatNumber(row.avg_score),
    },
    {
      key: "capability",
      header: "Capability",
      align: "right",
      sortable: true,
      sortValue: (row) => row.avg_capability_score,
      render: (row) => formatNumber(row.avg_capability_score),
    },
    {
      key: "outcome",
      header: "Notes",
      sortable: true,
      sortValue: (row) => row.failed,
      render: (row) =>
        row.failed === 0 ? (
          <Pill tone="good">all passed</Pill>
        ) : (
          <Pill tone="bad">{row.failed} failing</Pill>
        ),
    },
  ];

  return (
    <Panel className="h-full">
      <PanelHeader
        title="Benchmark Overview"
        subtitle={
          suite
            ? `${suite.name} · ${suite.case_count} cases discovered`
            : "Capability component scores from the benchmark engine"
        }
        actions={
          <>
            <button
              type="button"
              onClick={loadBenchmark}
              className="grid h-7 w-7 place-items-center rounded-md border border-[var(--ecp-border)] text-[var(--ecp-text-muted)] transition-colors hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)]"
              title="Refresh benchmark data"
            >
              <RefreshCw className="h-3.5 w-3.5" />
            </button>
            <button
              type="button"
              onClick={run}
              disabled={running}
              className="flex items-center gap-1.5 rounded-md bg-[var(--ecp-blue)] px-2.5 py-1.5 text-[11px] font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              <Play className="h-3 w-3" />
              {running ? "Running…" : "Run suite"}
            </button>
            {vendors.length === 0 && (
              <button
                type="button"
                onClick={loadScores}
                disabled={scoresLoading}
                className="flex items-center gap-1.5 rounded-md border border-[var(--ecp-gov)] px-2.5 py-1.5 text-[11px] font-semibold text-[var(--ecp-gov)] transition-opacity hover:opacity-80 disabled:opacity-50"
              >
                <BarChart3 className="h-3 w-3" />
                {scoresLoading ? "Scoring…" : "Load scores"}
              </button>
            )}
          </>
        }
      />

      {cce?.status === "error" && (
        <p className="border-b border-[var(--ecp-border)] bg-[var(--ecp-danger-soft)] px-4 py-1.5 text-[11px] text-[var(--ecp-danger)]">
          CCE history: {cce.message}
        </p>
      )}

      <PanelBody className="p-0">
        {scores.status === "loading" && vendors.length === 0 ? (
          <div className="space-y-2 p-4">
            {Array.from({ length: 5 }).map((_, index) => (
              <div key={index} className="h-7 animate-pulse rounded bg-[var(--ecp-surface-2)]" />
            ))}
          </div>
        ) : vendors.length === 0 ? (
          <p className="px-4 py-8 text-center text-xs text-[var(--ecp-text-dim)]">
            {scores.error
              ? scores.error
              : "Component scores are computed by executing the suite. Use “Load scores” or “Run suite” to populate this table."}
          </p>
        ) : (
          <>
            <div className="grid gap-4 border-b border-[var(--ecp-border)] p-4 lg:grid-cols-[1fr_200px]">
              <BarChart
                height={190}
                labels={vendors.map((vendor) => vendor.vendor)}
                series={[{ label: "avg score", values: vendors.map((v) => v.avg_score) }]}
                yTitle="score"
              />
              <div className="space-y-2">
                <ChartLegend
                  items={vendors.map((vendor) => ({
                    label: vendor.vendor,
                    color: CHART_PALETTE.gov,
                    value: formatNumber(vendor.avg_score),
                  }))}
                />
                <div className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-2.5 text-[11px] text-[var(--ecp-text-muted)]">
                  <p>
                    Suite average{" "}
                    <span className="font-semibold text-[var(--ecp-text)]">
                      {formatNumber(avgScore)}
                    </span>
                  </p>
                  <p>
                    Passing{" "}
                    <span className="font-semibold text-[var(--ecp-gov)]">
                      {suiteTotals.passed}/{suiteTotals.cases}
                    </span>
                  </p>
                </div>
              </div>
            </div>
            <DataTable
              rows={vendors}
              columns={columns}
              rowKey={(row) => row.vendor}
              dense
              searchable={false}
              initialSort={{ key: "cases", direction: "desc" }}
            />
          </>
        )}
      </PanelBody>
    </Panel>
  );
}