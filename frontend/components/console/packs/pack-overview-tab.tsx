"use client";

import { EmptyBlock } from "@/components/console/ui/states";
import { relativeTime, titleCase } from "@/lib/format";
import type { PackDetail } from "@/features/console/use-pack-detail";

export function Row({ label, value }: { label: string; value?: string | null }) {
  return (
    <div className="flex items-baseline justify-between gap-3 border-b border-[var(--ecp-border)]/60 pb-1.5">
      <dt className="text-[var(--ecp-text-dim)]">{label}</dt>
      <dd className="truncate font-medium text-[var(--ecp-text)]">{value ?? "—"}</dd>
    </div>
  );
}

export function OverviewTab({ detail }: { detail: PackDetail }) {
  const { governance, lifecycle } = detail;
  if (!governance && !lifecycle) {
    return (
      <EmptyBlock
        title="Pack not found"
        hint="Neither the governance registry nor the capability lifecycle knows this pack id."
      />
    );
  }

  const metrics = lifecycle?.metrics;
  const metadata = governance?.metadata ?? {};

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <section className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-4">
        <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
          Registry record
        </h3>
        <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
          <Row label="Pack id" value={governance?.pack_id ?? lifecycle?.id} />
          <Row label="Domain" value={governance?.domain ?? lifecycle?.category} />
          <Row label="Status" value={governance?.status ?? lifecycle?.state} />
          <Row label="Health" value={lifecycle?.health ?? "—"} />
          <Row label="Version" value={lifecycle?.version.display ?? "—"} />
          <Row label="Contract" value={lifecycle?.version.contract_version ?? "—"} />
          <Row
            label="Updated"
            value={relativeTime(governance?.updated_at ?? lifecycle?.updated_at)}
          />
          <Row label="Loaded" value={relativeTime(lifecycle?.loaded_at)} />
        </dl>
      </section>

      <section className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-4">
        <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
          Runtime metrics
        </h3>
        {metrics ? (
          <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
            <Row label="Executions" value={String(metrics.execution_count)} />
            <Row label="Successes" value={String(metrics.success_count)} />
            <Row label="Failures" value={String(metrics.failure_count)} />
            <Row label="Success rate" value={`${(metrics.success_rate * 100).toFixed(1)}%`} />
            <Row label="Avg latency" value={`${metrics.avg_latency_ms.toFixed(2)} ms`} />
            <Row label="Last executed" value={relativeTime(metrics.last_executed_at)} />
          </dl>
        ) : (
          <p className="text-xs text-[var(--ecp-text-dim)]">
            No lifecycle metrics reported for this pack.
          </p>
        )}
        {metrics?.last_error && (
          <p className="mt-3 rounded-md border border-[var(--ecp-danger)]/40 bg-[var(--ecp-danger-soft)] px-2.5 py-2 text-[11px] text-[var(--ecp-danger)]">
            {metrics.last_error}
          </p>
        )}
      </section>

      <section className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-4 lg:col-span-2">
        <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
          Pack metadata
        </h3>
        {Object.keys(metadata).length === 0 ? (
          <p className="text-xs text-[var(--ecp-text-dim)]">
            No metadata registered for this pack.
          </p>
        ) : (
          <dl className="grid grid-cols-1 gap-x-4 gap-y-2 text-xs md:grid-cols-2">
            {Object.entries(metadata).map(([key, value]) => (
              <Row
                key={key}
                label={titleCase(key)}
                value={typeof value === "object" ? JSON.stringify(value) : String(value)}
              />
            ))}
          </dl>
        )}
      </section>
    </div>
  );
}