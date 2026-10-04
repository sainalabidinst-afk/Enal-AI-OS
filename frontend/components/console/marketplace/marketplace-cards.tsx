"use client";

import { Copy, Download, Sparkles } from "lucide-react";
import { Pill } from "@/components/console/ui/states";
import { Rating } from "@/components/console/ui/controls";
import { formatNumber } from "@/lib/format";
import type { MarketplaceTemplate } from "@/types/console";

export function TemplateCard({
  template,
  active,
  onSelect,
  onClone,
  cloning,
}: {
  template: MarketplaceTemplate;
  active: boolean;
  onSelect: () => void;
  onClone: () => void;
  cloning: boolean;
}) {
  return (
    <article
      onClick={onSelect}
      className={`cursor-pointer rounded-xl border p-3 transition-colors ${
        active
          ? "border-[var(--ecp-gov)] bg-[var(--ecp-gov-soft)]"
          : "border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] hover:border-[var(--ecp-border-strong)]"
      }`}
    >
      <div className="flex items-start gap-2">
        <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-[var(--ecp-gov)]" />
        <div className="min-w-0 flex-1">
          <h3 className="truncate text-xs font-semibold">{template.name}</h3>
          <p className="truncate text-[10px] text-[var(--ecp-text-dim)]">
            {template.category} · {template.type}
          </p>
        </div>
      </div>
      <p className="mt-2 line-clamp-2 min-h-[30px] text-[11px] text-[var(--ecp-text-muted)]">
        {template.description}
      </p>
      <div className="mt-2 flex items-center justify-between">
        <Rating value={template.rating} />
        <Pill tone="neutral">
          <Download className="h-2.5 w-2.5" />
          {formatNumber(template.clones, 0)}
        </Pill>
      </div>
      <div className="mt-2 flex items-center gap-2">
        <button
          type="button"
          onClick={(event) => {
            event.stopPropagation();
            onClone();
          }}
          disabled={cloning}
          className="flex flex-1 items-center justify-center gap-1.5 rounded-md bg-[var(--ecp-blue)] px-2 py-1.5 text-[11px] font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-60"
        >
          <Copy className="h-3 w-3" />
          {cloning ? "Cloning…" : "Clone"}
        </button>
        <span className="text-[10px] text-[var(--ecp-text-dim)]">v{template.version}</span>
      </div>
    </article>
  );
}

export function DependencyList({ template }: { template: MarketplaceTemplate }) {
  const config = template.config ?? {};
  const tools = Array.isArray(config.tools) ? (config.tools as unknown[]) : [];
  const knowledge = Array.isArray(config.knowledge_base_ids)
    ? (config.knowledge_base_ids as unknown[])
    : [];
  const model = typeof config.model === "string" ? config.model : null;
  const items = [
    ...(model ? [{ label: `model: ${model}`, resolved: true }] : []),
    ...tools.map((tool) => ({ label: String(tool), resolved: true })),
    ...knowledge.map((entry) => ({ label: String(entry), resolved: false })),
  ];

  if (items.length === 0) {
    return (
      <p className="text-[11px] text-[var(--ecp-text-dim)]">
        This template declares no model, tool or knowledge dependencies.
      </p>
    );
  }

  return (
    <ul className="space-y-1.5">
      {items.map((item) => (
        <li key={item.label} className="flex items-center gap-2 text-[11px]">
          <span
            className={`h-1.5 w-1.5 rounded-full ${
              item.resolved ? "bg-[var(--ecp-gov)]" : "bg-[var(--ecp-alert)]"
            }`}
          />
          <span className="min-w-0 flex-1 truncate text-[var(--ecp-text-muted)]">
            {item.label}
          </span>
          <Pill tone={item.resolved ? "good" : "warn"}>
            {item.resolved ? "resolved" : "missing"}
          </Pill>
        </li>
      ))}
    </ul>
  );
}