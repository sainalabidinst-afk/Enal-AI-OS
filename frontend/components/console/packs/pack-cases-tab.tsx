"use client";

import { DataTable, type Column } from "@/components/console/ui/data-table";
import { EmptyBlock, LoadingBlock, Pill } from "@/components/console/ui/states";
import { useConsoleStore } from "@/store/console-store";
import type { BenchmarkCaseSummary } from "@/types/console";

export function RealCasesTab({ focusCase }: { focusCase?: string | null }) {
  const suite = useConsoleStore((s) => s.benchmarkSuite);
  const loadBenchmark = useConsoleStore((s) => s.loadBenchmark);

  const columns: Column<BenchmarkCaseSummary>[] = [
    { key: "case", header: "Case", render: (row) => row.case_id },
    { key: "vendor", header: "Vendor", render: (row) => row.vendor },
    { key: "category", header: "Category", render: (row) => row.category },
    {
      key: "tags",
      header: "Tags",
      render: (row) => (
        <span className="flex flex-wrap gap-1">
          {row.tags.slice(0, 3).map((tag) => (
            <Pill key={tag}>{tag}</Pill>
          ))}
        </span>
      ),
    },
  ];

  if (suite.status === "loading" && !suite.data) {
    return <LoadingBlock label="Loading real cases" />;
  }

  const cases = suite.data?.cases ?? [];

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between text-[11px] text-[var(--ecp-text-dim)]">
        <span>
          {suite.data?.name ?? "Real world suite"} · {cases.length} cases discovered on disk
        </span>
        <button
          type="button"
          onClick={loadBenchmark}
          className="rounded-md border border-[var(--ecp-border)] px-2 py-1 transition-colors hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)]"
        >
          Rescan
        </button>
      </div>
      {cases.length === 0 ? (
        <EmptyBlock
          title="No real cases available"
          hint={suite.error ?? "The benchmark suite found no case directories."}
        />
      ) : (
        <div className="overflow-hidden rounded-lg border border-[var(--ecp-border)]">
          <DataTable
            rows={focusCase ? cases.filter((item) => item.case_id === focusCase) : cases}
            columns={columns}
            rowKey={(row) => row.case_id}
            dense
            searchPlaceholder="Filter cases by id or vendor…"
          />
        </div>
      )}
    </div>
  );
}