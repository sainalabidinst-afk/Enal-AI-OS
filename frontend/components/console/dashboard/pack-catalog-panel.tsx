"use client";

import Link from "next/link";
import { ChevronRight } from "lucide-react";
import { Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { Pill, ResourceView } from "@/components/console/ui/states";
import { useConsoleStore } from "@/store/console-store";
import { usePackCatalog, type PackCatalogEntry } from "@/features/console/use-console";
import { cn } from "@/lib/utils";
import { formatPercent } from "@/lib/format";

function healthTone(entry: PackCatalogEntry) {
  if (entry.health === "healthy") return "good" as const;
  if (entry.health === "degraded") return "warn" as const;
  if (entry.health === "unhealthy") return "bad" as const;
  if (entry.state === "error") return "bad" as const;
  return "neutral" as const;
}

export function PackCatalogList({ limit }: { limit?: number }) {
  const lifecycle = useConsoleStore((s) => s.lifecycle);
  const loadGovernance = useConsoleStore((s) => s.loadGovernance);
  const catalog = usePackCatalog();
  const rows = limit ? catalog.slice(0, limit) : catalog;

  return (
    <ResourceView
      status={lifecycle.status}
      error={lifecycle.error}
      data={catalog}
      isEmpty={(rows) => rows.length === 0}
      loadingLabel="Loading capability packs"
      emptyTitle="No capability packs registered"
      emptyHint="Register a pack through POST /api/v1/governance/packs to see it here."
      onRetry={loadGovernance}
    >
      {() => (
        <ul className="divide-y divide-[var(--ecp-border)]/70">
          {rows.map((entry) => (
            <li key={entry.id}>
              <Link
                href={`/console/packs/${encodeURIComponent(entry.id)}`}
                className={cn(
                  "group flex items-center gap-3 px-4 py-2.5 transition-colors",
                  "hover:bg-[var(--ecp-surface-2)]"
                )}
              >
                <span
                  className={cn(
                    "h-2 w-2 shrink-0 rounded-full",
                    entry.health === "healthy"
                      ? "bg-[var(--ecp-gov)]"
                      : entry.health === "degraded"
                        ? "bg-[var(--ecp-alert)]"
                        : entry.health === "unhealthy"
                          ? "bg-[var(--ecp-danger)]"
                          : "bg-[var(--ecp-text-dim)]"
                  )}
                />
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-xs font-medium text-[var(--ecp-text)]">
                    {entry.name}
                  </span>
                  <span className="block truncate text-[11px] text-[var(--ecp-text-dim)]">
                    {entry.domain}
                    {entry.state ? ` · ${entry.state}` : ""}
                  </span>
                </span>
                {entry.status && (
                  <Pill tone={entry.status === "approved" || entry.status === "registered" ? "good" : "neutral"}>
                    {entry.status}
                  </Pill>
                )}
                {entry.successRate !== null && (
                  <span className="w-14 shrink-0 text-right text-[11px] text-[var(--ecp-text-muted)]">
                    {formatPercent(entry.successRate)}
                  </span>
                )}
                <Pill tone={healthTone(entry)} className="shrink-0">
                  {entry.health ?? "untracked"}
                </Pill>
                <ChevronRight className="h-3.5 w-3.5 shrink-0 text-[var(--ecp-text-dim)] opacity-0 transition-opacity group-hover:opacity-100" />
              </Link>
            </li>
          ))}
        </ul>
      )}
    </ResourceView>
  );
}

export function PackCatalogPanel() {
  const lifecycle = useConsoleStore((s) => s.lifecycle);
  const summary = useConsoleStore((s) => s.lifecycleSummary.data);

  return (
    <Panel className="h-full">
      <PanelHeader
        title="Capability Packs"
        subtitle={
          summary
            ? `${summary.loaded} loaded · ${summary.healthy} healthy · ${summary.total} tracked`
            : "Lifecycle state from the capability registry"
        }
        actions={
          <Link
            href="/console/packs"
            className="text-[11px] text-[var(--ecp-gov)] hover:underline"
          >
            View all
          </Link>
        }
      />
      <PanelBody className="p-0">
        <PackCatalogList limit={8} />
      </PanelBody>
      {lifecycle.status === "error" && lifecycle.error && (
        <p className="border-t border-[var(--ecp-border)] px-4 py-2 text-[11px] text-[var(--ecp-danger)]">
          {lifecycle.error}
        </p>
      )}
    </Panel>
  );
}