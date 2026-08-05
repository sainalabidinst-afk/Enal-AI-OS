"use client";

import { useState } from "react";
import { Database, Table2, FileCode, GitBranch, Lightbulb } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabPanel } from "@/components/ui/tabs";

type Tab = "sql" | "schema" | "results" | "history";

const TABS = [
  { id: "sql" as Tab, label: "SQL Editor", icon: <FileCode className="h-3.5 w-3.5" /> },
  { id: "schema" as Tab, label: "Schema", icon: <Database className="h-3.5 w-3.5" /> },
  { id: "results" as Tab, label: "Results", icon: <Table2 className="h-3.5 w-3.5" /> },
  { id: "history" as Tab, label: "History", icon: <GitBranch className="h-3.5 w-3.5" /> },
];

const SCHEMA_ITEMS = [
  { name: "users", rows: 12450, size: "4.2 MB" },
  { name: "orders", rows: 89100, size: "32.1 MB" },
  { name: "products", rows: 3200, size: "1.8 MB" },
  { name: "sessions", rows: 45000, size: "12.5 MB" },
];

const HISTORY_ITEMS = [
  { id: "Q-1", query: "SELECT * FROM users WHERE created_at > NOW() - INTERVAL '7 days'", time: "2 min ago", duration: "12ms" },
  { id: "Q-2", query: "SELECT COUNT(*) FROM orders WHERE status = 'completed'", time: "15 min ago", duration: "8ms" },
  { id: "Q-3", query: "EXPLAIN ANALYZE SELECT * FROM products WHERE category_id = 5", time: "1 hour ago", duration: "3ms" },
];

export function DatabaseWorkspace() {
  const [tab, setTab] = useState<Tab>("sql");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-[var(--color-border)] px-4 py-2">
        <h2 className="text-sm font-semibold">Database Workspace</h2>
        <Tabs tabs={TABS} activeTab={tab} onChange={(id) => setTab(id as Tab)} />
      </div>

      <TabPanel>
        {tab === "sql" && (
          <div className="h-full flex flex-col">
            <div className="flex items-center justify-between px-4 py-2 border-b border-[var(--color-border)]">
              <div className="flex items-center gap-2">
                <span className="text-xs text-[var(--color-text-secondary)]">Connection:</span>
                <span className="text-xs font-medium">production_db</span>
                <span className="text-xs text-green-400">● Connected</span>
              </div>
              <div className="flex items-center gap-2">
                <Button size="sm" variant="secondary">Format</Button>
                <Button size="sm">Execute</Button>
              </div>
            </div>
            <div className="flex-1 rounded-xl border border-dashed border-[var(--color-border)] bg-[var(--color-bg-secondary)] m-4 flex items-center justify-center">
              <div className="text-center space-y-2">
                <p className="text-4xl">💻</p>
                <p className="text-sm text-[var(--color-text-secondary)]">SQL editor with syntax highlighting will render here.</p>
                <p className="text-xs text-[var(--color-text-secondary)]">Supports PostgreSQL, MySQL, SQLite, MongoDB</p>
              </div>
            </div>
          </div>
        )}

        {tab === "schema" && (
          <div className="space-y-3">
            <div className="flex items-center justify-between px-4 py-2">
              <h3 className="text-sm font-medium">Tables</h3>
              <span className="text-xs text-[var(--color-text-secondary)]">{SCHEMA_ITEMS.length} tables</span>
            </div>
            <div className="grid gap-2">
              {SCHEMA_ITEMS.map((table) => (
                <Card key={table.name} padding={false}>
                  <div className="flex items-center justify-between px-4 py-3">
                    <div className="flex items-center gap-3">
                      <Table2 className="h-4 w-4 text-[var(--color-accent)]" />
                      <div>
                        <p className="text-sm font-medium">{table.name}</p>
                        <p className="text-xs text-[var(--color-text-secondary)]">{table.rows.toLocaleString()} rows</p>
                      </div>
                    </div>
                    <span className="text-xs text-[var(--color-text-secondary)]">{table.size}</span>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {tab === "results" && (
          <div className="space-y-3">
            <div className="flex items-center justify-between px-4 py-2">
              <h3 className="text-sm font-medium">Query Results</h3>
              <div className="flex items-center gap-2">
                <span className="text-xs text-[var(--color-text-secondary)]">1,247 rows returned in 12ms</span>
                <Button size="sm" variant="secondary">Export CSV</Button>
              </div>
            </div>
            <Card padding={false}>
              <div className="px-4 py-3 text-sm text-[var(--color-text-secondary)]">
                Run a query to see results here.
              </div>
            </Card>
          </div>
        )}

        {tab === "history" && (
          <div className="space-y-2">
            {HISTORY_ITEMS.map((item) => (
              <Card key={item.id} padding={false}>
                <div className="px-4 py-3">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-medium text-[var(--color-text-secondary)]">{item.id}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-[var(--color-text-secondary)]">{item.duration}</span>
                      <span className="text-xs text-[var(--color-text-secondary)]">•</span>
                      <span className="text-xs text-[var(--color-text-secondary)]">{item.time}</span>
                    </div>
                  </div>
                  <p className="text-sm font-mono text-[var(--color-text-primary)] line-clamp-1">{item.query}</p>
                </div>
              </Card>
            ))}
          </div>
        )}
      </TabPanel>
    </div>
  );
}