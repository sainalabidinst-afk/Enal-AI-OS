"use client";

import Link from "next/link";
import { useMemo } from "react";
import { PageHeader, Panel, PanelBody } from "@/components/console/ui/panel";
import { DataTable, type Column } from "@/components/console/ui/data-table";
import { Pill } from "@/components/console/ui/states";
import { DoughnutChart, ChartLegend } from "@/components/console/charts/charts";
import { MetricCard, MetricGrid } from "@/components/console/ui/metric-card";
import { usePackCatalog, type PackCatalogEntry } from "@/features/console/use-console";
import { useConsoleHydration } from "@/features/console/use-console";
import { formatNumber, formatPercent } from "@/lib/format";

export function PackCatalogView() {
  useConsoleHydration("governance");
  const catalog = usePackCatalog();

  const distribution = useMemo(() => {
    const counts = new Map<string, number>();
    catalog.forEach((entry) => {
      const key = entry.health ?? "untracked";
      counts.set(key, (counts.get(key) ?? 0) + 1);
    });
    return {
      labels: Array.from(counts.keys()),
      values: Array.from(counts.values()),
    };
  }, [catalog]);

  const totals = useMemo(() => {
    const latencies = catalog
      .map((entry) => entry.avgLatencyMs)
      .filter((value): value is number => value !== null && value > 0);
    const scores = catalog
      .map((entry) => entry.benchmarkScore)
      .filter((value): value is number => value !== null && value > 0);
    return {
      packs: catalog.length,
      avgLatency: latencies.length
        ? latencies.reduce((a, b) => a + b, 0) / latencies.length
        : null,
      avgScore: scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : null,
      dependencies: catalog.reduce((total, entry) => total + (entry.tests?.total ?? 0), 0),
    };
  }, [catalog]);

  const columns: Column<PackCatalogEntry>[] = [
    {
      key: "name",
      header: "Pack",
      sortable: true,
      sortValue: (row) => row.name,
      render: (row) => (
        <Link
          href={`/console/packs/${encodeURIComponent(row.id)}`}
          className="font-medium text-[var(--ecp-text)] hover:text-[var(--ecp-gov)] hover:underline"
        >
          {row.name}
        </Link>
      ),
    },
    { key: "domain", header: "Domain", sortable: true, sortValue: (row) => row.domain, render: (row) => row.domain },
    {
      key: "status",
      header: "Status",
      sortable: true,
      render: (row) =>
        row.status ? <Pill tone="info">{row.status}</Pill> : <Pill>unregistered</Pill>,
    },
    {
      key: "health",
      header: "Health",
      sortable: true,
      sortValue: (row) => row.health ?? "",
      render: (row) => (
        <Pill
          tone={
            row.health === "healthy"
              ? "good"
              : row.health === "degraded"
                ? "warn"
                : row.health === "unhealthy"
                  ? "bad"
                  : "neutral"
          }
        >
          {row.health ?? "—"}
        </Pill>
      ),
    },
    {
      key: "score",
      header: "Score",
      align: "right",
      sortable: true,
      sortValue: (row) => row.benchmarkScore ?? -1,
      render: (row) => formatPercent(row.benchmarkScore),
    },
    {
      key: "coverage",
      header: "Coverage",
      align: "right",
      sortable: true,
      sortValue: (row) => row.coverage ?? -1,
      render: (row) => formatPercent(row.coverage),
    },
    {
      key: "tests",
      header: "Tests",
      align: "right",
      sortable: true,
      sortValue: (row) => (row.tests ? row.tests.passed / Math.max(row.tests.total, 1) : -1),
      render: (row) =>
        row.tests ? `${row.tests.passed}/${row.tests.total}` : "—",
    },
    {
      key: "latency",
      header: "Avg latency",
      align: "right",
      sortable: true,
      sortValue: (row) => row.avgLatencyMs ?? -1,
      render: (row) => (row.avgLatencyMs ? `${formatNumber(row.avgLatencyMs)} ms` : "—"),
    },
    {
      key: "success",
      header: "Success",
      align: "right",
      sortable: true,
      sortValue: (row) => row.successRate ?? -1,
      render: (row) => formatPercent(row.successRate, 1),
    },
  ];

  return (
    <div className="space-y-4">
      <PageHeader
        title="Capability Packs"
        description="Governance registry and runtime lifecycle state for every registered pack"
      />

      <MetricGrid>
        <MetricCard label="Tracked packs" value={String(totals.packs)} tone="gov" />
        <MetricCard
          label="Avg benchmark score"
          value={formatPercent(totals.avgScore)}
          tone="sky"
        />
        <MetricCard
          label="Avg latency"
          value={totals.avgLatency ? `${formatNumber(totals.avgLatency)} ms` : "—"}
          tone="alert"
        />
        <MetricCard label="Registered tests" value={String(totals.dependencies)} tone="blue" />
      </MetricGrid>

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_300px]">
        <Panel>
          <PanelBody className="p-0">
            <DataTable
              rows={catalog}
              columns={columns}
              rowKey={(row) => row.id}
              searchPlaceholder="Filter packs by name or domain…"
              initialSort={{ key: "name", direction: "asc" }}
            />
          </PanelBody>
        </Panel>

        <Panel>
          <PanelBody className="space-y-4">
            <div>
              <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
                Health distribution
              </h3>
              {distribution.labels.length === 0 ? (
                <p className="text-xs text-[var(--ecp-text-dim)]">No lifecycle data yet.</p>
              ) : (
                <>
                  <DoughnutChart
                    labels={distribution.labels}
                    values={distribution.values}
                    height={190}
                    centerValue={String(totals.packs)}
                    centerLabel="packs"
                  />
                  <div className="mt-3">
                    <ChartLegend
                      items={distribution.labels.map((label, index) => ({
                        label,
                        color: ["#22c55e", "#f59e0b", "#ef4444", "#6b7890"][index % 4],
                        value: String(distribution.values[index]),
                      }))}
                    />
                  </div>
                </>
              )}
            </div>
          </PanelBody>
        </Panel>
      </div>
    </div>
  );
}