"use client";

import { BarChart, ChartLegend, RadarChart } from "@/components/console/charts/charts";
import { DataTable, type Column } from "@/components/console/ui/data-table";
import { EmptyBlock, Pill } from "@/components/console/ui/states";
import { useConsoleStore } from "@/store/console-store";
import { formatNumber } from "@/lib/format";
import type { PackDetail } from "@/features/console/use-pack-detail";
import type { VendorCapabilityScore } from "@/types/console";

const CAPABILITY_COLORS: Record<string, string> = {
  Parser: "#38bdf8",
  Reasoning: "#2dd4bf",
  Compliance: "#f59e0b",
};

export function BenchmarksTab({ detail }: { detail: PackDetail }) {
  const scores = useConsoleStore((s) => s.capabilityScores);
  const scoresLoading = useConsoleStore((s) => s.loading.includes("capabilityScores"));
  const run = useConsoleStore((s) => s.benchmarkRun.data);
  const loading = useConsoleStore((s) => s.loading.includes("benchmarkRun"));
  const execute = useConsoleStore((s) => s.executeBenchmarkRun);
  const loadScores = useConsoleStore((s) => s.loadCapabilityScores);

  const vendors = Object.values(scores.data?.capabilities ?? {});
  const columns: Column<VendorCapabilityScore>[] = [
    { key: "vendor", header: "Vendor", render: (row) => row.vendor },
    { key: "cases", header: "Cases", align: "right", render: (row) => row.cases },
    { key: "passed", header: "Passed", align: "right", render: (row) => row.passed },
    { key: "score", header: "Avg", align: "right", render: (row) => formatNumber(row.avg_score) },
    {
      key: "capability",
      header: "Capability",
      align: "right",
      render: (row) => formatNumber(row.avg_capability_score),
    },
    {
      key: "compliance",
      header: "Compliance",
      align: "right",
      render: (row) => formatNumber(row.compliance),
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={execute}
          disabled={loading}
          className="rounded-md bg-[var(--ecp-blue)] px-3 py-1.5 text-[11px] font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {loading ? "Running benchmark…" : "Run benchmark suite"}
        </button>
        {vendors.length === 0 && (
          <button
            type="button"
            onClick={loadScores}
            disabled={scoresLoading}
            className="rounded-md border border-[var(--ecp-gov)] px-3 py-1.5 text-[11px] font-semibold text-[var(--ecp-gov)] transition-opacity hover:opacity-80 disabled:opacity-50"
          >
            {scoresLoading ? "Loading component scores…" : "Load component scores"}
          </button>
        )}
        {run?.summary.total ? (
          <Pill tone={run.summary.failed === 0 ? "good" : "warn"}>
            {run.summary.passed}/{run.summary.total} passed · avg {formatNumber(run.summary.avg_score)}
          </Pill>
        ) : (
          <span className="text-[11px] text-[var(--ecp-text-dim)]">
            No suite run recorded in this session
          </span>
        )}
      </div>

      {vendors.length === 0 ? (
        <EmptyBlock
          title="No vendor benchmark data"
          hint={
            scores.error ??
            "Component scores are produced by executing the suite — load them or run the suite first."
          }
        />
      ) : (
        <>
          <div className="grid gap-4 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-4 lg:grid-cols-[1fr_220px]">
            <BarChart
              labels={vendors.map((vendor) => vendor.vendor)}
              series={[
                {
                  label: "parser",
                  values: vendors.map((vendor) => vendor.parser),
                  color: CAPABILITY_COLORS.Parser,
                },
                {
                  label: "reasoning",
                  values: vendors.map((vendor) => vendor.reasoning),
                  color: CAPABILITY_COLORS.Reasoning,
                },
                {
                  label: "compliance",
                  values: vendors.map((vendor) => vendor.compliance),
                  color: CAPABILITY_COLORS.Compliance,
                },
              ]}
              height={220}
              stacked
              yTitle="capability score"
            />
            <ChartLegend
              items={Object.entries(CAPABILITY_COLORS).map(([label, color]) => ({ label, color }))}
            />
          </div>
          <div className="overflow-hidden rounded-lg border border-[var(--ecp-border)]">
            <DataTable
              rows={vendors}
              columns={columns}
              rowKey={(row) => row.vendor}
              dense
              searchable={false}
            />
          </div>
        </>
      )}

      <div className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-4">
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
          Capability profile
        </h3>
        {vendors.length === 0 ? (
          <p className="text-xs text-[var(--ecp-text-dim)]">No capability profile yet.</p>
        ) : (
          <RadarChart
            labels={["parser", "reasoning", "evidence", "compliance", "executive report"]}
            series={vendors.slice(0, 3).map((vendor) => ({
              label: vendor.vendor,
              values: [
                vendor.parser,
                vendor.reasoning,
                vendor.evidence,
                vendor.compliance,
                vendor.executive_report,
              ],
            }))}
          />
        )}
      </div>

      <p className="text-[11px] text-[var(--ecp-text-dim)]">
        Pack {detail.packId} participates in these vendor suites through the shared
        capability core.
      </p>
    </div>
  );
}