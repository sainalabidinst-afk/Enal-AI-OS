"use client";

import { Sparkles, TrendingUp, Newspaper, FileText } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export function WorkspaceRightPanel() {
  return (
    <aside className="flex w-80 flex-col border-l border-[var(--color-border)] bg-[var(--color-bg-secondary)]">
      <div className="border-b border-[var(--color-border)] px-4 py-3">
        <h2 className="text-sm font-semibold">Insights</h2>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium">
              <Sparkles className="h-4 w-4 text-[var(--color-accent)]" />
              AI Insight
            </div>
          </CardHeader>
          <CardDescription>
            This panel will show AI-generated insights for the current workspace context.
          </CardDescription>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium">
              <TrendingUp className="h-4 w-4 text-[var(--color-accent)]" />
              Metrics
            </div>
          </CardHeader>
          <CardDescription>
            Key metrics and KPIs for the current workspace will appear here.
          </CardDescription>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium">
              <Newspaper className="h-4 w-4 text-[var(--color-accent)]" />
              News
            </div>
          </CardHeader>
          <CardDescription>
            Relevant news and updates will stream into this panel.
          </CardDescription>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-sm font-medium">
              <FileText className="h-4 w-4 text-[var(--color-accent)]" />
              Research
            </div>
          </CardHeader>
          <CardDescription>
            Research materials and references for the active workspace.
          </CardDescription>
        </Card>
      </div>
    </aside>
  );
}
