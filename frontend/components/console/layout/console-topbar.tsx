"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Cpu, Search, Server, X } from "lucide-react";
import { useConsoleStore } from "@/store/console-store";
import { cn } from "@/lib/utils";

interface SearchHit {
  id: string;
  group: "Capability Packs" | "Real Cases" | "Templates";
  label: string;
  detail: string;
  href: string;
}

export function ConsoleSearch() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const lifecycle = useConsoleStore((s) => s.lifecycle.data);
  const suite = useConsoleStore((s) => s.benchmarkSuite.data);
  const templates = useConsoleStore((s) => s.templates.data);

  const hits = useMemo<SearchHit[]>(() => {
    const all: SearchHit[] = [
      ...(lifecycle ?? []).map((item) => ({
        id: item.id,
        group: "Capability Packs" as const,
        label: item.name,
        detail: `${item.category} · ${item.health}`,
        href: `/console/packs/${item.id}`,
      })),
      ...(suite?.cases ?? []).slice(0, 200).map((item) => ({
        id: item.case_id,
        group: "Real Cases" as const,
        label: item.case_id,
        detail: `${item.vendor} · ${item.category}`,
        href: `/console/packs/benchmark?case=${encodeURIComponent(item.case_id)}`,
      })),
      ...(templates ?? []).map((item) => ({
        id: item.id,
        group: "Templates" as const,
        label: item.name,
        detail: `${item.category} · v${item.version}`,
        href: `/console/marketplace?template=${encodeURIComponent(item.id)}`,
      })),
    ];
    const needle = query.trim().toLowerCase();
    if (!needle) return all.slice(0, 8);
    return all
      .filter(
        (hit) =>
          hit.label.toLowerCase().includes(needle) ||
          hit.detail.toLowerCase().includes(needle)
      )
      .slice(0, 12);
  }, [lifecycle, suite, templates, query]);

  return (
    <div className="relative w-full max-w-[520px]">
      <div className="flex items-center gap-2 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface)] px-3 py-2 transition-colors focus-within:border-[var(--ecp-gov)]">
        <Search className="h-4 w-4 shrink-0 text-[var(--ecp-text-dim)]" />
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          onFocus={() => setOpen(true)}
          onBlur={() => window.setTimeout(() => setOpen(false), 160)}
          placeholder="Search packs, real cases, templates…"
          className="w-full bg-transparent text-sm text-[var(--ecp-text)] outline-none placeholder:text-[var(--ecp-text-dim)]"
        />
        {query && (
          <button type="button" onClick={() => setQuery("")} aria-label="Clear search">
            <X className="h-3.5 w-3.5 text-[var(--ecp-text-dim)] hover:text-[var(--ecp-text)]" />
          </button>
        )}
      </div>

      {open && hits.length > 0 && (
        <div className="absolute left-0 right-0 top-11 z-40 overflow-hidden rounded-xl border border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] shadow-[var(--ecp-shadow)]">
          {hits.map((hit) => (
            <button
              key={`${hit.group}-${hit.id}`}
              type="button"
              onMouseDown={(event) => event.preventDefault()}
              onClick={() => {
                router.push(hit.href);
                setOpen(false);
                setQuery("");
              }}
              className="flex w-full items-center gap-3 px-3 py-2.5 text-left transition-colors hover:bg-[var(--ecp-surface-2)]"
            >
              <span className="flex-1 truncate">
                <span className="block truncate text-sm text-[var(--ecp-text)]">{hit.label}</span>
                <span className="block truncate text-[11px] text-[var(--ecp-text-dim)]">{hit.detail}</span>
              </span>
              <span className="shrink-0 rounded-md bg-[var(--ecp-surface-3)] px-2 py-0.5 text-[10px] uppercase tracking-wide text-[var(--ecp-text-muted)]">
                {hit.group}
              </span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export function EnvironmentStatus() {
  const health = useConsoleStore((s) => s.health.data);
  const healthStatus = useConsoleStore((s) => s.health.status);
  const providers = useConsoleStore((s) => s.modelProviders.data);
  const packs = useConsoleStore((s) => s.packs.data);

  const provider = useMemo(() => {
    const list = providers ?? [];
    return list.find((item) => item.healthy || item.available) ?? list[0];
  }, [providers]);

  const providerName =
    provider?.name || provider?.provider || (provider ? "model gateway" : "no provider");
  const modelLabel = provider?.models?.[0];

  const apiTone = healthStatus === "success" && health?.status === "ok" ? "good" : "warn";

  return (
    <div className="flex shrink-0 items-center gap-2">
      <StatusChip
        tone={apiTone}
        icon={<Server className="h-3.5 w-3.5" />}
        label="API"
        value={health?.version ? `v${health.version}` : healthStatus === "error" ? "offline" : "checking"}
      />
      <StatusChip
        tone={provider ? "good" : "warn"}
        icon={<Cpu className="h-3.5 w-3.5" />}
        label="Model"
        value={modelLabel ?? providerName}
      />
      <StatusChip
        tone={(packs?.length ?? 0) > 0 ? "good" : "idle"}
        icon={<span className="ecp-pulse h-1.5 w-1.5 rounded-full bg-current" />}
        label="Packs"
        value={String(packs?.length ?? 0)}
      />
    </div>
  );
}

function StatusChip({
  tone,
  icon,
  label,
  value,
}: {
  tone: "good" | "warn" | "idle";
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  const toneClass = cn(
    "flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px]",
    tone === "good" && "border-[var(--ecp-border)] bg-[var(--ecp-surface)] text-[var(--ecp-text-muted)]",
    tone === "warn" && "border-[var(--ecp-alert)]/40 bg-[var(--ecp-alert-soft)] text-[var(--ecp-alert)]",
    tone === "idle" && "border-[var(--ecp-border)] bg-[var(--ecp-surface)] text-[var(--ecp-text-dim)]"
  );
  return (
    <span className={toneClass}>
      {icon}
      <span className="text-[var(--ecp-text-dim)]">{label}</span>
      <span className="font-medium">{value}</span>
    </span>
  );
}