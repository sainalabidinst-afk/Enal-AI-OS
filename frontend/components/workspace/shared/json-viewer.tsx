"use client";

import { type ReactNode } from "react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface JsonViewerProps {
  title?: string;
  data?: Record<string, unknown>;
  className?: string;
}

export function JsonViewer({ title = "JSON", data, className }: JsonViewerProps) {
  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>{title}</CardTitle>
              <CardDescription>JSON data</CardDescription>
            </div>
          </div>
        </CardHeader>
        <div className="p-4 rounded-b-xl border-t border-[var(--color-border)]">
          <pre className="text-xs text-[var(--color-text-secondary)] bg-[var(--color-bg-primary)] p-4 rounded-lg overflow-x-auto">
            {data ? JSON.stringify(data, null, 2) : "{}"}
          </pre>
        </div>
      </Card>
    </div>
  );
}
