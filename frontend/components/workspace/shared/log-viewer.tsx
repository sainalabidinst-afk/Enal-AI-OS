"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface LogViewerProps {
  title?: string;
  logs?: Array<{ level: "info" | "warn" | "error" | "debug"; message: string; timestamp?: string }>;
  className?: string;
}

const LEVEL_STYLES = {
  info: "text-[var(--color-text-secondary)]",
  warn: "text-yellow-400",
  error: "text-[var(--color-danger)]",
  debug: "text-[var(--color-text-secondary)] opacity-70",
};

export function LogViewer({ title = "Logs", logs = [], className }: LogViewerProps) {
  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>{title}</CardTitle>
              <CardDescription>Application logs</CardDescription>
            </div>
            <span className="text-xs text-[var(--color-text-secondary)]">{logs.length} entries</span>
          </div>
        </CardHeader>
        <div className="bg-[var(--color-bg-primary)] p-4 rounded-b-xl max-h-[300px] overflow-y-auto font-mono text-xs space-y-1">
          {logs.length === 0 && (
            <span className="text-[var(--color-text-secondary)]">No logs yet.</span>
          )}
          {logs.map((log, i) => (
            <div key={i} className={LEVEL_STYLES[log.level]}>
              <span className="text-[var(--color-text-secondary)] mr-2 select-none">
                {log.timestamp || new Date().toISOString().slice(11, 19)}
              </span>
              {log.message}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
