"use client";

import { Sparkles, TrendingUp, Newspaper, FileText } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/design-system/layout/card";

export function RightPanel() {
  return (
    <aside className="flex w-80 flex-col border-l border-[var(--color-border)] bg-[var(--color-surface)]" aria-label="Right panel">
      <div className="border-b border-[var(--color-border)] px-4 py-3">
        <h2 className="text-sm font-semibold">Insights</h2>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium">
              <Sparkles className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle>AI Insight</CardTitle>
            </div>
            <CardDescription>
              This panel will show AI-generated insights for the current workspace context.
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium">
              <TrendingUp className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle>Metrics</CardTitle>
            </div>
            <CardDescription>
              Key metrics and KPIs for the current workspace will appear here.
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium">
              <Newspaper className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle>News</CardTitle>
            </div>
            <CardDescription>
              Relevant news and updates will stream into this panel.
            </CardDescription>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium">
              <FileText className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle>Research</CardTitle>
            </div>
            <CardDescription>
              Research materials and references for the active workspace.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    </aside>
  );
}
