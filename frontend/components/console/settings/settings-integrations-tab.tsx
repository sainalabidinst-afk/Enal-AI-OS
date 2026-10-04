"use client";

import { useState } from "react";
import { DataTable, type Column } from "@/components/console/ui/data-table";
import { EmptyBlock } from "@/components/console/ui/states";
import { useConsoleStore } from "@/store/console-store";
import { useConsolePreferences } from "@/store/console-settings-store";
import { connectConnector, disconnectConnector } from "@/services/console/settings";
import type { ConnectorRecord } from "@/services/console/settings";

export function IntegrationsTab() {
  const connectors = useConsoleStore((s) => s.connectors);
  const loadSettings = useConsoleStore((s) => s.loadSettings);
  const toggleIntegration = useConsolePreferences((s) => s.toggleIntegration);
  const enabled = useConsolePreferences((s) => s.integrations);
  const [busy, setBusy] = useState<string | null>(null);

  async function toggle(connector: ConnectorRecord) {
    setBusy(connector.name);
    try {
      if (enabled[connector.name]) {
        await disconnectConnector(connector.name);
      } else {
        await connectConnector(connector.name);
      }
      toggleIntegration(connector.name);
      loadSettings();
    } finally {
      setBusy(null);
    }
  }

  const rows = connectors.data ?? [];
  const columns: Column<ConnectorRecord>[] = [
    { key: "name", header: "Connector", render: (row) => row.name },
    { key: "description", header: "Description", render: (row) => row.description ?? "—" },
    {
      key: "actions",
      header: "Actions",
      align: "right",
      render: (row) => `${row.actions?.length ?? 0}`,
    },
    {
      key: "state",
      header: "State",
      align: "right",
      render: (row) => (
        <button
          type="button"
          disabled={busy === row.name}
          onClick={() => toggle(row)}
          className="rounded-md border border-[var(--ecp-border)] px-2 py-1 text-[11px] text-[var(--ecp-text-muted)] transition-colors hover:border-[var(--ecp-gov)] hover:text-[var(--ecp-text)] disabled:opacity-50"
        >
          {enabled[row.name] ? "disconnect" : "connect"}
        </button>
      ),
    },
  ];

  return (
    <div className="space-y-3">
      {connectors.error && (
        <p className="text-[11px] text-[var(--ecp-danger)]">{connectors.error}</p>
      )}
      {rows.length === 0 ? (
        <EmptyBlock title="No connectors registered" hint="The action connector registry is empty." />
      ) : (
        <div className="overflow-hidden rounded-lg border border-[var(--ecp-border)]">
          <DataTable
            rows={rows}
            columns={columns}
            rowKey={(row) => row.name}
            dense
            searchPlaceholder="Filter connectors…"
          />
        </div>
      )}
    </div>
  );
}