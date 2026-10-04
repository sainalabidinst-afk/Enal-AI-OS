"use client";

import { useMemo } from "react";
import { Field, inputClass, selectClass } from "@/components/console/ui/controls";
import { DataTable, type Column } from "@/components/console/ui/data-table";
import { EmptyBlock, Pill } from "@/components/console/ui/states";
import { useConsoleStore } from "@/store/console-store";
import { useConsolePreferences } from "@/store/console-settings-store";
import { formatNumber } from "@/lib/format";
import type { ModelProviderStatus } from "@/types/console";

export function ModelSettingsTab() {
  const providers = useConsoleStore((s) => s.modelProviders);
  const prefs = useConsolePreferences();
  const setPref = useConsolePreferences((s) => s.set);

  const rows = useMemo(() => providers.data ?? [], [providers.data]);
  const models = useMemo(
    () => Array.from(new Set(rows.flatMap((provider) => provider.models ?? []))),
    [rows]
  );

  const columns: Column<ModelProviderStatus>[] = [
    {
      key: "provider",
      header: "Provider",
      render: (row) => row.name ?? row.provider ?? "—",
    },
    {
      key: "state",
      header: "State",
      render: (row) => (
        <Pill tone={row.healthy || row.available ? "good" : "bad"}>
          {row.status ?? (row.healthy || row.available ? "healthy" : "unavailable")}
        </Pill>
      ),
    },
    {
      key: "latency",
      header: "Latency",
      align: "right",
      render: (row) => (row.latency_ms ? `${formatNumber(row.latency_ms)} ms` : "—"),
    },
    {
      key: "models",
      header: "Models",
      render: (row) => (
        <span className="flex flex-wrap gap-1">
          {(row.models ?? []).slice(0, 3).map((model) => (
            <Pill key={model}>{model}</Pill>
          ))}
          {(row.models ?? []).length > 3 && <Pill>+{(row.models ?? []).length - 3}</Pill>}
        </span>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Default LLM provider">
          <select
            value={prefs.defaultProvider}
            onChange={(event) => setPref("defaultProvider", event.target.value)}
            className={selectClass()}
          >
            <option value="">gateway default</option>
            {rows.map((row, index) => (
              <option
                key={row.name ?? row.provider ?? index}
                value={row.name ?? row.provider ?? ""}
              >
                {row.name ?? row.provider ?? "provider"}
              </option>
            ))}
          </select>
        </Field>
        <Field label="Default model">
          <select
            value={prefs.defaultModel}
            onChange={(event) => setPref("defaultModel", event.target.value)}
            className={selectClass()}
          >
            <option value="">gateway default</option>
            {models.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>
        </Field>
      </div>

      {providers.status === "error" && providers.error ? (
        <p className="text-[11px] text-[var(--ecp-danger)]">{providers.error}</p>
      ) : rows.length === 0 ? (
        <EmptyBlock
          title="No model providers reported"
          hint="The gateway did not return provider status."
        />
      ) : (
        <div className="overflow-hidden rounded-lg border border-[var(--ecp-border)]">
          <DataTable
            rows={rows}
            columns={columns}
            rowKey={(row) => row.name ?? row.provider ?? "unknown"}
            dense
            searchable={false}
          />
        </div>
      )}
    </div>
  );
}