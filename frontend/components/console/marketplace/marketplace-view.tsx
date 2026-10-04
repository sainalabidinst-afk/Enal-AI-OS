"use client";

import { useMemo, useState } from "react";
import { PackageCheck, Search } from "lucide-react";
import { PageHeader, Panel, PanelBody, PanelHeader } from "@/components/console/ui/panel";
import { EmptyBlock, ErrorBlock, LoadingBlock, Pill } from "@/components/console/ui/states";
import { Rating, inputClass, selectClass } from "@/components/console/ui/controls";
import { DependencyList, TemplateCard } from "./marketplace-cards";
import { useConsoleStore } from "@/store/console-store";
import { useConsoleHydration } from "@/features/console/use-console";
import { relativeTime } from "@/lib/format";

export function MarketplaceView() {
  useConsoleHydration("marketplace");
  const templates = useConsoleStore((s) => s.templates);
  const listings = useConsoleStore((s) => s.listings);
  const cloneTemplate = useConsoleStore((s) => s.cloneTemplate);
  const receipts = useConsoleStore((s) => s.cloneReceipts);
  const loadMarketplace = useConsoleStore((s) => s.loadMarketplace);

  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [project, setProject] = useState("default");
  const [cloning, setCloning] = useState<string | null>(null);

  const rows = useMemo(() => templates.data ?? [], [templates.data]);
  const categories = useMemo(
    () => Array.from(new Set(rows.map((item) => item.category))).sort(),
    [rows]
  );

  const visible = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return rows.filter((item) => {
      const matchesCategory = category === "all" || item.category === category;
      const matchesQuery =
        !needle ||
        item.name.toLowerCase().includes(needle) ||
        item.description.toLowerCase().includes(needle) ||
        item.tags.some((tag) => tag.toLowerCase().includes(needle));
      return matchesCategory && matchesQuery;
    });
  }, [rows, query, category]);

  const selected = rows.find((item) => item.id === selectedId) ?? visible[0] ?? null;

  function clone(id: string) {
    setCloning(id);
    cloneTemplate(id, project);
    window.setTimeout(() => setCloning(null), 900);
  }

  return (
    <div className="space-y-4">
      <PageHeader
        title="Marketplace"
        description="Pre-built capability templates, shared agents and dependency resolution"
        actions={
          <button
            type="button"
            onClick={loadMarketplace}
            className="rounded-md border border-[var(--ecp-border)] px-3 py-1.5 text-[11px] text-[var(--ecp-text-muted)] transition-colors hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)]"
          >
            Refresh
          </button>
        }
      />

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_340px]">
        <Panel className="min-w-0">
          <PanelHeader
            title="Templates"
            subtitle={`${visible.length} of ${rows.length} templates`}
            actions={
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-1.5 rounded-md border border-[var(--ecp-border)] bg-[var(--ecp-bg-raised)] px-2 py-1.5">
                  <Search className="h-3.5 w-3.5 text-[var(--ecp-text-dim)]" />
                  <input
                    value={query}
                    onChange={(event) => setQuery(event.target.value)}
                    placeholder="Search templates"
                    className="w-40 bg-transparent text-[11px] outline-none placeholder:text-[var(--ecp-text-dim)]"
                  />
                </div>
                <select
                  value={category}
                  onChange={(event) => setCategory(event.target.value)}
                  className={selectClass()}
                >
                  <option value="all">All categories</option>
                  {categories.map((item) => (
                    <option key={item} value={item}>
                      {item}
                    </option>
                  ))}
                </select>
              </div>
            }
          />
          <PanelBody>
            {templates.status === "loading" && rows.length === 0 ? (
              <LoadingBlock label="Loading templates" />
            ) : templates.status === "error" && templates.error ? (
              <ErrorBlock message={templates.error} onRetry={loadMarketplace} />
            ) : visible.length === 0 ? (
              <EmptyBlock
                title="No templates match"
                hint="Adjust the search or category filter."
              />
            ) : (
              <div className="grid gap-3 sm:grid-cols-2 2xl:grid-cols-3">
                {visible.map((template) => (
                  <TemplateCard
                    key={template.id}
                    template={template}
                    active={selected?.id === template.id}
                    onSelect={() => setSelectedId(template.id)}
                    onClone={() => clone(template.id)}
                    cloning={cloning === template.id}
                  />
                ))}
              </div>
            )}
          </PanelBody>
        </Panel>

        <aside className="space-y-4">
          <Panel>
            <PanelHeader
              title="Dependency Resolution"
              subtitle={selected ? selected.name : "Select a template"}
              actions={<PackageCheck className="h-4 w-4 text-[var(--ecp-gov)]" />}
            />
            <PanelBody className="space-y-3">
              {selected ? (
                <>
                  <p className="text-xs text-[var(--ecp-text-muted)]">
                    {selected.description || "No description provided."}
                  </p>
                  <DependencyList template={selected} />
                  <label className="block space-y-1.5">
                    <span className="text-[11px] uppercase tracking-wide text-[var(--ecp-text-dim)]">
                      Target project
                    </span>
                    <input
                      value={project}
                      onChange={(event) => setProject(event.target.value)}
                      className={inputClass()}
                    />
                  </label>
                  <button
                    type="button"
                    onClick={() => clone(selected.id)}
                    disabled={cloning === selected.id}
                    className="w-full rounded-lg bg-[var(--ecp-gov)] px-3 py-2 text-xs font-semibold text-[#04121a] transition-opacity hover:opacity-90 disabled:opacity-60"
                  >
                    {cloning === selected.id ? "Cloning…" : "Run clone"}
                  </button>
                </>
              ) : (
                <p className="text-xs text-[var(--ecp-text-dim)]">
                  Pick a template to inspect its resolved dependencies.
                </p>
              )}
            </PanelBody>
          </Panel>

          <Panel>
            <PanelHeader title="Clone history" subtitle="This session" />
            <PanelBody className="space-y-2">
              {(receipts.data ?? []).length === 0 ? (
                <p className="text-xs text-[var(--ecp-text-dim)]">
                  No clones yet in this session.
                </p>
              ) : (
                (receipts.data ?? []).map((receipt) => (
                  <div
                    key={receipt.id}
                    className="rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2 text-[11px]"
                  >
                    <p className="truncate font-medium text-[var(--ecp-text)]">
                      {receipt.agent_id}
                    </p>
                    <p className="text-[var(--ecp-text-dim)]">
                      → {receipt.project} · {relativeTime(receipt.cloned_at)}
                    </p>
                  </div>
                ))
              )}
              {receipts.error && (
                <p className="text-[11px] text-[var(--ecp-danger)]">{receipts.error}</p>
              )}
            </PanelBody>
          </Panel>

          <Panel>
            <PanelHeader title="Shared agents" subtitle="Published listings" />
            <PanelBody>
              {listings.status === "loading" && !listings.data ? (
                <LoadingBlock />
              ) : (listings.data ?? []).length === 0 ? (
                <p className="text-xs text-[var(--ecp-text-dim)]">
                  No agents shared yet. Share one from the Builder workspace.
                </p>
              ) : (
                <ul className="space-y-2">
                  {(listings.data ?? []).map((listing) => (
                    <li
                      key={listing.id}
                      className="flex items-center gap-2 rounded-lg border border-[var(--ecp-border)] bg-[var(--ecp-surface-2)] px-3 py-2"
                    >
                      <span className="min-w-0 flex-1">
                        <span className="block truncate text-[11px] font-medium">
                          {listing.name}
                        </span>
                        <span className="block truncate text-[10px] text-[var(--ecp-text-dim)]">
                          {listing.author} · {listing.category}
                        </span>
                      </span>
                      <Pill tone="info">
                        <Rating value={listing.rating} compact />
                      </Pill>
                    </li>
                  ))}
                </ul>
              )}
            </PanelBody>
          </Panel>
        </aside>
      </div>
    </div>
  );
}