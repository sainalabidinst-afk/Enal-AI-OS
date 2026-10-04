"use client";

import { useEffect } from "react";
import { Sparkles, TrendingUp, Newspaper, FileText, Clock, CheckCircle, XCircle, AlertTriangle } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";
import { Badge } from "@/components/design-system/primitives/badge";
import { useWorkspaceStore } from "@/components/workspace/stores/workspace-store";
import { Timeline, type TimelineEvent } from "@/components/workspace/shared/timeline";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const STATUS_COLORS = {
  completed: "bg-[var(--color-success)]",
  running: "bg-[var(--color-accent)]",
  failed: "bg-[var(--color-danger)]",
  pending: "bg-[var(--color-text-secondary)]",
};

export function RightPanel() {
  const consents = useWorkspaceStore((s) => s.consents);
  const dismissConsent = useWorkspaceStore((s) => s.dismissConsent);
  const tasks = useWorkspaceStore((s) => s.tasks);
  const system = useWorkspaceStore((s) => s.system);

  const timelineEvents: TimelineEvent[] = tasks.map((t) => ({
    id: t.id,
    title: t.label,
    status: t.status,
    timestamp: new Date().toISOString(),
  }));

  const pendingConsents = consents;

  return (
    <aside
      className="flex h-full w-full min-w-0 flex-col border-l border-[var(--color-border)] bg-[var(--color-surface)]"
      aria-label="Right panel"
    >
      <div className="border-b border-[var(--color-border)] px-4 py-3">
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">Insights</h2>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden p-3 space-y-4">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium text-[var(--color-text-primary)]">
              <Clock className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle>Task Timeline</CardTitle>
            </div>
            <CardDescription>Recent task executions</CardDescription>
          </CardHeader>
          <div className="px-4 pb-2">
            <Timeline
              events={timelineEvents}
              className="border-none shadow-none"
            />
          </div>
        </Card>

        {pendingConsents.length > 0 && (
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 text-sm font-medium text-[var(--color-text-primary)]">
                <FileText className="h-4 w-4 text-[var(--color-warning)]" />
                <CardTitle>Governance Consent</CardTitle>
              </div>
              <CardDescription>Approval required before proceeding</CardDescription>
            </CardHeader>
            <div className="px-4 pb-4 space-y-3">
              {pendingConsents.map((c) => (
                <div
                  key={c.id}
                  className="rounded-lg border border-[var(--color-border)] p-3 space-y-2"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <p className="text-sm font-medium text-[var(--color-text-primary)]">{c.title}</p>
                      <p className="text-xs text-[var(--color-text-secondary)] mt-0.5">{c.description}</p>
                    </div>
                    <Badge
                      variant={
                        c.severity === "high"
                          ? "danger"
                          : c.severity === "medium"
                            ? "warning"
                            : "default"
                      }
                      className="shrink-0"
                    >
                      {c.severity}
                    </Badge>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      variant="ghost"
                      className="text-xs"
                      onClick={() => dismissConsent(c.id)}
                    >
                      Deny
                    </Button>
                    <Button size="sm" variant="primary" className="text-xs">
                      Approve
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium text-[var(--color-text-primary)]">
              <AlertTriangle className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle>System Alerts</CardTitle>
            </div>
            <CardDescription>Active alerts and recommendations</CardDescription>
          </CardHeader>
          <div className="px-4 pb-4">
            <div className="space-y-2">
              <div className="flex items-center gap-2 rounded-md bg-[var(--color-bg-tertiary)] px-2 py-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-[var(--color-success)] animate-pulse" />
                <span className="text-xs text-[var(--color-text-primary)]">
                  All capability packs loaded successfully
                </span>
              </div>
              {system.latencyMs > 0 && (
                <div className="flex items-center gap-2 rounded-md bg-[var(--color-bg-tertiary)] px-2 py-1.5">
                  <span className="h-1.5 w-1.5 rounded-full bg-[var(--color-warning)]" />
                  <span className="text-xs text-[var(--color-text-primary)]">
                    Latency: {system.latencyMs}ms — within normal range
                  </span>
                </div>
              )}
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium text-[var(--color-text-primary)]">
              <Sparkles className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle>AI Insight</CardTitle>
            </div>
            <CardDescription>Generated recommendations</CardDescription>
          </CardHeader>
          <div className="px-4 pb-4">
            <p className="text-xs text-[var(--color-text-secondary)]">
              AI insights for the current workspace will appear here based on
              your conversation and task history.
            </p>
          </div>
        </Card>
      </div>
    </aside>
  );
}
