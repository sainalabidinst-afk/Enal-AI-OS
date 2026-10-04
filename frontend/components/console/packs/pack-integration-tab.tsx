"use client";

import { useMemo } from "react";
import { BookOpen } from "lucide-react";
import { Field } from "@/components/console/ui/controls";
import { Pill } from "@/components/console/ui/states";
import { useConsoleStore } from "@/store/console-store";
import { titleCase } from "@/lib/format";
import type { PackDetail } from "@/features/console/use-pack-detail";

export function IntegrationTab({ detail }: { detail: PackDetail }) {
  const catalog = useConsoleStore((s) => s.lifecycle.data);
  const { dependencies, compatibility } = detail;

  const dependents = useMemo(
    () => (catalog ?? []).filter((item) => item.dependents.includes(detail.packId)),
    [catalog, detail.packId]
  );

  return (
    <div className="space-y-4">
      <section className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-4">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
            Contract compatibility
          </h3>
          {compatibility && (
            <Pill tone={compatibility.compatible ? "good" : "bad"}>
              {compatibility.compatible ? "compatible" : "incompatible"}
            </Pill>
          )}
        </div>
        {compatibility ? (
          <Field label={`Contract ${compatibility.required_contract}`}>
            <p className="text-xs text-[var(--ecp-text-muted)]">{compatibility.message}</p>
          </Field>
        ) : (
          <p className="text-xs text-[var(--ecp-text-dim)]">
            Compatibility check unavailable for this pack.
          </p>
        )}
      </section>

      <div className="grid gap-4 lg:grid-cols-2">
        <DependencyList
          title="Dependencies"
          items={dependencies?.dependencies ?? []}
          empty="No declared dependencies"
        />
        <DependencyList
          title="Connected packs"
          items={dependents.map((item) => item.id)}
          empty="No packs depend on this one"
        />
      </div>

      {dependencies && !dependencies.satisfied && (
        <p className="rounded-lg border border-[var(--ecp-alert)]/40 bg-[var(--ecp-alert-soft)] px-3 py-2 text-[11px] text-[var(--ecp-alert)]">
          Missing dependencies: {dependencies.missing.join(", ") || "unknown"}
        </p>
      )}
    </div>
  );
}

export function DocsTab({ detail }: { detail: PackDetail }) {
  const metadata = detail.governance?.metadata ?? {};
  const references = Object.entries(metadata).filter(([key]) => /rfc|adr|doc|link/i.test(key));

  return (
    <div className="space-y-4">
      <section className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-4">
        <h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
          Platform governance
        </h3>
        <ul className="space-y-1.5 text-xs text-[var(--ecp-text-muted)]">
          <li>RFC-0055 — Pilar 4 Governance (pack registry, sandbox, quality gate)</li>
          <li>GOVERNANCE.md — operational governance rules</li>
          <li>PRODUCT_CONTRACT.md — capability pack contract</li>
        </ul>
      </section>

      <section className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-4">
        <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
          Pack references
        </h3>
        {references.length === 0 ? (
          <div className="flex items-center gap-2 text-xs text-[var(--ecp-text-dim)]">
            <BookOpen className="h-3.5 w-3.5" />
            This pack has no RFC/ADR references registered in its metadata.
          </div>
        ) : (
          <ul className="space-y-1.5">
            {references.map(([key, value]) => (
              <li key={key} className="flex items-center gap-2 text-xs">
                <Pill tone="info">{titleCase(key)}</Pill>
                <span className="text-[var(--ecp-text-muted)]">
                  {typeof value === "object" ? JSON.stringify(value) : String(value)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

function DependencyList({
  title,
  items,
  empty,
}: {
  title: string;
  items: string[];
  empty: string;
}) {
  return (
    <section className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] p-4">
      <h3 className="mb-3 text-xs font-semibold uppercase tracking-wide text-[var(--ecp-text-dim)]">
        {title}
      </h3>
      {items.length === 0 ? (
        <p className="text-xs text-[var(--ecp-text-dim)]">{empty}</p>
      ) : (
        <ul className="flex flex-wrap gap-1.5">
          {items.map((item) => (
            <li key={item}>
              <Pill tone="info">{item}</Pill>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}